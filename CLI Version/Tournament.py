from Structures.Graph import Graph
# Main function to run the program.

# Getting the number of teams and their names from the user.
number_of_teams = int(input("Enter number of teams: "))
teams = [None for _ in range(number_of_teams)]
for i in range(number_of_teams):
    team = input(f"Enter Team {i + 1}'s name: ")
    ground = input(f"Enter Team {i + 1}'s Home Ground name: ")
    teams[i] = (team, ground)

# Initializing the tournament graph.
graph = Graph()
for team, ground in teams:
    graph.add_team(team, ground)

# Generating match edges and simulating matches.
graph.generate_edges()

# Displaying the points table after all matches are simulated.
graph.display_points_table()
