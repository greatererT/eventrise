from math import sqrt, pow
import random
#locations = {"a": [0, 50], "b": [0, 20], "c": [0, 90], "d": [99, 149],
#              "e": [70, 40], "f": [0, 130]}
locations = {"a": [20, 52], "b": [122, 161], "c": [70, 60], "d": [99, 149],
              "e": [70, 40], "f": [99, 124]}
DISTANCE = 0
PATH = 1
#    distances = {"a": [999, start_point], "b": [999, start_point], "c": [999, start_point],
#                "d": [999, start_point], "e": [999, start_point], "f": [999, start_point]}

def calc_distance(start, end):
    """accepts two [x,y] coordinates."""
    distance=sqrt(pow(start[0] - end[0], 2) + pow(start[1] - end[1], 2))
    return distance

    


def generate_random_route():
    start, end = random.sample(list(locations.keys()),2)
    route = Route(start,end, calc_distance(locations[start],locations[end]))
    #TODO: add certain vehicle to have differing speeds?



class Vehicle:
    """
    abstract class for a vehicle. speed is in km/h.
    vehicle_id: string
    capacity: int
    speed: float
    """

    def __init__(self, vehicle_id, capacity, speed):
        self.vehicle_id=vehicle_id
        self.capacity=capacity
        self.speed=speed

    def get_details(self):
        print(f"id is: {self.vehicle_id}\ncapacity is: {self.capacity}\nspeed is: {self.speed}")
    
    def calculate_travel_time(self, distance):
        """distance should be in kilometers."""
        print(f"it will take {int(distance/self.speed*60)} minutes to drive the distance of {distance} km.")

a = Vehicle("23", 500, 7.0)
a.get_details()
a.calculate_travel_time(100)


class Bus(Vehicle):
    def __init__(self, vehicle_id, capacity, speed, route_number):
        super().__init__(vehicle_id, capacity, speed)
        self.route_number=route_number

    def get_details(self):
        super().get_details()
        print(f"route number: {self.route_number}")


class Train(Vehicle):
    def __init__(self, vehicle_id, capacity, speed, line_name, num_cars):
        super().__init__(vehicle_id, capacity, speed)
        self.line_name=line_name
        self.num_cars=num_cars

    def get_details(self):
        super().get_details()
        print(f"line name: {self.line_name}")
        print(f"number of cars in train: {self.num_cars}")


class Tram(Vehicle):
    def __init__(self, vehicle_id, capacity, speed, track_length):
        super().__init__(vehicle_id, capacity, speed)
        self.track_length=track_length

    def get_details(self):
        super().get_details()
        print(f"line name: {self.track_length}")

class Route:
    def __init__(self, start_point, end_point, distance):
        self.start_point=start_point
        self.end_point=end_point
        self.distance=distance

    def get_route_info(self):
        print(f"start point: {self.start_point}\nend point: {self.end_point}\ndistance: {self.distance}")



    









a = Bus("23", 500, 7.0, "845")
a.get_details()
a.calculate_travel_time(100)




# Key: location(str), value: list of routes that are available to it, with start_point always being the key.
routes = {}


def populate_routes(max_distance):
    """
    max_distance: int. 
    makes routes between all locations who's distance is smaller than max_distance.
    """
    for start_name, start_coordinates in locations.items():
        closest_locations=[]
        for end_name, end_coordinates in locations.items():
            distance = calc_distance(start_coordinates, end_coordinates)
            if distance < max_distance and start_name != end_name:
                closest_locations.append([end_name, distance])
        print(f"closest to {start_name}: {closest_locations}")
        routes[start_name]= [Route(start_name,location[0],location[1]) for location in closest_locations]

populate_routes(75)




def find_optimal_route(start_point, end_point, algorithm):
    """
    takes two points (str names of locations) and calculates shortest route between them using available routes.
    which algorithm is used is based on algorithm var. options are a star and dijkstra.\n
    Returns the path found as a string concatenation of all locations.
    """

    # Key: location. Value: list containing path length from start point, and path taken (list with a string of all locations.)
    distances={}

    # Populates distances based on locations.
    for location in locations.keys():
        distances[location]=[9999, start_point]

    path_length = 0
    visited = []
    current_point=start_point
    
    #Sets the distance of start point to 0 (because distance is always measured from start point.)
    distances[start_point]=[0,start_point]

    for i in range(len(locations)-1):
        # doesnt matter which point it is as long as is wasn't visited, end_point is never be visited.
        min = end_point

        # Checks all routes starting from current point.
        for route in routes[current_point]:
            if route.end_point == end_point:
                return(distances[current_point][1]+route.end_point)
            
            # Checks if the found path is smaller than the smallest path to a certain point found until now.
            # If it is, it replaces it.
            if path_length+route.distance < distances[route.end_point][DISTANCE]:
                distances[route.end_point] = [path_length+route.distance, distances[current_point][1]+route.end_point]

        visited.append(current_point)

        if algorithm == "a star":
            for point, vals in distances.items():
                min = point if vals[DISTANCE]+calc_distance(locations[point],locations[end_point])  < \
                    distances[min][DISTANCE]+calc_distance(locations[min],locations[end_point]) and point not in visited else min
        elif algorithm == "dijkstra":
            for point, vals in distances.items():
                min = point if vals[DISTANCE] < distances[min][DISTANCE] and point not in visited else min
        else:
            print("incorrect algorithm name! options are: a star, dijkstra")
            return

        current_point = min
        path_length = distances[current_point][DISTANCE]


print(find_optimal_route("b","a","a star"))
