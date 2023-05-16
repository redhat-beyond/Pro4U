from calendar import HTMLCalendar
from reservation.models import Schedule


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, professional_id=None):
        self.year = year
        self.month = month
        self.professional_id = professional_id
        super(Calendar, self).__init__()

    def formatday(self, day, schedule):
        schedule_per_day = schedule.filter(start_day__day=day)
        d = ""
        for schedule in schedule_per_day:
            d += f"<li>  {schedule.get_html_url}  </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    def formatweek(self, theweek, schedule):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, schedule)
        return f"<tr> {week} </tr>"

    def formatmonth(self, withyear=True):
        schedule = Schedule.objects.filter(
            professional_id=self.professional_id,
            start_day__year=self.year, start_day__month=self.month
        )
        cal = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )  # noqa
        cal += (
            f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, schedule)}\n"
        return cal
