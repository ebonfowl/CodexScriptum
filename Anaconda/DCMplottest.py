import matplotlib.pyplot as plt
import numpy as np

x = np.array([1, 3, 12, 24]) # x values
y = np.array([3, 2.5, 3, 3.2]) # y values corresponding to participant's scores at each time point
x_ticks = [0, 3, 12, 24]
x_labels = ['0', '3', '12', '24']
y_ticks = [0, 1, 2, 3, 4]
y_labels = ['0', '1', '2', '3', '4']
  
# first plot with X and Y data
plt.plot(x, y)
  
x1 = [1, 3, 12, 24] # x values
y1 = [2, 2, 2, 2] # y values to create a cutoff point
  
# second plot for line depicting cutoff value
plt.plot(x1, y1, '-.')
  
plt.xlabel("Months")
plt.ylabel("Total Score")
plt.xticks(ticks=x_ticks, labels=x_labels)
plt.yticks(ticks=y_ticks, labels=y_labels)
plt.title('ECOG-12')
plt.show()