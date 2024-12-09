from math import sqrt, pow
import random
locations = {"a": [20, 52], "b": [122, 161], "c": [70, 60], "d": [99, 149],
              "e": [70, 40], "f": [99, 124]}
DISTANCE = 0
PATH = 1


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






routes = {}

def populate_routes():
    for start_name, start_coordinates in locations.items():
        closest_locations=[]
        for end_name, end_coordinates in locations.items():
            distance = calc_distance(start_coordinates, end_coordinates)
            if distance < 75 and start_name != end_name:
                closest_locations.append([end_name, distance])
        print(f"closest to {start_name}: {closest_locations}")
        routes[start_name]= [Route(start_name,location[0],location[1]) for location in closest_locations]

populate_routes()
for key, vals in routes.items():
    for val in vals:
        print(f"key: {key}, val: {val}")



def dijkstra(start_point, end_point):
    distances = {"a": [999, start_point], "b": [999, start_point], "c": [999, start_point],
                "d": [999, start_point], "e": [999, start_point], "f": [999, start_point]}
    path = start_point
    path_length = 0
    visited = []
    current_point=start_point
    distances[start_point]=[0,start_point]


    for i in range(5):
        min = max(distances, key=distances.get)

        for route in routes[current_point]:
            if path_length+route.distance < distances[route.end_point][DISTANCE]:                
                distances[route.end_point] = [path_length+route.distance, distances[current_point][1]+route.end_point]

        visited.append(current_point)
        print(current_point)
        for point, vals in distances.items():
            min = point if vals[DISTANCE] < distances[min][DISTANCE] and point not in visited else min
        

        #current_point = min(not_visited, key = not_visited.get)
        current_point = min
        print(f"aaaAAaa{current_point}")
        path = str(distances[current_point][PATH])
        path_length = distances[current_point][DISTANCE]

        for currentpoint, path in distances.items():
            print(currentpoint, path)
            
print("------------")

dijkstra("a","f")

        
        