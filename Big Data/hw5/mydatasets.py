import numpy as np
import pandas as pd
from scipy import sparse
import torch
from torch.utils.data import TensorDataset, Dataset
from functools import reduce

##### DO NOT MODIFY OR REMOVE THIS VALUE #####
checksum = '169a9820bbc999009327026c9d76bcf1'
##### DO NOT MODIFY OR REMOVE THIS VALUE #####

def load_seizure_dataset(path, model_type):
    """
    :param path: a path to the seizure data CSV file
    :return dataset: a TensorDataset consists of a data Tensor and a target Tensor
    """
    # TODO: Read a csv file from path.
    # TODO: Please refer to the header of the file to locate X and y.
    # TODO: y in the raw data is ranging from 1 to 5. Change it to be from 0 to 4.
    # TODO: Remove the header of CSV file of course.
    # TODO: Do Not change the order of rows.
    # TODO: You can use Pandas if you want to.
    df = pd.read_csv(path)
    input_ = torch.from_numpy(df.iloc[:,:-1].to_numpy().astype("float32"))
    target = torch.from_numpy(df.y.to_numpy().astype("long") - 1)

    if model_type == 'MLP':
        data = input_
        dataset = TensorDataset(data, target)
    elif model_type == 'CNN':
        data = input_.unsqueeze(1)
        dataset = TensorDataset(data, target)
    elif model_type == 'RNN':
        data = input_.unsqueeze(2)
        dataset = TensorDataset(data, target)
    else:
        raise AssertionError("Wrong Model Type!")

    return dataset


def calculate_num_features(seqs):
    """
    :param seqs:
    :return: the calculated number of features
    """
    # TODO: Calculate the number of features (diagnoses codes in the train set)
    lambda_func = lambda x,y: x + y
    fee = reduce(lambda_func, seqs)
    fee = reduce(lambda_func, fee)
    num_features = int(max(fee) + 1)
    return num_features


class VisitSequenceWithLabelDataset(Dataset):
    def __init__(self, seqs, labels, num_features):
        """
        Args:
            seqs (list): list of patients (list) of visits (list) of codes (int) that contains visit sequences
            labels (list): list of labels (int)
            num_features (int): number of total features available
        """

        if len(seqs) != len(labels):
            raise ValueError("Seqs and Labels have different lengths")

        self.labels = labels

        # TODO: Complete this constructor to make self.seqs as a List of which each element represent visits of a patient
        # TODO: by Numpy matrix where i-th row represents i-th visit and j-th column represent the feature ID j.
        # TODO: You can use Sparse matrix type for memory efficiency if you want.

        final_ls = []
        for example in seqs:
            mtx = np.zeros((len(example), num_features))
            for count,example_one in enumerate(example):
                for ii in example_one:
                    mtx[count, ii] = 1
            final_ls.append(mtx)
            self.seqs = final_ls

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        # returns will be wrapped as List of Tensor(s) by DataLoader
        return self.seqs[index], self.labels[index]


def visit_collate_fn(batch):
    """
    DataLoaderIter call - self.collate_fn([self.dataset[i] for i in indices])
    Thus, 'batch' is a list [(seq1, label1), (seq2, label2), ... , (seqN, labelN)]
    where N is minibatch size, seq is a (Sparse)FloatTensor, and label is a LongTensor

    :returns
        seqs (FloatTensor) - 3D of batch_size X max_length X num_features
        lengths (LongTensor) - 1D of batch_size
        labels (LongTensor) - 1D of batch_size
    """

    # TODO: Return the following two things
    # TODO: 1. a tuple of (Tensor contains the sequence data , Tensor contains the length of each sequence),
    # TODO: 2. Tensor contains the label of each sequence

    num_rows = []
    for count, (seq, _) in enumerate(batch):
        num_rows.append((len(seq), count))
    num_rows.sort(key = lambda s: s[0], reverse=True)
    line_row = num_rows[0][0]
    line_col = batch[0][0].shape[1]
    seqs_ls,labels_ls,length_ls = [], [], []
    for ii in list(map(lambda xx: xx[1], num_rows)):
        patient = batch[ii]
        sparse_matrix = np.zeros((line_row, line_col))
        sparse_matrix[0:len(patient[0]), 0:patient[0].shape[1]] = patient[0]
        seqs_ls.append(sparse_matrix)
        labels_ls.append(patient[1])
        length_ls.append(len(patient[0]))
        
    seqs_tensor = torch.FloatTensor(seqs_ls)
    lengths_tensor = torch.LongTensor(length_ls)
    labels_tensor = torch.LongTensor(labels_ls)

    return (seqs_tensor, lengths_tensor), labels_tensor
