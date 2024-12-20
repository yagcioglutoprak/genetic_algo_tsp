import numpy as np



def read_tsp_file(file_path):
    coordinates = {}
    city_names = {}
    reading_coords = False
    reading_names = False
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            if line == "COMMENT: City names for each node":
                reading_names = True
                continue
            elif line == "NODE_COORD_SECTION":
                reading_names = False
                reading_coords = True
                continue
            elif line == "EOF":
                break
            elif reading_names:
           
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    index, name = parts
                    city_names[int(index)] = name.strip()
            elif reading_coords:
             
                parts = line.split()
                if len(parts) == 3:
                    index, x, y = parts
                    coordinates[int(index)] = (float(x), float(y))
    
    return coordinates, city_names

coordinates, city_names = read_tsp_file('us_capitals.tsp')

def calculate_distance_coords(route_1, route_2):
    return np.sqrt((route_1[0] - route_2[0])**2 + (route_1[1] - route_2[1])**2)



def calculate_random_best_route(coordinates, city_names):
    random_route = np.random.permutation(len(coordinates)) + 1
    return random_route



def save_solution_to_file(route, city_names):
    if route is None:
        print("Error: No valid route was generated")
        return
        
    with open('random_route.txt', 'w') as f:
        # Header
        f.write("*" * 50 + "\n")
        f.write("*           Optimized Travel Route              *\n")
        f.write("*" * 50 + "\n\n")
        
        # Coordinates section
        f.write("City Coordinates:\n")
        f.write("-" * 20 + "\n")
        for city_index in route:
            coord = coordinates[city_index]
            f.write(f"({coord[0]:.2f}, {coord[1]:.2f})\n")
        
        f.write("\n")
        
        # City names with distances
        f.write("City Route and Distances:\n")
        f.write("-" * 20 + "\n")
        total_distance = 0
        
        for i in range(len(route)):
            current_city = route[i]
            next_city = route[(i + 1) % len(route)]  # Wrap around to first city
            
            # Calculate distance to next city
            distance = calculate_distance_coords(coordinates[current_city], coordinates[next_city])
            total_distance += distance
            
            f.write(f"{city_names[current_city]} → Distance: {distance:.2f} miles\n")
        
        f.write(f"\nTotal Route Distance: {total_distance:.2f} miles\n")
        f.write("\n" + "*" * 50 + "\n")

save_solution_to_file(calculate_random_best_route(coordinates, city_names), city_names)

def calculate_fitness(route, coordinates):
   
    total_distance = 0
    for i in range(len(route)):
        current_city = route[i]
        next_city = route[(i + 1) % len(route)]
        
        
        distance = calculate_distance_coords(coordinates[current_city], coordinates[next_city])
        total_distance += distance
    
    return total_distance


route = calculate_random_best_route(coordinates, city_names)
fitness = calculate_fitness(route, coordinates)



def greedy_algorithm(coordinates):
    
    best_distance = float('inf')
    best_route = None
    

    for start_city in coordinates.keys():
       
        current_city = start_city
        unvisited = set(coordinates.keys()) - {start_city}
        route = [start_city]
        
       
        while unvisited:
            
            nearest_city = min(
                unvisited,
                key=lambda x: calculate_distance_coords(coordinates[current_city], coordinates[x])
            )
            
            route.append(nearest_city)
            unvisited.remove(nearest_city)
            current_city = nearest_city
            
        
        distance = calculate_fitness(np.array(route), coordinates)
        
       
        if distance < best_distance:
            best_distance = distance
            best_route = route
    
    return np.array(best_route), best_distance


greedy_route, greedy_distance = greedy_algorithm(coordinates)



save_solution_to_file(greedy_route, city_names)

def calculate_multiple_random_solutions(coordinates, city_names, num_solutions=100):
  
    best_distance = float('inf')
    best_route = None
    all_distances = []  
    
    for i in range(num_solutions):
        
        current_route = calculate_random_best_route(coordinates, city_names)
        current_distance = calculate_fitness(current_route, coordinates)
        all_distances.append(current_distance)
        
       
        if current_distance < best_distance:
            best_distance = current_distance
            best_route = current_route
    
  
    avg_distance = np.mean(all_distances)
    worst_distance = np.max(all_distances)
    
    print(f"\nRandom Solutions Statistics (from 100 attempts):")
    print(f"Best Distance: {best_distance:.2f}")
    print(f"Average Distance: {avg_distance:.2f}")
    print(f"Worst Distance: {worst_distance:.2f}")
    print(f"Best Route: {best_route}")
    
    return best_route, best_distance


random_best_route, random_best_distance = calculate_multiple_random_solutions(coordinates, city_names)
print(f"\nComparison with Greedy Solution:")
print(f"Greedy Distance: {greedy_distance:.2f}"+"\n"+"Greedy Route: "+str(greedy_route))
print(f"Random Best Distance: {random_best_distance:.2f}")
print(f"Greedy is better by: {(random_best_distance - greedy_distance) / random_best_distance * 100:.1f}%")





save_solution_to_file(random_best_route, city_names)

def save_comparison_results(greedy_route, greedy_distance, random_route, random_distance, city_names):
    
    with open('route_comparison.txt', 'w') as f:

        f.write("*" * 60 + "\n")
        f.write("*           Route Optimization Comparison Results            *\n")
        f.write("*" * 60 + "\n\n")
        
      
        f.write("GREEDY ALGORITHM SOLUTION\n")
        f.write("=" * 30 + "\n")
        f.write(f"Total Distance: {greedy_distance:.2f} miles\n")
        f.write("Route: \n")
        for i, city_index in enumerate(greedy_route, 1):
            f.write(f"{i}. {city_names[city_index]}\n")
        f.write("\n")
        
       
        f.write("BEST RANDOM SOLUTION\n")
        f.write("=" * 30 + "\n")
        f.write(f"Total Distance: {random_distance:.2f} miles\n")
        f.write("Route: \n")
        for i, city_index in enumerate(random_route, 1):
            f.write(f"{i}. {city_names[city_index]}\n")
        f.write("\n")
        
  
        f.write("COMPARISON\n")
        f.write("=" * 30 + "\n")
        difference = random_distance - greedy_distance
        percentage = (difference / random_distance) * 100
        f.write(f"Difference: {difference:.2f} miles\n")
        f.write(f"Greedy solution is better by: {percentage:.1f}%\n")
        f.write("\n" + "*" * 60 + "\n")


save_comparison_results(
    greedy_route, 
    greedy_distance, 
    random_best_route, 
    random_best_distance, 
    city_names
)