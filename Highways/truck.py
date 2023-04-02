import simpy
import random
import geopy.distance

class Truck:
    def __init__(self, env, name, model, speed):
        self.env = env
        self.name = name
        self.model = model
        self.speed = speed

    def vehicle_size(self, l,b,h):
        return l * b * h

    # calculate the total distance base on intersection.
    def total_distance(self, road_segements):  # road segments is a parameter that consists of list of tuples.
        total_distance = 0
        start_position = 0
        end_position = 0

        for i, segment in enumerate(road_segements):
            if i == 0:
                start_position = segment[0]
            else:
                start_position = end_position

            end_position = segment[1]
            distance = geopy.distance.distance(start_position, end_position).km
            total_distance += distance

        return total_distance

    # road_segments: has the co-ordinates of road segments in list-tuple format.
    def move_truck(self, env, road_segments, intersections_point): #move along-ness from point 1 to point 2.
        travel_time = 0
        for segment in road_segments:
            start_position = segment[0]
            end_position = segment[1]

            distance = geopy.distance.distance(start_position, end_position).km
            travel_time += distance / self.speed

            yield env.timeout(travel_time)

            if end_position in intersections_point: # traffic signal.
                wait_time = 00.5 # constant wait time at intersection despite lights color.
                travel_time += wait_time
                yield env.timeout(wait_time)

            if road_segments[-1] == (start_position,end_position):
                return("Reached Destination. Time Required: {}.".format(travel_time))

    def fuel_consumption(self, distance_to_travel, fuel_efficiency): # fuel_efficiency- miles per gallon
        return distance_to_travel / fuel_efficiency # total fuel required to cover the distance.

    def maintenance_cost(self, miles_driven, cost_per_mile):
        return miles_driven * cost_per_mile

    def max_distance(self, tank_size, per_gallon_capacity):
        return tank_size * per_gallon_capacity

class SemiTruck(Truck):
    def __init__(self, env, name, model, speed, axles, num_dirvers, trailer_status = False ):
        super().__init__(env, name, model, speed)
        self.axles = axles
        self.num_drivers = num_dirvers
        self.trailer_status = trailer_status  # not attached.

    def trailer(self):
        if self.trailer_status == True:
            return "Trailer Attached."

        return "Trailer Not Attached."

    def num_drivers(self, num_semi_trucks, driving_hours_per_day):
        num_drivers = num_semi_trucks # if the driver driving hours is less than or equal to 10.

        if driving_hours_per_day > 10:
            num_drivers = 2 * num_semi_trucks

        return num_drivers

    def trailer_capacity(self,capacity):
        factor = 0 # factor will allow to estimate the total weight a truck can carry.
        weight_capacity = 0
        if self.axles == 2:
            factor = 2.5
        elif self.axles == 3:
            factor = 3.5
        elif self.axles == 5:
            factor = 5.5
        else:
            factor = 4.0

        weight_capacity = capacity * factor
        return weight_capacity

class BoxTruck(Truck):
    def __init__(self, env, name, model, speed, load_per_volume):
        super().__init__(env, name, model, speed)
        self.load = load_per_volume
        self.cargo_list = []

    # allows the labor to keep the track of the cargo inventory in the box truck.
    def add_list(self, item):
        self.cargo_list.append(item)

class DeckTruck(Truck):
    def __init__(self, env, name, model, speed, length, breadth, ramp_length):
        super().__init__(env, name, model, speed)
        self.deck_area = length * breadth
        self.ramp_length = ramp_length

    def ramp_access(self, length):
        if length == self.ramp_length - 5:
            return "Ramp is Extendable."

        else:
            return "Ramp is not Extendable. It is either short or long then requried length."

# create the simulation environment
env = simpy.Environment()

"""                   Semi Truck                """
semitruck1 = SemiTruck(env, "Semi Truck 1", "Semi Model 1", 55, 3, 2, True)
print(semitruck1.vehicle_size(15,5,6))
print(semitruck1.trailer())

fuel_consumption = semitruck1.fuel_consumption(200, 20)
print("Fuel Consumption: ", fuel_consumption, " gallons.")

semitruck2 = SemiTruck(env, "Semi Truck 2", "Semi Model 2", 60, 4, 2, False)
print(semitruck2.trailer())
print(semitruck2.trailer_capacity(25000))
print()
"""                   Box Truck                 """
boxtruck0 = BoxTruck(env, "Box Truck 1", "Model 1", 60, 85)
boxtruck1 = BoxTruck(env, "Box Truck 1", " Box Model 1", 58, 200)
print("Box Truck 1 load capacity: ", boxtruck1.load)
print(f"{boxtruck1.name} model is  {boxtruck1.model}.")

boxtruck2 = BoxTruck(env, "Box Truck 2", " Box Model 2", 65, 175)
print("Box Truck Size: ",boxtruck2.vehicle_size(7,3,2.4), "meter cube.")

print()
"""                   Deck Truck                """
decktruck1 = DeckTruck(env, "Deck Truck 1", "Deck Model 1", 54, 5, 2.5, 1.25)
print(f"{decktruck1.name} model is {decktruck1.model}.")
decktruck2 = DeckTruck(env, "Deck Truck 2", "Deck Model 2", 50, 5.2, 2.2, 1.2)
print(f"{decktruck2.name} {decktruck2.ramp_access(1.0)}")
print("Fuel Consumption: ",decktruck2.fuel_consumption(500, 40), " gallons.")


env.run(until=100)

road_segments = [ ((50.12,62.02),(50.15,62.04)),
                  ((50.15,62.04),(50.16,62.08)),
                  ((50.16,62.08),(50.21,62.14)),
                  ((50.21,62.14),(50.23,62.17)),
                  ((50.23,62.17),(50.55,62.35))
                  ]
intersections_point = [
                 ((50.15,62.04),(50.16,62.08)),
                 ((50.23,62.17),(50.55,62.35))
                ]

print(f"Total Distance: {boxtruck0.total_distance(road_segments):.2f} km")

