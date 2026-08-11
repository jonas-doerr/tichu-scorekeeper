# TICHU SCOREKEEPER

This program tracks scores for the card game Tichu and stores the data from each game. It also (in the future) provides analysis on that data.

## Journal
### 7.31
I created the program and set up a file structure. Then I built a simulator that can play a full game of tichu (based on random results) and collect data. 

### 8.4
Changed the TichuGame class to accept a Round class instead of a lot of variables. I improved the Player() class and underlying logic to better record statistics. Improved debugging by adding __str__ attributes to each class.

### 8.5
Made a function to store player data in SQLite database. Learned a lot about SQLite (this is my first time using it). Also can store some game data now.

### 8.6
Struggling a lot with saving all of the different data into SQLite using object-oriented programming. Debugged a few things, like player_id not storing correctly, and now everything is being stored properly. Can begin with web app.

Made a framework for the website. Still non-functional. I need to add add_player functions, improve the interface, and then link it up to actually store data. 

### 8.7
Created the widgets for all necessary parts of the scorekeeper. It still does not store data accurately, but I debugged several issues that came up, as I improve my knowledge of Streamlit. 

I put in a lot more work on the streamlit interface. Now it has a sortable list for turn order, shows an updated score, and accurately tracks the game. Still need to store data in database accurately.

### 8.11
The round scoring wasn't working correctly, so I returned to my round storage logic and fixed it after debugging several things, like player objects not matching up because I put a list inside a list.

Then I spent a ton of time upgradiong the web app and creating statistics and new pages for the app. It is now nearly complete. At this point it is mostly repetitive, just pulling different data out of the database to make stats with. The hardest part was realizing I had nothing to record the teams players were on, so I deleted my database and made a new table with that information.

## To-do
- Games won stats
- Player addition
- Stats with different teammates?
- Undo button?
- Improve README
- Deploy