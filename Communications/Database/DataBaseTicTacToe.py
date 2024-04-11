import sqlite3
class Database:
    def __init__(self):
        self.conn = None
        self.player = None
        self.username = None
        self.password = None
        self.email = None
        self.win = None
        self.loss = None
        self.draw = None
        self.gameId = None
        self.date = None
        self.time = None
        self.moveId = None
        self.moveTime = None
        self.gameMode = None 
        self.difficulty = None
        self.PlayerTurnOrder = None
        self.playerPosX = None
        self.playerPosY = None
        
    def CommitAndSave(self):        
        if self.conn:
                self.conn.commit()
                self.conn.close() 
    def CreateDataBase(self):        
        try:                                    
            # Step 2: Connect to the database (or create it if it doesn't exist)
            self.conn = sqlite3.connect('C:\\Year2Sem2\\Bus\\Sem4BusProject-main3\\Sem4BusProject-main\\Communications\\Database\\TicTacToe.db')

            # Step 3: Create a cursor object
            self.cursor = self.conn.cursor()

            # Step 4: Execute SQL commands to create tables
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Player (
                                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                                username TEXT,
                                password TEXT,
                                email TEXT
                            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS metrics (
                                Playerid INTEGER,
                                win INTEGER,
                                loss INTEGER,
                                draw INTEGER,
                                FOREIGN KEY (Playerid) REFERENCES Player(id)
                            ) ''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Game (
                                gameId INTEGER PRIMARY KEY AUTOINCREMENT,
                                Playerid INTEGER,
                                date DATE,
                                time TIME,
                                FOREIGN KEY (Playerid) REFERENCES Player(id)
                            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS Move (
                                moveId INTEGER PRIMARY KEY,
                                Playerid INTEGER,
                                gameId INTEGER,
                                X INTEGER,
                                Y INTEGER,
                                moveTime DATE,
                                FOREIGN KEY (Playerid) REFERENCES Player(id),
                                FOREIGN KEY (gameId) REFERENCES Game(gameId)
                            )''')

            self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
                                Playerid INTEGER,
                                gameId INTEGER,
                                gameMode INTEGER,
                                difficulty TEXT,
                                PlayerTurnOrder INTEGER,
                                FOREIGN KEY (Playerid) REFERENCES Player(id),
                                FOREIGN KEY (gameId) REFERENCES Game(gameId)
                            )''')
            self.insertDataToTables() 
            rows = self.cursor.fetchall()
            print(rows)          
        finally:            
            print("Database created")            
    def insertDataToTables(self):
        self.cursor.execute('INSERT INTO Player (id, username, password, email) VALUES (?, ?, ?,?)',
                            (self.player,self.username,self.password,self.email)) 
        self.cursor.execute('INSERT INTO metrics (Playerid, win, loss, draw) VALUES (?, ?, ?, ?)',
                            (self.player,self.win,self.loss,self.draw))
        self.cursor.execute('INSERT INTO game (gameId, Playerid, date, time) VALUES (?, ?, ?,?)',
                            (self.gameId,self.player,self.date,self.time))
        self.cursor.execute('INSERT INTO settings (Playerid, gameId, gameMode, difficulty, PlayerTurnOrder) VALUES (?, ?, ? , ?, ?)',
                            (self.player,self.gameId,self.gameMode,self.difficulty,1)) 
        self.cursor.execute('INSERT INTO Move (moveId, Playerid, gameId, X,Y,moveTime) VALUES (?, ?, ?, ?, ?, ?)',
                            (self.moveId,self.player,self.gameId,self.playerPosX, self.playerPosY, self.moveTime)) 
        

    def sendDataToDatabase(self,data):
        self.player = data[0] #data[0] will always be the id of the current player
        self.username = data[1]
        self.password = data[2]
        self.playerPosX = data[3]
        self.playerPosY = data[4]   
        self.CreateDataBase()  
        #print(data)             
        
    def playerInformation(self):
        # Ensure the connection is open
        self.conn = sqlite3.connect('C:\\Year2Sem2\\Bus\\Sem4BusProject-main3\\Sem4BusProject-main\\Communications\\Database\\TicTacToe.db')
        self.cursor = self.conn.cursor()

        # Correct and execute the SELECT query
        self.cursor.execute('''
            SELECT p.id, m.win, m.loss, m.draw
            FROM Player AS p
            JOIN metrics AS m ON p.id = m.Playerid
            JOIN Game AS g ON p.id = g.Playerid
        ''')

        # Fetch and print the results
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)

        # Close the connection            
    def playerMoveRetrival(self):
        gameId = 123
        self.cursor.execute('''
            SELECT m.Playerid, X, Y, moveTime
            FROM Move AS m
            JOIN Game AS g ON m.gameID = g.gameId
            WHERE g.gameId = ?
            ORDER BY moveTime
            ''', (gameId,))
def SendData():
    db = Database()
    db.CreateDataBase()  # Create tables if they don't exist
    db.insertDataToTables()  # Insert sample data    
    db.playerInformation()  # Retrieve and print player information
    db.playerMoveRetrival()  # Retrieve and print move details
    db.CommitAndSave()  # Close the database connection
SendData()

#Game mode, 1 for single player, 2 for multiplayer. 
#Difficulty = weak , strong.
#player turn order = 1  for player 1, 2 for player 2, 3 for ai.     
#Game ID will incremnet by 1.       
#Move id will need to be set manually, The game id will be needed to be linked to the each move to differentiate between the which move is linked to each game.