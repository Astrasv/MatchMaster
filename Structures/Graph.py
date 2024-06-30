from .Stack import Stack
from .PointsTable import PointTable
from .Scheduler import Scheduler

import streamlit as st
import pandas as pd
import numpy as np
# IS NO ABOUT CHOSEN TEAM ITS ABOUT CHOSEN MATCH
# CHECK ON IT


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
        self.scheduler = None
        self.point_table = PointTable()

    # Method to add a team to the graph.
    def add_team(self, team_name, home_ground):
        if team_name not in self.teams:
            team = Team(team_name, home_ground)
            self.teams[team_name] = team
            self.point_table.add_team(team)

    # Method to generate match edges between teams and simulate matches. Full connected graph
    def generate_matches(self):
        numteams = len(self.teams.keys())
        scheduler = Scheduler(numteams)
        scheduler.generate()
        self.scheduler = scheduler
        

    def generate_edges(self):
        teams = list(self.teams.keys())
        if len(teams) <= 1:
            st.error("We need at least 2 teams")
            return

        st.error(f"\nTotal Matches: {self.scheduler.totalmatches}\n")
        match_count = 1
        all_matches_processed = True

        for round in range(self.scheduler.rows * 2):
            for mc in range(self.scheduler.cols):
                i = self.scheduler.merged_table[round][mc][0]
                j = self.scheduler.merged_table[round][mc][1]
                if i == "bye" or j == "bye":
                    continue

                team1 = teams[i - 1]
                team2 = teams[j - 1]

                match_key = f"match_{match_count}_winner"
                match_processed_key = f"match_{match_count}_processed"

                if match_key not in st.session_state:
                    st.session_state[match_key] = "Choose"
                if match_processed_key not in st.session_state:
                    st.session_state[match_processed_key] = False
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.info(f"Match {match_count}")
                with col2:
                    st.warning(f"{team1} VS {team2}")
                with col3:
                    st.success(f"Ground: {self.teams[team1].ground}")
                winner_input = st.selectbox(
                    f"Winner",
                    ("Choose", team1, team2),
                    key=f"{match_key}",
                    disabled=st.session_state[match_processed_key]
                )
                st.write("\n\n________________________________________________________________________________________________________________________________________________________________________")

                if st.session_state[match_key] == "Choose" and winner_input != "Choose":
                    st.session_state[match_key] = winner_input
                    st.experimental_rerun()

                winner = st.session_state[match_key]
                loser = team1 if winner == team2 else team2

                if winner != "Choose" and not st.session_state[match_processed_key]:
                    self.scheduler.merged_table[round][mc][2] = 1
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

                    st.session_state[match_processed_key] = True
                    with st.container():
                        self.display_points_table()
                    st.experimental_rerun()

                if not st.session_state[match_processed_key]:
                    all_matches_processed = False

                match_count += 1

        # Check if all matches are processed
        if all_matches_processed:
            st.success("Tournament Over")
            st.balloons()

                


    
    def display_schedule(self):
        teams = list(self.teams.keys())
        schedule_data = []
        match_count = 1
        for round in range(self.scheduler.rows * 2):
            for mc in range(self.scheduler.cols):
                i = self.scheduler.merged_table[round][mc][0]
                j = self.scheduler.merged_table[round][mc][1]
                if i == "bye" or j == "bye":
                    continue

                team1 = teams[i - 1]
                team2 = teams[j - 1]
                schedule_data.append({
                    "Match" : f"Match {match_count}",
                    "Team 1": team1,
                    "Team 2": team2,
                    "Ground": self.teams[team1].ground
                })

                match_count += 1
        schedule_df = pd.DataFrame(schedule_data)
        schedule_df.index = np.arange(1, len(schedule_df)+1)
        st.dataframe(schedule_df, width = 1000, hide_index = True)
        
                        
    # Method to display the points table.
    def display_points_table(self):
        self.point_table.display_table()
