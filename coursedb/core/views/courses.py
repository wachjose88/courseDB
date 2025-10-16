from datetime import timedelta

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.translation import gettext as _

from core.forms import CourseDescriptionForm, CourseCreateForm
from core.models import CourseDescription, Course


@login_required
def course_description_list(request):
    descriptions = request.user.company.course_descriptions.all().order_by('title')
    paginator = Paginator(descriptions, settings.PAGINATOR_NUM_PER_PAGE)
    page = request.GET.get('page')
    descriptions = paginator.get_page(page)
    params = {
        'descriptions': descriptions,
    }
    return render(request, 'core/courses/description_list.html', params)


@login_required
def course_description_create_edit(request, description_id=None):
    description = None
    if description_id is not None:
        description = get_object_or_404(CourseDescription,
                                        pk=description_id,
                                        company=request.user.company)
    if request.method == 'POST':
        if description_id is not None:
            form = CourseDescriptionForm(request.POST, instance=description)
        else:
            form = CourseDescriptionForm(request.POST)
        if form.is_valid():
            client_saved = form.save(commit=False)
            client_saved.company = request.user.company
            client_saved.save()
            if description_id is not None:
                messages.success(request, _('Course description edited successfully'))
            else:
                messages.success(request, _('Course description created successfully'))
            return redirect('core.course.description.list')
    else:
        if description_id is not None:
            form = CourseDescriptionForm(instance=description)
        else:
            form = CourseDescriptionForm()
    params = {
        'form': form,
        'description': description,
    }
    return render(request, 'core/courses/description_create_edit.html', params)


@login_required
def course_description_delete(request, description_id):
    description = get_object_or_404(CourseDescription,
                                    pk=description_id,
                                    company=request.user.company)
    description.delete()
    messages.success(request, _('Course description deleted successfully'))
    return redirect('core.course.description.list')


@login_required
def course_description_copy(request, description_id):
    description = get_object_or_404(CourseDescription,
                                    pk=description_id,
                                    company=request.user.company)
    description.pk = None
    description.id = None
    description.title = description.title + _(' (copy)')
    description._state.adding = True
    description.save()
    messages.success(request, _('Course description copied successfully'))
    return redirect('core.course.description.list')


@login_required
def course_list(request):
    courses = Course.objects.filter(
        description__company=request.user.company,
    ).distinct().order_by('-created_at')
    paginator = Paginator(courses, settings.PAGINATOR_NUM_PER_PAGE)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    params = {
        'courses': courses,
    }
    return render(request, 'core/courses/list.html', params)


@login_required
def course_create(request):
    if request.method == 'POST':
        form = CourseCreateForm(request.POST, company=request.user.company)
        if form.is_valid():
            course = form.save()
            for i in range(0, course.description.units):
                add = timedelta(weeks=i)
                begin = form.cleaned_data['begin'] + add
                course.units.create(begin=begin, duration=course.description.duration)
            messages.success(request, _('Course created successfully'))
            return redirect('core.course.list')
    else:
        form = CourseCreateForm(company=request.user.company)
    params = {
        'form': form,
    }
    return render(request, 'core/courses/create.html', params)
