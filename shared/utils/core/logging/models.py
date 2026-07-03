from pynamodb.attributes import (
    JSONAttribute,
    NumberAttribute,
    UnicodeAttribute,
    UTCDateTimeAttribute,
)
from pynamodb.models import Model


class IngressAPILog(Model):
    service_name = UnicodeAttribute(hash_key=True)
    timestamp = UTCDateTimeAttribute(range_key=True)
    http_method = UnicodeAttribute()
    request_data = JSONAttribute(null=True)
    response_data = JSONAttribute(null=True)
    error = UnicodeAttribute(null=True)
    status_code = NumberAttribute(null=True)

    class Meta:
        table_name = "DjangoIngressAPILog"


class EgressAPILog(IngressAPILog):
    class Meta:
        table_name = "EgressAPILog"
