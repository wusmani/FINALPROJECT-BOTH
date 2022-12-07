# Name: Wasay Usmani
# ID- 1878157

import csv
file = open('ManufacturerList.csv')
csvreader = csv.reader(file)
manRows = []
priceRows = []
priceDict = {}
dateRows = []
dateDict = {}
manList = []
typeList = []
pastDate = []
askedDate = False

# copies each row in the csv to a dictionary manRows (Manufacturer rows)
# copies each unique instance of a manufacturer and item type to seperate lists
for row in csvreader:
    manRows.append(row)
    if row[1] not in manList:
        manList.append(row[1])
    if row[2] not in typeList:
        typeList.append(row[2])
        something2 = row[0]
        something1 = row[0]

file = open('PriceList.csv')
csvreader = csv.reader(file)
# copies elements from PriceList.csv to a dictiotionary
for row in csvreader:
    priceRows.append(row)

# copies elements from ServiceDatesList.csv to a dictiotionary
file = open('ServiceDatesList.csv')
csvreader = csv.reader(file)
for row in csvreader:
    dateRows.append(row)

# converts priceRows into a dictionary
for elem in priceRows:
    try:
        priceDict[elem[0]].append(elem[1])
    except KeyError:
        priceDict[elem[0]] = elem[1]
# converts dateRows into a dictionary
for elem in dateRows:
    try:
        dateDict[elem[0]].append(elem[1])
    except KeyError:
        dateDict[elem[0]] = elem[1]

# swaps manufacturer name to the begining of the list so it can be sorted alphabetically by this.
for li in manRows:
    temp = li[1]
    li[1] = li[0]
    li[0] = temp
manRows.sort()
# creates the FullInventory csv file and writes all rows in order by manufacturer name.
with open('FullInventory.csv', 'w') as file:
    writer = csv.writer(file)
    for i in range(len(manRows)):
        data = [manRows[i][1], manRows[i][0],
                manRows[i][2], priceDict.get(manRows[i][1]), dateDict.get(manRows[i][1]),  manRows[i][3]]
        writer.writerow(data)

# sorts the maufacturer rows back to its original format with ID at the beginning and sorts it by ID number.
for li in manRows:
    temp = li[1]
    li[1] = li[0]
    li[0] = temp
manRows.sort()

# creates csv files for all item types and adds each type to the right one. They are sorted by ID number ascendingly.
for itemType in typeList:
    with open(f'{itemType}Inventory.csv', 'w') as file:
        writer = csv.writer(file)
        for i in range(len(manRows)):
            if itemType == manRows[i][2]:
                data = [manRows[i][0], manRows[i][1],
                        manRows[i][2], priceDict.get(manRows[i][0]), dateDict.get(manRows[i][0]),  manRows[i][3]]
                writer.writerow(data)

while askedDate == False:
    # uses try code to make sure date is in correct format
    try:
        d1, m1, y1 = [int(x) for x in input(
            "Enter the current date in format DD/MM/YYYY: ").split('/')]
        askedDate = True
    except:
        print("Invalid date given. Try again.")

# creates a list, pastDate that records all items that are overdue their service date.
for i in range(len(manRows)):
    for j in range(len(dateRows)):
        if manRows[i][0] == dateRows[j][0]:
            d2, m2, y2 = [int(x) for x in dateRows[j][1].split('/')]
    if y2 < y1:
        pastDate.append([manRows[i][0], f'{d2}/{m2}/{y2}'])
    elif y2 > y1:
        continue
    else:
        if m2 < m1:
            pastDate.append([manRows[i][0], f'{d2}/{m2}/{y2}'])
        elif m2 > m1:
            continue
        else:
            if d2 < d1:
                pastDate.append([manRows[i][0], f'{d2}/{m2}/{y2}'])

# sorts the dates in the pastDate list in order of oldest to most recent
n = len(pastDate)
for i in range(n-1):

    for j in range(0, n-i-1):
        d1, m1, y1 = [int(x) for x in pastDate[j][1].split('/')]
        d2, m2, y2 = [int(x) for x in pastDate[j+1][1].split('/')]
        if y2 < y1:
            pastDate[j], pastDate[j + 1] = pastDate[j + 1], pastDate[j]
        elif y2 > y1:
            continue
        else:
            if m2 < m1:
                pastDate[j], pastDate[j + 1] = pastDate[j + 1], pastDate[j]
            elif m2 > m1:
                continue
            else:
                if d2 < d1:
                    pastDate[j], pastDate[j + 1] = pastDate[j + 1], pastDate[j]

# Creates the PastServiceDateInventory csv file and writes the past due items to it.
with open('PastServiceDateInventory.csv', 'w') as file:
    for date in pastDate:
        writer = csv.writer(file)
        for i in range(len(manRows)):
            if manRows[i][0] == date[0]:
                data = [manRows[i][0], manRows[i][1],
                        manRows[i][2], priceDict.get(manRows[i][0]), dateDict.get(manRows[i][0]),  manRows[i][3]]
                writer.writerow(data)

# Create and fill a list with all damaged items
damagedList = []
for i in range(len(manRows)):
    if manRows[i][3] == "damaged":
        damagedList.append([manRows[i][0], manRows[i][1],
                            manRows[i][2], priceDict.get(manRows[i][0]), dateDict.get(manRows[i][0]),  manRows[i][3]])

# Sort the damagedList in order from most to least expensive
n = len(damagedList)
for i in range(n-1):
    for j in range(0, n-i-1):
        if int(damagedList[j][3]) < int(damagedList[j + 1][3]):
            damagedList[j], damagedList[j +
                                        1] = damagedList[j + 1], damagedList[j]

# Creates the DamagedInventory csv and writes the damaged items to it.
with open('DamagedInventory.csv', 'w') as file:
    writer = csv.writer(file)
    for elem in damagedList:
        writer.writerow(elem)
