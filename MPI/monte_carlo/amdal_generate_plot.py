import csv
import sys
import matplotlib.pyplot as plt
import numpy

small = []
medium = []
big = []

csvFile = "amdal.csv"
reps = 3

# DANE PRZYCHODZĄ MI TAK, ŻE MAM POWTÓRZONE POMIARY KOŁO SIEBIE

with open(csvFile, 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=';')
    times = []

    for index, row in enumerate(plots):
        threads, time, size = row
        lineNumber = index + 1

        times.append(float(time))

        if len(times) == reps:
            avgTime = numpy.average(times)
            record = (int(threads), avgTime)

            if lineNumber <= reps * 12:  # small
                small.append(record)
            elif reps * 12 < lineNumber <= reps * 12 * 2:  # medium
                medium.append(record)
            elif lineNumber > reps * 12 * 2:  # big
                big.append(record)

            times = []

# POWYŻEJ POLICZENIE ŚREDNIEJ I PRZYGOTOWANIE DANYCH
# 3 PONIŻSZE TimeData TO KROTKI (ilość procesów, czas)

smallTimeData = (
    [entry[0] for entry in small],
    [entry[1] for entry in small]
)

mediumTimeData = (
    [entry[0] for entry in medium],
    [entry[1] for entry in medium]
)

bigTimeData = (
    [entry[0] for entry in big],
    [entry[1] for entry in big]
)

# PONIŻEJ RYSOWANIE WYKRESÓW


def drawPlot(xAndY, dataLabel, color, isSemiTransparent = False):
    plt.plot(xAndY[0], xAndY[1], linestyle='--', marker='o', color=color, label=dataLabel, alpha=0.2 if isSemiTransparent else 1)


def drawAllTimesPlot():
    drawPlot(smallTimeData, 'Small problem size', 'green')
    drawPlot(mediumTimeData, 'Medium problem size', 'orange')
    drawPlot(bigTimeData, 'Big problem size', 'red')

    plt.xlabel('Number of threads')
    plt.ylabel('Execution time [s]')
    plt.title('Execution time depending on the number of threads')


def drawOneSizeTimesPlot(size):
    if size == 'small':
        drawPlot(smallTimeData, 'Small problem size', 'green')
    elif size == 'medium':
        drawPlot(mediumTimeData, 'Medium problem size', 'orange')
    elif size == 'big':
        drawPlot(bigTimeData, 'Big problem size', 'red')

    plt.xlabel('Number of threads')
    plt.ylabel('Execution time [s]')
    plt.title('Execution time depending on the number of threads')


def speedup(t1, tn):
    return t1 / tn


def drawAllSpeedupPlot():
    smallT1 = smallTimeData[1][0]
    smallSpeedupData = (
        smallTimeData[0],
        [speedup(smallT1, entry) for entry in smallTimeData[1]]
    )

    mediumT1 = mediumTimeData[1][0]
    mediumSpeedupData = (
        mediumTimeData[0],
        [speedup(mediumT1, entry) for entry in mediumTimeData[1]]
    )

    bigT1 = bigTimeData[1][0]
    bigSpeedupData = (
        bigTimeData[0],
        [speedup(bigT1, entry) for entry in bigTimeData[1]]
    )

    idealScenario = (
        list(range(1, 13)),
        list(range(1, 13))
    )
    drawPlot(smallSpeedupData, 'Small problem size', 'green')
    drawPlot(mediumSpeedupData, 'Medium problem size', 'orange')
    drawPlot(bigSpeedupData, 'Big problem size', 'red')
    drawPlot(idealScenario, 'Ideal scenario', 'gray', True)

    plt.yticks(numpy.arange(1, 13, 1))
    plt.xlabel('Number of threads')
    plt.ylabel('Speedup')
    plt.title('Speedup depending on the number of threads')


def efficiency(t1, tn, n):
    Sn = speedup(t1, tn)
    return Sn / n


def drawAllEfficiencyPlot():
    smallT1 = smallTimeData[1][0]

    smallEfficiencyData = (
        smallTimeData[0],
        [efficiency(smallT1, entry, n + 1) for n, entry in enumerate(smallTimeData[1])]
    )

    mediumT1 = mediumTimeData[1][0]
    mediumEfficiencyData = (
        mediumTimeData[0],
        [efficiency(mediumT1, entry, n + 1) for n, entry in enumerate(mediumTimeData[1])]
    )

    bigT1 = bigTimeData[1][0]
    bigEfficiencyData = (
        bigTimeData[0],
        [efficiency(bigT1, entry, n + 1) for n, entry in enumerate(bigTimeData[1])]
    )

    idealScenario = (
        list(range(1, 13)),
        [1] * 12
    )
    drawPlot(smallEfficiencyData, 'Small problem size', 'green')
    drawPlot(mediumEfficiencyData, 'Medium problem size', 'orange')
    drawPlot(bigEfficiencyData, 'Big problem size', 'red')
    drawPlot(idealScenario, 'Ideal scenario', 'gray', True)

    plt.xlabel('Number of threads')
    plt.ylabel('Efficiency')
    plt.title('Efficiency depending on the number of threads')


def serialFraction(t1, tn, n):
    Sn = speedup(t1, tn)

    return ((1/Sn) - (1/n)) / (1 - (1/n))


def drawAllSerialFractionPlot():
    smallT1 = smallTimeData[1][0]

    # TUTAJ NIE BIERZEMY PIERWSZEGO ELEMENTU, ŻEBY NIE DZIELIĆ PRZEZ 0 - STĄD [1:]
    smallSerialFractionData = (
        smallTimeData[0][1:],
        [serialFraction(smallT1, entry, n + 2) for n, entry in enumerate(smallTimeData[1][1:])]
    )

    mediumT1 = mediumTimeData[1][0]
    mediumSerialFractionData = (
        mediumTimeData[0][1:],
        [serialFraction(mediumT1, entry, n + 2) for n, entry in enumerate(mediumTimeData[1][1:])]
    )

    bigT1 = bigTimeData[1][0]
    bigSerialFractionData = (
        bigTimeData[0][1:],
        [serialFraction(bigT1, entry, n + 2) for n, entry in enumerate(bigTimeData[1][1:])]
    )

    idealScenario = (
        list(range(1, 13)),
        [0] * 12
    )
    drawPlot(smallSerialFractionData, 'Small problem size', 'green')
    drawPlot(mediumSerialFractionData, 'Medium problem size', 'orange')
    drawPlot(bigSerialFractionData, 'Big problem size', 'red')
    drawPlot(idealScenario, 'Ideal scenario', 'gray', True)

    plt.xlabel('Number of threads')
    plt.ylabel('Serial fraction')
    plt.title('Serial fraction depending on the number of threads')


# PONIŻEJ WYWOŁANIA DLA POSZCZEGÓLNYCH WYKRESÓW

# drawAllTimesPlot()

# drawOneSizeTimesPlot('small')
# drawOneSizeTimesPlot('medium')
# drawOneSizeTimesPlot('big')

# drawAllSpeedupPlot()

# drawAllEfficiencyPlot()

# drawAllSerialFractionPlot()

plt.xticks(numpy.arange(1, 13, 1))
plt.grid()
plt.legend()
plt.show()
