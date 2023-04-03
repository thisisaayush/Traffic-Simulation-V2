''' This is the final update. '''
import geopy.distance
import simpy
import networkx as nx

class Roadways:
    road_count = 0
    def __init__(self, nodes, endpoints):
        Roadways.road_count += 1
        self.name = f"Road-{Roadways.road_count}"
        self.nodes = nodes # list of a road network.
        self.road_segments = nodes_distance().node_segment(self.nodes) # returns the distance of between given two nodes.
        self.endpoints = endpoints
class Highways:
    highway_count = 0
    def __init__(self, nodes, endpoints): # nodes: list of a highway network.
        Highways.highway_count += 1
        self.name = f"Highway-{Highways.highway_count}"
        self.nodes = nodes
        self.highways_segments = nodes_distance().node_segment(self.nodes)
        self.on_off_ramp = 5
        self.endpoints = endpoints # keeps endpoints list of tuples of coord of roads or highways.
        self.endpoints = endpoints

    def on_off_ramp(self):
        for x in self.nodes:
            if x == (4.2, 8.0) or x == (6.0, 3.3):
                return True # on-ramp- road to highway.

            elif x == (3.1, 7.9) or x == (6.5, 2.6):
                return False # off-ramp- highway to road.

class nodes_distance:
    def node_segment(self, coords):
        distances = []

        for i in range(len(coords) - 1):
            node1 = coords[i]
            node2 = coords[i + 1]
            distance = round(geopy.distance.distance(node1, node2).km, 2)

            distances.append(distance)

        return distances
class Intersections:
    def __init__(self):
        self.intersection = []
    def find_intersection(self, road_network1, road_network2):
       for coord1 in road_network1:
           for coord2 in road_network2:
               if coord1 == coord2:
                   self.intersection.append(coord1)

       if len(self.intersection) == 0:
           return False # intersection doesn't exist.

       return self.intersection # returns the list of tuples of intersected coordinates.


    def shortest_path(self, *roads, speed, start, end):
        graph = nx.Graph()
        coordinates = []
        travel_time = []
        distance_list = []

        for road in roads:
            coordinates.append(road.nodes) # creates list ( of list) of tuples for a network.

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
        yield env.timeout(5) # wait for 5 time unit to generate a truck.
        truck = Truck(env, 55)
        truck.trucks_generated.append(truck)

        for endpoint in roadways.endpoints:
            print(f"{truck.name} is queued at endpoints {endpoint} of a road {roadways.name} at {env.now} time.")

        if env.now >= until:
            break



# road and highway instantiation.
road1 = Roadways([(10.1, 7.2),(9.0, 7.2), (7.4, 7.4), (4.2, 8.0)], [(10.1, 7.2)])
road2 = Roadways([(9.8, 4.2), (9.1, 4.8), (7.3, 5.2), (4.2, 5.9), (3.2, 6.1), (1.2, 6.2)], [(9.8, 4.2), (1.2, 6.2)])
road3 = Roadways([(9.0, 9.2), (9.0, 7.2), (9.1, 4.8), (9.1, 1.8)], [(9.0, 9.2)])
road4 = Roadways([(7.2, 9.2), (7.4, 7.4), (7.3, 5.2), (7.5, 2.0), (7.5, 1.2)], [(7.2, 9.2), (7.5, 1.2)])
road5 = Roadways([(2.7, 7.2), (3.2, 6.9), (4.2, 5.9), (6.0, 3.3), (6.5, 2.6), (7.7, 2.0), (7.5, 1.8)], [(2.7, 7.2), (7.7, 1.8)])
road6 = Roadways([(3.1, 7.9), (3.2, 6.9), (3.2, 6.1), (3.4, 1.2)], [(3.4, 1.2)])
highway1 = Highways([(3.1, 10.0), (3.1, 7.9), (4.1, 4.0), (7.8, 2.6), (9.1, 1.8), (8.9, 1.5)], [(3.1, 10.0), (8.9, 1.5)])
highway2 = Highways([(1.5, 2.4), (6.0, 3.3), (6.5, 2.6), (7.8, 2.6), (10.1, 2.4)], [(1.5, 2.4), (10.1, 2.4)])

# intersection object instantiation- called function.
intersection1 = Intersections().find_intersection(road1.nodes, road3.nodes)
intersection2 = Intersections().find_intersection(road1.nodes, road4.nodes)
intersection3 = Intersections().find_intersection(road1.nodes, highway1.nodes)
intersection4 = Intersections().find_intersection(road2.nodes, road3.nodes)
intersection5 = Intersections().find_intersection(road2.nodes, road4.nodes)
intersection6 = Intersections().find_intersection(road2.nodes, road5.nodes)
intersection7 = Intersections().find_intersection(road2.nodes, road6.nodes)
intersection8 = Intersections().find_intersection(road4.nodes, road5.nodes)
intersection9 = Intersections().find_intersection(road5.nodes, road6.nodes)
intersection10 = Intersections().find_intersection(highway1.nodes, highway2.nodes)
intersection11 = Intersections().find_intersection(highway1.nodes, road3.nodes)
intersection12 = Intersections().find_intersection(highway1.nodes, road4.nodes)
intersection13 = Intersections().find_intersection(highway1.nodes, road6.nodes)
intersection14 = Intersections().find_intersection(highway2.nodes, road5.nodes)

# create a simpy environment.
env = simpy.Environment()

# generate trucks for each road.
for roadways in [road1, road2, road3, road4, road5, road6, highway1, highway2]:
    env.process(generate_trucks(env, roadways, 150))

env.run(until=50)
print()
# endpoints_coord = [(3.4, 1.2), (1.5, 2.4), (1.2, 6.2), (2.7, 7.2), (3.1, 10.0), (7.5, 1.2), (7.5, 1.8), (7.2, 9.2)
#    , (8.9, 1.5), (10.1, 2.4), (9.8, 4.2), (10.1, 7.2), (9.0, 9.2)]
x = Intersections()
start = (10.1, 7.2)
end = (9.8, 4.2)
x.shortest_path(road1, road2, road3, road4, road5, road6, highway1, highway2, speed=55, start=start, end=end)
