# Package class that will store all the information about a specific package
# The fields are based on the columns from the Package File

from DeliveryStatus import Status


# Importing the delivery status to be able to use it for package status.

class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, mass, note=""):
        # initializes the Package with all the potential details, and defaults note to a blank string.
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.mass = mass
        self.note = note
        self.status = Status.HUB
        # self.truck = 'None'
        self.timeDelivered = "Not delivered"

    # Returns all the package attributes as a string
    def getAllInfo(self):
        return self.id + ' | ' + self.address + ' | ' + self.city + ' | ' + self.state + ' | ' +\
               self.zipcode + ' | ' + self.deadline + ' | ' + self.mass + ' | Status: ' + self.status +\
               ' | Time Delivered: ' + self.timeDelivered + ' | Note: ' + self.note

    # Returns the ID of the package as an integer
    def getId(self):
        return int(self.id)