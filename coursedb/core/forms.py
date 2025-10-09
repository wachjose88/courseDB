
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import SplitPhoneNumberField

from core.models import User, Company, Client, CourseDescription
from core.fields import BootstrapSplitPhoneNumberField


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