from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html


from .forms import UserCreationForm, UserChangeForm
from .models import User, Follow

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))

    image_tag.short_description = 'Image'


    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    readonly_fields = ['image_tag']
    list_display = ('uid','nickname', 'email', 'introduce','image_tag' ,'birth','is_active', 'is_superuser', 'date_joined')
    list_display_links = ('nickname',)
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
    list_display = ('id','follower', 'followee','following')



# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)