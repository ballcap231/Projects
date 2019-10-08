import utils
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

def read_csv(filepath):
    
    '''
    TODO: This function needs to be completed.
    Read the events.csv, mortality_events.csv and event_feature_map.csv files into events, mortality and feature_map.
    
    Return events, mortality and feature_map
    '''

    #Columns in events.csv - patient_id,event_id,event_description,timestamp,value
    events = pd.read_csv(filepath + 'events.csv')
    
    #Columns in mortality_event.csv - patient_id,timestamp,label
    mortality = pd.read_csv(filepath + 'mortality_events.csv')

    #Columns in event_feature_map.csv - idx,event_id
    feature_map = pd.read_csv(filepath + 'event_feature_map.csv')
    """
    aggregate_events
    """
    return events, mortality, feature_map    
def calculate_index_date(events, mortality, deliverables_path):
    '''
    TODO: This function needs to be completed.    
    Suggested steps:
    1. Create list of patients alive ( mortality_events.csv only contains information about patients deceased)
    2. Split events into two groups based on whether the patient is alive or deceased
    3. Calculate index date for each patient
    
    IMPORTANT:
    Save indx_date to a csv file in the deliverables folder named as etl_index_dates.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, indx_date.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)

    Return indx_date
    '''
    mort_df = pd.concat([mortality.patient_id,(pd.to_datetime(mortality.timestamp)) - timedelta(days=30)], axis=1)
    mortality_list = mortality.patient_id
    alive_df = events[~events['patient_id'].isin(mortality_list)]
    alive_df = alive_df.groupby('patient_id').max().timestamp.reset_index()
    alive_df['timestamp'] = pd.to_datetime(alive_df['timestamp'])
    indx_date = pd.concat([mort_df,alive_df], axis = 0)
    indx_date.rename(columns = {'timestamp':'indx_date'},inplace=True)
        
    indx_date.to_csv(deliverables_path + 'etl_index_dates.csv', columns=['patient_id', 'indx_date'], index=False)
    return indx_date


def filter_events(events, indx_date, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 b

    Suggested steps:
    1. Join indx_date with events on patient_id
    2. Filter events occuring in the observation window(IndexDate-2000 to IndexDate)
    
    
    IMPORTANT:
    Save filtered_events to a csv file in the deliverables folder named as etl_filtered_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header 
    For example if you are using Pandas, you could write: 
        filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)

    Return filtered_events
    '''
    merged = pd.merge(events,indx_date, on = 'patient_id')
    filtered_events = merged[((pd.to_datetime(merged.indx_date) - pd.to_datetime(merged.timestamp)).dt.days).between(0,2000)]
    filtered_events.to_csv(deliverables_path + 'etl_filtered_events.csv', columns=['patient_id', 'event_id', 'value'], index=False)
    return filtered_events


def aggregate_events(filtered_events_df, mortality_df,feature_map_df, deliverables_path):
    
    '''
    TODO: This function needs to be completed.

    Refer to instructions in Q3 c

    Suggested steps:
    1. Replace event_id's with index available in event_feature_map.csv
    2. Remove events with n/a values
    3. Aggregate events using sum and count to calculate feature value
    4. Normalize the values obtained above using min-max normalization(the min value will be 0 in all scenarios)   
    
    IMPORTANT:
    Save aggregated_events to a csv file in the deliverables folder named as etl_aggregated_events.csv. 
    Use the global variable deliverables_path while specifying the filepath. 
    Each row is of the form patient_id, event_id, value.
    The csv file should have a header .
    For example if you are using Pandas, you could write: 
        aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)

    Return filtered_events
    '''
    #dropping NA from merged feature_map df
    full_events = pd.merge(filtered_events_df,feature_map_df,on="event_id",how="inner")
    full_events = full_events.loc[:,['patient_id','event_id','value','idx']].dropna()
    #splitting into counting and summing groups
    counters = full_events[full_events["event_id"].apply(lambda x: x.find("LAB")!=-1)]
    summers = full_events[~full_events["event_id"].apply(lambda x: x.find("LAB")!=-1)]
    #Processing then merging back lab summing and counting dataframe
    Diag_and_Drug = summers["value"].groupby([summers["patient_id"],summers["idx"]]).sum().to_frame().reset_index()
    Lab = counters["value"].groupby([counters["patient_id"],counters["idx"]]).count().to_frame().reset_index()
    patient_group = pd.concat([Diag_and_Drug[["patient_id","idx","value"]],Lab[["patient_id","idx","value"]]])
    #Normalizing value
    patient_group = pd.merge(patient_group,patient_group["value"].groupby(patient_group["idx"]).max().reset_index().rename(columns={"value":"normalizer"}),on="idx",how="inner")
    patient_group["value_norm"] = patient_group["value"]/patient_group["normalizer"]
    aggregated_events = patient_group[["patient_id","idx","value_norm"]].rename(columns={"idx":"feature_id","value_norm":"feature_value"})
    aggregated_events.sort_values(by=['patient_id','feature_value']).reset_index(drop=True)
    aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)
    return aggregated_events

def create_features(events, mortality, feature_map):
    
    deliverables_path = '../deliverables/'

    #Calculate index date
    indx_date = calculate_index_date(events, mortality, deliverables_path)

    #Filter events in the observation window
    filtered_events = filter_events(events, indx_date,  deliverables_path)
    
    #Aggregate the event values for each patient 
    aggregated_events = aggregate_events(filtered_events, mortality, feature_map, deliverables_path)

    '''
    TODO: Complete the code below by creating two dictionaries - 
    1. patient_features :  Key - patient_id and value is array of tuples(feature_id, feature_value)
    2. mortality : Key - patient_id and value is mortality label
    '''
    #Sorting aggregated_events as precaution
    aggregated_events = aggregated_events.sort_values(by=['patient_id','feature_id'],ascending=True).reset_index(drop='True')
    #creating patient_features
    patient_features = dict()
    for grouped_val, grouped_df in aggregated_events.groupby('patient_id'):
        tuples = [tuple(x) for x in grouped_df[['feature_id','feature_value']].values]
        patient_features.update({grouped_val:tuples})


    #creating mortality dictionary
    alive_df = aggregated_events[~aggregated_events['patient_id'].isin(mortality.patient_id)]
    dead_df = aggregated_events[aggregated_events['patient_id'].isin(mortality.patient_id)]
    alive_df = alive_df.assign(label=0)
    dead_df = dead_df.assign(label=1)
    dead_alive_df = pd.concat([alive_df,dead_df],axis=0).sort_values(by=['patient_id','feature_id'],ascending=True).reset_index(drop='True')
    mortality = dict(zip(dead_alive_df.patient_id,dead_alive_df.label))

    return patient_features, mortality

def save_svmlight(patient_features, mortality, op_file, op_deliverable):
    
    '''
    TODO: This function needs to be completed

    Refer to instructions in Q3 d

    Create two files:
    1. op_file - which saves the features in svmlight format. (See instructions in Q3d for detailed explanation)
    2. op_deliverable - which saves the features in following format:
       patient_id1 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...
       patient_id2 label feature_id:feature_value feature_id:feature_value feature_id:feature_value ...  
    
    Note: Please make sure the features are ordered in ascending order, and patients are stored in ascending order as well.     
    '''
    for patients_id in patient_features.keys():
            patient_features[patients_id] = sorted(patient_features[patients_id])
            patient_features[patients_id] = utils.bag_to_svmlight(patient_features[patients_id])

    op_file_str = "".join(
        [str(int(mortality[patients_id])) + " " +
        patient_features[patients_id] + " \n" for patients_id in sorted(patient_features.keys())])

    op_deliverable_str = "".join(
        [str(int(patients_id)) +" "+ str(int(mortality[patients_id])) + 
        " "+ patient_features[patients_id] + " \n" for patients_id in sorted(patient_features.keys())])

    deliverable1 = open(op_file, 'wb')
    deliverable2 = open(op_deliverable, 'wb')
    
    deliverable1.write(bytes((op_file_str),'UTF-8')); #Use 'UTF-8'
    deliverable2.write(bytes((op_deliverable_str),'UTF-8'));

def main():
    train_path = '../data/train/'
    events, mortality, feature_map = read_csv(train_path)
    patient_features, mortality = create_features(events, mortality, feature_map)
    save_svmlight(patient_features, mortality, '../deliverables/features_svmlight.train', '../deliverables/features.train')

if __name__ == "__main__":
    main()