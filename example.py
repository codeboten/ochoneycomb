import time
import os

from opencensus.trace import tracer as tracer_module
import honeycomb_exporter

exporter = honeycomb_exporter.HoneycombExporter(writekey=os.getenv("HONEYCOMB_WRITEKEY"), dataset=os.getenv("HONEYCOMB_DATASET"), service_name="test-app")

# exporter = file_exporter.FileExporter(file_name='traces')

# Initialize a tracer, by default using the `PrintExporter`
tracer = tracer_module.Tracer(exporter=exporter)

def do_something_to_trace():
    time.sleep(1)

# Example for creating nested spans
with tracer.span(name='span1') as span1:
    do_something_to_trace()
    with tracer.span(name='span1_child1') as span1_child1:
        span1_child1.add_annotation("something")
        do_something_to_trace()
    with tracer.span(name='span1_child2') as span1_child2:
        do_something_to_trace()
with tracer.span(name='span2') as span2:
    do_something_to_trace()
