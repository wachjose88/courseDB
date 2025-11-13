
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import gettext_lazy as _
from phonenumber_field.formfields import SplitPhoneNumberField
from dateutil import tz

from core.models import User, Company, Client, CourseDescription, Course, CourseAttendance
from core.fields import BootstrapSplitPhoneNumberField


class CourseAttendanceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CourseAttendanceForm, self).__init__(*args, **kwargs)
        self.fields['client'].queryset = Client.objects.filter(
            is_instructor=False,
            company=company
        )
        self.fields['enrolled_at'].widget=forms.DateTimeInput(
            attrs={'type': 'datetime-local'})
        if 'enrolled_at' in self.initial.keys():
            enrolled = self.initial['enrolled_at']
            to_zone = tz.tzlocal()
            enrolled = enrolled.astimezone(to_zone)
            self.initial['enrolled_at'] = f'{enrolled:%Y-%m-%d %H:%M}'

    class Meta:
        model = CourseAttendance
        exclude = ('course',)


class CourseUnitForm(forms.Form):

    begin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_('Begin'),
    )

    duration = forms.DurationField(
        label=_('Duration')
    )


class CourseSelectCreateForm(forms.Form):

    description = forms.ChoiceField(
        label=_('Description'),
    )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CourseSelectCreateForm, self).__init__(*args, **kwargs)
        choices = []
        for description in CourseDescription.objects.filter(company=company).order_by('title'):
            choices.append((description.id, description.title))
        self.fields['description'].choices = choices


class CourseCreateForm(forms.ModelForm):

    begin = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label=_('Begin'),
    )

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CourseCreateForm, self).__init__(*args, **kwargs)
        self.fields['instructors'].queryset = Client.objects.filter(
            is_instructor=True,
            company=company
        )
        self.fields['actual_costs'].required = False

    class Meta:
        model = Course
        exclude = ('created_at', 'attendees', 'description')


class CourseEditForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        company = kwargs.pop('company')
        super(CourseEditForm, self).__init__(*args, **kwargs)
        self.fields['instructors'].queryset = Client.objects.filter(
            is_instructor=True,
            company=company
        )

    class Meta:
        model = Course
        fields = ['description', 'title_extension', 'additional_description',
                  'actual_costs', 'instructors', ]


class CourseAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourseAdminForm, self).__init__(*args, **kwargs)
        self.fields['instructors'].queryset = Client.objects.filter(is_instructor=True)

    class Meta:
        model = Course
        exclude = ('created_at',)


class CourseDescriptionForm(forms.ModelForm):

    class Meta:
        model = CourseDescription
        exclude = ('created_at', 'company')


class ClientForm(forms.ModelForm):

    phone = BootstrapSplitPhoneNumberField(
        required=False,
    )

    class Meta:
        model = Client
        fields = ['gender', 'prefixed_title', 'first_name',
                  'last_name', 'postfixed_title', 'job_title',
                  'letter_salutation', 'street', 'zipcode',
                  'city', 'country', 'email', 'phone', 'job',
                  'additional_info']
        widgets = {
            'country': CountrySelectWidget(),
        }


class CompanyAdminForm(forms.ModelForm):

    phone = SplitPhoneNumberField(
        required=False,
    )

    class Meta:
        model = Company
        exclude = []
        widgets = {
            'country': CountrySelectWidget(),
        }


class ClientAdminForm(forms.ModelForm):

    phone = SplitPhoneNumberField(
        required=False,
    )

    class Meta:
        model = Client
        exclude = []
        widgets = {
            'country': CountrySelectWidget(),
        }


class UserAdminForm(UserChangeForm):

    class Meta:
        """
        Sets the model and defines the used fields.
        """

        model = User
        fields = '__all__'