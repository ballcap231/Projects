import utils
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, ShuffleSplit
from numpy import mean
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score,accuracy_score
#from etl import read_csv,create_features,calculate_index_date,filter_events,aggregate_events

#Note: You can reuse code that you wrote in etl.py and models.py and cross.py over here. It might help.
# PLEASE USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT
def aggregate_events(filtered_events_df, feature_map_df):
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
	#aggregated_events.to_csv(deliverables_path + 'etl_aggregated_events.csv', columns=['patient_id', 'feature_id', 'feature_value'], index=False)
	return aggregated_events

'''
You may generate your own features over here.
Note that for the test data, all events are already filtered such that they fall in the observation window of their respective patients. 
Thus, if you were to generate features similar to those you constructed in code/etl.py for the test data, 
all you have to do is aggregate events for each patient.
IMPORTANT: Store your test data features in a file called "test_features.txt" where each line has the
patient_id followed by a space and the corresponding feature in sparse format.
Eg of a line:
60 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514
Here, 60 is the patient id and 971:1.000000 988:1.000000 1648:1.000000 1717:1.000000 2798:0.364078 3005:0.367953 3049:0.013514 is the feature for the patient with id 60.

Save the file as "test_features.txt" and save it inside the folder deliverables

input:
output: X_train,Y_train,X_test
'''
def my_features():
	#TODO: complete this
	train_path = '../data/test/'
	events = pd.read_csv(train_path + 'events.csv')
	feature_map = pd.read_csv(train_path + 'event_feature_map.csv')
	aggregated = aggregate_events(events,feature_map)

	#Sorting aggregated_events as precaution
	aggregated_events = aggregated.sort_values(by=['patient_id','feature_id'],ascending=True).reset_index(drop='True')
	#creating patient_features
	patient_features = dict()
	for grouped_val, grouped_df in aggregated_events.groupby('patient_id'):
		tuples = [tuple(x) for x in grouped_df[['feature_id','feature_value']].values]
		patient_features.update({grouped_val:tuples})

	for patients_id in patient_features.keys():
		patient_features[patients_id] = sorted(patient_features[patients_id])
		patient_features[patients_id] = utils.bag_to_svmlight(patient_features[patients_id])

	op_my_model_str = "".join(
		[str(int(patients_id)) +
		" "+ patient_features[patients_id] + " \n" for patients_id in sorted(patient_features.keys())])

	deliverable1 = open('../deliverables/test_features.txt', 'wb')
	deliverable1.write(bytes((op_my_model_str),'UTF-8')) #Use 'UTF-8'
	deliverable1.close()

	X_train, Y_train = utils.get_data_from_svmlight("../deliverables/features_svmlight.train")
	X_test, Fake_y = utils.get_data_from_svmlight('../deliverables/test_features.txt')
	print(X_train.shape)
	print(Y_train.shape)
	print(X_test.shape)
	print(Fake_y.shape)
	return X_train,Y_train,X_test

'''
You can use any model you wish.

input: X_train, Y_train, X_test
output: Y_pred
'''
RANDOM_STATE = 545510477
def my_classifier_predictions(X_train,Y_train,X_test):
	#TODO: complete this
	kfold = KFold(n_splits=5,random_state=RANDOM_STATE)
	all_acc = []
	all_auc = []
	for train_index, test_index in kfold.split(X_train):
		X_training, X_testing = X_train[train_index], X_train[test_index]
		y_training, y_testing = Y_train[train_index], Y_train[test_index]
		model = GradientBoostingClassifier(max_depth=5,random_state=RANDOM_STATE).fit(X_training, y_training)
		log_output = model.predict(X_testing)
		auc = roc_auc_score(log_output,y_testing)
		accuracy = accuracy_score(log_output,y_testing)
		all_acc.append(accuracy)
		all_auc.append(auc)
	all_acc_avg, all_auc_avg = mean(np.array(all_acc)),mean(np.array(all_auc))
	#print(all_acc_avg,all_auc_avg)

	kfold = KFold(n_splits=5,random_state=RANDOM_STATE)
	all_acc = []
	all_auc = []
	for train_index, test_index in kfold.split(X_train):
		X_training, X_testing = X_train[train_index], X_train[test_index]
		y_training, y_testing = Y_train[train_index], Y_train[test_index]
		model = RandomForestClassifier(max_depth=5,random_state=RANDOM_STATE).fit(X_training, y_training)
		log_output = model.predict(X_testing)
		auc = roc_auc_score(log_output,y_testing)
		accuracy = accuracy_score(log_output,y_testing)
		all_acc.append(accuracy)
		all_auc.append(auc)
	all_acc_avg, all_auc_avg = mean(np.array(all_acc)),mean(np.array(all_auc))
	#print(all_acc_avg,all_auc_avg)

	clf1 = GradientBoostingClassifier(max_depth=5,random_state=RANDOM_STATE).fit(X_train,Y_train)
	Y_pred = clf1.predict(X_test)
	return Y_pred


def main():
	X_train, Y_train, X_test = my_features()
	Y_pred = my_classifier_predictions(X_train,Y_train,X_test)
	utils.generate_submission("../deliverables/test_features.txt",Y_pred)
	#The above function will generate a csv file of (patient_id,predicted label) and will be saved as "my_predictions.csv" in the deliverables folder.

if __name__ == "__main__":
    main()

	