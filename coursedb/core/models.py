from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
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


class CreatedAtMixin(models.Model):

    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Created at')
    )

    class Meta:
        abstract = True


class Company(AddressMixin, EMailMixin, PhoneMixin, CreatedAtMixin):

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


class Client(AddressMixin, EMailMixin, PhoneMixin, CreatedAtMixin):

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

    company = models.ForeignKey(
        Company,
        related_name='clients',
        on_delete=models.CASCADE,
        verbose_name=_('Company')
    )

    is_instructor = models.BooleanField(
        default=False,
        verbose_name=_('Is instructor')
    )

    def name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.name()

    class Meta:
        abstract = False
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class CourseDescription(CreatedAtMixin):

    title = models.CharField(
        max_length=128,
        verbose_name=_('Title')
    )

    short_description = HTMLField(
        blank=True,
        verbose_name=_('Short description')
    )

    long_description = HTMLField(
        blank=True,
        verbose_name=_('Long description')
    )

    units = models.IntegerField(
        verbose_name=_('Units')
    )

    duration = models.DurationField(
        verbose_name=_('Duration')
    )

    company = models.ForeignKey(
        Company,
        related_name='course_descriptions',
        on_delete=models.CASCADE,
        verbose_name=_('Company')
    )

    def __str__(self):
        return self.title

    class Meta:
        abstract = False
        verbose_name = _('Course description')
        verbose_name_plural = _('Course descriptions')


class Course(CreatedAtMixin):

    title_extension = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        verbose_name=_('Title extension')
    )

    additional_description = HTMLField(
        blank=True,
        verbose_name=_('Additional description')
    )

    description = models.ForeignKey(
        CourseDescription,
        related_name='courses',
        on_delete=models.CASCADE,
        verbose_name=_('Description')
    )

    instructors = models.ManyToManyField(
        Client,
        related_name='given_courses',
        verbose_name=_('Instructors')
    )

    def __str__(self):
        if self.title_extension is None:
            return self.description.title
        return f'{self.description.title} {self.title_extension}'

    class Meta:
        abstract = False
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')


class CourseUnit(models.Model):

    begin = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Begin')
    )

    duration = models.DurationField(
        verbose_name=_('Duration')
    )

    course = models.ForeignKey(
        Course,
        related_name='units',
        on_delete=models.CASCADE,
        verbose_name=_('Course')
    )

    def __str__(self):
        return f'{self.begin}'

    class Meta:
        abstract = False
        verbose_name = _('Course unit')
        verbose_name_plural = _('Course units')
