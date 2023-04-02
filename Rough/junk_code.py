''' Junk Code '''

'''
pygame for pointers. 
import pygame
import time
from rough import *

# initialize Pygame.
pygame.init()

# background image.
# background_image = pygame.image.load("map.jpg")

# set the dimensions of the screen.
screen_width = 600
screen_height = 600

# set the dimensions of each cell in the grid.
cell_size = 50

# set the number of rows and columns in the grid.
rows = 12
cols = 12

# endpoints colors.
colors = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)]

endpoints_coord = [(0.2, 1.1), (1.2, 5.2), (7.2, 11.2), (10.1, 9.4)]

dest_point = [(2.7, 7.2), (9.8, 4.2), (9.0, 9.2), (7.2, 9.2), (8.9, 1.0)]

# background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

screen = pygame.display.set_mode((screen_width, screen_height))

# draw row and column lines on the map.
for i in range(rows + 1):
    pygame.draw.line(screen, (50, 50, 50), (0, i * cell_size), (screen_width, i * cell_size))
for j in range(cols + 1):
    pygame.draw.line(screen, (50, 50, 50), (j * cell_size, 0), (j * cell_size, screen_height))

# screen.blit(background_image, (0, 0))

# draw the grid.
for row in range(rows):
    for col in range(cols):
        x = col * cell_size
        y = row * cell_size
        rect = pygame.Rect(x, y, cell_size, cell_size)
        pygame.draw.rect(screen, (50, 50, 50), rect, 1)

# draw the endpoint dots.
for i, coord in enumerate(endpoints_coord):
    x, y = int(coord[0] * cell_size), int(coord[1] * cell_size)
    color = colors[i % len(colors)]
    pygame.draw.circle(screen, color, (x, y), 8)


# define a function to move a point along a path
def move_point(start, end):
    # convert start and end points to pixel coordinates
    start_x, start_y = int(start[0] * cell_size), int(start[1] * cell_size)
    end_x, end_y = int(end[0] * cell_size), int(end[1] * cell_size)

    # calculate the step size and direction
    dx = (end_x - start_x) / 15
    dy = (end_y - start_y) / 15

    # move the point along the path
    for i in range(100):
        x = start_x + i * dx
        y = start_y + i * dy

        # draw the point on the screen
        pygame.draw.circle(screen, (255, 0, 0), (int(x), int(y)), 4)
        pygame.display.flip()

        # pause briefly to create the illusion of motion
        time.sleep(0.25)


Junk 2

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
    def simulate_traffic(self, coordinates, env): # first find the intersections and then implement traffic light properties for the intersectios.
        # finds the intersections of for the given road-highway network- coordinates.
        for i in range(len(coordinates)):
            for j in range(len(coordinates[i])):
                MapImplementation.graph.add_node(coordinates[i][j])

        for i in range(len(coordinates)):
            for j in range(len(coordinates[i]) - 1):
                MapImplementation.graph.add_edge(coordinates[i][j], coordinates[i][j + 1])

        for i in range(len(coordinates) - 1):
            for j in range(len(coordinates[i])):
                for k in range(len(coordinates[i + 1])):
                    if coordinates[i][j] == coordinates[i + 1][k]:
                        MapImplementation.graph.add_edge(coordinates[i][j], coordinates[i + 1][k])

        intersections_list = []

        # make a list of intersected node.
        for node in MapImplementation.graph.nodes():
            if MapImplementation.graph.degree[node] > 2:
                intersections_list.append(node)

        # intersected list will be used to simulate the traffic light.
        for intersection in intersections_list:
            light_status = "red"

            while True:
                if light_status == "red":
                    yield env.timeout(150)
                    light_status == "green"

                elif light_status == "yellow":
                    yield env.timeout(75)
                    light_status == "red"

                elif light_status == "green":
                    yield env.timeout(50)
                    light_status = "red"

    def shortest_path(self, coordinates, start, end, speed): # finds the shortest path for the given coordinates between the start and the end point.
        graph = nx.Graph()


        for coord_tuple in coordinates:
            for i in range(len(coord_tuple) - 1):
                edge_dist = geopy.distance.distance(coord_tuple[i], coord_tuple[i + 1]).km
                edge_time = round(edge_dist / speed, 2)
                graph.add_edge(coord_tuple[i], coord_tuple[i + 1], weight=edge_time)
        shortest_path_ = nx.shortest_path(graph, start, end, weight='weight')

        env = simpy.Environment()
        # simulates the traffic if the path come across the intersection.
        env.process(self.simulate_traffic(coordinates, env))

        travel_time = []
        distance_list = []
        x = 0
        for i in range(len(shortest_path_) - 1):
            edge_dist = geopy.distance.distance(shortest_path_[i], shortest_path_[i + 1]).km
            edge_time = round(edge_dist / speed * 3600, 2)
            env.timeout(edge_time)
            travel_time.append(edge_time)
            x = round(edge_dist, 2)
            distance_list.append(x)

        print("{:<20}{}{}".format("Travel time:", travel_time, " seconds."))
        print("{:<20}{}".format("Shortest path:", shortest_path_))
        print("{:<20}{}".format("Distance List:", distance_list, " km."))
        print()
        return shortest_path_, travel_time

    def queue_truck(self, coordinates, endpoint, queue, endpoints_coord): # queues truck at endpoints.
        yield self.env.timeout(5) # queues for 5 sec before entering.
        arrival_time = self.env.now
        print(f"{self.name} has queued at {endpoint} at {arrival_time} time.")
        queue.append(self)
        entry_time = 4 + arrival_time  # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} has entered the {endpoint} at {entry_time} time.")

        destinations = [x for x in endpoints_coord if x != endpoint]
        destination = random.choice(destinations)
        print(f"{self.name} destination is {destination}.")

        shortest_path_, travel_time = self.shortest_path(coordinates, endpoint, destination, 50)
        MapImplementation.generated_trucks.append((self.name, destination))

    def generate_trucks(self, endpoint, queue, endpoints_coord): # generates trucks at endpoints.
        while True:
            yield self.env.timeout(10) # generates a truck in every 10 sec.
            truck = MapImplementation(self.env) #
            self.env.process(truck.queue_truck(coordinates,endpoint, queue, endpoints_coord))

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

queue = []
for endpoint in endpoints_coord:
    env.process(map_impl.generate_trucks(endpoint, queue, endpoints_coord))
env.run(until=50)  # Run the simulation for 50 time units

y = MapImplementation(env)
z = y.convert_coordinate(coordinates)
print(z)


# the coordinates of turtle are weird, google it. It is moving but not the way it is expected to move.
# shortest_path = [(8.0, 224.0), (-80.0, 224.0), (-208.0, 208.0), (-464.0, 160.0)]
# x = MapImplementation(env)
# x.visualize_truck(shortest_path)
#

Junk 3 pygame-move point
import pygame
import time

class Grid:
    def __init__(self, rows, cols, cell_size, colors):
        # initialize Pygame.
        pygame.init()

        # background image.
        self.background_image = pygame.image.load("map.jpg")

        # set the dimensions of the screen.
        self.screen_width = 600
        self.screen_height = 600

        # set the dimensions of each cell in the grid.
        self.cell_size = cell_size

        # set the number of rows and columns in the grid.
        self.rows = rows
        self.cols = cols

        # endpoints colors.
        self.colors = colors

        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # draw row and column lines on the map.
        for i in range(rows + 1):
            pygame.draw.line(self.screen, (50, 50, 50), (0, i * cell_size), (self.screen_width, i * cell_size))
        for j in range(cols + 1):
            pygame.draw.line(self.screen, (50, 50, 50), (j * cell_size, 0), (j * cell_size, self.screen_height))

        self.screen.blit(self.background_image, (0, 0))

        # draw the grid.
        for row in range(rows):
            for col in range(cols):
                x = col * cell_size
                y = row * cell_size
                rect = pygame.Rect(x, y, cell_size, cell_size)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)

    # define a function to move a point along a path
    def move_point(self, shortest_path):
        # convert start point to pixel coordinates
        start_x, start_y = int(shortest_path[0][0] * self.cell_size), int(shortest_path[0][1] * self.cell_size)

        # move the point along the path
        for i in range(1, len(shortest_path)):
            # convert end point to pixel coordinates
            end_x, end_y = int(shortest_path[i][0] * self.cell_size), int(shortest_path[i][1] * self.cell_size)

            # calculate the step size and direction
            dx = (end_x - start_x) / 15
            dy = (end_y - start_y) / 15

            # draw the line on the screen
            for j in range(100):
                x = start_x + j * dx
                y = start_y + j * dy

                pygame.draw.line(self.screen, (255, 0, 0), (start_x, start_y), (x, y), 1)
                pygame.display.flip()

                # pause briefly to create the illusion of motion
                time.sleep(0.05)

            # set the new start point
            #start_x, start_y = end_x, end_y


grid = Grid(12, 12, 50, (128,0,0))
shortest_path = [(1.8, 5.6), (2.5,5.5), (4.2, 5.5), (7.2, 5.3), (8.8, 5.2), (10.1, 5.1)]
grid.move_point(shortest_path)



'''

