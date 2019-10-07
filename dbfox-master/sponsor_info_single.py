import os
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

# DoFn to perform on each element in the input PCollection.
# Split names of sponsors into first and last names
class SponsorFirstLast(beam.DoFn):
    def process(self, element):
        values = element.get('name')
        name = values.split(',', 1)  # ["last", "first, [suffix] (title)"]
        last = name[0].strip()
        first = name[1].strip().split(' (')[0] # remove the (title)
        district = element.get('district')
        state = element.get('state')
        thomas_id = element.get('thomas_id')
        title = element.get('title')
        return [(first, last, district, state, thomas_id, title)]

# Reformat into records
class MakeRecord(beam.DoFn):
    def process(self, element):
        record = {}
        features = ['first', 'last', 'district', 'state', 'thomas_id', 'title']
        for i in range(len(features)):
            record[features[i]] = element[i]
        return [record]

PROJECT_ID = os.environ['PROJECT_ID']
options = {
    'project': PROJECT_ID
    }
opts = beam.pipeline.PipelineOptions(flags=[], **options)

# Create a Pipeline using a local runner for execution.
with beam.Pipeline('DirectRunner', options=opts) as p:

    query_results = p | 'Read from BigQuery' >> beam.io.Read(
        beam.io.BigQuerySource(
            query='SELECT * FROM congress_bills.sponsor_info LIMIT 100'))

    # write PCollection to log file
    query_results | 'Write to input.txt' >> WriteToText('input.txt')

    # apply a ParDo to the PCollection 
    sponsor_pcoll = query_results | 'Extract Name' >> beam.ParDo(
        SponsorFirstLast())

    # write PCollection to log file
    sponsor_pcoll | 'Write to output.txt' >> WriteToText('output.txt')

    # make BQ records
    out_pcoll = sponsor_pcoll | 'Make BQ Record' >> beam.ParDo(MakeRecord())

    qualified_table_name = PROJECT_ID + ':congress_bills.Sponsors'
    table_schema = ('first:STRING,last:STRING,district:INTEGER,state:STRING,'
                    'thomas_id:INTEGER,title:STRING')

    # write to BQ
    out_pcoll | 'Write to BQ' >> beam.io.Write(
        beam.io.BigQuerySink(
            qualified_table_name,
            schema=table_schema,  
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))
