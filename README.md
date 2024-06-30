# Tournament Scheduler

## Overview

The Tournament Scheduler is a Python-based application that allows users to manage and simulate a sports tournament. This application provides functionalities for adding teams, scheduling matches, simulating results, and displaying a points table. The project is structured to make use of various data structures like stacks, deques, and graphs for efficient handling and simulation of tournament data. The project has now been converted into a Streamlit web application for an enhanced user interface and experience.

## Features

- **Add Teams:** Users can add teams along with their home grounds.
- **Schedule Matches:** Matches are scheduled in a round-robin format using a custom scheduling algorithm.
- **Simulate Matches:** Users can input match results to simulate the tournament.
- **Points Table:** Displays the points table sorted by team performance.
- **Last Five Matches:** Shows the last five matches played by each team.

## Project Structure

```plaintext
Root
├── Structures (Folder)
│   ├── Dequeue.py
│   ├── Graph.py
│   ├── PointsTable.py
│   ├── Scheduler.py
│   └── Stack.py
├── Tournament.py
├── README.md
└── streamlit_app.py
```

### File Descriptions

- **Tournament.py:** Main script to run the tournament simulation.
- **Structures/Graph.py:** Contains the `Graph` class to manage teams and matches.
- **Structures/PointsTable.py:** Manages the points table for the tournament.
- **Structures/Scheduler.py:** Schedules matches using a round-robin algorithm.
- **Structures/Stack.py:** Implements a stack data structure for storing match results.
- **Structures/Dequeue.py:** Implements a deque data structure used in the scheduler.
- **streamlit_app.py:** Streamlit application script for the web interface.

## Data Structures Used

- **Stack:** Used to store the last five matches of a team.
- **Deque:** Used in the match scheduling algorithm.
- **Graph:** Represents the tournament structure, with teams as nodes and matches as edges.

## Setup and Installation

1. **Clone the Repository:**
    ```sh
    git clone https://github.com/your-username/tournament-scheduler.git
    cd tournament-scheduler
    ```

2. **Install Dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Streamlit Application:**
    ```sh
    streamlit run streamlit_app.py
    ```

Replace `your-username` with your GitHub username in the clone URL.

This project provides a comprehensive way to organize and simulate tournaments using Python, leveraging fundamental data structures and a streamlined web interface for ease of use.
