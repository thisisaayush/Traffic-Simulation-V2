import simpy
import networkx as nx
import geopy.distance
import random
'''
Don't delete this file. Some concepts can you used later. 
'''
class MapImplementation:
    count = 0
    generated_trucks = []
    graph = nx.Graph()
    def __init__(self, env="unknown", speed="unknown"):
        MapImplementation.count += 1
        self.env = env
        self.name = "Truck {}".format(MapImplementation.count)
        self.speed = speed

        for road in coordinates:
            for i in range(len(road)-1):
                self.graph.add_edge(road[i], road[i+1])

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

    def shortest_path(self, coordinates, start, end, speed):
        graph = nx.Graph()
        for coord_tuple in coordinates:
            for i in range(len(coord_tuple) - 1):
                edge_dist = geopy.distance.distance(coord_tuple[i], coord_tuple[i + 1]).km
                edge_time = round(edge_dist / speed * 3600, 2)
                graph.add_edge(coord_tuple[i], coord_tuple[i + 1], weight=edge_time)
        shortest_path = nx.shortest_path(graph, start, end, weight='weight')

        env = simpy.Environment()
        env.process(self.simulate_traffic(coordinates, env))

        travel_time = []
        total_time = []
        x = 0
        for i in range(len(shortest_path) - 1):
            edge_dist = geopy.distance.distance(shortest_path[i], shortest_path[i + 1]).km
            edge_time = round(edge_dist / speed * 3600, 2)
            x = env.timeout(edge_time).value
            travel_time.append(edge_time)

        print("{:<20}{}{}".format("Travel time:", travel_time, " seconds."))
        print("{:<20}{}".format("Shortest path:", shortest_path))
        return shortest_path

    def queue_truck(self, endpoint, queue):
        yield self.env.timeout(5) # queues for 5 sec before entering.
        arrival_time = self.env.now
        print(f"{self.name} has queued the {endpoint} at {arrival_time} time.")
        queue.append(self)
        entry_time = 4 + arrival_time  # 4 time units is a time needed to enter a road/highway after queue time.
        print(f"{self.name} has entered the {endpoint} at {entry_time} time.\n")
        queue.pop(0)
        MapImplementation.generated_trucks.append((self.name, endpoint))

    def generate_trucks(self, endpoint, queue):
        while True:
            yield env.timeout(10) # generates a truck in every 10 sec.
            truck = MapImplementation(self.env)
            env.process(truck.queue_truck(endpoint, queue))



class Truck:
    count = 0
    def __init__(self, env, start, end, speed, queue):
        Truck.count += 1
        self.env = env
        self.name = f"Truck {Truck.count}"
        self.start = start
        self.end = end
        self.speed = speed
        self.queue = queue



if __name__ == "__main__":
    coordinates = [((10.1, 4.8), (9.0, 4.8), (7.4, 4.6), (4.2, 4.0)),
                   ((9.8, 7.8), (9.1, 7.2), (7.3, 6.8), (4.2, 6.1), (3.2, 5.9), (1.2, 5.8)),
                   ((9.0, 2.8), (9.0, 4.8), (9.1, 7.2), (9.1, 10.2)),
                   ((7.2, 2.8), (7.4, 4.6), (7.3, 6.8), (7.5, 10.0), (7.5, 10.8)),
                   ((2.7, 4.8), (3.2, 5.1), (4.2, 6.1), (6.0, 8.7), (6.5, 9.4), (7.5, 10.0), (7.5, 10.2)),
                   ((3.4, 10.8), (3.2, 5.9), (3.2, 5.1), (3.1, 4.1)),
                   ((3.1, 2.0), (3.1, 4.1), (4.2, 4.0), (7.8, 9.4), (9.1, 10.2), (8.9, 10.5)),
                   ((1.5, 9.6), (6.0, 8.7), (6.5, 9.4))]

    endpoints = {"End Point 1": [], "End Point 2": [], "End Point 3": [], "End Point 4": [], "End Point 5": [],
                 "End Point 6": [], "End Point 7": [], "End Point 8": [], "End Point 9": [], "End Point 10": [],
                 "End Point 11": [], "End Point 12": [],
                 "End Point 13": []}  # the endpoint will queue list of truck at the endpoint declared in there.

    endpoints_coord = [(3.4, 10.8), (1.5, 9.6), (1.2, 5.8), (2.7, 4.8), (3.1, 2.0), (7.5, 10.8), (7.5, 10.2), (7.2, 2.8)
       , (8.9, 10.5), (10.1, 9.6), (9.8, 7.8), (10.1, 4.8), (9.0, 2.8)]

    map = MapImplementation(coordinates)

    env = simpy.Environment()

    print("\n")
    for endpoint in endpoints:
        generate_truck = MapImplementation(env)
        env.process(generate_truck.generate_trucks(endpoint, endpoints[endpoint]))
    env.run(until=50)

    for i, endpoint in enumerate(endpoints):
        print("{:<15}{}{}".format(endpoint, "coordinates: ", endpoints_coord[i]), end=" ")
        truck_ = []

        for truck, endpoint_name in MapImplementation.generated_trucks:
            if endpoint_name == endpoint:
                truck_.append(truck)

        print(truck_)
    print()

    truck_routes = [
        {'start': (9.0,2.8), 'end': (1.2,5.8), 'speed': 50},
        {'start': (3.4,10.8), 'end': (1.2,5.8), 'speed': 60},
        {'start': (9.8,7.8), 'end': (7.2,2.8), 'speed': 65}
    ]

    for route in truck_routes:
        start = route['start']
        end = route['end']
        speed = route['speed']

        shortest_path = map.shortest_path(coordinates, start, end, speed)
        print()


    def traverse_trucks(endpoints, endpoints_coord, speed):
        all_trucks = []
        for key in endpoints.keys():
            trucks = endpoints[key]
            for truck in trucks:
                all_trucks.append((truck, key))

        coords_traversed = []
        time_taken = []

        for truck, start in all_trucks:
            for end in endpoints.keys():
                if end != start:
                    shortest_path = shortest_path_algorithm(endpoints_coord, start, end, speed)
                    for i in range(len(shortest_path) - 1):
                        edge_dist = geopy.distance.distance(shortest_path[i], shortest_path[i + 1]).km
                        edge_time = round(edge_dist / speed * 3600, 2)
                        coords_traversed.extend(shortest_path[i:i + 2])
                        time_taken.append(edge_time)

        return coords_traversed, time_taken


    def shortest_path_algorithm(coordinates, start, end, speed):
        graph = nx.Graph()
        for coord_tuple in coordinates:
            for i in range(len(coord_tuple) - 1):
                edge_dist = geopy.distance.distance(coord_tuple[i], coord_tuple[i + 1]).km
                edge_time = round(edge_dist / speed * 3600, 2)
                graph.add_edge(coord_tuple[i], coord_tuple[i + 1], weight=edge_time)
        shortest_path = nx.shortest_path(graph, start, end, weight='weight')
        return shortest_path



    coords_traversed, time_taken = traverse_trucks(endpoints, endpoints_coord, 50)

    print("Coordinates traversed: ", coords_traversed)
    print("Time taken for each truck: ", time_taken)
'''
  start = (10.1, 4.8)
        end = (7.5, 10.8)
        speed = 50
        path = map.shortest_path(coordinates, (10.1, 4.8), (7.5, 10.8), 60)
        print("{:<20}{}".format("Coordinates: ", path))
'''