# Based on:
# C950 - Webinar-1 - Let’s Go Hashing
# W-1_ChainingHashTable_zyBooks_Key-Value.py
# Ref: zyBooks: Figure 7.8.2: Hash table using chaining.

# Modified for Package Class

from DeliveryStatus import Status
from Package import Package

# HashTable class using chaining.
class PackageHashTable:
    # Constructor with optional initial capacity parameter.
    # Assigns all buckets with an empty list.
    def __init__(self, initial_capacity=40):
        # initialize the hash table with empty bucket list entries.
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new package into the hash table.
    def insert(self, package):
        # get the bucket list where this package will go.
        idnumber = package.getId()
        bucket = hash(idnumber) % len(self.table)
        bucket_list = self.table[bucket]

        # check if the package already exists in the table.
        for pack in bucket_list:
            if pack.getId() == idnumber:
                print("Package with ID: " + package.id + ' already exists in the Hashtable.')
                return True

        # if not, insert the package to the end of the bucket list.
        bucket_list.append(package)
        return True

    # Searches for the package in the hash table based on package ID.
    # Returns the package if found, or None if not found.
    def search(self, package): # can be searched by package object or just ID number
        idnumber = package
        if package is Package:
            # if the input is a Package object instead of just a number the idnumber is adjusted appropriately
            idnumber = package.getId()
        # get the bucket list where this key would be.
        bucket = hash(idnumber) % len(self.table)
        bucket_list = self.table[bucket]

        # search for the package ID in the bucket list
        for pack in bucket_list:
            if pack.getId() == idnumber:
                return pack
        return None

    # Removes package with matching ID from the hash table.
    def remove(self, package): # can use package ID or package object
        idnumber = package
        if package is Package:
            # if the input is a Package object instead of just a number the idnumber is adjusted appropriately
            idnumber = package.getId()
        # get the bucket list where this package will be removed from.
        bucket = hash(idnumber) % len(self.table)
        bucket_list = self.table[bucket]

        # remove the package from the bucket list if it is present.
        for pack in bucket_list:
            if pack.getId() == idnumber:
                bucket_list.remove(pack)

    # Searches for and retrieves information for corresponding package or package ID.
    # Returns a text string of all the package information.
    def getInfo(self, package):
        if self.search(package) is not None:
            pack = self.search(package)
            return pack.getAllInfo()

    # Prints the details of every package in the hashtable
    def getAllPackagesInfo(self):
        count = 1
        while count <= len(self.table):
            print(self.getInfo(count))
            count = count + 1