import pandas as pd
import numpy as np
import itertools
from collections import Counter

# Load the data from data.csv
data = pd.read_csv('data.csv')

# Extract the 2-digit numbers from the 'Winning Numbers' column and format them with leading zeros
winning_numbers = data['Winning Numbers'].apply(lambda x: [f"{int(num):02d}" for num in x.split()])

# Flatten the list of winning numbers
all_numbers = list(itertools.chain(*winning_numbers))

# Calculate the correlation matrix
correlation_matrix = pd.DataFrame(index=[f"{i:02d}" for i in range(1, 100)], columns=[f"{i:02d}" for i in range(1, 100)]).fillna(0)
for numbers in winning_numbers:
    for num1, num2 in itertools.combinations(numbers, 2):
        correlation_matrix.at[num1, num2] += 1
        correlation_matrix.at[num2, num1] += 1

# Normalize the correlation matrix
correlation_matrix = correlation_matrix.div(correlation_matrix.max().max())

# Compare the correlation matrix to an expected correlation matrix (e.g., random data)
expected_correlation_matrix = np.random.rand(99, 99)
expected_correlation_matrix = (expected_correlation_matrix + expected_correlation_matrix.T) / 2  # Make it symmetric

# Calculate the difference between the observed and expected correlation matrices
difference_matrix = correlation_matrix.values - expected_correlation_matrix

# Calculate Mean Absolute Error (MAE)
mae = np.mean(np.abs(difference_matrix))

# Calculate Mean Squared Error (MSE)
mse = np.mean(np.square(difference_matrix))

# Calculate Root Mean Squared Error (RMSE)
rmse = np.sqrt(mse)

print(f"Mean Absolute Error (MAE): {mae:.4f}")
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")

