from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _

from core.forms import CourseDescriptionForm
from core.models import CourseDescription


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
        description = get_object_or_404(CourseDescription, pk=description_id)
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
    description = get_object_or_404(CourseDescription, pk=description_id)
    description.delete()
    messages.success(request, _('Course description deleted successfully'))
    return redirect('core.course.description.list')


@login_required
def course_description_copy(request, description_id):
    description = get_object_or_404(CourseDescription, pk=description_id)
    description.pk = None
    description.id = None
    description.title = description.title + _(' (copy)')
    description._state.adding = True
    description.save()
    messages.success(request, _('Course description copied successfully'))
    return redirect('core.course.description.list')
