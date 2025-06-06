import matplotlib.pyplot as plt
import numpy as np
import statistics

# Given data
tries = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]

# Statistical analysis
mean_score = statistics.mean(tries)
median_score = statistics.median(tries)
std_dev = statistics.stdev(tries)
min_score = min(tries)
max_score = max(tries)
score_range = max_score - min_score

# Calculate moving average for trend analysis
def moving_average(data, window_size=3):
    return np.convolve(data, np.ones(window_size), 'valid') / window_size

moving_avg = moving_average(tries, 3)

# Create figure with subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Snake A* Algorithm Performance Analysis', fontsize=16, fontweight='bold')

# 1. Main trip plot with enhanced features
ax1.plot(range(len(tries)), tries, marker='o', linestyle='-', linewidth=2, 
         markersize=6, color='blue', alpha=0.7, label='Scores')
ax1.plot(range(len(moving_avg)), moving_avg, color='red', linewidth=2, 
         label=f'Moving Average (window=3)')
ax1.axhline(mean_score, color='green', linestyle='--', alpha=0.8, 
           label=f'Mean: {mean_score:.1f}')
ax1.fill_between(range(len(tries)), 
                 [mean_score - std_dev] * len(tries),
                 [mean_score + std_dev] * len(tries),
                 alpha=0.2, color='green', label=f'±1 Std Dev: {std_dev:.1f}')
ax1.set_xlabel('Trial Number')
ax1.set_ylabel('Score')
ax1.set_title('Score Progression Over Trials')
ax1.grid(True, alpha=0.3)
ax1.legend()

# 2. Score distribution histogram
ax2.hist(tries, bins=8, color='skyblue', edgecolor='black', alpha=0.7)
ax2.axvline(mean_score, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_score:.1f}')
ax2.axvline(median_score, color='green', linestyle='--', linewidth=2, label=f'Median: {median_score:.1f}')
ax2.set_xlabel('Score')
ax2.set_ylabel('Frequency')
ax2.set_title('Score Distribution')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 3. Performance metrics
metrics_text = f"""
Performance Metrics:
• Mean Score: {mean_score:.2f}
• Median Score: {median_score:.2f}
• Standard Deviation: {std_dev:.2f}
• Min Score: {min_score}
• Max Score: {max_score}
• Range: {score_range}
• Coefficient of Variation: {(std_dev/mean_score)*100:.1f}%
"""
ax3.text(0.05, 0.95, metrics_text, transform=ax3.transAxes, fontsize=11,
         verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8))
ax3.set_xlim(0, 1)
ax3.set_ylim(0, 1)
ax3.axis('off')
ax3.set_title('Statistical Summary')

# 4. Performance trend analysis
# Calculate differences between consecutive trials
score_diffs = np.diff(tries)
improvements = sum(1 for x in score_diffs if x > 0)
deteriorations = sum(1 for x in score_diffs if x < 0)
no_change = sum(1 for x in score_diffs if x == 0)

ax4.bar(['Improvements', 'Deteriorations', 'No Change'], 
        [improvements, deteriorations, no_change],
        color=['green', 'red', 'gray'], alpha=0.7)
ax4.set_ylabel('Number of Occurrences')
ax4.set_title('Trial-to-Trial Performance Changes')
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Additional analysis output
print("=" * 50)
print("SNAKE A* ALGORITHM PERFORMANCE ANALYSIS")
print("=" * 50)
print(f"Total Trials: {len(tries)}")
print(f"Mean Score: {mean_score:.2f}")
print(f"Median Score: {median_score:.2f}")
print(f"Standard Deviation: {std_dev:.2f}")
print(f"Best Performance: {max_score} (Trial {tries.index(max_score) + 1})")
print(f"Worst Performance: {min_score} (Trial {tries.index(min_score) + 1})")
print(f"Performance Consistency (CV): {(std_dev/mean_score)*100:.1f}%")
print(f"Improvement Rate: {improvements}/{len(score_diffs)} ({improvements/len(score_diffs)*100:.1f}%)")
print("=" * 50)
