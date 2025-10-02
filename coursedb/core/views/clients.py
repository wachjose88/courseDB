from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.translation import gettext as _

from core.models import Client
from forms import ClientForm


@login_required
def client_list(request):
    clients = request.user.company.clients.all()
    params = {
        'clients': clients,
    }
    return render(request, 'core/clients/list.html', params)


@login_required
def client_create_edit(request, client_id=None):
    client = None
    if client_id is not None:
        client = get_object_or_404(Client, pk=client_id)
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
    client = get_object_or_404(Client, pk=client_id)
    client.delete()
    messages.success(request, _('Client deleted successfully'))
    return redirect('core.client.list')
