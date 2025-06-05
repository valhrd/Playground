import numpy as np

range_vals = np.arange(-100, 101)
n1_grid, n2_grid = np.meshgrid(range_vals, range_vals)
n1_flat = n1_grid.flatten()
n2_flat = n2_grid.flatten()

X = np.stack([n1_flat, n2_flat], axis=1)

sums = n1_flat + n2_flat
y_indices = sums + 200

y = np.zeros((X.shape[0], 401))
y[np.arange(X.shape[0]), y_indices] = 1

weights = np.random.randn(401, 2) * 0.01
learning_rate = 0.01

def softmax(z):
    z = z - np.max(z, axis=1, keepdims=True)
    exp_z = np.exp(z)
    return exp_z / np.sum(exp_z, axis=1, keepdims=True)

def categorical_cross_entropy(y_pred, y_true):
    epsilon = 1e-7
    y_pred = y_pred + epsilon
    return -np.mean(np.sum(y_true * np.log(y_pred), axis=1))

epochs = 50

for epoch in range(epochs):
    logits = X @ weights.T
    y_pred = softmax(logits)

    loss = categorical_cross_entropy(y_pred, y)

    grad_logits = (y_pred - y) / X.shape[0]
    grad_weights = grad_logits.T @ X

    weights -= learning_rate * grad_weights

    if epoch % 5 == 0:
        print(f"Epoch {epoch}: Loss = {loss:.4f}")
