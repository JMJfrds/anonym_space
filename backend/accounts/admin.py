from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['email', 'nickname', 'role']

    # Parol xatosini yo'qotish uchun fieldsets'ni qaytadan yozamiz
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy', {'fields': ('nickname', 'role', 'points')}),
        ('Huquqlar', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nickname', 'role', 'password1', 'password2'),
            # 'password_confirm' UserCreationForm bilan birga keladi
        }),
    )

    search_fields = ('email', 'nickname')
    ordering = ('email',)