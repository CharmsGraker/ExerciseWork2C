import numpy as np
import tensorflow as tf

from keras.layers.recurrent_v2 import LSTM
from spektral.layers import GCNConv, GATConv
from tensorflow.python.keras import Input
from tensorflow.python.keras.models import Model
import keras
from keras.optimizers import Adam

sequence_length = 10

X_train_feat = 3
from keras.layers import Flatten, Concatenate, Dropout, Dense, BatchNormalization

import torch


def get_laplacian(self, graph, normalize):
    """
    return the laplacian of the graph.
    :param graph: the graph structure without self loop, [N, N].
    :param normalize: whether to used the normalized laplacian.
    :return: graph laplacian.
    """
    """
    得到图的拉普拉斯矩阵
    """
    if normalize:
        D = torch.diag(torch.sum(graph, dim=-1) ** (-1 / 2))
        L = torch.eye(graph.size(0), device=graph.device, dtype=graph.dtype) - torch.mm(torch.mm(D, graph), D)
    else:
        D = torch.diag(torch.sum(graph, dim=-1))
        L = D - graph
    return L


def Graphmodel():
    nodes_cnt = 195
    input_feature = 3
    inp_seq = Input((sequence_length, nodes_cnt))
    adj = GATConv((nodes_cnt, input_feature), concat_heads=nodes_cnt)
    adj = np.mean(adj, axis=-1)
    inp_lap = get_laplacian(adj, normalize=True)
    # inp_lap = Input((nodes_cnt, nodes_cnt))
    inp_feat = Input((nodes_cnt, X_train_feat.shape[-1]))
    x = GCNConv(32, activation='relu')([inp_feat, inp_lap])
    x = GCNConv(16, activation='relu')([x, inp_lap])
    x = Flatten()(x)
    xx = LSTM(128, activation='relu', return_sequences=True)(inp_seq)
    xx = LSTM(32, activation='relu')(xx)
    x = Concatenate()([x, xx])
    x = BatchNormalization()(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.3)(x)
    out = Dense(1)(x)
    model = Model([inp_seq, inp_feat], out)
    model.compile(optimizer=Adam(0.1), loss='mse', metrics=[tf.keras.metrics.RootMeanSquaredError()])
    return model
