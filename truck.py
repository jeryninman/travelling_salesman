#  Jeryn Inman Student ID: #000948438
from src.time import Time


# class designed to represent a package delivery truck
class Truck:
    def __init__(self, location, start):
        self.location = location
        self.capacity = 16
        self.loaded_packages = []
        self.speed = float(18.00) / 60  # 18mph to miles per minute
        self.miles_driven = 0
        self.trucks_time = start
        self.not_finished = True

    # calculates time to stop, then calls the selection algorithm until doing so would surpass the time or no packages
    # O(N^2)
    def advance(self, time, advancement, locations, at_hub, undelivered):
        halt = Time(time.hour, time.minute)  # copy, rather than reference, placeholder for end of time
        halt.advance(advancement)

        while self.trucks_time < halt and self.not_finished and (at_hub or self.loaded_packages):
            advanced_to = self.selection_algorithm(locations, at_hub, halt, undelivered)
            advancement = advanced_to - self.trucks_time
        self.trucks_time.advance(advancement)
        print("Miles driven: " + str(self.miles_driven) + " Packages on: " + str(len(self.loaded_packages)))
        self.not_finished = True  # reset finished for next use

    # adds packages to truck
    # O(3)
    def load_package(self, package):
        self.capacity -= 1
        self.loaded_packages.append(package)
        package.status = "In-route"

    # removes package from both loaded and undelivered lists, adds the miles, advances time and changes package status,
    # and truck's location
    # O(N^2)
    def deliver_package(self, package, distance, undelivered):
        self.capacity += 1
        if package in self.loaded_packages:
            delivered = self.loaded_packages.index(package)
            self.loaded_packages.pop(delivered)
            if package in undelivered:
                delivered = undelivered.index(package)
                undelivered.pop(delivered)
            self.miles_driven += distance
            self.trucks_time.advance(distance / self.speed)
            package.status = "Delivered at " + str(self.trucks_time)
            self.location = package.address

    # Puts next package object from hub list into truck inventory list
    # O(N)
    def reload(self, at_hub, undelivered):
        while self.capacity > 0 and at_hub:
            package = at_hub.pop()
            self.load_package(package)
            undelivered.append(package)
            self.capacity -= 1

    # Finds current location in location list, figures out distance, and advances time/mileage accordingly
    # O(N)
    def return_to_hub(self, locations_data, at_hub, undelivered):
        # find distance to hub add distance + time
        current_location = self.location
        for i in locations_data:
            if current_location == i[0]:
                distance = float(i[2])
                self.location = "HUB"
                self.miles_driven += distance
                self.trucks_time.advance(distance / self.speed)
        if not self.loaded_packages and at_hub:
            self.reload(at_hub, undelivered)

    # Simple greedy algorithm, finds closest package in list of loaded packages, delivers it if time permits
    # sets first package as closest, then finds the distance to other packages' destinations, compares to find lowest
    # O(N^2)
    def selection_algorithm(self, locations_data, at_hub, halt, undelivered):
        finished_time = self.trucks_time

        while self.loaded_packages and self.trucks_time < halt and self.not_finished:
            closest = self.loaded_packages[0] # first packages will be default closest
            found = False

            # find current location's index
            for i in locations_data:
                if self.location == i[0]:
                    current_location = locations_data.index(i)
                    break

            # find distance for first package based on current location
            for i in locations_data:
                if self.loaded_packages[0].address == i[0]:
                    index = locations_data.index(i)
                    if index > current_location:  # Table only shows one direction, + 2 for title and zip slots
                        distance = float(locations_data[index][current_location + 2])
                    else:
                        distance = float(locations_data[current_location][index + 2])
                    found = True

            if not found:
                print("Location not found: " + self.loaded_packages[0].address)

            if len(self.loaded_packages) > 1:   # last package will always be closest
                # cycle through packages, finding the distance
                for j in self.loaded_packages:
                    for i in locations_data:
                        if j.address in i[0]:
                            index = locations_data.index(i)
                            if index > current_location:
                                distance_compare = float(locations_data[index][current_location + 2])
                            else:
                                distance_compare = float(locations_data[current_location][index + 2])
                            if distance > distance_compare:
                                distance = distance_compare
                                closest = j

            if int(closest.package_id) == 9:
                if self.trucks_time >= Time(10, 20):  # update address to correct delivery address at proper time
                    closest.address = "410 S State St"
                    closest.zip_code = "84111"
                    closest.special_notes = ""
                else:
                    print("\n\n\ndelivered package 9 too early\n\n\n")

            # make sure won't exceed time specified
            temp_time = Time(self.trucks_time.hour, self.trucks_time.minute)
            temp_time.advance(distance / self.speed)
            if temp_time <= halt:
                self.deliver_package(closest, distance, undelivered)
                finished_time = self.trucks_time
            else:
                self.not_finished = False  # reset not_finished for next time called

            # if empty go to reload
            if not self.loaded_packages:
                self.return_to_hub(locations_data, at_hub, undelivered)

        return finished_time
