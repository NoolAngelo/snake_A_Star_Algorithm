import statistics
import matplotlib.pyplot as plt

# Given data
tries = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]

# Calculating mean, median, and mode
mean = statistics.mean(tries)
median = statistics.median(tries)
mode = statistics.mode(tries)

# Plotting the data with mean, median, and mode
plt.hist(tries, bins=10, color='lightblue', edgecolor='black', alpha=0.7)
plt.axvline(mean, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean}')
plt.axvline(median, color='green', linestyle='dashed', linewidth=1, label=f'Median: {median}')
plt.axvline(mode, color='orange', linestyle='dashed', linewidth=1, label=f'Mode: {mode}')
plt.xlabel('Score')
plt.ylabel('Frequency')
plt.title('Histogram of Score Tries with Mean, Median, and Mode')
plt.legend()
plt.show()
