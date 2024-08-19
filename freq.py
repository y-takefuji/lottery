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
