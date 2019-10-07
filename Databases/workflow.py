import datetime
from airflow import models
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_dag_args = {
    # https://airflow.apache.org/faq.html#what-s-the-deal-with-start-date
    'start_date': datetime.datetime(2019, 5, 3)
}

###### SQL variables ###### 
sql_cmd_start = 'bq query --use_legacy_sql=false '

sql_weather_create = '''create table workflow.weather as (
                     select * from congress_bills.weather)'''
sql_weather_group_by = '''create table workflow.weather_avg as (
                     select date, avg(temp) as temp, avg(templow) as templow, avg(hum) as hum, avg(baro) as baro, avg(wind) as wind
                     from workflow.weather group by date order by date desc)'''

###### Beam variables ######          
LOCAL_MODE=1 # run beam jobs locally
DIST_MODE=2  # run beam jobs on Dataflow

mode=LOCAL_MODE

if mode == LOCAL_MODE:
    weather_script = 'weather_single.py'
    
if mode == DIST_MODE:
    weather_script = 'weather_cluster.py'

###### DAG section ###### 
with models.DAG(
        'workflow',
        schedule_interval=datetime.timedelta(days=1),
        default_args=default_dag_args) as dag:

    ###### SQL tasks ######
    delete_dataset = BashOperator(
            task_id='delete_dataset',
            bash_command='bq rm -r -f workflow')
                
    create_dataset = BashOperator(
            task_id='create_dataset',
            bash_command='bq mk workflow')
                    
    create_weather_table = BashOperator(
            task_id='create_weather_table',
            bash_command=sql_cmd_start + '"' + sql_weather_create + '"')
            
    group_by_weather_table = BashOperator(
            task_id='group_by_weather_table',
            bash_command=sql_cmd_start + '"' + sql_weather_group_by + '"')
            
    ###### Beam tasks ######     
    weather_beam = BashOperator(
            task_id='student_beam',
            bash_command='python /home/uohzgniy/dbfox/' + weather_script)
            
    transition = DummyOperator(task_id='transition')
            
    delete_dataset >> create_dataset >> create_weather_table >> group_by_weather_table >> transition
    transition >> weather_beam
