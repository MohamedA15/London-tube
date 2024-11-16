import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from bellman_ford import bellman_ford


class UndergroundMap:
    def __init__(self, station_mapping):
        # Create a mapping between station names and integer indices
        self.station_mapping = station_mapping
        # initialise the graph
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

    # Run Bellman Ford algorithm to find the shortest path and distances
    result = bellman_ford(underground_map.graph, start)

    if isinstance(result, tuple) and len(result) >= 2:
        d, pi = result[:2]
    elif isinstance(result, dict):
        d = result
        pi = {v: None for v in result}
    else:
        raise ValueError("Unexpected return type or structure from bellman_ford")

    # Retrieve the path using the predecessors
    path = []
    current = end
    while current is not None:
        path.insert(0, current)
        current = pi[current]

    if d[end] != float('inf'):
        stops_count = len(path) - 1  # Number of stops is the number of vertices in the path minus 1
        print(f"Number of stops from {start_station} to {end_station}: {stops_count} stops")
        print("Stations to go through:", " -> ".join([stations[i] for i in path]))
        return stops_count
    else:
        print(f"No valid path found from {start_station} to {end_station}")
        return 0


# Calculate journey times for all station pairs
journey_times = []

for start_station in stations:
    start_index = underground_map.station_mapping[start_station]
    for end_station in stations:
        if start_station != end_station:
            journey_time = plan_route(underground_map, start_station, end_station)
            if journey_time > 0:
                journey_times.append(journey_time)

# Create a histogram from the journey_times list
plt.hist(journey_times, bins=range(min(journey_times), max(journey_times) + 1, 1), edgecolor='black')
plt.title('Histogram of Journey Times Between Station Pairs')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')
plt.show()