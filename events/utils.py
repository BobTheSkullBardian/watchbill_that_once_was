from calendar import HTMLCalendar, SUNDAY, monthrange
from collections import defaultdict
# from django.core.exceptions import MultipleObjectsReturned
from datetime import (
    # datetime as dtime,
    date,
    timedelta,
    # time
)
from .models import (
    Event,
    Position,
    # Watch
)
from sailors.models import (
    Qual,
)


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None, events=None):
        super(Calendar, self).__init__()
        self.year = year
        self.month = month
        self.setfirstweekday(SUNDAY)
        # print(f'Sunday: {SUNDAY}')
        self.events = events

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday, events):
        if day == 0:
            return '<td><span class="noday">&nbsp;</span></td>'
        events_per_day = events.filter(day__day=day, active=True)
        times = defaultdict(list)
        for event in events_per_day:
            times[(event.day, event.position.start_time)].append(event)
        d = ''
        for (_d, _t), events in sorted(times.items()):
            d += f'<li>{_t.strftime("%H%M")}<ul>'
            for event in events:
                _name = f'{event.stander.rate_lname()}'
                if 'Null' in _name:
                    continue
                status = f'{("no_qual","")[any([str(event.position.qual) == "NBP 306", event.stander.quald])]} {("bg-warning", "")[event.acknowledged]}'
                d += f'<li class="{status}">{event.position.qual}</br>'
                d += f'{_name}</li>'  # {event.stander.name.split(",")[0]}</li>'
            d += '</ul>'
        return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, weekday, events)
        return f'<tr>{week}</tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True):
        events = Event.objects.filter(
            day__year=self.year,
            day__month=self.month,
        )

        cal = '<table class="calendar">\n'
        # cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        cal += '</table>'
        return cal


class DivLayout():
    def __init__(self, year=None, month=None, auth=False):
        super(DivLayout, self).__init__()
        self.year = year
        self.month = month
        self.auth = auth
        self.monthyear = date(self.year, self.month, day=1)
        self.prev_month = self.monthyear - timedelta(days=1)
        self.next_month = self.monthyear.replace(day=monthrange(self.year, self.month)[1]) + timedelta(days=1)
        self.quals = Qual.objects.all()
        self.positions = Position.objects.all().order_by('start_time')
        self.tab = "\t"

    def formatmonth(self, withyear=True):
        self.events = Event.objects.filter(
            day__year=self.year,
            day__month=self.month,
            active=True,
        ).order_by('day')
        days = self.events.dates('day', 'day')  # set([event.day for event in events])
        body = '<!-- begin calendar content-->\n'
        # body += self.formatheaders()
        for day in days:
            body += self.formatday(day)
        body += '<!-- end calendar content-->'
        return body

    # def formatheaders(self):
    #     # data = 'data'
    #     # headers = ['', *self.quals]
    #     _header = '<div class="row">\n'
    #     _header += f'<div class="col-1"></div>\n'
    #     for data in self.quals:
    #         _header += f'<div class="col h4 float-center">{data}</div>\n'
    #     _header += f'</div>\n'
    #     return _header
        
    def formatday(self, day):
        tab = "\t"
        events = self.events.filter(day=day)
        style = (" text-muted", " ack")[day >= date.today()]
        _day = f'{tab*1}<div class="row border border-dark{style}">\n'
        _day += f'{tab*2}<div class="col-sm-1 align-self-center h5">{day.strftime("%d%b %a")}</div>\n'
        for i, position in enumerate(self.quals):
            _watches = events.filter(position__qual=list(self.quals).index(position) + 1)
            _day += f'{tab*2}<div class="col border border-dark {position}">\n'
            for watch in _watches:
                if self.auth:
                    name = watch.stander.get_absolute_url_flat()
                    pos = watch.get_absolute_url_flat()
                else:
                    name = watch.stander.rate_lname()
                    pos = watch.position
                status = f'{("bg-danger","")[watch.stander.quald or str(position) == "NBP 306"]}'
                _day += f'{tab*3}<div class="row {watch.position.label}{(" bg-warning", "")[watch.acknowledged]}">\n'
                _day += f'{tab*4}<div class="col-xl-5 col-lg-7 col-md-8">\n{tab*5}<span class="text-nowrap">{pos}</span>\n{tab*4}</div>\n'
                _day += f'{tab*4}<div class="col">\n{tab*5}<span class="{status} text-nowrap">{(name, "")[name[-4:]=="Null"]}</span>\n{tab*4}</div>\n'
                _day += f'{tab*3}</div>\n'
            _day += f'{tab*2}</div>\n'
        _day += f'{tab*1}</div>\n'
        return _day
