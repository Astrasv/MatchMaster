# Defining a class to represent the points table.

class PointTable:
    def __init__(self):
        self.table = []

    # Method to add a team to the points table.
    def add_team(self, team):
        self.table.append(team)

    # Helper method for quicksort partitioning.
    def partition(self, arr, low, high):
        pivot = arr[high].points
        i = low - 1
        for j in range(low, high):
            if arr[j].points > pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    # Method to sort teams by points using quicksort.
    def sort_by_points(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.sort_by_points(arr, low, pi - 1)
            self.sort_by_points(arr, pi + 1, high)

    # Method to display the points table.
    def display_table(self):
        print("Points Table:")
        print("{:<20} {:<10} {:<10} {:<10} {:<10} {:<20}".format("Team", "Matches", "Wins", "Loses","Points","Last (5/Less) Matches"))
        
        # Inplace sort in descending order of team points
        self.sort_by_points(self.table , 0 , len(self.table) - 1)
        
        if len(self.table) <= 1:
            print("\t\tWe need atleast 2 teams to generate Points table")
            return
        elif len(self.table) == 2:
            print("\t\t  No need of points table. Its a knockout match")
            return

            
        for team in self.table:
            last_five_matches_stack = team.get_last_five_matches()
            
            # Store last 5 matches result as a string
            last_five_matches = ""
            
            # Concatinate to the string till stack is empty
            while not last_five_matches_stack.is_empty():
                popped = last_five_matches_stack.pop()
                opponent = popped.opponent
                result = popped.result
                last_five_matches += f"{opponent}({result})  "
                
            print("{:<20} {:<10} {:<10} {:<10} {:<10}  {:<20}".format(team.name, team.matches ,team.wins, team.loses,team.points, last_five_matches))
