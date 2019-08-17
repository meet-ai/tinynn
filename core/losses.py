# Author: borgwang <borgwang@126.com>
#
# Filename: losses.py
# Description: Implementation of common loss functions in neural network.


import numpy as np


class BaseLoss(object):

    def loss(self, predicted, actual):
        raise NotImplementedError

    def grad(self, predicted, actual):
        raise NotImplementedError


class MSELoss(BaseLoss):

    def loss(self, predicted, actual):
        m = predicted.shape[0]
        return 0.5 * np.sum((predicted - actual) ** 2) / m

    def grad(self, predicted, actual):
        m = predicted.shape[0]
        return (predicted - actual) / m


class MAELoss(BaseLoss):

    def loss(self, predicted, actual):
        m = predicted.shape[0]
        return np.sum(np.abs(predicted - actual)) / m

    def grad(self, predicted, actual):
        m = predicted.shape[0]
        return np.sign(predicted - actual) / m


class CrossEntropyLoss(BaseLoss):
    """
    L = weight[class] * (-log(exp(x[class]) / sum(exp(x))))

    weight is a 1D tensor assigning weight to each of the classes.
    """
    def __init__(self, weight=None, sparse=True):
        self._sparse = sparse
        if weight is not None:
            assert len(weight.shape) == 1
            self._weight = np.asarray(weight)
        else:
            self._weight = None

    def loss(self, predicted, actual):
        m = predicted.shape[0]

        exps = np.exp(predicted - np.max(predicted))
        p = exps / np.sum(exps)
        if self._sparse:
            nll = -np.log(np.sum(p * actual, axis=1))
        else:
            nll = -np.log(p[range(m), actual])

        if self._weight is not None:
            nll *= self._weight[actual]
        return np.sum(nll) / m

    def grad(self, predicted, actual):
        m = predicted.shape[0]
        grad = np.copy(predicted)
        if self._sparse:
            grad -= actual
        else:
            grad[range(m), actual] -= 1.0
        return grad / m
