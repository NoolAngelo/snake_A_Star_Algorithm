import matplotlib.pyplot as plt
import seaborn as sns

# Your data
tries = [15, 32, 34, 32, 12, 32, 33, 31, 35, 43, 54, 43, 45, 43, 32, 27, 29, 21, 25, 26, 24, 22, 21, 20]

# Create a strip plot
sns.stripplot(data=tries, jitter=True, color='blue', alpha=0.5)

# Set the title and labels
plt.title('Strip Plot of Tries')
plt.xlabel('Index')
plt.ylabel('Tries')

# Show the plot
plt.show()
