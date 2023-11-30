# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import numpy as np

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def plot_distribution(values, probs):
    # Plotting
    plt.bar(values, probs)

    # Adding labels and title
    plt.xlabel('Values')
    plt.ylabel('Probability')
    plt.title('Histogram')
    plt.ylim([0,1])

    # Display the histogram
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Values and corresponding frequencies
    # values = np.array([0, 1, 2, 3])
    # probs1 =  np.array([0.25, 0.25, 0.25, 0.25])
    # probs2 =  np.array([0.1, 0.3, 0.4, 0.2])
    # plot_distribution(values, probs1)
    # plot_distribution(values, probs2)
    values = ["2 В", "1 В","0 В"]
    probs = [1/4, 2/4, 1/4]
    values = ["4 В", "3 В","2 В", "1 В","0 В"]
    probs = [1/16, 4/16, 6/16, 4/16, 1/16]
    plot_distribution(values, probs)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
