# TICHU SCOREKEEPER

This program tracks scores for the card game Tichu and stores the data from each game. It also (in the future) provides analysis on that data.

### 7.31
I created the program and set up a file structure. Then I built a simulator that can play a full game of tichu (based on random results) and collect data. 

### 8.4
Changed the TichuGame class to accept a Round class instead of a lot of variables. I improved the Player() class and underlying logic to better record statistics. Improved debugging by adding __str__ attributes to each class.

### 8.5
Made a function to store player data in SQLite database.

## To-do
-Add save/load with SQLite
-Make Streamlit interface
-Add charts/analysis
-Deploy