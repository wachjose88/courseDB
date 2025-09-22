
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import SplitPhoneNumberField

from core.models import User, Company, Client


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