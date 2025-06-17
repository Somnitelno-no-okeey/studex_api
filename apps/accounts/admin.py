from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from django import forms
from django.core.exceptions import PermissionDenied

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'is_active', 'is_staff', 'is_verificated')

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['patronymic'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_is_staff(self):
        is_staff = self.cleaned_data.get('is_staff')
        request = getattr(self, '_request', None)
        if is_staff and (not request or not request.user.is_superuser):
            raise forms.ValidationError("Только суперюзер может создавать администраторов.")
        return is_staff

class CustomUserChangeForm(UserChangeForm):
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        required=False,
        help_text=_("Enter a new password to change the current one. Leave blank to keep the existing password.")
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'patronymic', 'is_active', 'is_staff', 'is_superuser',
                  'is_verificated', 'groups')

    def __init__(self, *args, **kwargs):
        self._request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.fields['patronymic'].required = False

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean_password(self):
        return self.initial.get('password')

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password and len(new_password) < 8:
            raise forms.ValidationError("Новый пароль должен содержать минимум 8 символов.")
        return new_password

    def clean_is_staff(self):
        is_staff = self.cleaned_data.get('is_staff')
        request = getattr(self, '_request', None)
        if is_staff and (not request or not request.user.is_superuser):
            raise forms.ValidationError("Только суперюзер может назначать статус администратора.")
        return is_staff

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'first_name', 'last_name', 'patronymic', 'is_staff', 'is_active', 'is_verificated', 'is_deleted')
    list_filter = ('is_staff', 'is_active', 'is_verificated', 'is_deleted')
    search_fields = ('email', 'first_name', 'last_name', 'patronymic')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'new_password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'patronymic')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        (_('Verification'), {'fields': ('is_verificated', 'verification_code', 'verification_code_sent_at')}),
        (_('Password reset'), {'fields': ('password_reset_code', 'password_reset_code_sent_at')}),
        (_('Soft deletion'), {'fields': ('is_deleted',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'patronymic',
                       'is_active', 'is_staff', 'is_verificated'),
        }),
    )

    readonly_fields = ('verification_code', 'verification_code_sent_at', 'password_reset_code',
                       'password_reset_code_sent_at')

    filter_horizontal = ('groups',)

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        else:
            defaults['form'] = self.form
        defaults.update(kwargs)
        form_class = super().get_form(request, obj, **defaults)
        original_init = form_class.__init__

        def new_init(self, *args, **kwargs):
            kwargs['request'] = request
            original_init(self, *args, **kwargs)

        form_class.__init__ = new_init
        return form_class

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(form.cleaned_data['password1'])
        else:
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                obj.set_password(new_password)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        """Делаем поля только для чтения для не-суперюзеров"""
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not request.user.is_superuser:
            pass
        return readonly_fields
    
    def get_fieldsets(self, request, obj=None):
        """Скрываем поля groups, is_staff и is_superuser для не-суперюзеров"""
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.is_superuser:
            modified_fieldsets = []
            for name, options in fieldsets:
                if name == _('Permissions'):
                    fields = list(options['fields'])
                    restricted_fields = ['groups', 'is_staff', 'is_superuser']
                    for field in restricted_fields:
                        if field in fields:
                            fields.remove(field)
                    modified_options = options.copy()
                    modified_options['fields'] = tuple(fields)
                    modified_fieldsets.append((name, modified_options))
                else:
                    modified_fieldsets.append((name, options))
            return modified_fieldsets
        return fieldsets

class GroupAdmin(BaseGroupAdmin):
    """Админ для групп с ограничением доступа только для суперюзеров"""
    
    def has_add_permission(self, request):
        """Разрешить добавление групп только суперюзерам"""
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        """Разрешить удаление групп только суперюзерам"""
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        """Разрешить изменение групп только суперюзерам"""
        return request.user.is_superuser
    
    def has_view_permission(self, request, obj=None):
        """Разрешить просмотр групп только суперюзерам"""
        return request.user.is_superuser
    
    def has_module_permission(self, request):
        """Показывать модуль групп в админке только суперюзерам"""
        return request.user.is_superuser

admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, GroupAdmin)