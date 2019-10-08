import time
import pandas as pd
import numpy as np


# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    '''
    TODO : This function needs to be completed.
    Read the events.csv and mortality_events.csv files. 
    Variables returned from this function are passed as input to the metric functions.
    '''
    events = pd.read_csv(filepath + 'events.csv')
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    return events, mortality

def event_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the event count metrics.
    Event count is defined as the number of events recorded for a given patient.
    '''
    mortality_list = mortality.patient_id
    alive_df = events[~events['patient_id'].isin(mortality_list)]
    dead_df = events[events['patient_id'].isin(mortality_list)]
    alive_event_count = alive_df.groupby('patient_id').count().event_id
    dead_event_count = dead_df.groupby('patient_id').count().event_id


    avg_dead_event_count = dead_event_count.mean()
    max_dead_event_count = dead_event_count.max()
    min_dead_event_count = dead_event_count.min()
    avg_alive_event_count = alive_event_count.mean()
    max_alive_event_count = alive_event_count.max()
    min_alive_event_count = alive_event_count.min()

    return min_dead_event_count, max_dead_event_count, avg_dead_event_count, min_alive_event_count, max_alive_event_count, avg_alive_event_count

def encounter_count_metrics(events, mortality):
    '''
    TODO : Implement this function to return the encounter count metrics.
    Encounter count is defined as the count of unique dates on which a given patient visited the ICU. 
    '''
    unique_t_events = events.drop_duplicates(['patient_id','timestamp'])
    mortality_list = mortality.patient_id
    alive_df = unique_t_events[~unique_t_events['patient_id'].isin(mortality_list)]
    dead_df = unique_t_events[unique_t_events['patient_id'].isin(mortality_list)]
    alive_encounter_count = alive_df.groupby('patient_id').count().event_id
    dead_encounter_count = dead_df.groupby('patient_id').count().event_id

    avg_dead_encounter_count = dead_encounter_count.mean()
    max_dead_encounter_count = dead_encounter_count.max()
    min_dead_encounter_count = dead_encounter_count.min()
    avg_alive_encounter_count = alive_encounter_count.mean()
    max_alive_encounter_count = alive_encounter_count.max()
    min_alive_encounter_count = alive_encounter_count.min()

    return min_dead_encounter_count, max_dead_encounter_count, avg_dead_encounter_count, min_alive_encounter_count, max_alive_encounter_count, avg_alive_encounter_count

def record_length_metrics(events, mortality):
    '''
    TODO: Implement this function to return the record length metrics.
    Record length is the duration between the first event and the last event for a given patient. 
    '''
    mortality_list = mortality.patient_id
    alive_df = events[~events['patient_id'].isin(mortality_list)]
    dead_df = events[events['patient_id'].isin(mortality_list)]
    alive_min = alive_df.groupby('patient_id').min().timestamp
    alive_max = alive_df.groupby('patient_id').max().timestamp
    dead_min = dead_df.groupby('patient_id').min().timestamp
    dead_max = dead_df.groupby('patient_id').max().timestamp


    avg_dead_rec_len = round((pd.to_datetime(dead_max) - pd.to_datetime(dead_min)).mean().total_seconds() / (24 * 60 * 60) *2)/2
    max_dead_rec_len = (pd.to_datetime(dead_max) - pd.to_datetime(dead_min)).max().days
    min_dead_rec_len = (pd.to_datetime(dead_max) - pd.to_datetime(dead_min)).min().days
    avg_alive_rec_len = round((pd.to_datetime(alive_max) - pd.to_datetime(alive_min)).mean().total_seconds() / (24 * 60 * 60) *2)/2
    max_alive_rec_len = (pd.to_datetime(alive_max) - pd.to_datetime(alive_min)).max().days
    min_alive_rec_len = (pd.to_datetime(alive_max) - pd.to_datetime(alive_min)).min().days

    return min_dead_rec_len, max_dead_rec_len, avg_dead_rec_len, min_alive_rec_len, max_alive_rec_len, avg_alive_rec_len

def main():
    '''
    DO NOT MODIFY THIS FUNCTION.
    '''
    # You may change the following path variable in coding but switch it back when submission.
    train_path = '../data/train/'

    # DO NOT CHANGE ANYTHING BELOW THIS ----------------------------
    events, mortality = read_csv(train_path)

    #Compute the event count metrics
    start_time = time.time()
    event_count = event_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute event count metrics: " + str(end_time - start_time) + "s"))
    print(event_count)

    #Compute the encounter count metrics
    start_time = time.time()
    encounter_count = encounter_count_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute encounter count metrics: " + str(end_time - start_time) + "s"))
    print(encounter_count)

    #Compute record length metrics
    start_time = time.time()
    record_length = record_length_metrics(events, mortality)
    end_time = time.time()
    print(("Time to compute record length metrics: " + str(end_time - start_time) + "s"))
    print(record_length)
    
if __name__ == "__main__":
    main()
