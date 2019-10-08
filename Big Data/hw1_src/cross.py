import models_partc
from sklearn.model_selection import KFold, ShuffleSplit
from numpy import mean
import numpy as np
import utils

# USE THE GIVEN FUNCTION NAME, DO NOT CHANGE IT

# USE THIS RANDOM STATE FOR ALL OF YOUR CROSS VALIDATION TESTS, OR THE TESTS WILL NEVER PASS
RANDOM_STATE = 545510477

#input: training data and corresponding labels
#output: accuracy, auc
def get_acc_auc_kfold(X,Y,k=5):
	#TODO:First get the train indices and test indices for each iteration
	#Then train the classifier accordingly
	#Report the mean accuracy and mean auc of all the folds
	kfold = KFold(n_splits=k,random_state=RANDOM_STATE)
	all_acc = []
	all_auc = []
	for train_index, test_index in kfold.split(X):
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = Y[train_index], Y[test_index]
		log_output = models_partc.logistic_regression_pred(X_train, y_train, X_test)
		accuracy,auc,_,_,_ = models_partc.classification_metrics(log_output,y_test)
		all_acc.append(accuracy)
		all_auc.append(auc)
	return mean(np.array(all_acc)),mean(np.array(all_auc))


#input: training data and corresponding labels
#output: accuracy, auc
def get_acc_auc_randomisedCV(X,Y,iterNo=5,test_percent=0.2):
	#TODO: First get the train indices and test indices for each iteration
	#Then train the classifier accordingly
	#Report the mean accuracy and mean auc of all the iterations
	shuffle_split = ShuffleSplit(n_splits=iterNo,test_size=test_percent,random_state=RANDOM_STATE)
	all_acc = []
	all_auc = []
	for train_index, test_index in shuffle_split.split(X):
		X_train, X_test = X[train_index], X[test_index]
		y_train, y_test = Y[train_index], Y[test_index]
		log_output = models_partc.logistic_regression_pred(X_train, y_train, X_test)
		accuracy,auc,_,_,_ = models_partc.classification_metrics(log_output,y_test)
		all_acc.append(accuracy)
		all_auc.append(auc)
	return mean(np.array(all_acc)),mean(np.array(all_auc))


def main():
	X,Y = utils.get_data_from_svmlight("../deliverables/features_svmlight.train")
	print("Classifier: Logistic Regression__________")
	acc_k,auc_k = get_acc_auc_kfold(X,Y)
	print(("Average Accuracy in KFold CV: "+str(acc_k)))
	print(("Average AUC in KFold CV: "+str(auc_k)))
	acc_r,auc_r = get_acc_auc_randomisedCV(X,Y)
	print(("Average Accuracy in Randomised CV: "+str(acc_r)))
	print(("Average AUC in Randomised CV: "+str(auc_r)))

if __name__ == "__main__":
	main()

