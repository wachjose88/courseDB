from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField
from tinymce.models import HTMLField


class AddressMixin(models.Model):

    street = models.CharField(
        max_length=128,
        verbose_name=_('Street a. No.')
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
        blank=True,
        null=True,
        verbose_name=_('E-mail')
    )

    class Meta:
        abstract = True


class PhoneMixin(models.Model):

    phone = PhoneNumberField(
        blank=True,
        null=True,
        verbose_name=_('Phone')
    )

    class Meta:
        abstract = True


class Company(AddressMixin, EMailMixin, PhoneMixin):

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

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


class Family(models.Model):

    letter_salutation = models.CharField(
        max_length=128,
        verbose_name=_('Letter salutation')
    )

    name = models.CharField(
        max_length=128,
        verbose_name=_('Name')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Family')
        verbose_name_plural = _('Families')


class Client(AddressMixin, EMailMixin, PhoneMixin):

    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_DIVERSE = 'd'
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
        (GENDER_DIVERSE, _('Diverse')),
    )

    gender = models.CharField(
        max_length=1,
        verbose_name=_('Gender'),
        choices=GENDER_CHOICES,
        default=GENDER_MALE,
    )

    letter_salutation = models.CharField(
        max_length=128,
        verbose_name=_('Letter salutation')
    )

    prefixed_title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Prefixed title')
    )

    first_name = models.CharField(
        max_length=128,
        verbose_name=_('Firstname')
    )

    last_name = models.CharField(
        max_length=128,
        verbose_name=_('Lastname')
    )

    postfixed_title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Postfixed title')
    )

    job_title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Job title')
    )

    job = models.CharField(
        max_length=128,
        verbose_name=_('Job')
    )

    additional_info = HTMLField(
        blank=True,
        verbose_name=_('Additional info')
    )

    family = models.ForeignKey(
        Family,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='members',
        verbose_name=_('Family')
    )

    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.name()

    class Meta:
        abstract = False
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

