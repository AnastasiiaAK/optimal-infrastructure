import matplotlib.pyplot as plt
import numpy as np
import math
from collections import defaultdict


# data for region Europe(London), OS (Linux)
# 1. M5a (large, xlarge, 2xlarge, 4xlarge)
# 2. M5 (large, xlarge, 2xlarge, 4xlarge)
# 3. C5n (large, xlarge, 2xlarge, 4xlarge)
# 4. r5b (large, xlarge, 2xlarge, 4xlarge)

CPU = [2, 4, 8, 16]

coreFreq1 = 2.5
coreFreq2 = 3.1
coreFreq3 = 3.4
coreFreq4 = 3.5

# True price
truePrice1 = [0.1, 0.2, 0.4, 0.8]
truePrice2 = [0.111, 0.222, 0.444, 0.888]
truePrice3 = [0.128, 0.256, 0.512, 1.024]
truePrice4 = [0.175, 0.35, 0.7, 1.40]

switchesFreq = [0.1, 1, 10]
priceOfSwitches = [5, 100, 10000]
numberOfConnectedDevices = [4, 8, 16]
# Price with a quadratic correction


# изменим цены на машины, чтобы влияние количества ядер на цену было больше
def dependency_price_from_cores(core_freq, true_price, cpu):
    freq = core_freq
    price = true_price[0] / cpu[0]
    x = np.linspace(0, 40, 1000)
    y1 = x ** 2 / 10000 * core_freq ** 2 * 7.3 + price * x
    y2 = price * x
    '''
    fig, ax = plt.subplots()
    ax.plot(x, y1, label="quadratic")
    ax.plot(x, y2, label="linear")
    ax.legend()
    plt.xlabel("Number of cores")
    plt.ylabel("Price")
    plt.title("Dependency price from cores")
    plt.show()
    '''
    return list(map((lambda core: round(core ** 2 / 10000 * core_freq ** 2 * 7.3 + price * core_freq, 3)), CPU))


dictWithPrices = {}
for i in range(1, 5, 1):
    val = dependency_price_from_cores(locals()['coreFreq'+str(i)], locals()['truePrice'+str(i)], CPU)
    key = [2, 4, 8, 16]
    dictWithPrices[i] = dict(zip(key, val))
print(dictWithPrices)
dictFreq = {1: 2.5, 2: 3.1, 3: 3.4, 4: 3.5}


dictSwitches = defaultdict(dict)
for x, y, z, t in zip(list(range(1, len(switchesFreq) + 1, 1)), switchesFreq, priceOfSwitches, numberOfConnectedDevices):
    dictSwitches[x]["price"] = z
    dictSwitches[x]["frequency"] = y
    dictSwitches[x]["number_attached"] = t

# print("freq", truePrice1[2] / dictWithPrices[1][8])
# print("freq", truePrice1[3] / dictWithPrices[1][16]) # должно быть 0.62

# print("cores", truePrice4[3] / dictWithPrices[4][16]) # должно быть 0.54





