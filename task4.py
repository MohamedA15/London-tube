import pandas as pd
from adjacency_list_graph import AdjacencyListGraph

class UndergroundMap:
    def __init__(self, station_mapping):
        # Create a mapping between station names and integer indices
        self.station_mapping = station_mapping
        # initialise the graph
        self.graph = AdjacencyListGraph(len(station_mapping), directed=False, weighted=True)

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

def is_adjacent(station1, station2, excel_data):
    """
    Check if two stations are adjacent based on their order of appearance in the original data.
    """
    return any(
        ((row["StationA"] == station1 and row["StationB"] == station2) or
         (row["StationA"] == station2 and row["StationB"] == station1))
        for _, row in excel_data.iterrows()
    )

def justify_closure(graph_copy, stations, excel_data):
    """
    Check if closure is justified based on the conditions.
    """
    for i in range(len(stations) - 1):
        start_station = stations[i]
        end_station = stations[i + 1]

        # Check if stations are adjacent
        if is_adjacent(start_station, end_station, excel_data):
            # Omitted Kruskal's algorithm

            # Check if there is a path between start_station and end_station
            path = []
            visited = set()

            # Helper function to perform DFS on the graph
            def dfs(current):
                visited.add(current)
                path.append(current)

                for edge in graph_copy.get_adj_list(current):
                    neighbor = edge.get_v()
                    if neighbor not in visited:
                        dfs(neighbor)

            dfs(underground_map.station_mapping[start_station])

            if underground_map.station_mapping[end_station] not in visited:
                print(f"No path from {start_station} to {end_station}")

    return True

def plan_route(underground_map, start_station, end_station):
    start = underground_map.station_mapping[start_station]
    end = underground_map.station_mapping[end_station]

    path = []
    visited = set()

    # Helper function to perform DFS on the graph
    def dfs(current):
        visited.add(current)
        path.append(current)

        for edge in underground_map.graph.get_adj_list(current):
            neighbor = edge.get_v()
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start)

    if end in visited:
        print(f"Path from {start_station} to {end_station}:")
        print("Stations to go through:", " -> ".join([stations[i] for i in path]))
    else:
        print(f"No valid path found from {start_station} to {end_station}")

# Loop through every edge and simulate closure
for edge in underground_map.graph.get_edge_list():
    u, v = edge
    # Check if the stations are adjacent
    station_u = next((station for station, index in station_mapping.items() if index == u), None)
    station_v = next((station for station, index in station_mapping.items() if index == v), None)

    if is_adjacent(station_u, station_v, excel_data):
        # Create a copy of the graph to simulate closure
        graph_copy = underground_map.graph.copy()
        graph_copy.delete_edge(u, v)

        # Check if the closure satisfies the conditions
        is_feasible = justify_closure(graph_copy, [station_u, station_v], excel_data)

        if is_feasible:
            print(f"Closure can be executed for edge: {station_u} -- {station_v}")
        else:
            print(f"Closure cannot be executed for edge: {station_u} -- {station_v}")