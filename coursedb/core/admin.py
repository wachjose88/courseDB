from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from core.forms import UserAdminForm, CompanyAdminForm, ClientAdminForm, CourseAdminForm
from core.models import User, Company, Client, Family, CourseDescription, CourseUnit, Course


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
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class CompanyAdmin(admin.ModelAdmin):

    fields = ('name', 'street', 'zipcode', 'city', 'country', 'email', 'phone')
    inlines = (UserInline,)
    list_display = ('name',)
    search_fields = ('name',)
    list_filter = ('country',)
    form = CompanyAdminForm


class ClientAdmin(admin.ModelAdmin):

    fields = ('gender', 'letter_salutation', 'prefixed_title', 'first_name',
              'last_name', 'postfixed_title', 'job_title',
              'street', 'zipcode', 'city', 'country', 'email', 'phone', 'job',
              'additional_info', 'family', 'is_instructor')
    list_display = ('name', 'is_instructor')
    search_fields = ('first_name', 'last_name')
    list_filter = ('is_instructor', 'country')
    form = ClientAdminForm


class ClientInline(admin.TabularInline):

    model = Client
    fields = (
        'first_name',
        'last_name',
    )
    extra = 0
    verbose_name = _('Member')
    verbose_name_plural = _('Members')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FamilyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = (ClientInline,)


class CourseDescriptionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class CourseUnitInline(admin.TabularInline):

    model = CourseUnit
    fields = (
        'begin',
        'duration',
    )
    extra = 0
    verbose_name = _('Course unit')
    verbose_name_plural = _('Course units')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    search_fields = ('description__title', 'title_extension')
    inlines = (CourseUnitInline,)
    form = CourseAdminForm


admin.site.register(User, LocalUserAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(CourseDescription, CourseDescriptionAdmin)
admin.site.register(Course, CourseAdmin)

# Change admin site title
admin.site.site_header = _("courseDB Administration")
admin.site.site_title = _("courseDB Admin")