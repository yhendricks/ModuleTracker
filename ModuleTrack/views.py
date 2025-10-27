from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

from .models import PcbType
from .forms import PcbTypeForm


@login_required
def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


class PcbTypePermissionMixin(PermissionRequiredMixin):
    permission_required = 'ModuleTrack.view_pcbtype'  # Default permission
    login_url = reverse_lazy('login')


class PcbTypeListView(PcbTypePermissionMixin, ListView):
    model = PcbType
    template_name = 'pcb_type/list.html'
    context_object_name = 'pcb_types'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        return queryset

    def get_template_names(self):
        if self.request.htmx:
            return 'pcb_type/partials/pcb_type_table.html'
        return self.template_name


class PcbTypeCreateView(PcbTypePermissionMixin, CreateView):
    model = PcbType
    form_class = PcbTypeForm
    template_name = 'pcb_type/partials/pcb_type_form.html'
    success_url = reverse_lazy('pcb_type_list')
    permission_required = 'ModuleTrack.add_pcbtype'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, 'PCB Type created successfully!')
            # Manually paginate the queryset for HTMX response
            all_pcb_types = PcbType.objects.all().order_by('id')
            paginator = Paginator(all_pcb_types, 10)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            response = render(self.request, 'pcb_type/partials/pcb_type_table.html', {
                'pcb_types': page_obj.object_list,
                'page_obj': page_obj
            })
            response['HX-Trigger'] = 'hideModal'
            return response
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.htmx:
            return render(self.request, 'pcb_type/partials/pcb_type_form.html', {'form': form})
        return response


class PcbTypeUpdateView(PcbTypePermissionMixin, UpdateView):
    model = PcbType
    form_class = PcbTypeForm
    template_name = 'pcb_type/partials/pcb_type_form.html'
    success_url = reverse_lazy('pcb_type_list')
    permission_required = 'ModuleTrack.change_pcbtype'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.htmx:
            messages.success(self.request, 'PCB Type updated successfully!')
            # Manually paginate the queryset for HTMX response
            all_pcb_types = PcbType.objects.all().order_by('id')
            paginator = Paginator(all_pcb_types, 10)
            page_number = self.request.GET.get('page', 1)
            page_obj = paginator.get_page(page_number)
            response = render(self.request, 'pcb_type/partials/pcb_type_table.html', {
                'pcb_types': page_obj.object_list,
                'page_obj': page_obj
            })
            response['HX-Trigger'] = 'hideModal'
            return response
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.htmx:
            return render(self.request, 'pcb_type/partials/pcb_type_form.html', {'form': form})
        return response


class PcbTypeDeleteView(PcbTypePermissionMixin, DeleteView):
    model = PcbType
    template_name = 'pcb_type/partials/pcb_type_confirm_delete.html'
    success_url = reverse_lazy('pcb_type_list')
    permission_required = 'ModuleTrack.delete_pcbtype'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get('confirm_name') == self.object.name:
            messages.success(self.request, f'PCB Type \'{self.object.name}\' deleted successfully!')
            self.object.delete()
            if request.htmx:
                # Manually paginate the queryset for HTMX response
                all_pcb_types = PcbType.objects.all().order_by('id')
                paginator = Paginator(all_pcb_types, 10)
                page_number = self.request.GET.get('page', 1)
                page_obj = paginator.get_page(page_number)
                response = render(self.request, 'pcb_type/partials/pcb_type_table.html', {
                    'pcb_types': page_obj.object_list,
                    'page_obj': page_obj
                })
                response['HX-Trigger'] = 'hideModal'
                return response
            return redirect(self.get_success_url())
        else:
            messages.error(self.request, 'Confirmation name does not match.')
            if request.htmx:
                return render(self.request, 'pcb_type/partials/pcb_type_confirm_delete.html', {'object': self.object})
            return render(request, self.template_name, {'object': self.object})


class PcbTypeDetailView(PcbTypePermissionMixin, DetailView):
    model = PcbType
    template_name = 'pcb_type/partials/pcb_type_detail.html'
    context_object_name = 'pcb_type'
    permission_required = 'ModuleTrack.view_pcbtype'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        return response