# TICHU SCOREKEEPER

This program tracks scores for the card game Tichu and stores the data from each game. It also (in the future) provides analysis on that data.

### 7.31
I created the program and set up a file structure. Then I built a simulator that can play a full game of tichu (based on random results) and collect data. 

### 8.4
Changed the TichuGame class to accept a Round class instead of a lot of variables. I improved the Player() class and underlying logic to better record statistics. Improved debugging by adding __str__ attributes to each class.

### 8.5
Made a function to store player data in SQLite database. Learned a lot about SQLite (this is my first time using it). Also can store some game data now.

### 8.6
Struggling a lot with saving all of the different data into SQLite using object-oriented programming. Debugged a few things, like player_id not storing correctly, and now everything is being stored properly. Can begin with web app.

Made a framework for the website. Still non-functional. I need to add add_player functions, improve the interface, and then link it up to actually store data. 

## To-do
- Make Streamlit interface
- Add charts/analysis
- Deploy