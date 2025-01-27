from django.shortcuts import render, redirect
from django.views import generic
from .models import Customer, Vehicle
from .forms import VehicleForm, VehicleFormBasic, VehicleFormSet
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.


class CustomerListView(generic.ListView):
    queryset = Customer.objects.all().order_by('first_name', 'last_name')
    context_object_name = 'helloworld'

class CustomerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Customer
    fields = [
        'first_name', 
        'last_name',
        'email',
        'phone_number',
        'address',
        'city',
        'country'
        ]
    success_url = reverse_lazy('all_customers')

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.created_by = self.request.user
        customer.save()
        return super().form_valid(form)


class CustomerDetailView(generic.DetailView):
    model = Customer
    # template_name = 'rent/mycustomer.html'


class CustomerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Customer
    fields = '__all__'
    success_url = reverse_lazy('all_customers')


@login_required
def create_vehicle(request):
    form = VehicleFormBasic()
    if request.method == 'POST':
        form = VehicleFormBasic(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            vehicle = Vehicle(**form.cleaned_data)
            vehicle.created_by = request.user.profile
            vehicle.save()
            redirect('all_customers')
    
    return render(request, 'rent/create_vehicle.html', {'form':form})



@login_required
def create_multi_vehicle(request):
    formset = VehicleFormSet()
    if request.method == 'POST':
        formset = VehicleFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
                vehicle = Vehicle(**form.cleaned_data)
                vehicle.created_by = request.user.profile
                vehicle.save()
            redirect('all_customers')
    
    return render(request, 'rent/multicreate_vehicle.html', {'formset':formset})


class VehicleDetailView(generic.DetailView):
    model = Vehicle