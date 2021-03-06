import os, datetime
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText

#testingtesting
# DoFn to perform on each element in the input PCollection.
# Split names of sponsors into first and last names
class TempDiff(beam.DoFn):
    def process(self, element):
        new_features = []
        features = ['date','temp','templow','tempdiff','hum','baro','wind']
        for feature in features:
            if feature == 'tempdiff':
                if new_features[1] is not None and new_features[2] is not None:
                    new_features.append(round(new_features[1]-new_features[2], 5))
                else:
                    new_features.append(None)
            elif feature == 'date':
                new_features.append(element.get(feature))
            else:
                val = element.get(feature)
                if val is not None:
                    val = round(val, 5)
                new_features.append(val)
        return [tuple(new_features)]

# Reformat into records
class MakeRecord(beam.DoFn):
    def process(self, element):
        record = {}
        features = ['date','temp','templow','tempdiff','hum','baro','wind']
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
            query='SELECT * FROM congress_bills.weather_avg ORDER BY date LIMIT 100'))

    # write PCollection to log file
    query_results | 'Write to input.txt' >> WriteToText('input.txt')

    # apply a ParDo to the PCollection 
    weather_pcoll = query_results | 'Extract Name' >> beam.ParDo(
        TempDiff())

    # write PCollection to log file
    weather_pcoll | 'Write to output.txt' >> WriteToText('output.txt')

    # make BQ records
    out_pcoll = weather_pcoll | 'Make BQ Record' >> beam.ParDo(MakeRecord())

    qualified_table_name = PROJECT_ID + ':congress_bills.Weather_single'
    table_schema = ('date:DATE,temp:FLOAT,templow:FLOAT,tempdiff:FLOAT,hum:FLOAT,baro:FLOAT,wind:FLOAT')
    
    # write to BQ
    out_pcoll | 'Write to BQ' >> beam.io.Write(
        beam.io.BigQuerySink(
            qualified_table_name,
            schema=table_schema,  
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE))
