
import random



class minesweeper_game():

    def __init__(self,n_mines=5,board_size=[5,5]):
        
        minelist=[True]*n_mines+[False]*(board_size[0]*board_size[1]-n_mines)
        random.shuffle(minelist)
        self.board_size=board_size

        self.flags=0
        self.correct_flags=0

        self.game_over=False


        #Generate bord
        self.board={}
        self.numbers_of_mines=0
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):

                #Assing mines
                mine_bool= minelist[i*board_size[1]+j]
                
                if mine_bool:
                    self.numbers_of_mines+=1

                #Define datastructure
                self.board[(i,j)]={"mine": mine_bool, "number":0,"flag":False, "checked":False}

        #Find all numbers
        for i in range(self.board_size[0]):
            for j in range(self.board_size[1]):
                self.count_mines((i,j))

    def count_mines(self,cordinate):
        n=0
        for i in range(cordinate[0]-1,cordinate[0]+2):
            for j in range(cordinate[1]-1,cordinate[1]+2):
                #Check if cordinate is in bord
                if self.board.get((i,j),{"mine":False})["mine"]:
                    n+=1
                    
        #update board
        self.board[cordinate]["number"]=n
        return n


    def check(self,cordinate):

        #Check cordinate return True if mine
        self.seach(cordinate)
        return self.board[cordinate]["mine"]

    def flag(self,cordinate):

        if self.board[cordinate]["flag"]:
            self.board[cordinate]["flag"]=False
            self.flags-=1
            if self.board[cordinate]["mine"]:
                self.correct_flags-=1
                
        else:
            self.board[cordinate]["flag"]=True
            self.flags+=1
            if self.board[cordinate]["mine"]:
                self.correct_flags+=1

        return self.correct_flags==self.numbers_of_mines and self.correct_flags==self.flags
    
    def seach(self,cordinate):
        #an recusive function that reval field that are next to 0
        self.board[cordinate]["checked"]=True
        
        if self.board[cordinate]["number"] == 0:
        
            for i in range(cordinate[0]-1,cordinate[0]+2):
                for j in range(cordinate[1]-1,cordinate[1]+2):
                    #Check if cordinate is in bord
                    if (self.board.get((i,j),{"checked":True})["checked"] != True):
                        self.seach((i,j))
            
        

import tkinter as tk
 
class UI(tk.Tk):
    def __init__(self,game):
        self.game=game
        super(UI,self).__init__()
 
        self.title("Minesweaper")
        self.minsize(100*self.game.board_size[0],100*self.game.board_size[1])

        #intitalise board
        for i in range(self.game.board_size[0]):
            for j in range(self.game.board_size[1]):
                button=tk.Frame(self, width=100, height=100, bg="gray",relief="solid") #Initialize button
                button.grid(row=i,column=j,padx=2,pady=2) #Place buttons in grid
                tk.Label(button,text="",bg="gray").place(x=45,y=45)
                
                button.ID=(i,j)
                button.bind("<Button-1>",self.check) #check on right click
                button.bind("<Button-3>",self.flag) #Flag on left click
                game.board[(i,j)]["button"]=button
                
    def update_board(self):
        for i in range(self.game.board_size[0]):
            for j in range(self.game.board_size[1]):
                if self.game.board[(i,j)]["checked"]:
                    if self.game.board[(i,j)]["mine"]:
                        button=tk.Frame(self, width=100, height=100, bg="red",relief="solid") #Initialize button
                        button.grid(row=i,column=j,padx=2,pady=2) #Place buttons in grid
                        tk.Label(button,text="M",bg="red").place(x=45,y=45)

                    else:
                        button=tk.Frame(self, width=100, height=100, bg="green",relief="solid") #Initialize button
                        button.grid(row=i,column=j,padx=2,pady=2) #Place buttons in grid
                        tk.Label(button,text=self.game.board[(i,j)]["number"],bg="green").place(x=45,y=45)
                elif self.game.board[(i,j)]["flag"]:
                    button=tk.Frame(self, width=100, height=100, bg="white",relief="solid") #Initialize button
                    button.grid(row=i,column=j,padx=2,pady=2) #Place buttons in grid
                    tk.Label(button,text="F",bg="white").place(x=45,y=45)
                else:
                    button=tk.Frame(self, width=100, height=100, bg="gray",relief="solid") #Initialize button
                    button.grid(row=i,column=j,padx=2,pady=2) #Place buttons in grid
                    tk.Label(button,text="",bg="gray").place(x=45,y=45)
                
                button.ID=(i,j)
                button.bind("<Button-1>",self.check) #check on right click
                button.bind("<Button-3>",self.flag) #Flag on left click
                game.board[(i,j)]["button"]=button

    def flag(self,event):

        won=self.game.flag(event.widget.ID)
        self.update_board()

        if won:
            self.end_game(True)

    def check(self,event):
        
        ID=event.widget.ID
        lost=self.game.check(ID)

        self.update_board()

        if lost:
            self.end_game(False)

    
    def end_game(self,player_won):
        top= tk.Toplevel(self)
        top.geometry("300x100")
        top.title("Game Over")
        if player_won:
            tk.Label(top, text= "You won").place(x=10,y=10)
        else:
            tk.Label(top, text= "You lost").place(x=10,y=10)
            
    

 
#Game loop
game=minesweeper_game()
root = UI(game)
root.mainloop()
