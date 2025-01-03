import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data = pd.read_csv('naukri_jobs_ml.csv')

# Check for missing and infinite values
data.replace([float('inf'), float('-inf')], float('nan'), inplace=True)
data.fillna(data.mean(), inplace=True)

# Encode categorical variables
label_encoder = LabelEncoder()
data['Company Name'] = label_encoder.fit_transform(data['Company Name'])
data['Location'] = label_encoder.fit_transform(data['Location'])

# Features and target variable
X = data[['Company Name', 'Rating', 'Location', 'Min Experience']]
y = data['Avg Salary']

# Drop any remaining NaN values
X = X.dropna()
y = y.dropna()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Dictionary to hold models and their names
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(),
    "Random Forest": RandomForestRegressor()
}

# Dictionary to store performance metrics
performance = {}

# Train each model, make predictions, and evaluate
for model_name, model in models.items():
    
    # Train the model
    model.fit(X_train, y_train)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Store performance
    performance[model_name] = {'MSE': mse, 'R2': r2}
    
    # Print evaluation metrics for each model
    print(f"{model_name}:")
    print(f"  Mean Squared Error: {mse}")
    print(f"  R-squared: {r2}\n")

# Determine the best model based on MSE and R²
best_model = min(performance, key=lambda x: (performance[x]['MSE'], -performance[x]['R2']))

print(f"Best performing model: {best_model}")
print(f"  MSE: {performance[best_model]['MSE']}")
print(f"  R-squared: {performance[best_model]['R2']}")

import matplotlib.pyplot as plt
import seaborn as sns

# Example: Visualize predictions for the best model
best_model_instance = models[best_model]
y_pred = best_model_instance.predict(X_test)

# Scatter plot of actual vs. predicted
plt.figure(figsize=(8, 6))
sns.scatterplot(x=y_test, y=y_pred, alpha=0.7)
plt.xlabel('Actual Values')
plt.ylabel('Predicted Values')
plt.title(f'Actual vs Predicted Values ({best_model})')
plt.axline([0, 0], [1, 1], color='red', linestyle='--', linewidth=2)  # 45-degree line
plt.show()

# Residual plot
residuals = y_test - y_pred
plt.figure(figsize=(8, 6))
sns.histplot(residuals, kde=True, bins=30, color='blue')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.title('Residuals Distribution')
plt.show()
