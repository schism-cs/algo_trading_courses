import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import linear_model

# Number of observations and train/test split
N = 500
split = int(0.8 * N)

# Intercept and slope
alpha = 2.0
beta = 3.0

# Mean and variance of noise in the dataset
eps_mu = 0.0
eps_sigma = 30.0

# Mean and variance of the X data
X_eps = 0.0
X_sigma = 10.0

# Create random noise and data
eps = np.random.normal(loc=eps_mu, scale=eps_sigma, size=N)
X = np.random.normal(loc=X_eps, scale=X_sigma, size=N)
y = alpha + beta * X + eps

X = X.reshape(-1, 1)

# Dataset partition
X_train = X[:split]
y_train = y[:split]

X_test = X[split:]
y_test = y[split:]


# Fit a scikit lin reg to the train data
lr_model = linear_model.LinearRegression()
lr_model.fit(X_train, y_train)

# Output the estimated parameters for the fitted model
print(f"Estimated intercept, slope : {lr_model.intercept_:.3f}, {lr_model.coef_[0]:.3f}")

# Scatterplot of the test data with the fitted estimate line
plt.scatter(X_test, y_test, color='red')
plt.plot(X_test, lr_model.predict(X_test), color='blue', linewidth=1)
plt.xlabel('X')
plt.ylabel('y')
plt.show()