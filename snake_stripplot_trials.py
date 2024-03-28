import matplotlib.pyplot as plt

# Given data
tries = [33, 48, 68, 35, 43, 52, 61, 36, 41, 56, 45, 78, 80, 79, 36, 48, 92, 56, 40, 36]

# Plotting the trip plot
plt.plot(range(len(tries)), tries, marker='o', linestyle='-')
plt.xlabel('Attempts')
plt.ylabel('Score')
plt.title('Trip Plot of Score Tries')
plt.grid(True)
plt.show()
