#  Jeryn Inman Student ID: #000948438


# Class to represent a package being shipped with pertinent information, with an override to string function
# pertinent information based on needs set by requirements
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.status = "At Hub"

    def __str__(self):
        return "Package " + str(self.package_id) + ":   " + str(self.address) + " " + str(self.city) + " " \
               + str(self.zip_code) + " Special Notes:" + str(self.special_notes)\
               + "\nStatus: " + str(self.status) + " Deadline: " + str(self.deadline)


# custom hash table class with add, lookup, getter and setter functions
class HashTable:
    def __init__(self):
        self.size = 40
        self.keys = [None] * self.size
        self.values = [None] * self.size

    def hash(self, key):
        return key % self.size

    def rehash(self, old_hash):
        return(old_hash + 1) % self.size

    # add method
    def insert(self, key, value):
        hash = self.hash(key)

        if self.keys[hash] is None:
            self.keys[hash] = key
            self.values[hash] = value
        else:
            if self.keys[hash] == key:
                self.values[hash] = value  # replace with new value for updated package information
            else:  # won't happen with current configuration, in for scale ability later
                next_available = self.rehash(hash)

                # Find next empty space or one with same key
                while self.keys[next_available] is not None and self.keys[next_available] != key:
                    next_available = self.rehash(next_available)

                # If empty fill
                if self.keys[next_available] is None:
                    self.keys[next_available] = key
                    self.values[next_available] = value
                else:
                    self.values[next_available] = value  # replace data if key is same

    # find method
    def lookup(self, key):
        start = self.hash(key)
        value = None
        stop = False
        found = False
        position = start

        # searches until either found, or searched entire table
        while self.keys[start] is not None and not found and not stop:
            if self.keys[position] == key:
                found = True
                value = self.values[position]
            else:
                position = self.rehash(position)
                if position == start:
                    stop = True
        return value

    # set method
    def __setitem__(self, key, value):
        self.insert(key, value)

    # get method
    def __getitem__(self, key):
        return self.lookup(key)

    # print method
    def print(self):
        for item in self.values:
            if item is not None:
                print(str(item))
