# StudentID: 012518846

import csv

numPackages = 0
csv1 = []
with open('WGUPS_Package_File.csv', 'r') as file:   # collects csv1 data
    csv_reader = csv.reader(file)
    for row in csv_reader:
        csv1.append(row)
        numPackages += 1


class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]  # List of buckets for chaining
    def _hash(self, key):
        return key % self.size
    def insert(self, key, value):
        index = self._hash(key)
        # Check if key exists; if so, update it
        for i, (existing_key, _) in enumerate(self.table[index]):
            if existing_key == key:
                self.table[index][i] = (key, value)
                return
        # Otherwise, insert new key-value pair
        self.table[index].append((key, value))
    def search(self, key):
        index = self._hash(key)
        for existing_key, value in self.table[index]:
            if existing_key == key:
                return value
        return None
    def __str__(self):
        return str(self.table)


# csv1 = list of rows, each row is like: ['PackageID', 'Address', ...]
# Skip header, so start from index 1
numPackages = len(csv1)
packageHashTable = HashTable(numPackages - 1)
for row in csv1[1:]:
    package_id = int(row[0])
    row.append(0)  # delivery status = 0 (undelivered)
    packageHashTable.insert(package_id, row)


load1 = []  #truck 1
load2 = []  #truck 3
load3 = []  #truck 2
def assignLoad(package):    #assigns packages to different loads for trucks
    loadNum = 0

    # deadline sorting
    if package[5] == "9:00 AM":
        loadNum = 1
    elif float(package[0]) == 6:   # package delayed
        loadNum = 3
    elif package[5] == "10:30 AM" and float(package[0]) != 6:
        if float(package[0]) < 21:
            loadNum = 1
        else:
            loadNum = 2

    # general sorting
    if float(package[0]) in (3, 18, 36, 38):   # 2nd truck only check
        loadNum = 3
    elif float(package[0]) in (9, 25, 28, 32):    # delayed arrival check
        loadNum = 3

    #final loading
    match loadNum:
        case 1:
            load1.append(package)
        case 2:
            load2.append(package)
        case 3:
            load3.append(package)
        case 0:
            if len(load1) < 16:
                load1.append(package)
            elif len(load3) < 14:
                load3.append(package)
            else:
                load2.append(package)


for x in range(packageHashTable.size):
    assignLoad(packageHashTable.search(x+1))


csv2 = []
numColumns = 0
numRows = 0
with open('WGUPS_Distance_Table.csv', 'r') as file:     # collects csv2 data
    csv_reader = csv.reader(file)
    for row in csv_reader:
        numColumns = len(row)
        numRows += 1
        csv2.append(row)


for c in range(numColumns):     # mirrors values from rows and columns for easier searching
    for r in range(numRows):
        if (csv2[r][c]) == "":
            (csv2[r][c]) = (csv2[c-2][r+2])


locations = []
for x in range(packageHashTable.size):   # matches locations to package IDs
    for r in range(numRows):
        if packageHashTable.search(x+1)[1] in csv2[r][0]:
            locations.append([packageHashTable.search(x+1)[1], r])
            if len(locations) == 11:
                locations.append([packageHashTable.search(12)[1], 16])


route1 = []
route2 = []
route3 = []
packageCheck = []
totalDistances = []
def routeMaker(load, route):    # sifts through packages in loads to create route order
    x = 0
    totalD = 0
    while len(load) > 0:      # while unvisited locations in load
        shortestDist = 100
        loading = []
        rows = []
        for y in range(len(load)):
            if int(load[y][0]) == 40:
                rows.append(2)
            else:
                rows.append(int(locations[int(load[y][0])][1]))
        for y in range(len(load)):
            r = rows[y]
            if len(route) > 0:
                if int(route[x-1][0][0]) == 40:
                    c = 20
                else:
                    c = int(locations[int(route[x - 1][0][0])][1]) + 2  # -1 after int(route[x-1][0][0]) ?
            else:
                c = 2
            if float(csv2[r][c]) < shortestDist and r in rows:  # adds distance and package data into the route array
                shortestDist = float(csv2[r][c])
                loading = load[y]
        totalD += shortestDist
        route.append([loading, shortestDist])
        packageCheck.append(loading)
        load.remove(loading)
        x += 1
    totalDistances.append(totalD)
    #wrong address for package ID 9 fix
    changeP = route[0]
    for p in route:
        if p[0][0] == '9':
            changeP = p
    if changeP[0][0] == '9':
        route.append(changeP)
        route.remove(changeP)


routeMaker(load1, route1)
routeMaker(load2, route2)
routeMaker(load3, route3)


delivered = 0
truckMileage = [0,0,0]
def routeTimer(milage, route,time, routeNum, delay = 0.0):     # sets up the time function for package tracking
    miles = 0   # distance needed for next packages
    for x in route:
        if (float((miles+x[1])/18)+delay) <= time:
            global delivered
            delivered += 1
            x[0][8] = 2
            milage = round(milage, 1)
            milage += round(x[1],1)
            truckMileage[routeNum] = round(milage,1)
        miles += x[1]
    return milage

def routeStatus(timeCap):   # allows user to check package status for each package and each route
    time = 0
    global delivered
    if time < .1: #.11
        delivered = 0
        for x in route1:
            x[0][8] = 1  # loaded = 1
        for x in route2:
            x[0][8] = 1  # loaded = 1
        for x in route3:
            x[0][8] = 0  # at hub = 0

    while delivered < 40:
        if time <= 1.083 and not time > 1.2:  # sets packages to 'not received' if necessary
            for x in route3:
                if x[0][0] in ['6', '25', '28', '32']:
                    x[0][8] = -1
        while time < timeCap:
            milage1 = 0
            milage2 = 0
            milage3 = 0
            time += .1
            if time >= 1.5 and time <= 1.6:     # sets route3 to loaded at 9:30
                for x in route3:
                    x[0][8] = 1  # loaded = 1
            milage1 = routeTimer(milage1, route1, time, 0)
            milage2 = routeTimer(milage2, route2, time, 1)
            milage3 = routeTimer(milage3,route3, time, 2, 1.5)
            if time > 2.2:  # package ID 9 being late address fix
                route3[15][0][1] = "410 S. State St."
                route3[15][0][4] = "84111"
        break
    # printing functions for truck and route data
    print("PACKAGE ID = p, STATUS CODE = s  ->  \'[p, s]\'      CODES KEY: -1 = not received, 0 = at hub, 1 = on truck, 2 = delivered  ")
    print("~~~~~~~~~")
    print("Truck 1 Cargo:   ", end="")
    for x in range(len(route1)):
        print("[",route1[x][0][0], ",", route1[x][0][8], end=" ]")
        if x != len(route1)-1:
            print(" , ", end="")
    print("\nMileage: ", truckMileage[0]) #getMileage(route1,time))
    print("Truck 3 Cargo:   ", end="")
    for x in range(len(route2)):
        print("[",route2[x][0][0], ",", route2[x][0][8], end=" ]")
        if x != len(route2)-1:
            print(" , ", end="")
    print("\nMileage: ", truckMileage[1])  # getMileage(route2,time))
    print("Truck 2 Cargo:   ", end="")
    for x in range(len(route3)):
        print("[",route3[x][0][0], ",", route3[x][0][8], end=" ]")
        if x != len(route3)-1:
            print(" , ", end="")
    print("\nMileage: ", truckMileage[2]) #getMileage(route3,time))
    print("\nTotal Mileage = ", round((truckMileage[0] + truckMileage[1] + truckMileage[2]),1))



running = True
while running:      # user interface for checking package information
    setTime = 0
    done = False
    while not done:
        truckMileage = [0,0,0]  # resets truck mileage for new calculation
        try:
            pack_ID = int(input("Package Id Look-Up: "))
        except:
            print("~~~  Invalid Input!  ~~~")
        else:
            try:
                time_H = int(input("Select Hour: "))
            except:
                print("~~~  Invalid Input!  ~~~")
            else:
                try:
                    time_M = int(input("Select Minutes: "))
                except:
                    print("~~~  Invalid Input!  ~~~")
                else:
                    print("~~~~~~~~~")
                    timeHM = time_H-8 + round(time_M/60, 1)
                    routeStatus(timeHM)
                    package = packageHashTable.search(pack_ID % (numPackages - 1))
                    print("~~~~~~~~~")
                    print("Address:  ", package[1], "\nDeadline: ", package[5], "\nCity:     ", package[2], "\nZip Code: ", package[4], "\nWeight:   ", package[6])
                    match package[8]:
                        case -1:
                            print("Location:    ~ NOT RECEIVED ~")
                        case 0:  # 0 = at hub
                            print("Location:    ~ HUB ~")
                        case 1:  # 1 = on route
                            print("Location:    ~ ON TRUCK ~")
                        case 2:  # 2 = delivered
                            print("Location:    ~ DELIVERED ~")
                    print("~~~~~~~~~\n")

                    end = input("End Session?\n(input \'y\' if so) : ")
                    if end == 'y':
                        running = False
                        done = True
# final exit information and goodbye
print("\n~~~~~~~\nTotal Distances:\n  Truck 1: ", totalDistances[0], "\n  Truck 2: ", totalDistances[2], "\n  Truck 3: ", totalDistances[1], "\n  TOTAL: ", (totalDistances[0]+totalDistances[1]+totalDistances[2]),"\n~~~~~~~\n\nThank you for using WGUPS Systems!\n\nGood-Bye!\n\n~~~~~~~")


