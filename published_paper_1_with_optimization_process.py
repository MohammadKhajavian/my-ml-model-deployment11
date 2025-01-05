# -*- coding: utf-8 -*-
"""Published paper 1 with optimization process.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Q1-Vgqzyt_W-alrhfA79GCyEReQQoFW

#Linear reg modeling (standscaler just used for X (not y)
"""

pip install --upgrade keras

pip install scikeras[tensorflow]

from pandas import read_csv
from keras.models import Sequential
from keras.layers import Dense
#from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

df = read_csv("input.csv")

df

"""#Data splitting"""

X = df.drop('Removal', axis = 1)
Y = df['Removal']

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=20)

"""#Scaling data"""

from sklearn.preprocessing import StandardScaler
scaler=StandardScaler()
scaler.fit(X_train)

X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

"""#experiment with deeper and wider networl"""

model = Sequential()
model.add(Dense(128, input_dim=3, activation='relu'))
model.add(Dense(64, activation='relu'))

"""#Output layer"""

model.add(Dense(1, activation='linear'))
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['mae'])
model.summary()

history = model.fit(X_train_scaled, Y_train, validation_split=0.2, epochs=100)

"""#plot training and validation accuracy and and loss at each epoch"""

loss = history.history['loss']
val_loss = history.history['val_loss']
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, 'y', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.xlabel('Epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

acc = history.history['mae']
val_acc = history.history['val_mae']
plt.plot(epochs, acc, 'y', label='Training MAE')
plt.plot(epochs, val_acc, 'r', label='Validation MAE')
plt.title('Training and validation MAE')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()
plt.show()

# Predictions vs. Actual values
predictions = model.predict(X_train_scaled)
plt.figure(figsize=(10, 6))
sns.scatterplot(x=Y_train, y=predictions.flatten())
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title('Actual vs. Predicted Values')
plt.show()

# Residuals plot
residuals = Y_train - predictions.flatten()
plt.figure(figsize=(10, 6))
sns.scatterplot(x=predictions.flatten(), y=residuals)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()

# Distribution of Residuals
plt.figure(figsize=(10, 6))
sns.histplot(residuals, kde=True)
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Distribution of Residuals')
plt.show()

"""# Predict test data"""

predictions = model.predict(X_test_scaled[:5])
print("Predicted values are:", predictions)
print("Real values are:", Y_test[:5])

"""#Compare with other models

# Nueral Network
"""

mse_neural, mae_neural = model.evaluate(X_test_scaled, Y_test)
print('Mean squared error from neural net:', mse_neural)
print('Mean absolute error from neural net:', mae_neural)

"""#optmization for NN method"""

pip install --upgrade scipy

from scipy.optimize import differential_evolution

# Define the bounds for each parameter
bounds = [(0.08, 1), (5, 100), (5, 7)]

# Define the bounds for Y_train
y_bounds = [(1, 100)]

def optimize_features(x):
    # Extract the features from
    adsorbent_mass, initial_concentration, pH = x

    # Set the features in X_train_scaled
    X_train_scaled[:, 0] = adsorbent_mass
    X_train_scaled[:, 1] = initial_concentration
    X_train_scaled[:, 2] = pH

    # Train the model with the updated features
    history = model.fit(X_train_scaled, Y_train, validation_split=0.2, epochs=1)

    # Get the maximum value of Y_train
    max_Y_train = max(history.history['val_loss'])

    return max_Y_train

# Perform the differential evolution optimization
result = differential_evolution(optimize_features, bounds, args=(), disp=True)

# Extract the optimized features and maximized Y_train
optimized_features = result.x
max_Y_train = result.fun

print("Optimized features:", optimized_features)
print("Maximized Y_train:", max_Y_train)

import matplotlib.pyplot as plt

# Plot the optimized point among other points for each feature separately
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

for i in range(3):
    # Plot the training data points
    axs[i].scatter(X_train.iloc[:, i], Y_train, label='Training Data')



    # Plot the optimized point
    axs[i].scatter(optimized_features[i], max_Y_train, color='red', label='Optimized Point')

    # Set the plot title and labels
    axs[i].set_title(f'Feature {i+1}')
    axs[i].set_xlabel(f'Feature {i+1}')
    axs[i].set_ylabel('Y')

    # Add legend to the plot
    #axs[i].legend()

# Show the plot
plt.tight_layout()
plt.show()

"""# write linear reg and its error"""

from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import seaborn as sns

lr_model = linear_model.LinearRegression()
lr_model.fit(X_train_scaled, Y_train)
Y_pred_lr = lr_model.predict(X_test_scaled)
mse_lr = mean_squared_error(Y_test, Y_pred_lr)
mae_lr = mean_absolute_error(Y_test, Y_pred_lr)
print('Mean squared error from linear regression:', mse_lr)
print('Mean absolute error from linear regression:', mae_lr)

"""# Optimization of X1, X2, and X3 to maximize Y (method 1) for LR"""

import numpy as np
from sklearn import linear_model

# Define the ranges for each feature
X1_range = np.arange(0.08, 1.01, 0.01)
X2_range = np.arange(5, 100.01, 1)
X3_range = np.arange(5, 7.01, 0.01)

best_Y = 0
best_X1 = 0
best_X2 = 0
best_X3 = 0

# Iterate over the ranges and find the best combination
for X1 in X1_range:
    for X2 in X2_range:
        for X3 in X3_range:
            # Create a new dataset with selected X1, X2, and X3
            X_train_subset = X_train_scaled.copy()
            X_train_subset[:, 0] = X1
            X_train_subset[:, 1] = X2
            X_train_subset[:, 2] = X3

            # Fit the linear regression model using the subset dataset
            lr_model = linear_model.LinearRegression()
            lr_model.fit(X_train_subset, Y_train)

            # Calculate the quantity of Y_train within the range of 1 to 99
            Y_train_subset = lr_model.predict(X_train_subset)
            selected_Y = Y_train_subset[(Y_train_subset >= 1) & (Y_train_subset <= 99)].shape[0]
            highest_amount_index = np.argmax(Y_train_subset)
            highest_amount = Y_train_subset[highest_amount_index]

            # Update the best combination if the current quantity is higher
            if selected_Y == highest_amount:
                maximized_Y = highest_amount
                best_X1 = X1
                best_X2 = X2
                best_X3 = X3

print("Optimal X1:", best_X1)
print("Optimal X2:", best_X2)
print("Optimal X3:", best_X3)
print("Maximized Y:", highest_amount)

"""# Optimization of X1, X2, and X3 to maximize Y (method 2) for LR using differential method"""

import numpy as np
from scipy.optimize import differential_evolution
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler

# Define the objective function
def objective_function(X):
    # Rescale the input variables to their original range

    # Train the decision tree regressor with the rescaled training data
    lr_model = linear_model.LinearRegression()
    lr_model.fit(X_train_scaled, Y_train)

    # Calculate the mean squared error (MSE) of the model's predictions on the training data
    Y_pred = lr_model.predict(X_train_scaled)
    mse = np.mean((Y_pred - Y_train)**2)

    # Return the negative MSE to maximize Y_train
    return -mse

# Perform differential evolution optimization
bounds = [(0, 1), (0, 1), (0, 1)]  # Define the bounds for the three columns of X_train_scaled
result = differential_evolution(objective_function, bounds)

# Extract the optimized values for X_train_scaled
X_optimized = result.x

# Rescale the optimized X_train_scaled to its original range
X_optimized_original = scaler.inverse_transform(X_optimized.reshape(1, -1)[:, :3])
Y_pred_lr = lr_model.predict(X_optimized_original)
Y_pred_lr
X_optimized_original

Y_pred_lr

import matplotlib.pyplot as plt

# Plot the optimized point among other points for each feature separately
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

for i in range(3):
    # Plot the training data points
    axs[i].scatter(X_train.iloc[:, i], Y_train, label='Training Data')

    # Plot the optimized point
    axs[i].scatter(X_optimized[i], Y_pred_lr, color='red', label='Optimized Point')

    # Set the plot title and labels
    axs[i].set_title(f'Feature {i+1}')
    axs[i].set_xlabel(f'Feature {i+1}')
    axs[i].set_ylabel('Y')

    # Add legend to the plot
    #axs[i].legend()

# Show the plot
plt.tight_layout()
plt.show()

from sklearn import linear_model
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import MinMaxScaler

def visualize_linear_regression(lr_model, X_train, Y_train):
    # Scatter plot of actual vs. predicted values
    predictions = lr_model.predict(X_train)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=Y_train, y=predictions)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs. Predicted Values for Linear Regression')
    plt.show()

    # Residual plot
    residuals = Y_train - predictions
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=predictions, y=residuals)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot for Linear Regression')
    plt.show()

    # Distribution of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals for Linear Regression')
    plt.show()

# Example usage:
# Assuming you have X_train_scaled, Y_train, and lr_model
lr_model = LinearRegression()
lr_model.fit(X_train_scaled, Y_train)

# Generate plots for linear regression
visualize_linear_regression(lr_model, X_train_scaled, Y_train)

"""# write Decission tree and its error"""

import seaborn as sns
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.tree import DecisionTreeRegressor, plot_tree
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

tree = DecisionTreeRegressor()
tree.fit(X_train_scaled, Y_train)
Y_pred_tree = tree.predict(X_test_scaled)
mse_dt = mean_squared_error(Y_test, Y_pred_tree)
mae_dt = mean_absolute_error(Y_test, Y_pred_tree)
print('Mean squared error using decision tree:', mse_dt)
print('Mean absolute error using decision tree:', mae_dt)

"""# Optimization of X1, X2, and X3 to maximize Y (method 1) for DT using differential method"""

import numpy as np
from scipy.optimize import differential_evolution
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler

# Define the objective function
def objective_function(X):
    # Rescale the input variables to their original range

    # Train the decision tree regressor with the rescaled training data
    tree = DecisionTreeRegressor()
    tree.fit(X_train_scaled, Y_train)

    # Calculate the mean squared error (MSE) of the model's predictions on the training data
    Y_pred = tree.predict(X_train_scaled)
    mse = np.mean((Y_pred - Y_train)**2)

    # Return the negative MSE to maximize Y_train
    return -mse

# Perform differential evolution optimization
bounds = [(0, 1), (0, 1), (0, 1)]  # Define the bounds for the three columns of X_train_scaled
result = differential_evolution(objective_function, bounds)

# Extract the optimized values for X_train_scaled
X_optimized = result.x

# Rescale the optimized X_train_scaled to its original range
X_optimized_original = scaler.inverse_transform(X_optimized.reshape(1, -1)[:, :3])
Y_pred_tree1 = tree.predict(X_optimized_original)
Y_pred_tree1
X_optimized_original

Y_pred_tree1

import matplotlib.pyplot as plt

# Plot the optimized point among other points for each feature separately
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

for i in range(3):
    # Plot the training data points
    axs[i].scatter(X_train.iloc[:, i], Y_train, label='Training Data')



    # Plot the optimized point
    axs[i].scatter(X_optimized[i], Y_pred_tree1, color='red', label='Optimized Point')

    # Set the plot title and labels
    axs[i].set_title(f'Feature {i+1}')
    axs[i].set_xlabel(f'Feature {i+1}')
    axs[i].set_ylabel('Y')

    # Add legend to the plot
    #axs[i].legend()

# Show the plot
plt.tight_layout()
plt.show()

def visualize_decision_tree(tree_model, X_train, Y_train, feature_names=None):
    # Convert X_train to DataFrame if it's a NumPy array
    if not isinstance(X_train, pd.DataFrame):
        X_train = pd.DataFrame(X_train, columns=feature_names)

    # Scatter plot of actual vs. predicted values
    predictions = tree_model.predict(X_train)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=Y_train, y=predictions)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs. Predicted Values for Decision Tree')
    plt.show()

    # Residual plot
    residuals = Y_train - predictions
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=predictions, y=residuals)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot for Decision Tree')
    plt.show()

    # Distribution of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals for Decision Tree')
    plt.show()

    # Plot decision tree
    plt.figure(figsize=(15, 8))
    plot_tree(tree_model, filled=True, feature_names=X_train.columns)
    plt.show()

# Example usage:
# Assuming you have X_train_scaled, Y_train, and tree_model
tree_model = DecisionTreeRegressor()
tree_model.fit(X_train_scaled, Y_train)

# Generate plots for decision tree
visualize_decision_tree(tree_model, X_train_scaled, Y_train, feature_names=X_train.columns)

"""# Random forest

# increase the number of trees and see what happens
"""

from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error

model = RandomForestRegressor(n_estimators=40, random_state=30)

model.fit(X_train_scaled, Y_train)

Y_pred_RF = model.predict(X_test_scaled)

mse_RF = mean_squared_error(Y_test, Y_pred_RF)
mae_RF = mean_absolute_error(Y_test, Y_pred_RF)
print('Mean squared error using Random Forest:', mse_RF)
print('Mean absolute error using Random Forest:', mae_RF)

"""# Optimization of X1, X2, and X3 to maximize Y (method 1) for RF using differential method"""

import numpy as np
from scipy.optimize import differential_evolution
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler

# Define the objective function
def objective_function(X):
    # Rescale the input variables to their original range

    # Train the decision tree regressor with the rescaled training data
    model = RandomForestRegressor(n_estimators=40, random_state=30)
    model.fit(X_train_scaled, Y_train)

    # Calculate the mean squared error (MSE) of the model's predictions on the training data
    Y_pred = model.predict(X_train_scaled)
    mse = np.mean((Y_pred - Y_train)**2)

    # Return the negative MSE to maximize Y_train
    return -mse

# Perform differential evolution optimization
bounds = [(0, 1), (0, 1), (0, 1)]  # Define the bounds for the three columns of X_train_scaled
result = differential_evolution(objective_function, bounds)

# Extract the optimized values for X_train_scaled
X_optimized = result.x

# Rescale the optimized X_train_scaled to its original range
X_optimized_original = scaler.inverse_transform(X_optimized.reshape(1, -1)[:, :3])
Y_pred_RF = model.predict(X_optimized_original)
Y_pred_RF
X_optimized_original

Y_pred_RF

import matplotlib.pyplot as plt

# Plot the optimized point among other points for each feature separately
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

for i in range(3):
    # Plot the training data points
    axs[i].scatter(X_train.iloc[:, i], Y_train, label='Training Data')



    # Plot the optimized point
    axs[i].scatter(X_optimized[i], Y_pred_RF, color='red', label='Optimized Point')

    # Set the plot title and labels
    axs[i].set_title(f'Feature {i+1}')
    axs[i].set_xlabel(f'Feature {i+1}')
    axs[i].set_ylabel('Y')

    # Add legend to the plot
    #axs[i].legend()

# Show the plot
plt.tight_layout()
plt.show()

def visualize_random_forest(rf_model, X_train, Y_train, feature_names=None):
    # Convert X_train to DataFrame if it's a NumPy array
    if not isinstance(X_train, pd.DataFrame):
        X_train = pd.DataFrame(X_train, columns=feature_names)

    # Scatter plot of actual vs. predicted values
    predictions = rf_model.predict(X_train)
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=Y_train, y=predictions)
    plt.xlabel('Actual Values')
    plt.ylabel('Predicted Values')
    plt.title('Actual vs. Predicted Values for Random Forest')
    plt.show()

    # Residual plot
    residuals = Y_train - predictions
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=predictions, y=residuals)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Values')
    plt.ylabel('Residuals')
    plt.title('Residual Plot for Random Forest')
    plt.show()

    # Distribution of residuals
    plt.figure(figsize=(10, 6))
    sns.histplot(residuals, kde=True)
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Residuals for Random Forest')
    plt.show()

    # Plot feature importance for random forest
    feature_importance = rf_model.feature_importances_
    sorted_idx = np.argsort(feature_importance)

    plt.figure(figsize=(10, 6))
    plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx])
    plt.yticks(range(len(sorted_idx)), X_train.columns[sorted_idx])
    plt.xlabel('Feature Importance')
    plt.title('Feature Importance for Random Forest')
    plt.show()

# Example usage:
# Assuming you have X_train_scaled, Y_train, and model (RandomForestRegressor)
rf_model = RandomForestRegressor(n_estimators=40, random_state=30)
rf_model.fit(X_train_scaled, Y_train)

# Generate plots for random forest
visualize_random_forest(rf_model, X_train_scaled, Y_train, feature_names=X_train.columns)

"""# one of the advantages of random forest is that it can rank the features by below code"""

feature_list = list(X.columns)

feature_imp = pd.Series(model.feature_importances_, index=feature_list).sort_values

print(feature_imp)