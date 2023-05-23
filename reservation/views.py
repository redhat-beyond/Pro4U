from reservation.models import Schedule, TypeOfJob
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from reservation.utils import Calendar
from django.contrib.auth.mixins import LoginRequiredMixin
from reservation.forms import ScheduleForm, TypeOfJobForm
from django.contrib import messages
from datetime import datetime, timezone, timedelta, date
from django.urls import reverse_lazy, reverse
import calendar

now = datetime.now(timezone.utc)+timedelta(hours=3)


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


class TypeOfJobUpdate(generic.UpdateView):
    model = TypeOfJob
    fields = ['typeOfJob_name', 'price']
    template_name = "reservation/typeOfJob_form.html"

    def get_success_url(self):
        return reverse_lazy("typeOfJob", kwargs={"professional": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "The type of job was updated successfully.")
        return super(TypeOfJobUpdate, self).form_valid(form)


class TypeOfJobDelete(generic.DeleteView):
    model = TypeOfJob
    context_object_name = 'typeOfJob'

    def get_success_url(self):
        return reverse_lazy("typeOfJob", kwargs={"professional": self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "The type of job was deleted successfully.")
        return super(TypeOfJobDelete, self).form_valid(form)


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = "month=" + str(prev_month.year) + "-" + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = "month=" + str(next_month.year) + "-" + str(next_month.month)
    return month


def create_schedule(request):
    form = ScheduleForm(request.POST or None)
    if request.POST and form.is_valid():
        start_day = form.cleaned_data["start_day"]
        end_day = form.cleaned_data["end_day"]
        meeting_time = form.cleaned_data["meeting_time"]
        schedule = list(Schedule.objects.filter(professional_id__profile_id__user_id=request.user,
                                                start_day__day=start_day.day))
        if start_day >= end_day or start_day.day != end_day.day or start_day < now:
            messages.error(request, "Entering incorrect details")
            return redirect('schedule_new')
        elif len(schedule) >= 1:
            messages.error(request, "You have already set a meeting schedule for this day")
            return redirect('schedule_new')
        else:
            schedule = list(Schedule.objects.filter(professional_id__profile_id__user_id=request.user))
            Schedule.objects.get_or_create(
                professional_id=schedule[0].professional_id,
                start_day=start_day,
                end_day=end_day,
                meeting_time=meeting_time,
            )
            messages.success(request, 'Schedule created successfully')
            return HttpResponseRedirect(reverse("calendar"))
    return render(request, "reservation/schedule.html", {"form": form})


def schedule_details(request, schedule_id):
    schedule = Schedule.objects.get(schedule_id=schedule_id)
    context = {"schedule": schedule}
    return render(request, "reservation/schedule_details.html", context)


class ScheduleEdit(generic.UpdateView):
    model = Schedule
    fields = ["start_day", "end_day", "meeting_time"]
    template_name = "reservation/schedule.html"


class ScheduleDeleteView(generic.DeleteView):
    model = Schedule
    template_name = "reservation/schedule_delete.html"
    success_url = reverse_lazy("calendar")


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Schedule
    template_name = "reservation/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        schedule = list(Schedule.objects.filter(professional_id__profile_id__user_id=self.request.user))
        cal = Calendar(d.year, d.month, schedule[0].professional_id)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context
