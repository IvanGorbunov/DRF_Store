from datetime import datetime

from django.utils.timezone import utc
from django_filters.rest_framework import FilterSet

from store.models import Order


class ReportFilter(FilterSet):
    """
    Фильтр отчета
    """
    class Meta:
        model = Order
        fields = (
        )

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        date_start = datetime.strptime(
            self.data.get('date_start', '01.01.1970 00:00:00'),
            '%d.%m.%Y %H:%M:%S'
        )
        date_end = datetime.strptime(
            self.data.get('date_end', datetime.now().strftime('%d.%m.%Y %H:%M:%S')),
            '%d.%m.%Y %H:%M:%S'
        )
        qs = qs.filter(create_dt__range=(date_start.replace(tzinfo=utc), date_end.replace(tzinfo=utc)))
        return qs
