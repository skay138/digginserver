from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

from .forms import UserCreationForm, UserChangeForm
from .models import User, Follow


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('uid','get_full_name', 'email', 'nickname', 'introduce', 'birth','is_active', 'is_superuser', 'date_joined')
    list_display_links = ('get_full_name',)
    list_filter = ('is_superuser', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('nickname', )}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('uid','email', 'nickname', 'password1', 'password2', 'birth', 'introduce', 'image')}
         ),
    )
    search_fields = ('email','nickname')
    ordering = ('-date_joined',)
    filter_horizontal = ()

class FollowAdmin(admin.ModelAdmin):
    list_display = ('id','__str__')



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)