from reservation.models import TypeOfJob
from django.shortcuts import render, redirect
from reservation.forms import TypeOfJobForm
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy


def typeOfJob_list(request, professional):
    if request.method == 'GET':
        typeOfjob = list(TypeOfJob.objects.filter(professional_id__professional_id=professional))
        if typeOfjob:
            typeOfjobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(typeOfjob[0].professional_id)
            return render(request, "reservation/typeOfJob_list.html", {'typeOfjobs_by_pro': typeOfjobs_by_pro})
        else:
            return render(request, "reservation/typeOfJob_list.html", {'typeOfjobs_by_pro': []})


def create_typeOfJob(request, professional):
    if request.method == 'GET':
        form1 = TypeOfJobForm()
        return render(request, 'reservation/typeOfJob_form.html', {'form': form1})

    if request.method == 'POST':
        form = TypeOfJobForm(request.POST)
        if form.is_valid():
            typeOfjob_by_pro = list(TypeOfJob.objects.filter(professional_id__professional_id=professional))
            typeOfjob = TypeOfJob.objects.create(professional_id=typeOfjob_by_pro[0].professional_id,
                                                 typeOfJob_name=form.cleaned_data['typeOfJob_name'],
                                                 price=form.cleaned_data['price'])

            typeOfjob.save()
            messages.success(request, "The typeOfJob was created successfully.")
            return redirect('typeOfJob', professional=professional)
        else:
            messages.error(request, "Entering incorrect details")
            return render(request, 'reservation/typeOfJob_form.html', {'form': form})


class TypeOfJobUpdate(UpdateView):
    model = TypeOfJob
    fields = ['typeOfJob_name', 'price']
    template_name = "reservation/typeOfJob_form.html"

    def get_success_url(self):
        return reverse_lazy("typeOfJob", kwargs={"professional": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "The type of job was updated successfully.")
        return super(TypeOfJobUpdate, self).form_valid(form)


class TypeOfJobDelete(DeleteView):
    model = TypeOfJob
    context_object_name = 'typeOfJob'

    def get_success_url(self):
        return reverse_lazy("typeOfJob", kwargs={"professional": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "The type of job was deleted successfully.")
        return super(TypeOfJobDelete, self).form_valid(form)
