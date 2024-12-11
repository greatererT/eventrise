from math import sqrt, pow
import random
import abc

DISTANCE = 0
PATH = 1

locations = {"a": [20, 52], "b": [122, 161], "c": [70, 60], "d": [99, 149],
              "e": [70, 40], "f": [99, 124]}

def calc_distance(start, end):
    """accepts two [x,y] coordinates."""
    distance=sqrt(pow(start[0] - end[0], 2) + pow(start[1] - end[1], 2))
    return distance


class Vehicle(abc.ABC):
    """
    abstract class for a vehicle.
    vehicle_id: string
    capacity: int
    speed: float, in km/h.
    """

    def __init__(self, capacity, speed):
        self.vehicle_id=str(random.randrange(10000000,99999999))
        self.capacity=capacity
        self.speed=speed
        if type(self.capacity) != int or type(self.speed) != float:
            raise(TypeError("incorrect data type entered!"))


    def get_vehicle_id(self):
        return self.vehicle_id

    def set_vehicle_id(self, id):
        self.vehicle_id = id

    @abc.abstractmethod
    def get_details(self):
        print(f"id is: {self.vehicle_id}\ncapacity is: {self.capacity}\nspeed is: {self.speed}")


    
    def calculate_travel_time(self, distance):
        """distance in km."""
        return int(distance/self.speed*60)


class Bus(Vehicle):
    def __init__(self, capacity, speed, route_number):
        super().__init__(capacity, speed)
        self.route_number=route_number
        if type(self.route_number) != str:
            raise(TypeError("incorrect data type entered!"))

    
    def get_details(self):
        super().get_details()
        print(f"route number: {self.route_number}")


class Train(Vehicle):
    def __init__(self, capacity, speed, line_name, num_cars):
        super().__init__(capacity, speed)
        self.line_name=line_name
        self.num_cars=num_cars
        if type(self.line_name) != str or type(self.num_cars) != int:
            raise(TypeError("incorrect data type entered!"))

    def get_details(self):
        super().get_details()
        print(f"line name: {self.line_name}")
        print(f"number of cars in train: {self.num_cars}")


class Tram(Vehicle):
    def __init__(self, capacity, speed, track_length):
        super().__init__(capacity, speed)
        self.track_length=track_length
        if type(self.track_length) != float:
            raise(TypeError("incorrect data type entered!"))

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


# Key: location(str), value: list of routes that are available to it, with start_point always being the key.
routes = {}


def populate_routes(max_distance):
    """
    max_distance: int. 
    makes routes between all locations who's distance is smaller than max_distance.
    inserts into routes.
    """
    for start_name, start_coordinates in locations.items():
        closest_locations=[]
        for end_name, end_coordinates in locations.items():
            distance = calc_distance(start_coordinates, end_coordinates)
            if distance < max_distance and start_name != end_name:
                closest_locations.append([end_name, distance])
        routes[start_name]= [Route(start_name,location[0],location[1]) for location in closest_locations]

populate_routes(75)


class RoutePlanner():
    def __init__(self, routes):
        self.routes = routes
    vehicles = []
    
    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id):
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                self.vehicles.remove(vehicle)
                print("vehicle removed.")
                break

    
    def find_optimal_route(self, start_point, end_point, algorithm):
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

    def sort_vehicles(self, strategy):
        strategy = QuickSortStrategy() if strategy == "quick sort" else MergeSortStrategy()
        return strategy.sort(self.vehicles)


    
class SortStrategy(abc.ABC):
    @abc.abstractmethod
    def sort(data):
        pass

class QuickSortStrategy(SortStrategy):
    def sort(self, data):
        if len(data) <= 1:
            return data
        else:
            pivot = data[0]
            left = [x for x in data[1:] if x.speed < pivot.speed]
            right = [x for x in data[1:] if x.speed >= pivot.speed]
            return self.sort(left) + [pivot] + self.sort(right)

class MergeSortStrategy(SortStrategy):

    def sort(self,data):
        if len(data) <= 1:
            return data

        mid = len(data) // 2
        leftHalf = data[:mid]
        rightHalf = data[mid:]

        sortedLeft = self.sort(leftHalf)
        sortedRight = self.sort(rightHalf)

        return self.merge(sortedLeft, sortedRight)


    def merge(self, left, right):
        result = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i].speed < right[j].speed:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])

        return result



def cli():
    routes_and_vehicles = RoutePlanner(routes)
    command=""
    print("welcome to route planner!")
    while command != "exit":
        command = input("options:\n \
              1. add or remove vehicle.\n \
              2. show all vehicle details.\n \
              3. get optimal route between two points.\n \
              4. sort vehicles by speed.\n \
              enter 'exit' to exit.\n")
        if command == "1":
            option = input("to remove vehicle, enter only the vehicle id.\n"
                           "to add new vehicle, enter vehicle type and details seperated by spaces.\n")
            if len(option) == 8:
                    routes_and_vehicles.remove_vehicle(option)
                
            else:
                option = option.split()
                try:
                    match option[0]:
                        case "bus": routes_and_vehicles.add_vehicle(Bus(int(option[1]),float(option[2]),
                                                                          option[3]))
                        case "train": routes_and_vehicles.add_vehicle(Train(int(option[1]),float(option[2])
                                                                            ,option[3],int(option[4])))
                        case "tram": routes_and_vehicles.add_vehicle(Tram(int(option[1]),float(option[2]),
                                                                          float(option[3])))
                except (ValueError, TypeError, IndexError):
                    print("incorrect details entered!")
                    continue
        elif command == "2":
            for vehicle in routes_and_vehicles.vehicles:
                vehicle.get_details()
        elif command == "3":
            option = input("enter starting point, end point, and algorithm seperated by , (without space).")
            try:
                start, end, algorithm = option.split(",")
                print(routes_and_vehicles.find_optimal_route(start, end, algorithm))
            except:
                print("invalid info entered!")
        elif command == "4":
            option = input("enter sorting algoritm (quick sort or merge sort)")
            if option == "quick sort" or "merge sort":
                for vehicle in routes_and_vehicles.sort_vehicles(option):
                    print(vehicle.vehicle_id, vehicle.speed)
            else:
                print("incorrect option!")
        else:
            print("incorrect option entered.")
        

def main():
    cli()
            
if __name__ == "main":
    main()

