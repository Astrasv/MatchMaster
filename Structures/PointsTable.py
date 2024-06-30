# PointsTable.py
import streamlit as st
import pandas as pd
import numpy as np

class PointTable:
    def __init__(self):
        self.table = []

    def add_team(self, team):
        self.table.append(team)

    def partition(self, arr, low, high):
        pivot = arr[high].points
        i = low - 1
        for j in range(low, high):
            if arr[j].points > pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def sort_by_points(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.sort_by_points(arr, low, pi - 1)
            self.sort_by_points(arr, pi + 1, high)

    def display_table(self):
        if len(self.table) <= 1:
            st.write("We need at least 2 teams to generate Points table")
            return
        elif len(self.table) == 2:
            st.write("No need of points table. It's a knockout match")
            return

        self.sort_by_points(self.table, 0, len(self.table) - 1)

        data = {
            "Team": [],
            "Matches": [],
            "Wins": [],
            "Loses": [],
            "Points": [],
            "Last (5/Less) Matches": []
        }

        for team in self.table:
            last_five_matches_stack = team.get_last_five_matches()
            last_five_matches = ""
            
            while not last_five_matches_stack.is_empty():
                popped = last_five_matches_stack.pop()
                opponent = popped.opponent
                result = popped.result
                last_five_matches += f"{opponent}({result})  "
            
            data["Team"].append(team.name)
            data["Matches"].append(team.matches)
            data["Wins"].append(team.wins)
            data["Loses"].append(team.loses)
            data["Points"].append(team.points)
            data["Last (5/Less) Matches"].append(last_five_matches)

        df = pd.DataFrame(data)
        df.index = np.arange(1, len(df)+1)
        st.dataframe(df, width = 1000, hide_index = True)