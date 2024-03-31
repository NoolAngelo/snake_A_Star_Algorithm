#mean median and mode with time taken for each trial
import matplotlib.pyplot as plt
import statistics

# Trial numbers
trials = list(range(1, 21))

# Scores
scores = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]

# Time taken (converted to seconds for uniformity)
time_taken = [53, 75, 178, 56.4, 91, 135, 150, 59, 80, 110, 98, 190, 201, 185, 73, 74, 75, 76, 77, 78]

# Calculate mean, median, and mode
mean_time = statistics.mean(time_taken)
median_time = statistics.median(time_taken)
mode_time = statistics.mode(time_taken)

# Plotting the graph
plt.figure(figsize=(10, 6))
plt.scatter(trials, time_taken, color='blue', label='Time Taken')
plt.axhline(mean_time, color='red', linestyle='--', label=f'Mean: {mean_time:.2f} sec')
plt.axhline(median_time, color='green', linestyle='--', label=f'Median: {median_time:.2f} sec')
plt.axhline(mode_time, color='orange', linestyle='--', label=f'Mode: {mode_time:.2f} sec')
plt.title('Scores Over Time for Each Trial')
plt.xlabel('Trial Number')
plt.ylabel('Time Taken (seconds)')
plt.legend()
plt.grid(True)
plt.show()
