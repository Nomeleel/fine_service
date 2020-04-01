from module.neuralnetwork.neuralNetwork import NeuralNetwork
from util import singleton
import numpy as np
import os

@singleton.singleton
class DigitalRecognizer:

    def __init__(self):
        self.neuralNetwork = NeuralNetwork(os.getcwd() + '\\module\\neuralnetwork\\dataset\\digit')

    def digitRecognition(self, target):
        score = self.neuralNetwork.recognition(target)
        digit = np.argmax(score)

        return str(digit) if score[digit] > 0.5 else None