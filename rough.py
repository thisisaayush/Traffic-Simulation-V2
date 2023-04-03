import geopy.distance
import simpy
import networkx as nx
import random
class Roadways:
    road_count = 0
    def __init__(self, nodes, endpoints):
        Roadways.road_count += 1
        self.name = f"Road-{Roadways.road_count}"
        self.nodes = nodes # list of a road network.
        #self.road_segments = nodes_distance().node_segment(self.nodes) # returns the distance of between given two nodes.
        self.endpoints = endpoints
class Highways:
    highway_count = 0
    def __init__(self, nodes, endpoints): # nodes: list of a highway network.
        Highways.highway_count += 1
        self.name = f"Highway-{Highways.highway_count}"
        self.nodes = nodes
        #self.highways_segments = nodes_distance().node_segment(self.nodes)
        self.on_off_ramp = 5
        self.endpoints = endpoints # keeps endpoints list of tuples of coord of roads or highways.
        self.endpoints = endpoints
class Intersections:
    def __init__(self):
        self.intersection = []

    def all_nodes(self, *roads):
        coordinates = []
        for road in roads:
            coordinates.append(road.nodes) # creates list ( of list) of tuples for a network.

        return coordinates
    def shortest_path(self, *roads, speed, start, end):
        graph = nx.Graph()
        travel_time = []
        distance_list = []

        coordinates = self.all_nodes(*roads)

        for coord_list in coordinates:
            for i in range(len(coord_list) - 1):
                edge_dist = geopy.distance.distance(coord_list[i], coord_list[i + 1]).km
                edge_time = round(edge_dist / speed, 2)
                graph.add_edge(coord_list[i], coord_list[i + 1], weight=edge_time)
        shortest_path_ = nx.shortest_path(graph, start, end, weight='weight')
        for i in range(len(shortest_path_) - 1):
            edge_dist = round(geopy.distance.distance(shortest_path_[i], shortest_path_[i + 1]).km,2)
            edge_time = round(edge_dist / speed * 3600, 2)
            travel_time.append(edge_time)
            distance_list.append(edge_dist)

        print("{:<20}{}{}".format("Travel time:", travel_time, " seconds."))
        print("{:<20}{}".format("Shortest path:", shortest_path_))
        print("{:<20}{}{}".format("Distance List:", distance_list, " km."))
        #return shortest_path_, travel_time
class Truck(Roadways):
    truck_count = 0
    def __init__(self, env, speed):
        Truck.truck_count += 1
        self.env = env
        self.name = f"Truck-{Truck.truck_count}"
        self.speed = speed
        self.trucks_generated = []

    def generate_trucks(env, roadways, until):

        while True:
            yield env.timeout(5)  # queues for 5 sec before entering.
            truck = Truck(env, 55)
            truck.trucks_generated.append(truck)
            arrival_time = env.now
            for endpoint in roadways.endpoints:
                print(f"{truck.name} is queued at endpoints {endpoint} of a road {roadways.name} at {env.now} time.")
                entry_time = 4 + arrival_time  # 4 time units is a time needed to enter a road/highway after queue time.
                print(f"{truck.name} has entered the {endpoint} at {entry_time} time.")

            # dest = random.choice(endpoints_coord)
            # shortest_route = Intersections().shortest_path(roadways, speed=truck.speed, start=roadways.endpoints, end=dest)

            if env.now >= until:
                break



road1 = Roadways([(10.1, 7.2),(9.0, 7.2), (7.4, 7.4), (4.2, 8.0)], [(10.1, 7.2)])
road2 = Roadways([(9.8, 4.2), (9.1, 4.8), (7.3, 5.2), (4.2, 5.9), (3.2, 6.1), (1.2, 6.2)], [(9.8, 4.2), (1.2, 6.2)])
road3 = Roadways([(9.0, 9.2), (9.0, 7.2), (9.1, 4.8), (9.1, 1.8)], [(9.0, 9.2)])
road4 = Roadways([(7.2, 9.2), (7.4, 7.4), (7.3, 5.2), (7.5, 2.0), (7.5, 1.2)], [(7.2, 9.2), (7.5, 1.2)])
road5 = Roadways([(2.7, 7.2), (3.2, 6.9), (4.2, 5.9), (6.0, 3.3), (6.5, 2.6), (7.7, 2.0), (7.5, 1.8)], [(2.7, 7.2), (7.7, 1.8)])
road6 = Roadways([(3.1, 7.9), (3.2, 6.9), (3.2, 6.1), (3.4, 1.2)], [(3.4, 1.2)])
highway1 = Highways([(3.1, 10.0), (3.1, 7.9), (4.1, 4.0), (7.8, 2.6), (9.1, 1.8), (8.9, 1.5)], [(3.1, 10.0), (8.9, 1.5)])
highway2 = Highways([(1.5, 2.4), (6.0, 3.3), (6.5, 2.6), (7.8, 2.6), (10.1, 2.4)], [(1.5, 2.4), (10.1, 2.4)])

# env = simpy.Environment()
# # generate trucks for each road.
# for roadways in [road1, road2, road3, road4, road5, road6, highway1, highway2]:
#     env.process(Truck.generate_trucks(env, roadways, 150))
#
# env.run(until=50)

x = Intersections()
x.shortest_path(road1, road2, road3, road4, road5, road6, highway1, highway2, start=(10.1, 7.2), end=(9.8, 4.2), speed=55)

# endpoints_list = []
#
# for x in [road1, road2, road3]:
#     endpoints_list.extend(x.endpoints)
# print(endpoints_list)