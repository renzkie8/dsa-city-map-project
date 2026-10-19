import heapq

# Class to represent the map of establishments and their connections
class EstablishmentMap:
    def __init__(self):
        # Initialize an empty graph to store establishments and their connections
        self.graph = {}
    
    # Method to add an establishment to the map
    def add_establishment(self, establishment):
        if establishment not in self.graph:
            self.graph[establishment] = []  # Add a new establishment with no connections
    
    # Method to add a road (connection) between two establishments with a specified distance
    def add_road(self, establishment1, establishment2, distance):
        if establishment1 in self.graph and establishment2 in self.graph:
            # Add the road in both directions (undirected graph)
            self.graph[establishment1].append((establishment2, distance))
            self.graph[establishment2].append((establishment1, distance))
    
    # Method to find the shortest path between two establishments using Dijkstra's algorithm
    def shortest_path(self, start, end):
        heap = [(0, start)]  # Priority queue to store (distance, establishment)
        distances = {establishment: float('inf') for establishment in self.graph}  # Distance to each establishment
        distances[start] = 0  # Distance to the start is 0
        previous = {establishment: None for establishment in self.graph}  # Track previous establishments on the path
        
        while heap:
            current_dist, current_establishment = heapq.heappop(heap)  # Get establishment with the smallest distance
            
            if current_establishment == end:  # If destination is reached
                # Reconstruct the path by backtracking
                path = []
                while previous[current_establishment]:
                    path.insert(0, current_establishment)
                    current_establishment = previous[current_establishment]
                path.insert(0, start)  # Add the starting point
                return path, current_dist  # Return the path and its total distance
            
            # Update distances for neighbors
            for neighbor, weight in self.graph[current_establishment]:
                distance = current_dist + weight
                if distance < distances[neighbor]:  # Found a shorter path
                    distances[neighbor] = distance
                    previous[neighbor] = current_establishment  # Update previous establishment
                    heapq.heappush(heap, (distance, neighbor))  # Push neighbor to the heap
        
        return None, float('inf')  # Return if no path exists

    # Method to check if two establishments are connected using Depth-First Search (DFS)
    def are_connected(self, establishment1, establishment2):
        visited = set()  # Keep track of visited establishments
        
        def dfs(establishment):
            if establishment == establishment2:  # If target is found
                return True
            visited.add(establishment)  # Mark current establishment as visited
            # Explore neighbors
            for neighbor, _ in self.graph[establishment]:
                if neighbor not in visited and dfs(neighbor):
                    return True
            return False
        
        return dfs(establishment1)  # Start DFS from the first establishment
    
    # Method to display all establishments and their connections
    def display_map(self):
        for establishment, neighbors in self.graph.items():
            # Print each establishment and its connected neighbors with distances
            print(f"{establishment} is connected to: " + ", ".join([f"{neighbor} (Distance: {dist}m)" for neighbor, dist in neighbors]))

# Example usage with user input:

establishment_map = EstablishmentMap()

# Input establishments
establishments = input("Enter establishments separated by commas (example: BFP,CSPC,LCC,RHU): ").split(',')
for establishment in establishments:
    establishment_map.add_establishment(establishment.strip())

# Input roads and distances
while True:
    road_input = input("Enter a road connection and distance (example: BFP LCC 20) or 'done' to finish: ")
    if road_input.lower() == 'done':
        break
    establishment1, establishment2, distance = road_input.split()
    establishment_map.add_road(establishment1.strip(), establishment2.strip(), int(distance))

# Input action to perform
while True:
    action = input("Choose an action: \n1. Find shortest path \n2. Check if establishments are connected \n3. Display map \n4. Exit\n")
    
    if action == '1':
        # Find and display the shortest path between two establishments
        start = input("Enter the start establishment: ").strip()
        end = input("Enter the destination establishment: ").strip()
        path, distance = establishment_map.shortest_path(start, end)
        if path:
            print(f"Shortest path from {start} to {end}: {path} with distance {distance}m")
        else:
            print(f"No path found from {start} to {end}")
    
    elif action == '2':
        # Check if two establishments are connected
        establishment1 = input("Enter the first establishment: ").strip()
        establishment2 = input("Enter the second establishment: ").strip()
        if establishment_map.are_connected(establishment1, establishment2):
            print(f"{establishment1} and {establishment2} are connected.")
        else:
            print(f"{establishment1} and {establishment2} are not connected.")
    
    elif action == '3':
        # Display the map of establishments and connections
        establishment_map.display_map()
    
    elif action == '4':
        # Exit the program
        print("Exiting...")
        break
    else:
        print("Invalid choice, please select again.")