import simpy
import networkx as nx
import geopy.distance
import random
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
                    yield env.timeout(10)
                    light_status == "green"

                elif light_status == "yellow":
                    yield env.timeout(5)
                    light_status == "red"

                elif light_status == "green":
                    yield env.timeout(2)
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

    def queue_truck(self, coordinates, endpoint, queue, endpoints_coord):
        yield self.env.timeout(5) # queues for 5 sec before entering.
        arrival_time = self.env.now
        print(f"{self.name} has queued at {endpoint} at {arrival_time} time.")
        queue.append(self)
        entry_time = 4 + arrival_time  # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} has entered the {endpoint} at {entry_time} time.")

        destinations = [x for x in endpoints_coord if x != endpoint]
        destination = random.choice(destinations)
        print(f"{self.name} is traveling to {destination}.")

        shortest_path_, travel_time = self.shortest_path(coordinates, endpoint, destination, 50)
        MapImplementation.generated_trucks.append((self.name, destination))

    def generate_trucks(self, endpoint, queue, endpoints_coord):
        while True:
            yield self.env.timeout(10) # generates a truck in every 10 sec.
            truck = MapImplementation(self.env) #
            self.env.process(truck.queue_truck(coordinates,endpoint, queue, endpoints_coord))

coordinates = [((10.1, 4.8), (9.0, 4.8), (7.4, 4.6), (4.2, 4.0)),
               ((9.8, 7.8), (9.1, 7.2), (7.3, 6.8), (4.2, 6.1), (3.2, 5.9), (1.2, 5.8)),
               ((9.0, 2.8), (9.0, 4.8), (9.1, 7.2), (9.1, 10.2)),
               ((7.2, 2.8), (7.4, 4.6), (7.3, 6.8), (7.5, 10.0), (7.5, 10.8)),
               ((2.7, 4.8), (3.2, 5.1), (4.2, 6.1), (6.0, 8.7), (6.5, 9.4), (7.5, 10.0), (7.5, 10.2)),
               ((3.4, 10.8), (3.2, 5.9), (3.2, 5.1), (3.1, 4.1)),
               ((3.1, 2.0), (3.1, 4.1), (4.2, 4.0), (7.8, 9.4), (9.1, 10.2), (8.9, 10.5)),
               ((1.5, 9.6), (6.0, 8.7), (6.5, 9.4), (7.8,9.4), (10.1,9.6))]

endpoints_coord = [(3.4, 10.8), (1.5, 9.6), (1.2, 5.8), (2.7, 4.8), (3.1, 2.0), (7.5, 10.8), (7.5, 10.2), (7.2, 2.8)
   , (8.9, 10.5), (10.1, 9.6), (9.8, 7.8), (10.1, 4.8), (9.0, 2.8)]

env = simpy.Environment()
map_impl = MapImplementation(env)
queue = []
for endpoint in endpoints_coord:
    env.process(map_impl.generate_trucks(endpoint, queue, endpoints_coord))
env.run(until=50)  # Run the simulation for 100 time units



