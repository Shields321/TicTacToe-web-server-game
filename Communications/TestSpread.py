import gspread
import webbrowser
from oauth2client.service_account import ServiceAccountCredentials
class SpreadSheet:
    def __init__(self):
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
        self.moveIndex = 1        
        self.spreadsheetId = None
        self.client = None
        self.gameId = 1
        self.game_id = None
        self.email =None
    def createSpreadsheet(self):
        self._createSpreadsheet()
    def openSpreadsheet(self):
        url = f'https://docs.google.com/spreadsheets/d/{self.spreadsheetId}'
        return url        
    def resetMoveIndex(self):
        self._resetMoveIndex()
    
    def _createSpreadsheet(self):
        # Define the scope and credentials
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('C:\\Year2Sem2\\Bus\\Sem4BusProject-main3\\Sem4BusProject-main\\Communications\\charged-ground-419314-e4fe99cb9076.json', scope)

        # Authorize the client
        self.client = gspread.authorize(creds)

        # Check if the spreadsheet exists
        try:
            # Try to open the existing spreadsheet
            existing_spreadsheet = self.client.open('My New Spreadsheet')            
            self.spreadsheetId = existing_spreadsheet.id                       
            print("Spreadsheet 'My New Spreadsheet' already exists. Opening it...")
        except gspread.SpreadsheetNotFound:
            # If the spreadsheet doesn't exist, create a new one
            print("Spreadsheet 'My New Spreadsheet' does not exist. Creating it...")
            new_spreadsheet = self.client.create('My New Spreadsheet')
            self.spreadsheetId = new_spreadsheet.id
            # Share the spreadsheet with anyone with the link so that after the link can be displayed on the hosts machine
            self.client.insert_permission(self.spreadsheetId, None, perm_type='anyone', role='writer')
            print("Spreadsheet created successfully.") 
              
        #when starting the game initialize the header names
        sheet = self.client.open_by_key(self.spreadsheetId).sheet1
        first_row_data = ["Game id","Move id", "Player id", "Username","Email", "Password", "X Position", "Y Position"]
        for col, value in enumerate(first_row_data, start=1):
            sheet.update_cell(1, col, value)
            
        # Retrieve the current gameId from the spreadsheet        
        sheet = self.client.open_by_key(self.spreadsheetId).sheet1
        self.game_id = sheet.col_values(1)[2:]  # Skip header row 
        self.game_id = max(map(int, self.game_id))
        if isinstance(self.game_id,int):
            self.game_id +=1
        else:
            self.game_id = 1
                                                                                                     
    def _Insert(self):  
                                           
        if self.spreadsheetId:  
            try:                      
                # Open the spreadsheet
                sheet = self.client.open_by_key(self.spreadsheetId).sheet1            
                # Data to be sent
                data = [self.game_id,self.moveIndex ,self.player, self.username,self.email, self.password, self.playerPosX, self.playerPosY]
                self.moveIndex += 1            
                # Append the data to the first empty row in the spreadsheet
                sheet.append_row(data)
            except Exception:
                print("an error happened when entering the data into the spreadsheet")                                    
        else:
            print("No spreadsheet exists. Please create one first.")
            
    def _openSpreadsheet(self):
        url = f'https://docs.google.com/spreadsheets/d/{self.spreadsheetId}'
        webbrowser.open(url)
        
    def _resetMoveIndex(self):
        self.moveIndex = 0
        
    def sendDataToSpreadSheet(self, data):
        self.player = data[0]  # data[0] will always be the id of the current player
        self.username = data[1]
        self.email = data[2]
        self.password = data[3]
        self.playerPosX = data[4]
        self.playerPosY = data[5]   
        self._Insert()