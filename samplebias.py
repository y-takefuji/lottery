import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import itertools
from collections import Counter

# Load the data from data.csv
data = pd.read_csv('data.csv')

# Extract the 2-digit numbers from the 'Winning Numbers' column and format them with leading zeros
winning_numbers = data['Winning Numbers'].apply(lambda x: [f"{int(num):02d}" for num in x.split()])

# Flatten the list of winning numbers
all_numbers = list(itertools.chain(*winning_numbers))

# Calculate the frequency of each 2-digit number
frequency = Counter(all_numbers)

# Convert frequency to a DataFrame
frequency_df = pd.DataFrame.from_dict(frequency, orient='index', columns=['Frequency']).sort_index()

# Plot the frequency distribution
plt.figure(figsize=(10, 6))
ax = frequency_df.plot(kind='bar', legend=False)
plt.title('Frequency Distribution of 2-Digit Numbers')
plt.xlabel('2-Digit Number')
plt.ylabel('Frequency')

# Set small font size for x-ticks
ax.set_xticklabels(ax.get_xticklabels(), rotation=90, fontsize=8)

plt.tight_layout()
plt.savefig('result.png', dpi=300)
plt.show()

# Perform Chi-Square test to compare observed frequencies with expected frequencies
expected_frequency = [len(all_numbers) / 99] * 99  # Assuming uniform distribution
observed_frequency = [frequency.get(f"{i:02d}", 0) for i in range(1, 100)]
chi2, p_value = chi2_contingency([observed_frequency, expected_frequency])[:2]

print(f"Chi-Square Statistic: {chi2}")
print(f"P-Value: {p_value}")

