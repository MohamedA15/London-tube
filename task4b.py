import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

class UndergroundMap:
    def __init__(self, station_mapping):
        self.station_mapping = station_mapping
        self.graph = AdjacencyListGraph(len(station_mapping), directed=False, weighted=True)

# Function to calculate journey metrics
def calculate_journey_metrics(underground_map, stations):
    journey_times = []
    stops_counts = []

    for start_station in stations:
        start_index = underground_map.station_mapping[start_station]
        distances, predecessors = dijkstra(underground_map.graph, start_index)

        for end_station in stations:
            if start_station != end_station:
                end_index = underground_map.station_mapping[end_station]
                journey_time = distances[end_index] if end_index < len(distances) else float('inf')
                journey_times.append(journey_time)

                # Calculate number of stops
                num_stops = 0
                current = end_index
                while current != start_index and current != None:
                    current = predecessors[current]
                    num_stops += 1
                num_stops -= 1  # Adjust count since start station is included
                stops_counts.append(max(0, num_stops))  # Ensure non-negative

    return journey_times, stops_counts


# Function to create histograms
def create_histogram(data, title, xlabel, ylabel):
    plt.hist(data, bins='auto', edgecolor='black')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.show()


# Load data and create graph
excel_data = pd.read_excel("London Underground data.xlsx")
stations = sorted(set(excel_data["StationA"]).union(excel_data["StationB"]))
station_mapping = {station: i for i, station in enumerate(stations)}
underground_map = UndergroundMap(station_mapping)

for index, row in excel_data.iterrows():
    stationA, stationB, Time = row["StationA"], row["StationB"], row["Time"]
    stationA_index = underground_map.station_mapping[stationA]
    stationB_index = underground_map.station_mapping[stationB]
    if not underground_map.graph.has_edge(stationA_index, stationB_index):
        underground_map.graph.insert_edge(stationA_index, stationB_index, Time)

# Calculate metrics before closures
pre_closure_times, pre_closure_stops = calculate_journey_metrics(underground_map, stations)

# Calculate metrics after closures
post_closure_times, post_closure_stops = calculate_journey_metrics(underground_map, stations)

# Create and display histograms for journey times
create_histogram(pre_closure_times, "Pre-Closure Journey Times", "Time (minutes)", "Frequency")
create_histogram(post_closure_times, "Post-Closure Journey Times", "Time (minutes)", "Frequency")

# Create and display histograms for stops counts
create_histogram(pre_closure_stops, "Pre-Closure Stops Count", "Number of Stops", "Frequency")
create_histogram(post_closure_stops, "Post-Closure Stops Count", "Number of Stops", "Frequency")