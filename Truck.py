from Package import Package
import DeliveryStatus
from Hashtable import PackageHashTable
from datetime import time
import MiscFunctions

class Truck:
    def __init__(self, hashTable):
        # Creates a truck instance with a blank list of package IDs to keep track of which
        # packages are on which trucks
        # Also requires the hashtable being used to store all packages to be included in the constructor.
        self.packageIds = []
        self.packageHashTable = hashTable
        self.milesCurrentTrip = 0 # total miles traveled only for the current package
        self.milesTotal = 0 # running total of miles travelled by the truck
        self.milesToDestination = 0 # distance between current and destination address
        self.MAX_PACKAGES = 16
        self.addressCurrent = 'HUB' # most recently visited address, where truck is departing from
        self.addressDestination = '' # address of the package being delivered
        self.currentPackageID = None # package ID of the package currently being delivered
        self.finished = False
        self.trips = 0
        self.atHub = True
        self.addressDict = MiscFunctions.createAddressDictionary('addresses.csv')
        self.distanceMatrix = MiscFunctions.createDistanceMatrix('distances.csv')


    def addPackage(self, packageId):
        # Changes a package's status to En Route and adds it to the truck's packageIds list.
        # If the package ID is already in the list, then nothing happens.
        # If the truck is at max capacity, then nothing happens.
        if len(self.packageIds) >= self.MAX_PACKAGES:
            return

        if isinstance(packageId, Package):
            # makes packID the package ID if a package is passed instead of an integer.
            packID = packageId.getId()
        else:
            packID = packageId

        notAdded = True

        for item in self.packageIds:
            if item == packID:
                notAdded = False

        if notAdded:
            self.packageHashTable.search(packID).status = DeliveryStatus.Status.ENROUTE
            self.packageIds.append(packID)

    def removePackage(self, packageId):
        # Finds and removes a packageId from the Truck's packageIds list
        if isinstance(packageId, Package):
            # makes packID the package ID if a package is passed instead of an integer.
            packID = packageId.getId()
        else:
            packID = packageId

        for item in self.packageIds:
            if item == packID:
                self.packageIds.remove(item)

    def deliverPackage(self, currentTime):
        # Changes a package's status to Delivered
        # and changes its Time Delivered to the current time of the simulation
        # and then removes it from the truck's package list
        # then switches the Destination to the next package, or if that was the last package it
        # sends the truck back to the HUB.

        if self.currentPackageID is not None:
            # Checks to see if package ID exists to avoid errors trying to edit a None object
            self.packageHashTable.search(self.currentPackageID).status = DeliveryStatus.Status.DELIVERED
            self.packageHashTable.search(self.currentPackageID).timeDelivered = currentTime.strftime("%H:%M")
            self.removePackage(self.currentPackageID)

        if len(self.packageIds) == 0:
            # Changes destination to HUB if no more packages are in the truck
            self.addressCurrent = self.addressDestination
            self.addressDestination = 'HUB'
            self.currentPackageID = None
            self.milesToDestination = MiscFunctions.addressDistanceLookup(self.addressCurrent, self.addressDestination,
                                                                          self.addressDict, self.distanceMatrix)
            self.trips = self.trips + 1
            # adds one to the counter to indicate the truck has completed one delivery trip
            self.atHub = True
        else:
            # If there are still packages in the truck, it will
            # find the next closest package address and being to deliver that package.
            self.switchDestination(self.findClosestAddress(self.packageHashTable.search(self.currentPackageID).address))
            if self.milesToDestination == 0:
                # If the next package is the same address, it will deliver both at the same time.
                self.deliverPackage(currentTime)


    def switchDestination(self, packageId):
        # Switches the Destination to the current address, and then puts the next address as the destination.
        if isinstance(packageId, Package):
            # makes packID the package ID if a package is passed instead of an integer.
            packID = packageId.getId()
        else:
            packID = packageId

        self.addressCurrent = self.addressDestination
        self.setDestination(packID)


    def setDestination(self, packageId):
        # sets the destination address and next package to be delivered.
        # Also sets the distance to the next destination.
        if isinstance(packageId, Package):
            # makes packID the package ID if a package is passed instead of an integer.
            packID = packageId.getId()
        else:
            packID = packageId

        self.addressDestination = self.packageHashTable.search(packID).address
        self.currentPackageID = packID
        self.milesToDestination = MiscFunctions.addressDistanceLookup(self.addressCurrent, self.addressDestination,
                                                                      self.addressDict, self.distanceMatrix)


    def travel(self, distance_in_miles, current_time):
        # Has the truck travel the given distance and adds it to the total and current trip.
        # If the current trip amount exceeds the miles to destination, then that means the package is
        # delivered so it gets marked down and swapped, and the remainder of the distance is put onto
        # the next current trip total.
        if self.finished and self.addressCurrent == 'HUB' and len(self.packageIds) == 0:
            # Does nothing if completed so miles stop accumulated.
            return
        else:
            self.milesTotal = self.milesTotal + distance_in_miles
            self.milesCurrentTrip = self.milesCurrentTrip + distance_in_miles
            if self.milesCurrentTrip >= self.milesToDestination:
                leftover = self.milesCurrentTrip - self.milesToDestination
                self.deliverPackage(current_time)
                self.milesCurrentTrip = leftover


    def findClosestAddress(self, currentLocation):
        # Iterates through all the package IDs currently in the truck and selects the ID that has the
        # least distance from the current address the truck is at.
        # Returns the ID of the package with the lowest address distance that is loaded on the truck.
        closest = self.packageIds[0]
        for item in self.packageIds:
            if item != self.currentPackageID:
                # Used to avoid comparing to itself or else it would always be the closest

                # New distance being checked
                x = MiscFunctions.addressDistanceLookup(currentLocation,
                                                        self.packageHashTable.search(item).address,
                                                        self.addressDict, self.distanceMatrix)
                # Current closest address distance
                y = MiscFunctions.addressDistanceLookup(currentLocation,
                                                        self.packageHashTable.search(closest).address,
                                                        self.addressDict, self.distanceMatrix)
                if x < y:
                    # If the new distance is closer than the previous closest, the closest changes.
                    closest = item

        return closest
