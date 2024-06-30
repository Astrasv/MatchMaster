from Structures.Graph import Graph
import streamlit as st

# Initialize the graph in session state if not already initialized
if 'graph' not in st.session_state:
    st.session_state.graph = Graph()
    st.session_state.page = "Teams"

imcol1,imcol2,imcol3 = st.columns(3)
with imcol2:
    st.image('./images/MatchMaster.png',use_column_width="auto")
st.markdown("""
<h1 style="text-align:center">The Tournament Scheduler</h1>

""", 
unsafe_allow_html=True)
def team_input():
    graph = st.session_state.graph
    # Getting the number of teams and their names from the user.
    st.write("______________________________________________")
    st.warning("Enter number of teams")
    number_of_teams = st.number_input("Number of teams:", min_value=3, step=1)
    st.write("______________________________________________")
    teams = [None for _ in range(number_of_teams)]
    col1, col2 = st.columns(2)

    with col1:
        st.info("Enter team name")
    with col2: 
        st.success("Enter Ground name")
        
    for i in range(number_of_teams):
        with col1:
            team = st.text_input(f"Team{i+1}", key=f"team{i}")
        with col2:
            ground = st.text_input(f"Ground{i+1}", key=f"ground{i}")
        teams[i] = (team, ground)

    for team, ground in teams:
        if team and ground:
            graph.add_team(team, ground)

    if st.button("Proceed to Matches"):
        st.session_state.page = "Matches"
        st.experimental_rerun()

def match_input():
    graph = st.session_state.graph
    # Generating match edges and simulating matches.
    graph.generate_matches()
    graph.display_points_table()


    graph.generate_edges()

def point_table():
    graph = st.session_state.graph
    graph.display_points_table()

def schedule():
    graph = st.session_state.graph
    graph.generate_matches()
    graph.display_schedule()

pages = {
    "Teams": team_input,
    "Match Results": match_input,
    "Match Schedule": schedule,
    "Points Table" : point_table,
}

# Hide the "Teams" page from sidebar after navigating to "Matches"
if st.session_state.page == "Teams":
    selection = "Teams"
else:
    st.sidebar.image('./images/MatchMaster.png',use_column_width="auto")
    st.sidebar.info("Navigate To")
    selection = st.sidebar.radio("", ["Match Results", "Match Schedule", "Points Table"], index=0)

# Call the selected page function
pages[selection]()
