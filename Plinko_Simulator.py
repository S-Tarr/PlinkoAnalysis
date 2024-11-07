import matplotlib.pyplot as plt
import numpy as np
import math
from collections import Counter

ROWS = 16
NUM_BALLS = 10000
BALL_COST = 100
RISK = "Low"
plinko = {
    "Low": {8: [5.6, 2.1, 1.1, 1, 0.5, 1, 1.1, 2.1, 5.6], 16: [16, 9, 2, 1.4, 1.4, 1.2, 1.1, 1, 0.5, 1, 1.1, 1.2, 1.4, 1.4, 2, 9, 16]},
    "Medium": {8: [13, 3, 1.3, 0.7, 0.4, 0.7, 1.3, 3, 13], 16: [110, 41, 10, 5, 3, 1.5, 1, 0.5, 0.3, 0.5, 1, 1.5, 3, 5, 10, 41, 110]},
    "High": {8: [29, 4, 1.5, 0.3, 0.2, 0.3, 1.5, 4, 29], 16: [1000, 130, 26, 9, 4, 2, 0.2, 0.2, 0.2, 0.2, 0.2, 2, 4, 9, 26, 130, 1000]}
    }


def calculatePascalRow(n):
    return [math.comb(n, k) for k in range(0, n+1)]


def calculateEndBalance(board, numBalls):
    probabilities = calculatePascalRow(ROWS)

    counts = {}
    for i in range(len(board)):
        counts[board[i]] = counts.get(board[i], 0) + (probabilities[i] / 2**(ROWS)) * numBalls

    print("counts:", counts)
    res = 0
    for key in counts:
        counts[key] = round(counts[key], 0)
        counts[key] *= BALL_COST * key
    
    return sum(counts.values())


def makeHist(axis, board, numBalls):
    data = []
    triangle = calculatePascalRow(ROWS)
    for i in range(len(board)):
        data.extend([i for _ in range(int(round((triangle[i] / 2**ROWS) * numBalls, 0)))])
    
    # Create a pandas DataFrame
    # Plot the histogram
    _, _, bars = plt.hist(data, bins=np.arange(-0.5, ROWS+1), edgecolor='black', linewidth=1.2)

    # Add a title and labels
    axis.set_title(f'{numBalls} Balls Expected Plinko Distribution')
    axis.xaxis.set_ticks(np.arange(len(board)))
    axis.xaxis.set_ticklabels(board)
    axis.set_ylabel('Frequency')

    axis.bar_label(bars)


def printProfits():
    startingBalance = NUM_BALLS * BALL_COST
    print("Starting balance: $" + str(startingBalance))
    endBalance = calculateEndBalance(plinko[RISK][ROWS], NUM_BALLS)
    print("Ending balance: $" + str(endBalance))
    print("Profit: $" + str(endBalance - startingBalance))
    print("Percentage: " + str(round(endBalance / startingBalance * 100 - 100, 3)) + "%")


def plotProfitTrend(axis, risk, rows):
    # Chart Profits as ball count grows
    profitGrowth = []
    for numBalls in (10**i for i in range(1, 9)):
        startingBalance = numBalls * BALL_COST
        endBalance = calculateEndBalance(plinko[risk][rows], numBalls)
        profitGrowth.append(endBalance / startingBalance * 100 - 100)

    axis.plot(np.arange(8), profitGrowth)
    axis.xaxis.set_ticklabels([10**i for i in range(8)])
    axis.set_title(f"Risk {risk} with {rows} Rows")


def plotProfitTrends():
    fig = plt.figure(1, figsize=(7,7))
    ax1 = fig.add_subplot(211)
    plotProfitTrend(ax1, "Low", ROWS)
    ax2 = fig.add_subplot(212)
    plotProfitTrend(ax2, "Medium", ROWS)
    ax3 = fig.add_subplot(221)
    plotProfitTrend(ax3, "High", ROWS)


def plotExpectedLayouts():
    fig = plt.figure(1, figsize=(10,10))
    ax1 = fig.add_subplot(221)
    makeHist(ax1, plinko["High"][ROWS], 100)
    ax2 = fig.add_subplot(222)
    makeHist(ax2, plinko["High"][ROWS], 1000)
    ax3 = fig.add_subplot(223)
    makeHist(ax3, plinko["High"][ROWS], 10000)
    ax4 = fig.add_subplot(224)
    makeHist(ax4, plinko["High"][ROWS], 100000)
