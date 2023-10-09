from django.contrib import admin

from users.models import User, VerificationCode


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    list_filter = ('id',)
    search_fields = ('email',)


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'user',)
