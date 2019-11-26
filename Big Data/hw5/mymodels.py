import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
import torch.nn.functional as torchfunc
import numpy as np
##### DO NOT MODIFY OR REMOVE THIS VALUE #####
checksum = '169a9820bbc999009327026c9d76bcf1'
##### DO NOT MODIFY OR REMOVE THIS VALUE #####


class MyMLP(nn.Module):
    def __init__(self):
        super(MyMLP, self).__init__()
        self.hidden_1st = nn.Linear(178, 80)
        self.hidden_2nd = nn.Linear(80, 16) #improvement
        self.drop_drop = nn.Dropout(p = 0.5) #improvment
        self.output_layer = nn.Linear(16, 5)
        self.b_norm = nn.BatchNorm1d(178)

    def forward(self, x):
        tensor = torchfunc.relu(self.drop_drop(self.hidden_1st(self.b_norm(x))))
        tensor = torchfunc.relu(self.drop_drop(self.hidden_2nd(tensor)))
        tensor = self.output_layer(tensor)
        return tensor



class MyCNN(nn.Module):
	def __init__(self):
		super(MyCNN, self).__init__()
		self.layer1 = nn.Conv1d(in_channels = 1, out_channels= 6, kernel_size = 5)
		self.layer2 = nn.Conv1d(6, 16, 5) 
		self.pool = nn.MaxPool1d(kernel_size = 2) 
		self.input_layer = nn.Linear(in_features=16 * 41, out_features=128) 
		self.output_layer = nn.Linear(128, 5) 
		self.drop_drop = nn.Dropout(p = 0.1) 

	def forward(self, x):
		#32 x 1 x 178 = x.shape
		tensor = self.pool(torchfunc.relu(self.layer1(x))) 
		tensor = self.pool(torchfunc.relu(self.layer2(tensor))) 
		tensor = tensor.view(-1, 16 * 41) 
		tensor = torchfunc.relu(self.drop_drop(self.input_layer(tensor))) 
		tensor = self.output_layer(tensor) 
		return tensor



class MyRNN(nn.Module):
	def __init__(self):
		super(MyRNN, self).__init__()
		self.rnn_model = nn.GRU(input_size= 1, hidden_size= 16, num_layers = 2, batch_first = True)
		self.input_layer = nn.Linear(in_features = 16, out_features = 5)

	def forward(self, x):
		#32 x 178 x 1 = x.shape
		x, _ = self.rnn_model(x)
		#32 x 178 x 16 = x.shape after 1st GRU with 16 hidden size with any number of num_layers
		x = self.input_layer(torchfunc.relu(x[:, -1, :]))
		return x


class MyVariableRNN(nn.Module):
    def __init__(self, dim_input):
        super(MyVariableRNN, self).__init__()
        self.FC1 = nn.Linear(in_features=dim_input, out_features=32) 
        self.GRU_layer = nn.GRU(input_size=32, hidden_size=16, num_layers=2, batch_first=True, dropout=0.5)
        self.FC2 = nn.Linear(in_features=16, out_features=2) 
        nn.init.xavier_normal_(self.FC2.weight)
    def forward(self, input_tuple):
        seqs, lengths = input_tuple
        seqs = torchfunc.leaky_relu(self.FC1(seqs), negative_slope = 0.02)
        seqs = pack_padded_sequence(seqs, lengths, batch_first=True) 
        seqs, _ = self.GRU_layer(seqs) 
        pack_output, _ = pad_packed_sequence(seqs, batch_first=True) 
        index_ = (torch.LongTensor(lengths) - 1).view(-1, 1).expand(len(lengths), pack_output.size(2)).unsqueeze(1)
        out_out = pack_output.gather(1, index_).squeeze(1)
        seqs = self.FC2(out_out)
        return seqs
