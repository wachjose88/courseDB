from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _
from django.conf import settings

from core.models import Client, CourseAttendance
from forms import ClientForm


@login_required
def client_list(request):
    clients = request.user.company.clients.filter(is_instructor=False).order_by(
        'last_name', 'first_name')
    paginator = Paginator(clients, settings.PAGINATOR_NUM_PER_PAGE)
    page = request.GET.get('page')
    clients = paginator.get_page(page)
    params = {
        'clients': clients,
    }
    return render(request, 'core/clients/list.html', params)


@login_required
def client_create_edit(request, client_id=None):
    client = None
    if client_id is not None:
        client = get_object_or_404(Client, pk=client_id, company=request.user.company)
    if request.method == 'POST':
        if client_id is not None:
            form = ClientForm(request.POST, instance=client)
        else:
            form = ClientForm(request.POST)
        if form.is_valid():
            client_saved = form.save(commit=False)
            client_saved.company = request.user.company
            client_saved.save()
            if client_id is not None:
                messages.success(request, _('Client edited successfully'))
            else:
                messages.success(request, _('Client created successfully'))
            return redirect('core.client.list')
    else:
        if client_id is not None:
            form = ClientForm(instance=client)
        else:
            form = ClientForm()
    params = {
        'form': form,
        'client': client,
    }
    return render(request, 'core/clients/create_edit.html', params)


@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, pk=client_id, company=request.user.company)
    client.delete()
    messages.success(request, _('Client deleted successfully'))
    return redirect('core.client.list')


@login_required
def client_copy(request, client_id):
    client = get_object_or_404(Client, pk=client_id, company=request.user.company)
    client.pk = None
    client.id = None
    client.last_name = client.last_name + _(' (copy)')
    client._state.adding = True
    client.save()
    messages.success(request, _('Client copied successfully'))
    return redirect('core.client.list')


@login_required
def client_details(request, client_id):
    client = get_object_or_404(Client, pk=client_id, company=request.user.company)
    courses = CourseAttendance.objects.filter(client=client).order_by(
        'enrolled_at'
    )
    params = {
        'client': client,
        'courses': courses,
    }
    return render(request, 'core/clients/details.html', params)
