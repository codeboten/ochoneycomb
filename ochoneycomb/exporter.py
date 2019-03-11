# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Export the trace spans to Honeycomb"""

import datetime

import libhoney
import libhoney.state as state
from opencensus.trace.exporters import base
from opencensus.common.transports import sync
from opencensus.common.utils import timestamp_to_microseconds, ISO_DATETIME_REGEX

class HoneycombExporter(base.Exporter):
    """Export the spans to Honeycomb.

    :type service_name: str
    :param service_name: Service that logged an annotation in a trace.
                         Classifier when query for spans.
    :type writekey: str
    :param writekey: Honeycomb write key.
    :type dataset: str
    :param dataset: Dataset identifier.
    :type sample_fraction: float
    :param sample_fraction: Set on the exporter to be the sample rate given to the ProbabilitySampler if used.
    :type transport: :class:`type`
    :param transport: Class for creating new transport objects. It should
                      extend from the base :class:`.Transport` type and
                      implement :meth:`.Transport.export`. Defaults to
                      :class:`.SyncTransport`. The other option is
                      :class:`.AsyncTransport`.
    """

    def __init__(
            self,
            writekey=None,
            dataset=None,
            service_name=None,
            sample_fraction=0,
            transport=sync.SyncTransport,
            ):
        
        libhoney.init(writekey=writekey, dataset=dataset, debug=True)
        self.builder = libhoney.Builder()
        self.service_name = service_name
        self.sample_fraction = sample_fraction
        self.transport = transport(self)

    def emit(self, span_datas):
        """Send SpanData tuples to Honeycomb API.
        :type span_datas: list of :class:
            `~opencensus.trace.span_data.SpanData`
        :param list of opencensus.trace.span_data.SpanData span_datas:
            SpanData tuples to emit
        """
        for sd in span_datas:
            ev = self.builder.new_event()
            hs = honeycombSpan(sd)
            ev.add(hs)

            ev.created_at = datetime.datetime.strptime(sd.start_time, ISO_DATETIME_REGEX)
            # Add an event field for each attribute
            if len(sd.attributes) != 0:
                for (key, value) in sd.attributes:
                    ev.add_field(key, value) 
                
            # Add an event field for status code and status message
            if sd.status and sd.status.code != 0:
                ev.add_field("status_code", sd.status.code)
            
            if sd.status and sd.status.message != "":
                ev.add_field("status_description", sd.status.message)

            if self.sample_fraction != 0:
                ev.sample_rate = 1 / self.sample_fraction
            
            if self.service_name is not None:
                ev.add_field("service_name", self.service_name)
            
            ev.send()

    def export(self, span_datas):
        self.transport.export(span_datas)

def honeycombSpan(span_data):
    start_timestamp_mus = timestamp_to_microseconds(span_data.start_time)
    end_timestamp_mus = timestamp_to_microseconds(span_data.end_time)

    sc = span_data.context
    hcSpan = {
        "trace.trace_id": sc.trace_id,
        "name": span_data.name,
        "trace.span_id": span_data.span_id,
        "duration_ms": round((end_timestamp_mus - start_timestamp_mus) / 1000),
    }
    if span_data.parent_span_id != None:
        hcSpan["trace.parent_id"] = span_data.parent_span_id
    
    if len(span_data.time_events):
        hcSpan["annotations"] = _extract_annotations_from_span(span_data)
    
    return hcSpan

def _extract_annotations_from_span(span):
    """Extract and convert time event annotations to Honeycomb annotations"""
    if span.time_events is None:
        return []

    annotations = []
    for time_event in span.time_events:
        annotation = time_event.annotation
        if not annotation:
            continue

        annotations.append({'timestamp': time_event.timestamp,
                            'value': annotation.description})

    return annotations