import csv
from Package import Package
from Hashtable import PackageHashTable
from datetime import time, timedelta, datetime


# Reads in the distance file and puts it into a 2D array
# Returns the 2D array of address distance information.
def createDistanceMatrix(file):
    # Reading in the distances file
    distanceFile = open(file)
    csvreader = csv.reader(distanceFile)

    distanceMatrix = []
    # creating a 2D matrix from lists. 27 rows and 29 columns for the current example data.
    for row in csvreader:
        distanceMatrix.append(row)

    distanceFile.close()

    return distanceMatrix


# Reads in the package file and sorts the items into a 2D matrix, then into a List of Package objects
# and inserts those into a package Hash Table.
# Returns the filled Package Hash Table
def createPackageHashTable(file):
    # Reading in the packages file
    packageFile = open(file)
    csvreader = csv.reader(packageFile)

    packageMatrix = []
    # making another 2d matrix for package info
    for row in csvreader:
        packageMatrix.append(row)

    packageList = []
    # List of packages to be read into Hashtable
    for row in packageMatrix:
        # iterating through the package detail matrix to store values in package objects
        item = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        packageList.append(item)

    # Creating and filling the Hashtable with package objects
    packageHashTable = PackageHashTable(40)

    for item in packageList:
        packageHashTable.insert(item)

    packageFile.close()

    return packageHashTable


# Reads in the address name file into a dictionary with the address as Key
# and their index in the DistanceMatrix as the Value
# Returns the filled Address Dictionary
def createAddressDictionary(file):
    # Opening address file to read into dictionary
    addressFile = open(file)
    csvreader = csv.reader(addressFile)

    addressDict = {}
    count = 0

    for row in csvreader:
        # iterating through the address list and storing the value with the address' index in the matrix
        # so it can be looked up easier
        addressDict[row[0]] = count
        count = count + 1

    addressFile.close()

    return addressDict


def addressDistanceLookup(address1, address2, addressDictionary, distanceMatrix):
    # Looks through the given addressDictionary using 2 given addresses and uses the associated index
    # to locate the distance between the 2 addresses in the distanceMatrix 2d array.
    # Returns the distance between the 2 addresses as a number.
    a1 = addressDictionary[address1]
    a2 = addressDictionary[address2]
    # checks for which index is larger to position the larger one first to accommodate for the format of the
    # provided data. Adds 2 to the second index for the same reason (the first 2 values are address and location name)
    if a1 > a2:
        return float(distanceMatrix[a1][a2 + 2])
    else:
        return float(distanceMatrix[a2][a1 + 2])


def addOneMinute(initialTime):
    # Adds one minute of time onto the time given in the parameters.
    timeChange = timedelta(minutes=1)
    # time converted to datetime temporarily to allow for timedelta to be added.
    tempDateTime = datetime.combine(datetime(1,1,1), initialTime)
    newTime = (tempDateTime + timeChange).time()
    return newTime