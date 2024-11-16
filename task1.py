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


def plan_route(underground_map, start_station, end_station):
    start = underground_map.station_mapping[start_station]
    end = underground_map.station_mapping[end_station]

    # Run Dijkstra's algorithm to find the shortest path and distances
    d, pi = dijkstra(underground_map.graph, start)

    # Retrieve the path using the predecessors
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = pi[current]

    if d[end] != float('inf'):
        print(f"Shortest journey duration from {start_station} to {end_station}: {d[end]} minutes")
        print("Stations to go through:", " -> ".join([stations[i] for i in path]))
    else:
        print(f"No valid path found from {start_station} to {end_station}")


# Extra blank line added after the class definition
start_station_input = input("Enter your starting station: ")
end_station_input = input("Enter your destination station: ")

if start_station_input in underground_map.station_mapping and end_station_input in underground_map.station_mapping:
    plan_route(underground_map, start_station_input, end_station_input)
else:
    print("Invalid station names! Please enter valid station names.")