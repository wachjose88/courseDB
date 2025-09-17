from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class AddressMixin(models.Model):

    street = models.CharField(
        max_length=128,
        verbose_name=_('Street')
    )
    zipcode = models.CharField(
        max_length=128,
        verbose_name=_('ZIP')
    )
    city = models.CharField(
        max_length=128,
        verbose_name=_('City')
    )
    country = CountryField(
        verbose_name=_('Country')
    )

    class Meta:
        abstract = True


class EMailMixin(models.Model):

    email = models.EmailField(
        verbose_name=_('E-mail')
    )

    class Meta:
        abstract = True


class PhoneMixin(models.Model):

    phone = PhoneNumberField(
        verbose_name=_('Phone')
    )

    class Meta:
        abstract = True


class Company(AddressMixin, EMailMixin, PhoneMixin):

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name')
    )

    class Meta:
        abstract = False
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')



class User(AbstractUser, PermissionsMixin):

    company = models.ForeignKey(
        Company,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        verbose_name=_('Company')
    )

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

