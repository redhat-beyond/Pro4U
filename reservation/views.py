from reservation.models import Schedule
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from reservation.utils import Calendar
from reservation.forms import ScheduleForm
from django.contrib import messages
from datetime import datetime, timezone, timedelta, date
from django.urls import reverse_lazy, reverse
import calendar

now = datetime.now(timezone.utc)+timedelta(hours=3)


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
            if schedule:
                professional_id = schedule[0].professional_id
            else:
                messages.error(request, "No schedule exists for this user")
                return redirect('schedule_new')

            Schedule.objects.get_or_create(
                professional_id=professional_id,
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


class CalendarView(generic.ListView):
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
