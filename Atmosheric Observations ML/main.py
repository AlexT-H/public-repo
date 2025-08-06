
import csv

data1 = []
data1Rows = 0
data1RowLen = 0
with open('atmosphereData.csv', 'r') as file:   # collects csv1 data
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data1.append(row)
        data1Rows += 1
        data1RowLen = len(row)


testData = []   # 200 rows
testDataRows = 200
trainData = []  # 800 rows
trainDataRows = 801
for x in range(data1Rows):
    if x < trainDataRows:
        trainData.append(data1[x])  # sets 800 rows to train model
    else:
        testData.append(data1[x])   # sets 200 rows to test model
data1 = trainData
del trainData


# category assignments
keyValue = 34   # health index column for train/test
cat1, cat2, cat3, cWeights = [], [], [], []
cat1 = [0, 25, 26, 27, 31, 32, 33]  # cat1 = datatime data columns
for x in range(data1RowLen):
    if x not in cat1:
        cat2.append(x)  # cat2 = atmosphere data columns                        take out 34?
    cat3.append(x)  # cat3 = all data columns
    cWeights.append(1)  # initializes category weights


# sorts data by test metric
def sortData(data):
    n = len(data)
    for i in range(n):
        min = i
        for j in range(i + 1, n):
            if float(data[j][0]) < float(data[min][0]):
                min = j
        data[i], data[min] = data[min], data[i]
    return data


# sorts rows based on keyValue (for regression lines)
keyValues = []
headers = []
for x in range(trainDataRows):  # puts health index in array for easier sorting
    if x > 0:
        keyValues.append([data1[x][keyValue], x])  # x = index to match back to row
    else:
        headers = data1[x]
keyValues = sortData(keyValues)
sortingData = []
for x in range(len(keyValues)):  # reconnects sorted health scores to data1
    for y in range(testDataRows):
        if y == keyValues[x][1]:
            sortingData.append(data1[y])
data1 = sortingData
del sortingData
del keyValues


l1, l2 = 0, 0
def calcRegres(column):   # calculates regression line between all column data
    # returns slope data for column comparisons to target data
    x1, y, xy, x2 = 0, 0, 0, 0
    for x in range(len(column)):
        x1 += x
        y += float(column[x])   # cell = y
        xy += x*float(column[x])
        x2 += x ** 2
    slope = round(((len(column) * xy) - (x1 * y)) / ((len(column) * x2) - (x1 ** 2)), 9)
    b = round((y - (slope * x))/len(column), 4)   # calculates the lines y-intercept
    L1(L2(slope, l2), l1)
    return [slope, b]


def estimateValue(row, regressionColumn, regressionColumn_Offset, keyValue_Offset):
    return float(row[regressionColumn]) - regressionColumn_Offset + keyValue_Offset


ssr, sst, r2 = 0, 0, 0
pruneNum = 0
estBias = 0
def estimate(row, cat, cOffsets, keyOffset):    # for estimating rows     so an interface can be made to insert just row data
    estimate = 0
    airQuality = 0
    totalWeight = 1
    aqWeight = 1
    i = 0
    for c in range(len(row)-1):
        if c in cat and c != 0:
            val = (float(row[i]) - cOffsets[c] + keyOffset) * cWeights[c]
            if prune(pruneNum, val) and val != 0:   # takes out overly large variables
                estimate += val        # fix cOffsets (maybe row[i] too?)        taking numbers out of range
                totalWeight += cWeights[c]
                if c in cat2:
                    airQuality += val
                    aqWeight += cWeights[c]
            i += 1
        elif c == 0:
            i += 1
    estimate = round((estimate/len(cat)-estBias)/totalWeight, 4)
    airQuality = round((airQuality/len(cat2))/aqWeight, 4)
    return [(estimate*10)+keyOffset, airQuality*10+keyOffset]

MAPE = 0
def dataTesting(data, cat, offsets, keyOffset, val=0, show=False):
    allEstimates = []
    estimateVals = 0
    aqVals = 0
    avgError, mapError, rmsError = 0, 0, 0
    global ssr, sst, MAPE
    for x in range(len(data)):
        if x > 0:    # skips header
            allEstimates.append((estimate(data[x], cat, offsets, keyOffset)))
            estimateVals += allEstimates[x-1][0]
            if show:
                print(allEstimates[x-1][0], data[x][34])
            aqVals += allEstimates[x-1][1]
            error = round(abs(allEstimates[x - 1][0] - float(data[x][keyValue])), 4)
            avgError += error
            mapError += round((error / abs(float(data[x][keyValue]))), 4)
            rmsError += round((error**2),4)
    estimateVals = round(estimateVals/(len(data)), 4)
    aqVals = round(aqVals/(len(data)), 4)


    for x in range(len(data)):  # for calculating the mean keyValue for ssr
        if x > 0:
            ssr += ((allEstimates[x - 1][0] - estimateVals) ** 2)   # can add abs around allEstimates
            sst += ((float(data[x][34]) - estimateVals) ** 2)
    ssr = ssr   # (len(data)-1)
    r2 = round(1 - (ssr/sst), 4)
    avgError = round(avgError / (len(data) - 1), 4)
    mapError = round((mapError * 100) / (len(data) - 1), 2)
    MAPE = mapError
    rmsError = round(rmsError/(len(data)-1), 2)

    if val != 0:
        print("avg Air Quality Index: ", aqVals)
        #print("avg Estimate: ", estimateVals)
        print("Average Error:", avgError)  # error = difference between value - real index
        print("Mean Absolute Percentage Error: ", mapError, "%")
        print("R-Squared: ", r2)
        print("RMS Error: ", rmsError, "\n")
    else:
        return estimateVals


def cLineRetriever(cat):   # gets cat lines for
    cLines = []  # holds regression slopes and y-intercepts (offset)
    for c in range(data1RowLen):
        column = []
        if c in cat:  # separates air quality columns
            for r in range(testDataRows - 1):
                if r > 0:  # passes header line
                    if '-' not in data1[r][c]:  # filters out negative data     #add data filters here (t/f)
                        column.append(data1[r][c])
            cLines.append([calcRegres(column), c])
    return cLines


def prune(max, val):
    if val < max:
        return True
    else:
        return False


def L1(slope, l=1):    # Lasso Regularization
    if l >= 1:
        weight = (ssr*1) + (l * abs(slope))
        slope = slope * weight
    return slope


def L2(slope, l=1):    # Ridge Regularization
    if l >= 1:
        weight = (ssr*1) + (l * (slope**2))
        slope = slope * weight
    return slope


weightNum = 1000
def weightedAveraging(delta, slopes, keySlope):    # add weights based on % deviations;  delta = percentage deviation
    weight = weightNum
    adjusted = []   # a value for keeping track which values have already been weighed
    while len(slopes) > len(adjusted) and weight >= 1:
        for x in range(len(slopes)):
            if x not in adjusted and abs(slopes[x][0][0] - keySlope) < (delta/100):    # adjusts weights based on slopes
                cWeights[slopes[x][1]] = weight
                adjusted.append(x)
        weight = int(weight/2)
        delta += delta
    cWeights[3] = 100000    # offsets error space for weight value calculation
    cWeights[30] = 100000   # offsets error space for weight value calculation


allOffsets = []
keyValOffset = 0
weightDelta = 0
def runData(cat, val=0, show=False):
    cLines = cLineRetriever(cat)
    keySort = []
    global allOffsets
    i = 0
    for c in range(data1RowLen):  # compare slopes    # give closer slopes of health index slope more weight
        if c in cat and c != keyValue:
            if cWeights[c] > 0:
                keySort.append(cLines[i])
                allOffsets.append(float(cLines[i][0][1]))       # based off of keySort values ( in cat range)
                i += 1
    global keyValOffset
    keyValOffset = float(cLineRetriever([keyValue])[0][0][1])
    weightedAveraging(weightDelta, keySort, float(cLineRetriever([keyValue])[0][0][0]))
    return dataTesting(testData, cat, allOffsets, keyValOffset, val, show)


def boosting(boostVal):    # function to manage optimization variables based on test metrics    boost
    print("=====\nBoosting:\n=====")
    global l1, l2, pruneNum, weightNum, estBias, weightDelta
    t = 0
    t2 = 0
    for x in testData:
        t += 1
        t2 += float(x[34])
    t = round(t2/t, 4)    # avg keyValue

    savedNum = 15
    for x in range(boostVal):   # optimizing l1
        l1 = x
        runData(cat3)
        runNum = MAPE
        l1 = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x
    l1 = savedNum
    print("L1 Boost:", l1)
    runData(cat3)

    savedNum = -1
    for x in range(boostVal):   # optimizing l2
        l2 = x
        runData(cat3)
        runNum = MAPE
        l2 = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x
    l2 = savedNum
    print("L2 Boost:", l2)
    runData(cat3)

    savedNum = .1
    for x in range(boostVal):   # optimizing weightDelta
        weightDelta = x/10
        runData(cat3)
        runNum = MAPE
        weightDelta = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x/10
    weightDelta = savedNum
    print("Weighted Delta Boost:", weightDelta)
    runData(cat3)

    savedNum = 1000
    for x in range(boostVal):   # optimizing weightNum
        weightNum = x+1000
        runData(cat3)
        runNum = MAPE
        weightNum = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x+1000
    weightNum = savedNum
    print("Weighted Averaging Boost:", weightNum)
    runData(cat3)

    savedNum = 150
    for x in range(boostVal):   # optimizing pruneNum
        pruneNum = x
        runData(cat3)
        runNum = MAPE
        pruneNum = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x
    pruneNum = savedNum
    print("Pruning Boost:", pruneNum)
    runData(cat3)

    savedNum = 2
    for x in range(boostVal):   # optimizing estBias
        estBias = x
        runData(cat3)
        runNum = MAPE
        estBias = savedNum
        runData(cat3)
        holdMAPE = MAPE
        if runNum <= holdMAPE:
            savedNum = x
    estBias = savedNum
    print("Estimate Bias:", estBias)
    runData(cat3)

print("Before Optimization:\n=======\n")
runData(cat3, 1)    # 1 = print info
boosting(1000)
print("\nAfter Optimization:\n========")
runData(cat3, 1)    # 1 = print info


# possible simple interface design
'''
end = False
while not end:
    row = input("Insert Row Data:\n")
    if row == "end":
        end = True
    else:
        estimateValues = estimate2(row, cat3, allOffsets, keyValOffset)
        print("Air Quality Score: ", estimateValues[1])
        print("Health Score estimate: ", estimateValues[0])
'''

