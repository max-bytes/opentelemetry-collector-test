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
from random import random
from typing import Iterable
import time

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

def observable_gauge_func(options: CallbackOptions) -> Iterable[Observation]:
    # print ("yield observation")
    yield Observation(random(), attributes={"foo": "bar"})
meter.create_observable_gauge("test-gauge", [observable_gauge_func], unit="s", description="test description")

try:
    while True: # just a idle infinite loop, cancellable via Ctrl-C
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

print("done")