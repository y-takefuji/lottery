import pandas as pd
from collections import Counter
import itertools

# Load the data from data.csv
data = pd.read_csv('data.csv')

# Extract the 2-digit numbers from the 'Winning Numbers' column and format them with leading zeros
winning_numbers = data['Winning Numbers'].apply(lambda x: [f"{int(num):02d}" for num in x.split()])

# Flatten the list of winning numbers
all_numbers = list(itertools.chain(*winning_numbers))

# Calculate the frequency of each 2-digit number
frequency = Counter(all_numbers)

# Find the top forty high-frequency 2-digit numbers
top_forty_numbers = frequency.most_common(40)
print("Top Forty High-Frequency 2-Digit Numbers:")
for number, freq in top_forty_numbers:
    print(f"Number: {number}, Frequency: {freq}")

# Calculate the correlation between the top forty 2-digit numbers and other 2-digit numbers
correlation_matrix = pd.DataFrame(index=[f"{i:02d}" for i in range(1, 100)], columns=[f"{i:02d}" for i in range(1, 100)]).fillna(0)
for numbers in winning_numbers:
    for num1, num2 in itertools.combinations(numbers, 2):
        correlation_matrix.at[num1, num2] += 1
        correlation_matrix.at[num2, num1] += 1

# Normalize the correlation matrix
correlation_matrix = correlation_matrix.div(correlation_matrix.max().max())

# Extract the top forty correlation matrix
top_forty_matrix = correlation_matrix.loc[[num for num, _ in top_forty_numbers], [num for num, _ in top_forty_numbers]]

# Create a new DataFrame to include headers and indices
matrix_with_headers = pd.DataFrame(index=[''] + [num for num, _ in top_forty_numbers], columns=[''] + [num for num, _ in top_forty_numbers])

# Fill the headers
matrix_with_headers.iloc[0, 1:] = [num for num, _ in top_forty_numbers]
matrix_with_headers.iloc[1:, 0] = [num for num, _ in top_forty_numbers]

# Fill the matrix values
for i, num1 in enumerate([num for num, _ in top_forty_numbers]):
    for j, num2 in enumerate([num for num, _ in top_forty_numbers]):
        matrix_with_headers.iloc[i + 1, j + 1] = f'{top_forty_matrix.loc[num1, num2]:.2f}'

# Save the matrix as a CSV file with space separators
matrix_with_headers.to_csv('correlation_matrix.csv', sep=',', index=False, header=False)

