import csv
import DeliveryStatus
from Package import Package
from Hashtable import PackageHashTable
from datetime import time, timedelta, datetime
from Truck import Truck
import sys
import MiscFunctions


# packageHashTable.getAllPackagesInfo()
# print(packageHashTable.getInfo(2))

# Loads Truck 1 with the first set of packages to be delivered. The packages in this load can be changed
# manually based on what packages need to be delivered sooner and have other conditions.
# Also changes the Truck to be set to not at the Hub and sets its destination for the closest package address.
def truck1FirstLoad(truck):
    packageSet = [13, 14, 15, 16, 19, 20, 31, 34]
    for i in packageSet:
        truck.addPackage(i)
    truck.setDestination(truck.findClosestAddress('HUB'))
    truck.atHub = False

# Loads Truck 1 with the second set of packages to be delivered. The packages in this load can be changed
# manually based on what packages need to be delivered sooner and have other conditions.
# Also changes the Truck to be set to not at the Hub and sets its destination for the closest package address.
def truck1SecondLoad(truck):
    packageSet = [1, 22, 24, 25, 26, 27, 29, 35, 39, 40]
    for i in packageSet:
        truck.addPackage(i)
    truck.setDestination(truck.findClosestAddress('HUB'))
    truck.atHub = False

# Loads Truck 2 with the first set of packages to be delivered. The packages in this load can be changed
# manually based on what packages need to be delivered sooner and have other conditions.
# Also changes the Truck to be set to not at the Hub and sets its destination for the closest package address.
def truck2FirstLoad(truck):
    packageSet = [2, 3, 5, 7, 8, 10, 11, 12, 18, 23, 30, 37, 38]
    for i in packageSet:
        truck.addPackage(i)
    truck.setDestination(truck.findClosestAddress('HUB'))
    truck.atHub = False

# Loads Truck 2 with the second set of packages to be delivered. The packages in this load can be changed
# manually based on what packages need to be delivered sooner and have other conditions.
# Also changes the Truck to be set to not at the Hub and sets its destination for the closest package address.
def truck2SecondLoad(truck):
    packageSet = [4, 6, 9, 17, 21, 28, 32, 33, 36]
    for i in packageSet:
        truck.addPackage(i)
    truck.setDestination(truck.findClosestAddress('HUB'))
    truck.atHub = False


loopActive = True
endProgram = False


# Main program loop used to ask for user input of Time, and then print out the status of all packages
# and trucks up to that point in time. Repeats after doing that and asks for another time.
while loopActive:

    startTime = time(hour=8, minute=0)
    currentTime = time(hour=8, minute=0)

    # creating 2d distance array
    distanceMatrix = MiscFunctions.createDistanceMatrix('distances.csv')
    # Creating and filling a package Hash Table
    packageHashTable = MiscFunctions.createPackageHashTable('packages.csv')
    # Creating address dictionary for use in finding address index in the distance Matrix
    addressDict = MiscFunctions.createAddressDictionary('addresses.csv')

    while True:
        # Asks user to input a time that will be used to check the status of all the trucks and packages
        # up to that point. If an invalid input is used then it asks the user to enter it again.
        # If the user wants to end the program they can enter END and the program will end.
        userInput = input("To see the status of the trucks and packages, enter a time between \n"
                          "08:00 and 23:59 (include leading zeros) in the format of HH:MM. (ex. 09:30) \n"
                          "Otherwise, if you want to end the program type END: ")

        if userInput in ('END', 'end', "End"):
            # checks if the user entered 'End' in some way
            endProgram = True
            break
        else:
            try:
                # checks if the user input was a time in the correct format
                userTime = time.fromisoformat(userInput)
                if userTime <= startTime:
                    print('Invalid input. Please enter a time after 08:00.'
                          + '\n')
                elif isinstance(userTime, time):
                    break
                    # exits inner loop asking for time
            except:
                print(sys.exc_info()[0], ' occurred.')
                print('Please enter a valid input. Make sure you have leading zeros if applicable.'
                      + '\n')
    if endProgram:
        # Exits main program loop if user is ending the program.
        break

    # Asks the user which package they want to see the status of at the entered time. If anyting else
    # besides a valid ID number is entered then it defaults to all packages.
    userInput2 = input("\nEnter the ID number of the package you'd like to see the status of, \n"
                       "or leave blank and hit enter to see the status of every package. \n"
                       "(Invalid input will default to showing every package status): ")

    truck1 = Truck(packageHashTable)
    truck2 = Truck(packageHashTable)
    # Creating the 2 trucks

    while currentTime < userTime:
        # Has the trucks deliver packages until the given time and then prints a report of package status.
        # Add another else if statement and add another number of trips if more than 2 trips are needed.
        if truck1.trips == 0 and truck1.atHub:
            # Loads the truck
            truck1FirstLoad(truck1)
        elif truck1.trips == 1 and truck1.atHub:
            # Checks if the truck is at the Hub and completed first trip of deliveries and then loads it
            # with the second set of packages.
            truck1SecondLoad(truck1)
            truck1.finished = True

        truck1.travel(0.3, currentTime)

        # Add another else if statement and add another number of trips if more than 2 trips are needed.
        if truck2.trips == 0 and truck2.atHub:
            # Loads the truck
            truck2FirstLoad(truck2)
        elif truck2.trips == 1 and truck2.atHub:
            # Checks if the truck is at the Hub and completed first trip of deliveries and then loads it
            # with the second set of packages.
            truck2SecondLoad(truck2)
            truck2.finished = True

        truck2.travel(0.3, currentTime)

        currentTime = MiscFunctions.addOneMinute(currentTime)

    if str.isdigit(userInput2):
        # Checks if the user entered an integer
        try:
            if packageHashTable.getInfo(int(userInput2)) is None:
                # Checks if there is a package with the given ID number
                print("There is no package with that ID.\n")
            else:
                print(packageHashTable.getInfo(int(userInput2)) + "\n")
                # Prints the package information of the given ID.
        except:
            packageHashTable.getAllPackagesInfo()
            print('Truck 1: ' + '{:.1f}'.format(truck1.milesTotal) + ' miles driven.')
            print('Truck 2: ' + '{:.1f}'.format(truck2.milesTotal) + ' miles driven.')
            print('Total combined miles driven: ' + '{:.1f}'.format(truck1.milesTotal + truck2.milesTotal))
            # Prints all the information about packages as well as the miles driven by the trucks.
    else:
        packageHashTable.getAllPackagesInfo()
        print('Truck 1: ' + '{:.1f}'.format(truck1.milesTotal) + ' miles driven.')
        print('Truck 2: ' + '{:.1f}'.format(truck2.milesTotal) + ' miles driven.')
        print('Total combined miles driven: ' + '{:.1f}'.format(truck1.milesTotal + truck2.milesTotal))
        # Prints all the information about packages as well as the miles driven by the trucks.


print("Ending Program...")

