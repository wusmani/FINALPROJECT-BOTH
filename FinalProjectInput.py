# Name- Wasay Usmani
# ID- 1878157

import csv
file = open('ManufacturerList.csv')
csvreader = csv.reader(file)
manRows = []
priceRows = []
dateRows = []
manList = []
typeList = []
askedDate = False

# copies each row in the csv to a dictionary manRows (Manufacturer rows)
# copies each unique instance of a manufacturer and item type to seperate lists
for row in csvreader:
    manRows.append(row)
    if row[1] not in manList:
        manList.append(row[1])
    if row[2] not in typeList:
        typeList.append(row[2])

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


while True:
  # asks the user for the current date since instructions state we cannot import date functionality
    while askedDate == False:
      # uses try code to make sure date is in correct format
        try:
            d1, m1, y1 = [int(x) for x in input(
                "Enter the current date in format DD/MM/YYYY: ").split('/')]
            askedDate = True
        except:
            print("Invalid date given. Try again.")
    query = input("Enter the manufacturer and item type. Enter 'q' to quit. ")
    # qList creates a list out of the input the user just inputted. "Apple laptop" becomes ["Apple", "laptop"]
    qList = list(query.split(" "))
    foundMan = False
    foundType = False
    invalid = False
    trimQuery = [None] * 2
    matchRow = []
    cleanedMatches = []
    relatedRows = []
    cleanedRelated = []
    # exits loop if user presses 'q'
    if query == "q":
        break
    # Function of this loop is to go through the qList and see which words are relevent for the search
    for i in range(len(qList)):
        # checks if the current word we're looking at is a manufacturer
        if qList[i] in manList:
            # foundMan (found manufacturer) is set to true when we have already found a word that
            # matches with a manufacturer. This is used to make sure the query doesn't have two
            # manufacturers listed
            if foundMan == False:
                foundMan = True
                trimQuery[0] = qList[i]
            else:
                print("No such item in inventory")
                invalid = True
                break
        # checks if the current word we're looking at is an item type
        if qList[i] in typeList:
            # foundType has same functionality as foundMan
            if foundType == False:
                foundType = True
                trimQuery[1] = qList[i]
            else:
                print("No such item in inventory")
                invalid = True
                break
    # invalid is false if the previous loop found that the query was indeed valid (no multiple manufacturers or item types.)
    if (invalid == False):
        # goes through rows to find matches
        for i in range(len(manRows)):
            if manRows[i][2] == trimQuery[1]:
                # the item type is matched with so we save this in related items list.
                relatedRows.append(i)
                if manRows[i][1] == trimQuery[0]:
                    # There is a match
                    # Adds the row of a match to the list matchRows
                    relatedRows.remove(i)
                    matchRow.append(i)
        # cleaned matches will be all the matches to the query which are not damaged or past due
        cleanedMatches = matchRow.copy()
        # no matches therefore no items in inventory
        if (len(matchRow) == 0):
            print("No such item in inventory")
        else:
            for i in range(len(matchRow)):
                # one of the matches is damages, so we take it out of cleaned matches.
                if manRows[matchRow[i]][3] == "damaged":
                    cleanedMatches.remove(matchRow[i])
                else:
                    # look through date rows to find matching id to find service date.
                    for j in range(len(dateRows)):
                        # save service date to 3 variables (d,m,y)
                        if manRows[matchRow[i]][0] == dateRows[j][0]:
                            d2, m2, y2 = [int(x)
                                          for x in dateRows[j][1].split('/')]
                    # checks if service date was in the past or not, if so, we remove that match since it is past due.
                    # y1, m1, and d1 are from where the user was asked to input the current date.
                    if y2 < y1:
                        cleanedMatches.remove(matchRow[i])
                    elif y2 > y1:
                        break
                    else:
                        if m2 < m1:
                            cleanedMatches.remove(matchRow[i])
                        elif m2 > m1:
                            break
                        else:
                            if d2 < d1:
                                cleanedMatches.remove(matchRow[i])
        maxPrice = 0
        finalRow = 0
        # checks to see which one of the matches is the most expensive.
        for i in range(len(matchRow)):
            for j in range(len(priceRows)):
                if priceRows[j][0] == manRows[matchRow[i]][0]:
                    if int(priceRows[j][1]) > maxPrice:
                        maxPrice = int(priceRows[j][1])
                        finalRow = matchRow[i]

        if (len(matchRow) > 0):
            # this if statement means "if there are matches, but none of them can be used, the item(s) must be damaged or past due"
            if (len(cleanedMatches) == 0):
                print("The item is damaged or past service due data.")
            else:
                # prints the item along withc its information
                itemId = manRows[finalRow][0]
                manu = manRows[finalRow][1]
                itemType = manRows[finalRow][2]
                print("Your item is: " + itemId + ", " +
                      manu + ", " + itemType + ", $" + str(maxPrice))

        cleanedRelated = relatedRows.copy()
        # cleans up the matches for related items the same way it was done for the normal matches.
        for i in range(len(relatedRows)):
            if manRows[relatedRows[i]][3] == "damaged":
                cleanedRelated.remove(relatedRows[i])
            else:
                for j in range(len(dateRows)):
                    if manRows[relatedRows[i]][0] == dateRows[j][0]:
                        d2, m2, y2 = [int(x)
                                      for x in dateRows[j][1].split('/')]
                if y2 < y1:
                    cleanedRelated.remove(relatedRows[i])
                elif y2 > y1:
                    break
                else:
                    if m2 < m1:
                        cleanedRelated.remove(relatedRows[i])
                    elif m2 > m1:
                        break
                    else:
                        if d2 < d1:
                            cleanedRelated.remove(relatedRows[i])
        priceDifference = 1000000
        finalRelatedRow = 0
        relatedPrice = 0
        # for the related items, we are looking for an item closest in price to the match,
        for i in range(len(cleanedRelated)):
            for j in range(len(priceRows)):
                if priceRows[j][0] == manRows[cleanedRelated[i]][0]:
                    # if the price difference for this item is smaller than the previous, this item is closer in price to
                    # the matched item, and therefore is saved.
                    if abs(int(priceRows[j][1]) - maxPrice) < priceDifference:
                        priceDifference = abs(int(priceRows[j][1]) - maxPrice)
                        relatedPrice = int(priceRows[j][1])
                        finalRelatedRow = cleanedRelated[i]
        # if there are related items, then print the one we found with the closest price
        if (len(cleanedRelated) > 0):
            itemId = manRows[finalRelatedRow][0]
            manu = manRows[finalRelatedRow][1]
            itemType = manRows[finalRelatedRow][2]
            print("You may also consider: " + itemId + ", " +
                  manu + ", " + itemType + ", $" + str(relatedPrice))
