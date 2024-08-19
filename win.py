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

print("\nCorrelation Matrix for Top Forty Numbers:")
print(correlation_matrix.loc[[num for num, _ in top_forty_numbers], [num for num, _ in top_forty_numbers]])

# Generate top twenty sets of 5 2-digit numbers based on maximum correlations
top_sets = []
top_set_values = []
used_numbers = set()
for _ in range(20):
    top_set = []
    remaining_numbers = set(correlation_matrix.index) - used_numbers
    while len(top_set) < 5 and remaining_numbers:
        if not top_set:
            num = max(remaining_numbers, key=lambda x: frequency[x])
        else:
            num = max(remaining_numbers, key=lambda x: sum(correlation_matrix.at[x, y] for y in top_set))
        top_set.append(num)
        remaining_numbers.remove(num)
    if len(top_set) == 5:
        top_sets.append(top_set)
        used_numbers.update(top_set)
        # Calculate the maximized value for the set
        set_value = sum(correlation_matrix.at[num1, num2] for num1, num2 in itertools.combinations(top_set, 2))
        top_set_values.append(set_value)

# Sort the sets based on their maximized values in descending order
sorted_sets = sorted(zip(top_sets, top_set_values), key=lambda x: x[1], reverse=True)

print("\nTop Twenty Sets of 5 2-Digit Numbers Based on Maximum Correlations (Sorted):")
for i, (top_set, set_value) in enumerate(sorted_sets, 1):
    print(f"Set {i}: {top_set}, Maximized Value: {set_value:.2f}")

