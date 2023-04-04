import simpy
import networkx as nx
import geopy.distance
import random
import turtle
class MapImplementation:
    generated_trucks = []
    count = 0
    def __init__(self, env):
        MapImplementation.count += 1
        self.env = env
        self.name = "Truck-{}".format(MapImplementation.count)
    def convert_coordinate(self, coordinates):
        turtle_coordinates = []

        for path in coordinates:
            turtle_path = []
            for coord in path:
                py_x, py_y = coord
                turt_x = round((-py_x + 10) * -80, 2)
                turt_y = round((-10 + py_y) * -80, 2)
                turtle_path.append((turt_x, turt_y))
            turtle_coordinates.append(turtle_path)

        return turtle_coordinates

    def visualize_truck(self, shortest_path): # turtle to visualize the trucks traversing the xy plane.
        # create a turtle screen.
        turtle.bgpic("map.jpg")
        screen = turtle.Screen()
        screen.bgcolor("grey")

        # truck path-turtle.
        truck_path = turtle.Turtle()
        truck_path.speed(1)
        truck_path.pensize(2)
        truck_path.color("blue")

        # the path truck will follow.
        for i in range(len(shortest_path) - 1):
            start_coord = shortest_path[i]
            end_coord = shortest_path[i + 1]
            start_x, start_y = start_coord
            end_x, end_y = end_coord
            truck_path.penup()
            truck_path.goto(start_x, start_y)
            truck_path.pendown()
            truck_path.goto(end_x, end_y)

        turtle.exitonclick()

coordinates = [((10.1, 7.2), (9.0, 7.2), (7.4, 7.4), (4.2, 8.0)),
               ((9.8, 4.2), (9.1, 4.8), (7.3, 5.2), (4.2, 5.9), (3.2, 6.1), (1.2, 6.2)),
               ((9.0, 9.2), (9.0, 7.2), (9.1, 4.8), (9.1, 1.8)),
               ((7.2, 9.2), (7.4, 7.4), (7.3, 5.2), (7.5, 2.0), (7.5, 1.2)),
               ((2.7, 7.2), (3.2, 6.9), (4.2, 5.9), (6.0, 3.3), (6.5, 2.6), (7.5, 2.0), (7.5, 1.8)),
               ((3.4, 1.2), (3.2, 6.1), (3.2, 6.9), (3.1, 7.9)),
               ((3.1, 10.0), (3.1, 7.9), (4.2, 8.0), (7.8, 2.6), (9.1, 1.8), (8.9, 1.5)),
               ((1.5, 2.4), (6.0, 3.3), (6.5, 2.6), (7.8,2.6), (10.1, 2.4))]

endpoints_coord = [(3.4, 1.2), (1.5, 2.4), (1.2, 6.2), (2.7, 7.2), (3.1, 10.0), (7.5, 1.2), (7.5, 1.8), (7.2, 9.2)
   , (8.9, 1.5), (10.1, 2.4), (9.8, 4.2), (10.1, 7.2), (9.0, 9.2)]

env = simpy.Environment()
map_impl = MapImplementation(env)

y = MapImplementation(env)
z = y.convert_coordinate(coordinates)
print(z)

# the coordinates of turtle are weird, google it. It is moving but not the way it is expected to move.
shortest_path = [(-16.0, 464.0), (-72.0, 416.0), (-216.0, 384.0), (-464.0, 328.0), (-544.0, 312.0), (-704.0, 304.0)]
x = MapImplementation(env)
x.visualize_truck(shortest_path)
