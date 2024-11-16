import pandas as pd
import matplotlib.pyplot as plt
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


# Function to calculate the number of stops for all station pairs
def calculate_stops_for_all_pairs(underground_map, stations):
    stops_counts = []
    pos_of_station = {station: i for i, station in enumerate(stations)}

    for start_station in stations:
        start_index = underground_map.station_mapping[start_station]
        d, pi = dijkstra(underground_map.graph, start_index)

        for end_station in stations:
            if start_station != end_station:
                path_length = find_path_stations(pi, pos_of_station, start_station, end_station)
                if path_length > 0:
                    stops_counts.append(path_length)
    return stops_counts


# Calculate stops for all station pairs
stops_counts = calculate_stops_for_all_pairs(underground_map, stations)

# Create a histogram from the stops_counts list
plt.hist(stops_counts, bins=range(min(stops_counts), max(stops_counts) + 1, 1), edgecolor='black')
plt.title('Histogram of Stops Count Between Station Pairs')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')
plt.show()