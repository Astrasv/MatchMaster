from .Stack import Stack
from .PointsTable import PointTable
from .Scheduler import Scheduler

# Defining a class to store match results between teams.

class MatchResult:
    def __init__(self, opponent, result):
        self.opponent = opponent
        self.result = result

# Defining a class to represent a team.

class Team:
    def __init__(self, name, ground):
        self.name = name
        self.ground = ground
        self.last_five_matches = Stack()
        self.points = 0
        self.wins = 0
        self.loses = 0
        self.matches = 0

    # Method to get the last five matches of the team.
    def get_last_five_matches(self):
        
        # Create result and temporary stack
        temp_stack = Stack()
        res_stack = Stack()
        
        # Get last 5 matches for above 5 teams and all matches for below 5
        match_count = self.matches if self.matches < 5 else 5
        
        # Push the top 5/less matches into temp stack
        for _ in range(match_count):
            temp_stack.push(self.last_five_matches.pop())
            
        # Push the data from temp stack to result stack 
        while not temp_stack.is_empty():
            popped = temp_stack.pop()
            res_stack.push(popped)
            self.last_five_matches.push(popped)

        return res_stack


# Defining a class to represent a match edge between two teams.

class MatchEdge:
    def __init__(self, team1, team2, winner):
        self.team1 = team1
        self.team2 = team2
        self.winner = winner

# Defining a class to represent the tournament graph.

# Using Edge list representation
# Since we are dealing with Full connected graph we need to work more with edges so we preffered edge list
class Graph:
    def __init__(self):
        self.teams = {} # Vertex is stored in a hashmap (teamname : teamobject)
        self.edges = Stack()
        self.point_table = PointTable()

    # Method to add a team to the graph.
    def add_team(self, team_name, home_ground):
        if team_name not in self.teams:
            team = Team(team_name, home_ground)
            self.teams[team_name] = team
            self.point_table.add_team(team)

    # Method to generate match edges between teams and simulate matches. Full connected graph
    def generate_edges(self):
        teams = list(self.teams.keys())
        if len(teams) <= 1:
            print("We need atleast 2 teams")
            return
        
        
        scheduler = Scheduler(len(teams))
        scheduler.generate()
        
        print(f"\nTotal Matches: {scheduler.totalmatches}\n")
        match_count = 1
        for round in scheduler.merged_table:
            for i,j in round:
                if i == "bye" or j == "bye":
                    continue
                
                team1 = teams[i-1]
                team2 = teams[j-1]
                
                
                # Simulating a match and getting the winner from user input.
                while True:
                    winner_input = input(f"Match {match_count} | {team1} VS {team2} | Ground:{self.teams[team1].ground} | Winner:  ")
                    if winner_input not in [team1 , team2]:
                        print("Invalid entry! Please enter either " + team1 + " or " + team2 + ".")
                    else:
                        
                        break
                winner = team1 if winner_input == team1 else team2
                
                # Updating teams' statistics based on the match result.
                loser = team2 if winner == team1 else team1
                winner_team = self.teams[winner]
                loser_team = self.teams[loser]
                match_result_win = MatchResult(loser_team.name, "W")
                match_result_lose = MatchResult(winner_team.name, "L")
                winner_team.last_five_matches.push(match_result_win)
                loser_team.last_five_matches.push(match_result_lose)
                winner_team.points += 2
                winner_team.wins += 1
                winner_team.matches += 1
                loser_team.matches += 1
                loser_team.loses += 1

                match_edge = MatchEdge(team1, team2, winner)
                self.edges.push(match_edge)
                
                match_count += 1
                self.display_points_table()
            
    # Method to display the points table.
    def display_points_table(self):
        self.point_table.display_table()
