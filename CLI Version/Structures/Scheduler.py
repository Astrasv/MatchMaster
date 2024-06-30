from .Dequeue import Deque

class Scheduler:
    def __init__(self, teams) -> None:
        self.teams = teams
        self.n = self.teams if self.teams % 2 == 0 else self.teams + 1
        self.totalmatches = (self.n // 2) * (self.n - 1) if self.teams % 2 == 0 else ((self.n // 2) - 1) * (self.n - 1) 
        self.table1 = []
        self.table2 = []
        self.merged_table = []
    
    def generate_table1(self):
        n_half = self.n // 2
        num_rows = self.n - 1
        sequence = Deque()
        sequence.range_queue(1 , num_rows + 1)
        
        self.table1 = []
        for _ in range(num_rows):
            row = []
            for _ in range(n_half):
                row.append(sequence.peek_front())
                sequence.rotate_left()
            self.table1.append(row)
    
    def generate_table2(self):
        num_rows = self.n - 1
        self.table2 = []
        
        for i in range(num_rows):
            next_row = self.table1[(i + 1) % num_rows]
            reversed_row = next_row[::-1]
            self.table2.append(reversed_row)
    
    def merge_tables(self):
        self.merged_table = []
        for row1, row2 in zip(self.table1, self.table2):
            merged_row = [(cell1, cell2) for cell1, cell2 in zip(row1, row2)]
            self.merged_table.append(merged_row)
        
        # Reorder rows: odd rows first, then even rows
        odd_rows = [self.merged_table[i] for i in range(len(self.merged_table)) if i % 2 == 0]
        even_rows = [self.merged_table[i] for i in range(len(self.merged_table)) if i % 2 != 0]
        self.merged_table = odd_rows + even_rows
    
    def update_first_column(self):
        
        player_or_bye = self.n if self.teams%2 == 0 else "bye"
            
        for i in range(len(self.merged_table)):
            if i % 2 == 0:
                self.merged_table[i][0] = (player_or_bye, self.merged_table[i][0][1])
            else:
                self.merged_table[i][0] = (self.merged_table[i][0][0], player_or_bye)
    
    def new_face_off(self):
        second_table = []
        for row in self.merged_table:
            new_row = []
            for match in row:
                new_row.append((match[1],match[0]))
            
            second_table.append(new_row)
        
        self.merged_table += second_table
                
    
    def generate(self):
        self.generate_table1()
        self.generate_table2()
        self.merge_tables()
        self.update_first_column()
        self.new_face_off()

