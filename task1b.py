import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
import matplotlib.pyplot as plt

class UndergroundMap:
    def __init__(self, station_mapping):
        # Create a mapping between station names and integer indices
        self.station_mapping = station_mapping
        # initialize the graph
        self.graph = AdjacencyListGraph(len(station_mapping), directed=True,
                                        weighted=True)  # Set directed and weighted accordingly

# Load the data from the provided Excel sheet into a pandas DataFrame
excel_data = pd.read_excel("London Underground data.xlsx")
# Create a mapping between station names and integer indices
stations = sorted(set(excel_data["StationA"]).union(excel_data["StationB"]))
station_mapping = {station: i for i, station in enumerate(stations)}
underground_map = UndergroundMap(station_mapping)

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

# Calculate journey times for all station pairs
journey_times = []
for start_station in range(len(stations)):
    for end_station in range(len(stations)):
        if start_station != end_station:
            d, _ = dijkstra(underground_map.graph, start_station)

            # Check if the end_station is reachable from the start_station
            if d[end_station] != float('inf'):
                journey_times.append(d[end_station])

# Create a histogram of journey times
plt.hist(journey_times, bins=30, color='skyblue', edgecolor='black')
plt.xlabel('Journey Time (minutes)')
plt.ylabel('Frequency')
plt.title('Histogram of Journey Times between Station Pairs')
plt.grid(True)

# Show the histogram
plt.show()