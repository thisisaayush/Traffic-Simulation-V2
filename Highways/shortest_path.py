import geopy.distance
import networkx as nx
import simpy


class Find_Path:
    def __init__(self):
        self.graph = nx.Graph()
        self.traversed_coordinates = []
        self.traversed_distances = []

    def add_edges(self, edges):
        for edge in edges:
            for i in range(len(edge) - 1):
                node_from, node_to = edge[i], edge[i+1]
                distance = geopy.distance.distance(node_from, node_to).km
                self.graph.add_edge(node_from, node_to, weight=distance)

    def shortest_distance(self, start, end):
        shortest_path = nx.shortest_path(self.graph, source=start, target=end, weight="weight")
        self.traversed_coordinates = shortest_path
        self.traversed_distances = [self.graph.edges[i,j]["weight"] for i, j in zip(shortest_path[:-1], shortest_path[1:])]
        total_distance = sum(self.traversed_distances)

        return f"{total_distance:.2f}"

    def traversed_coordinate(self):
        return self.traversed_coordinates

    @property
    def traversed_distance(self):
        distance_list = []
        for distance in self.traversed_distances:
            distance_list.append(round(distance, 2))

        return distance_list
def find_path(coordinates, start, end):
    edges = []

    for x in coordinates:
        edges.append(x)

    distance_1 = Find_Path()
    distance_1.add_edges(edges)

    distance_ = distance_1.shortest_distance(start, end)
    trav_distances = distance_1.traversed_distance
    trav_coord = distance_1.traversed_coordinates


    return distance_, trav_distances, trav_coord

def simulate_truck(coordinates, start, end, speed):
    distance_, trav_distances, trav_coord = find_path(coordinates, start, end)
    x = float(distance_)
    time = round(x / (speed / 3600), 2)

    env = simpy.Environment()
    truck_process = env.process(truck_simulation(env, trav_coord, trav_distances, speed))

    env.run(until=truck_process)

    truck_status = truck_process.value
    return truck_status.locations_list, truck_status.times_list

def truck_simulation(env, coordinates_list, distance_list, speed):
    location_status = coordinates_list[0]
    time_status = 0

    truck_status = Truck_Status(locations_list=[location_status], times_list=[time_status])

    for i, distance in enumerate(distance_list):
        x = float(distance)
        time_to_travel_distance = round(x / (speed / 3600), 2)

        yield env.timeout(time_to_travel_distance)

        location_status = coordinates_list[i + 1]
        time_status += time_to_travel_distance

        truck_status.locations_list.append(location_status)
        truck_status.times_list.append(time_status)

    return truck_status

class Truck_Status:
    def __init__(self, locations_list=None, times_list=None):
        self.locations_list = locations_list
        self.times_list = times_list

# co-ordinates of roads & highways.
coordinates = [((10.1,4.8), (9.0,4.8), (7.4,4.6), (4.2,4.0)),
               ((9.8,7.8), (9.1,7.2), (7.3,6.8), (4.2,6.1), (3.2,5.9), (1.2,5.8)),
               ((9.0,2.8), (9.0,4.8), (9.1,7.2), (9.1,10.2)),
               ((7.2,2.8),(7.4,4.6), (7.3,6.8), (7.5,10.0), (7.5,10.8)),
               ((2.7,4.8), (3.2,5.1), (4.2,6.1), (6.0,8.7), (6.5,9.4), (7.5,10.0), (7.5,10.2)),
               ((3.4,10.8), (3.2,5.9), (3.2,5.1),(3.1,4.1)),
               ((3.1,2.0), (3.1,4.1), (4.2,4.0), (7.8,9.4), (9.1,10.2),(8.9,10.5)),
               ((1.5,9.6), (6.0,8.7),(6.5,9.4), (7.8,9.4), (10.1,9.6))]

start1 = (10.1,4.8)
end1 = (3.4,10.8)
speed1 = 65

distance1, distances_list1, coordinates_list1 = find_path(coordinates, start1, end1)
locations1, times1 = simulate_truck(coordinates, start1, end1, speed1)


from geopy.distance import geodesic

# ...

def shortest_path(coordinates, start, end, speed):
    graph = nx.Graph()
    for coord_tuple in coordinates:
        for i in range(len(coord_tuple)-1):
            edge_dist = geodesic(coord_tuple[i], coord_tuple[i+1]).km
            edge_time = round(edge_dist/speed * 3600, 2)
            graph.add_edge(coord_tuple[i], coord_tuple[i+1], weight=edge_time)
    shortest_path = nx.shortest_path(graph, start, end, weight='weight')
    return shortest_path

def simulate_path(coordinates, start, end, speed, env):
    path = shortest_path(coordinates, start, end, speed)
    current_location = path[0]
    travel_times = []
    for next_location in path[1:]:
        edge_dist = geodesic(current_location, next_location).km
        edge_time = round(edge_dist/speed * 3600, 2)
        travel_times.append(edge_time)
        yield env.timeout(edge_time)
        current_location = next_location
    return travel_times

print("{:<20}{}".format("Distance List: ", distances_list1))
print("{:<20}{}".format("Co-ordinates List: ", coordinates_list1))
print("{:<20}{}".format("Locations List: ", locations1))
print("{:<20}{}".format("Times List: ", times1))
