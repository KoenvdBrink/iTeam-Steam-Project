from steam_data_main import collect_regression_data, normalize_data, gradient_descent,plot_regression
koen = "76561198030044972"
zack = "76561198055954925"
nizar = "76561198266159443"
gamer = "76561198056739081"

# Collect regression data for a specific user
regression_data = collect_regression_data(nizar)

# Normalize data
normalized_x, min_x, max_x = normalize_data([d["playtime_hours"] for d in regression_data])
normalized_y, min_y, max_y = normalize_data([d["achievements_unlocked"] for d in regression_data])

# Perform gradient descent
coefficients = gradient_descent(normalized_x, normalized_y)
print(f"Regression coefficients: {coefficients}")

# Original, non-normalized data
original_x = [d["playtime_hours"] for d in regression_data]
original_y = [d["achievements_unlocked"] for d in regression_data]

# Plot the regression
plot_regression(normalized_x, normalized_y, original_x, original_y, coefficients)