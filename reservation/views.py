from reservation.models import Schedule, TypeOfJob, Appointment
from account.models.professional import Professional
from account.models.client import Client
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from reservation.utils import Calendar
from reservation.forms import ScheduleForm, TypeOfJobForm
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import calendar
import pytz

israel_tz = pytz.timezone('Asia/Jerusalem')
now = timezone.now().astimezone(israel_tz)


@login_required
def typeOfJob_list(request):
    if request.method == 'GET':
        typeOfjob = list(TypeOfJob.objects.filter(professional_id__profile_id__user_id=request.user))
        if typeOfjob:
            typeOfjobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(typeOfjob[0].professional_id.professional_id)
            return render(request, "reservation/typeOfJob_list.html", {'typeOfjobs_by_pro': typeOfjobs_by_pro})
        else:
            return render(request, "reservation/typeOfJob_list.html", {'typeOfjobs_by_pro': []})


@login_required
def create_typeOfJob(request):
    if request.method == 'GET':
        form1 = TypeOfJobForm()
        return render(request, 'reservation/typeOfJob_form.html', {'form': form1})

    if request.method == 'POST':
        form = TypeOfJobForm(request.POST)
        if form.is_valid():
            typeOfjob_by_pro = list(TypeOfJob.objects.filter(professional_id__profile_id__user_id=request.user))
            typeOfjob = TypeOfJob.objects.create(professional_id=typeOfjob_by_pro[0].professional_id,
                                                 typeOfJob_name=form.cleaned_data['typeOfJob_name'],
                                                 price=form.cleaned_data['price'])

            typeOfjob.save()
            messages.success(request, "The typeOfJob was created successfully.")
            return redirect('typeOfJob')
        else:
            return render(request, 'reservation/typeOfJob_form.html', {'form': form})


class TypeOfJobUpdate(LoginRequiredMixin, generic.UpdateView):
    model = TypeOfJob
    fields = ['typeOfJob_name', 'price']
    success_url = reverse_lazy('typeOfJob')
    template_name = "reservation/typeOfJob_form.html"

    def form_valid(self, form):
        messages.success(self.request, "The type of job was updated successfully.")
        return super(TypeOfJobUpdate, self).form_valid(form)


@login_required
def type_of_job_delete(request, pk):
    type_of_job = TypeOfJob.objects.filter(typeOfJob_id=pk)[0]
    type_of_job.delete()
    return redirect('typeOfJob')


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


@login_required
def create_schedule(request):
    form = ScheduleForm(request.POST or None)
    if request.POST and form.is_valid():
        start_day = form.cleaned_data["start_day"]
        end_day = form.cleaned_data["end_day"]
        meeting_time = form.cleaned_data["meeting_time"]
        schedule = list(Schedule.objects.filter(professional_id__profile_id__user_id=request.user,
                                                start_day__day=start_day.day))
        if start_day >= end_day or start_day.day != end_day.day or start_day < now:
            messages.error(request, 'Entering incorrect details')
            return redirect('schedule_new')
        elif len(schedule) >= 1:
            messages.error(request, 'You have already set a meeting schedule for this day')
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


@login_required
def schedule_details(request, schedule_id):
    schedule = Schedule.objects.get(schedule_id=schedule_id)
    context = {"schedule": schedule}
    return render(request, "reservation/schedule_details.html", context)


@login_required
def confirm_appointment(request, professional_id, meeting, day, month, year):
    start_meeting = meeting.split("-")[0]
    end_meeting = meeting.split("-")[1]

    if request.method == 'GET':
        typeOfjobs = TypeOfJob.objects.filter(professional_id__professional_id=professional_id)
        if typeOfjobs:
            typeOfjobs_by_pro = TypeOfJob.get_typeofjobs_by_professional(typeOfjobs[0].professional_id.professional_id)
        else:
            return redirect('homepage')

        return render(request, "reservation/confirm_appointment.html", {
            'professional_id': professional_id,
            'start_meeting': start_meeting,
            'end_meeting': end_meeting,
            'typeOfjobs_by_pro': typeOfjobs_by_pro,
            'day': day,
            'month': month,
            'year': year
        })

    if request.method == 'POST':
        selected_service = request.POST.get('service')
        typeOfJob = TypeOfJob.objects.filter(typeOfJob_id=selected_service).first()  # Use first() instead of [0]
        professional = Professional.objects.filter(
            professional_id=professional_id).first()  # Use first() instead of [0]
        client = Client.objects.filter(profile_id__user_id=request.user).first()  # Use first() instead of [0]

        start_appointment = datetime(year, month, day, int(start_meeting.split(':')[0]),
                                     int(start_meeting.split(':')[1]))
        end_appointment = datetime(year, month, day, int(end_meeting.split(':')[0]), int(end_meeting.split(':')[1]))

        appointment = Appointment.objects.create(
            professional_id=professional,
            client_id=client,
            typeOfJob_id=typeOfJob,
            start_appointment=start_appointment,
            end_appointment=end_appointment
        )
        appointment.save()

        return redirect('make_appointment', pk=professional_id)


class ScheduleEdit(LoginRequiredMixin, generic.UpdateView):
    model = Schedule
    fields = ["start_day", "end_day", "meeting_time"]
    template_name = "reservation/schedule.html"


class ScheduleDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Schedule
    template_name = "reservation/schedule_delete.html"
    success_url = reverse_lazy("calendar")


class CalendarView(LoginRequiredMixin, generic.ListView):
    model = Schedule
    user = False

    def get_template_names(self):
        if self.user:
            return ["reservation/make_appointment.html"]
        else:
            return ["reservation/calendar.html"]

    def get_context_data(self, **kwargs):
        user = self.user
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        if user is False:
            schedule = list(Schedule.objects.filter(professional_id__profile_id__user_id=self.request.user))
        else:
            professional_id = self.kwargs['pk']
            schedule = list(Schedule.objects.filter(professional_id__professional_id=professional_id))
            context["professional_id"] = professional_id

        if schedule:
            cal = Calendar(d.year, d.month, schedule[0].professional_id.professional_id, user)
        else:
            cal = Calendar(d.year, d.month, None, user)

        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context
