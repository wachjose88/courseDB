from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.forms import UserAdminForm
from core.models import User, Company


class LocalUserAdmin(UserAdmin):

    model = User
    form = UserAdminForm

    fieldsets = UserAdmin.fieldsets + (
        (
            _('Additional information'),
            {
                'fields': ('company',)
            }
        ),
    )


class UserInline(admin.TabularInline):

    model = User
    fields = (
        'username',
        'first_name',
        'last_name',
    )
    extra = 0
    verbose_name = _('User')
    verbose_name_plural = _('Users')

    def has_add_permission(self, request, obj=None):
        """
        Removes the permission to add.
        """
        return False

    def has_change_permission(self, request, obj=None):
        """
        Removes the permission to change.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Removes the permission to delete.
        """
        return False


class CompanyAdmin(admin.ModelAdmin):

    fields = ('name', 'street', 'zipcode', 'city', 'country', 'email', 'phone')
    inlines = (UserInline,)
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('country',)


admin.site.register(User, LocalUserAdmin)
admin.site.register(Company, CompanyAdmin)

# Change admin site title
admin.site.site_header = _("courseDB Administration")
admin.site.site_title = _("courseDB Admin")