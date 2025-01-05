import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
data_file = "app_details.csv"
data = pd.read_csv(data_file)

# Extract relevant data columns
peak_players = data["Peak Players"]
user_score = data["User Score (%)"]

# Apply a logarithmic transformation to normalize peak players
data["Log Peak Players"] = np.log1p(peak_players)  # Log(1 + x) to handle zero values

# Separate data for zoomed-in user scores from 65% to 100%
high_user_score = data[(data["User Score (%)"] >= 65) & (data["User Score (%)"] <= 100)]

# Normalize features and target
x = high_user_score["User Score (%)"].values
x_normalized = (x - np.mean(x)) / np.std(x)  # Normalize user scores
y = high_user_score["Log Peak Players"].values
y_normalized = (y - np.mean(y)) / np.std(y)  # Normalize log peak players

# Perform gradient descent for linear regression
def gradient_descent(x, y, learning_rate=0.001, epochs=1000):
    m, b = 0, 0  # Initialize slope and intercept
    n = len(x)
    for _ in range(epochs):
        y_pred = m * x + b
        dm = (-2 / n) * np.dot(x, (y - y_pred))  # Vectorized operation
        db = (-2 / n) * np.sum(y - y_pred)

        if np.isinf(dm) or np.isinf(db) or np.isnan(dm) or np.isnan(db):
            print("Gradient descent diverged. Adjusting learning rate or data.")
            break

        m -= learning_rate * dm
        b -= learning_rate * db
    return m, b

# Run gradient descent
m, b = gradient_descent(x_normalized, y_normalized)

# Denormalize the regression line to plot in the original scale
x_vals = np.linspace(65, 100, 500)
x_vals_normalized = (x_vals - np.mean(x)) / np.std(x)
y_vals_normalized = m * x_vals_normalized + b
y_vals = y_vals_normalized * np.std(y) + np.mean(y)

# Create the scatterplot with normalized peak players
plt.figure(figsize=(10, 6))
plt.scatter(high_user_score["User Score (%)"], high_user_score["Log Peak Players"], alpha=0.7, edgecolors='w', color='blue', label="Data Points")

# Add the regression line from gradient descent
plt.plot(x_vals, y_vals, color='green', label="Gradient Descent Regression Line")

# Zoom into the user score range of 65% to 100%
plt.xlim(65, 100)
plt.ylim(high_user_score["Log Peak Players"].min() - 0.5, high_user_score["Log Peak Players"].max() + 0.5)

# Add labels, title, legend, and grid
plt.title("Zoomed Scatterplot of User Score (65-100%) vs Log-Transformed Peak Players", fontsize=14)
plt.xlabel("User Score (%)", fontsize=12)
plt.ylabel("Log-Transformed Peak Players", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

# Add custom ticks for readability
log_ticks = [0, 5, 10, 15]
real_values = [np.expm1(tick) for tick in log_ticks]
plt.yticks(log_ticks, [f"{int(val):,}" for val in real_values])

# Show the plot
plt.show()
