from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.metrics import (
    CallbackOptions,
    Observation
)
from opentelemetry.util.types import Attributes
from random import randint
from typing import Iterable

resource = Resource(attributes={
    SERVICE_NAME: "your-service-name"
})
reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(
        endpoint="localhost:4317", 
        insecure=True # NOTE: only needed when target endpoint is non-HTTP
    ),
    export_interval_millis=1000 # how often should gauge be observed
)
provider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)

def write_single_gauge_metric(value: int|float, name: str, unit: str = "", description: str = "", attributes: Attributes = None):
    def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
        yield Observation(value, attributes)
    meter.create_observable_gauge(name, [observable_gauge_func], unit=unit, description=description)

res = randint(1, 6)
write_single_gauge_metric(res, "test-single-gauge", attributes={"foo": "bar"})

provider.force_flush()

print("done")