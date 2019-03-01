# OpenCensus Python exporter for Honeycomb

A simple exporter to translate OpenCensus span data into Honeycomb traces.

## Usage

```python
from opencensus.trace import tracer as tracer_module
from opencensus.trace.exporters import file_exporter

from opencensus.trace.exporters import honeycomb_exporter

exporter = honeycomb_exporter.HoneycombExporter(writekey="REDACTED", dataset="dataset", service_name="test-app")

tracer = tracer_module.Tracer(exporter=exporter)

# Example for creating nested spans
with tracer.span(name='span1') as span1:
    do_something_to_trace()
    with tracer.span(name='span1_child1') as span1_child1:
        span1_child1.add_annotation("great annotation")
        do_something_to_trace()

```

## Example

Currently there's no easy way to install this. Will get this sorted out sooner than later. For now, you can clone the repo and copy the exporter to the `opencensus/trace/exporters` directory where your Python libraries are.

```bash
git clone https://github.com/codeboten/opencensus-python-honeycomb-exporter
cd opencensus-python-honeycomb-exporter
HONEYCOMB_WRITEKEY=XXXXXX HONEYCOMB_DATASET=test-data-set python example.py
```

## Requirements

```bash
pip install opencensus
pip install libhoney
```

