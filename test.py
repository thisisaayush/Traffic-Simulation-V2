import simpy
import networkx as nx
import geopy.distance
import random
class MapImplementation:
    generated_trucks = []

    def __init__(self, env):
        self.env = env
        self.name = "Truck-" + str(len(MapImplementation.generated_trucks) + 1)

    def simulate_traffic(self, coordinates, env): # first find the intersections and then implement traffic light properties for the intersectios.
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

        for node in MapImplementation.graph.nodes():
            if MapImplementation.graph.degree[node] > 2:
                intersections_list.append(node)

        for intersection in intersections_list:
            light_status = "red"

            while True:
                if light_status == "red":
                    print("Traffic light at intersection ", intersection, ": Red.")
                    yield env.timeout(10)
                    light_status == "green"

                elif light_status == "yellow":
                    print("Traffic light at intersection ", intersection, ": Yellow.")
                    yield env.timeout(5)
                    light_status == "red"

                elif light_status == "green":
                    print("Traffic light at intersection ",intersection, ": Green.")
                    yield env.timeout(2)
                    light_status = "red"
    def shortest_path(self, coordinates, start, end, speed, endpoints_coord):
        graph = nx.Graph()
        for coord_tuple in coordinates:
            for i in range(len(coord_tuple) - 1):
                edge_dist = geopy.distance.distance(coord_tuple[i], coord_tuple[i + 1]).km
                edge_time = round(edge_dist / speed * 3600, 2)
                graph.add_edge(coord_tuple[i], coord_tuple[i + 1], weight=edge_time)
        shortest_path_ = nx.shortest_path(graph, start, end, weight='weight')

        env = simpy.Environment()
        env.process(self.simulate_traffic(coordinates, env))

        travel_time = []
        total_time = []
        x = 0
        for i in range(len(shortest_path_) - 1):
            edge_dist = geopy.distance.distance(shortest_path_[i], shortest_path_[i + 1]).km
            edge_time = round(edge_dist / speed * 3600, 2)
            x = env.timeout(edge_time).value
            travel_time.append(edge_time)

        print("{:<20}{}{}".format("Travel time:", travel_time, " seconds."))
        print("{:<20}{}".format("Shortest path:", shortest_path_))
        print()

        return shortest_path_, travel_time

    def queue_truck(self, coordinates, endpoint, queue, endpoints_coord):
        yield self.env.timeout(5) # queues for 5 sec before entering.
        arrival_time = self.env.now
        print(f"{self.name} has queued at {endpoint} at {arrival_time} time.")
        queue.append(self)
        entry_time = 4 + arrival_time  # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} has entered the {endpoint} at {entry_time} time.")

        destinations = [coord for coord in endpoints_coord if coord != endpoint]
        destination = random.choice(destinations)
        print(f"{self.name} is traveling to {destination}.")

        shortest_path_, travel_time = self.shortest_path(coordinates, endpoint, destination, 50, endpoints_coord)
        MapImplementation.generated_trucks.append((self.name, destination))

    def generate_trucks(self, endpoint, queue, endpoints_coord):
        while True:
            yield self.env.timeout(10) # generates a truck in every 10 sec.
            truck = MapImplementation(self.env)
            self.env.process(truck.queue_truck(coordinates,endpoint, queue, endpoints_coord))

coordinates = [((10.1, 4.8), (9.0, 4.8), (7.4, 4.6), (4.2, 4.0)),
               ((9.8, 7.8), (9.1, 7.2), (7.3, 6.8), (4.2, 6.1), (3.2, 5.9), (1.2, 5.8)),
               ((9.0, 2.8), (9.0, 4.8), (9.1, 7.2), (9.1, 10.2)),
               ((7.2, 2.8), (7.4, 4.6), (7.3, 6.8), (7.5, 10.0), (7.5, 10.8)),
               ((2.7, 4.8), (3.2, 5.1), (4.2, 6.1), (6.0, 8.7), (6.5, 9.4), (7.5, 10.0), (7.5, 10.2)),
               ((3.4, 10.8), (3.2, 5.9), (3.2, 5.1), (3.1, 4.1)),
               ((3.1, 2.0), (3.1, 4.1), (4.2, 4.0), (7.8, 9.4), (9.1, 10.2), (8.9, 10.5)),
               ((1.5, 9.6), (6.0, 8.7), (6.5, 9.4))]

endpoints_coord = [(3.4, 10.8), (1.5, 9.6), (1.2, 5.8), (2.7, 4.8), (3.1, 2.0), (7.5, 10.8), (7.5, 10.2), (7.2, 2.8)
   , (8.9, 10.5), (10.1, 9.6), (9.8, 7.8), (10.1, 4.8), (9.0, 2.8)]

env = simpy.Environment()
map_impl = MapImplementation(env)

queue = []
for endpoint in endpoints_coord:
    env.process(map_impl.generate_trucks(endpoint, queue, endpoints_coord))
env.run(until=150)  # Run the simulation for 100 time units
