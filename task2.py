import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

class UndergroundMap:
    def __init__(self, station_mapping):
        # Create a mapping between station names and integer indices
        self.station_mapping = station_mapping
        # initialize the graph
        self.graph = AdjacencyListGraph(len(station_mapping), directed=True, weighted=True)

# Load the data from the provided Excel sheet into a pandas DataFrame
excel_data = pd.read_excel("London Underground data.xlsx")

# Create a mapping between station names and integer indices
stations = sorted(set(excel_data["StationA"]).union(excel_data["StationB"]))
station_mapping_outer = {station: i for i, station in enumerate(stations)}
underground_map = UndergroundMap(station_mapping_outer)

# Create a graph representation from the DataFrame
for index, row in excel_data.iterrows():
    stationA, stationB, Time = row["StationA"], row["StationB"], row["Time"]
    # Map station names to integer indices
    stationA_index = underground_map.station_mapping[stationA]
    stationB_index = underground_map.station_mapping[stationB]

    # Check if the edge already exists before insertion
    if not underground_map.graph.has_edge(stationA_index, stationB_index):
        underground_map.graph.insert_edge(stationA_index, stationB_index, Time)

def get_user_input() -> tuple[str, str]:
    user_start_station = input("Enter the start station: ")
    user_end_station = input("Enter the end station: ")
    return user_start_station, user_end_station

def find_path_stations(pi: list, pos_of_station: dict, start_station: str, end_station: str) -> int:
    end_pos = pos_of_station[end_station]

    # Check if a path exists
    if pi[end_pos] is None:
        return 0

    path_length = 1
    new_pos = pi[end_pos]

    while new_pos != pos_of_station[start_station]:
        position = list(pos_of_station.values()).index(new_pos)
        new_pos = pi[pos_of_station[list(pos_of_station.keys())[position]]]
        path_length += 1

    return path_length

start_station_input, end_station_input = get_user_input()

if start_station_input in underground_map.station_mapping and end_station_input in underground_map.station_mapping:
    start = underground_map.station_mapping[start_station_input]
    end = underground_map.station_mapping[end_station_input]
    pos_of_station_inner = {station: i for i, station in enumerate(stations)}

    # Run Dijkstra's algorithm to find the shortest path and distances
    d, pi = dijkstra(underground_map.graph, start)

    # Retrieve the path length using the predecessors
    path_length = find_path_stations(pi, pos_of_station_inner, start_station_input, end_station_input)

    if path_length > 0:
        print(f"Number of stations from {start_station_input} to {end_station_input}: {path_length}")
        # Retrieve the actual path using the predecessors
        path = [end]
        while pi[path[-1]] is not None:
            path.append(pi[path[-1]])
        path.reverse()
        print("Stations to go through:", " -> ".join([stations[i] for i in path]))
    else:
        print(f"No valid path found from {start_station_input} to {end_station_input}")
else:
    print("Invalid station names! Please enter valid station names.")
