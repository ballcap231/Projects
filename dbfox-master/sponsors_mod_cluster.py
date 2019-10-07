import os, datetime
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
        title = name[1].strip().split('(')[1].split(')')[0]
        # repeat for cosponsor
        values = element.get('cospons_name')
        cosp_name = values.split(',', 1)
        cosp_last = cosp_name[0].strip()
        cosp_first = cosp_name[1].strip().split(' (')[0]
        cosp_title = cosp_name[1].strip().split('(')[1].split(')')[0]
        bill_id = element.get('bill_id')
        sponsored_at = element.get('sponsored_at')
        withdrawn_at = element.get('withdrawn_at')
        return [(bill_id, first, last, title, cosp_first, cosp_last, cosp_title,
                 sponsored_at, withdrawn_at)]

# Reformat into records
class MakeRecord(beam.DoFn):
    def process(self, element):
        record = {}
        features = ['bill_id', 'first', 'last', 'title', 'cosp_first', 'cosp_last',
                    'cosp_title','sponsored_at','withdrawn_at']
        for i in range(len(features)):
            record[features[i]] = element[i]
        return [record]

PROJECT_ID = os.environ['PROJECT_ID']
BUCKET = os.environ['BUCKET']
DIR_PATH = BUCKET + '/output/' + datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '/'

# run pipeline on Dataflow 
options = {
    'runner': 'DataflowRunner',
    'job_name': 'transform-sponsors-mod-table',
    'project': PROJECT_ID,
    'temp_location': BUCKET + '/temp',
    'staging_location': BUCKET + '/staging',
    'machine_type': 'n1-standard-2', # machine types listed here: https://cloud.google.com/compute/docs/machine-types
    'num_workers': 5
}
opts = beam.pipeline.PipelineOptions(flags=[], **options)

# Create a Pipeline using a local runner for execution.
with beam.Pipeline('DataflowRunner', options=opts) as p:

    query_results = p | 'Read from BigQuery' >> beam.io.Read(
        beam.io.BigQuerySource(
            query='SELECT * FROM congress_bills.sponsors_mod'))

    # write PCollection to log file
    query_results | 'Write to input.txt' >> WriteToText(DIR_PATH + 'input.txt')

    # apply a ParDo to the PCollection 
    sponsor_pcoll = query_results | 'Extract Name' >> beam.ParDo(
        SponsorFirstLast())

    # write PCollection to log file
    sponsor_pcoll | 'Write to output.txt' >> WriteToText(DIR_PATH + 'output.txt')

    # make BQ records
    out_pcoll = sponsor_pcoll | 'Make BQ Record' >> beam.ParDo(MakeRecord())

    qualified_table_name = PROJECT_ID + ':congress_bills.BillSponsors'
    table_schema = ('bill_id:STRING,first:STRING,last:STRING,title:STRING,'
                    'cosp_first:STRING,cosp_last:STRING,cosp_title:STRING,'
                    'sponsored_at:DATE,withdrawn_at:TIMESTAMP')

    # write to BQ
    out_pcoll | 'Write to BQ' >> beam.io.Write(
        beam.io.BigQuerySink(
            qualified_table_name,
            schema=table_schema,  
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))