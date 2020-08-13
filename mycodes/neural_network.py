import numpy as np
from graph import transpose

class NeuralNetwork:

    def __init__(self, x, y, epochs=1000, threshold=0.9):
        self.x = x
        self.y = y
        self.epochs = epochs
        self.threshold = threshold
        self.weights = 2 * np.random.random((3,1)) - 1

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_deriv(self, x):
        return x * (1 - x)

    def train(self):
        for _ in range(self.epochs):
            output = self.train_observation(self.x)
            error = self.y - output
            self.weights += np.dot(transpose(self.x), error * self.sigmoid_deriv(output))

    def train_observation(self, x):
        res = self.sigmoid(np.dot(self.x, self.weights))
        return res

    def predict(self, x):
        return int(np.dot(x, self.weights) > self.threshold)

x = [[1, 1, 1], [1, 0, 1], [0, 0, 1]]
y = transpose([[1, 1, 0]])

net = NeuralNetwork(x, y)
net.train()
p = net.predict([0, 1, 0])
print(p)