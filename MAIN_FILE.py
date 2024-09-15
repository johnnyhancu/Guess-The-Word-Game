import random
from words import words
from tkinter import *
import string
import time
import threading

win = Tk()
win.title("GUESS THE WORD")
win.geometry("1100x600")
#Below I define the initial labels and buttons displayed on the window. The user will choose a mode by clicking a button
Label1=Label(win,text="This game can be played by 1,2 or 3 players.\n Make your choice by clicking the corresponding button", font="Raleway, 15")
Label1.grid(row=0, column=0, padx= 10, pady=20)
Button1=Button(win, text="1 player", font="Raleway, 14", padx=8, pady=7, command=lambda: single_player())
Button1.grid(row=1, column=0, padx= 10, pady=10)
Button2=Button(win, text="2 players", font="Raleway, 14", padx=8, pady=7, command=lambda: play(2))
Button2.grid(row=2, column=0, padx= 10, pady=10)
Button3=Button(win, text="3 players", font="Raleway, 14", padx=8, pady=7, command=lambda: play(3))
Button3.grid(row=3, column=0, padx= 10, pady=10)
Label1=Label(win,text="Clicking the following button will start a computer simulation mode, \n simulating the game being played by 3 players", font="Raleway, 15")
Label1.grid(row=4, column=0, padx= 10, pady=20)
Button4=Button(win, text="Computer Simulation Mode", font="Raleway, 14", padx=8, pady=7, command=lambda: simulation_mode())
Button4.grid(row=5, column=0, padx= 10, pady=10)

#This function, when called, creates the current state of the word, letters that are not guessed yet are substituted with '_'
def get_current_word():
    current_word =''
    for letter in word:
        if letter in used_letters:
            current_word += letter
        else:
            current_word += "_ "
    return current_word

#The next function generates a 'template' for a new game. 
#It defines all the main elements that can be used in all operating modes, starting with selecting a new random word
def new_game():
    global word, word_letters, used_letters, word_to_guess, Wrong_guesses, Wrong_guesses_label,InfoLabel,alphabet,LettersFrame, letter_buttons, players, players_label 
    word = random.choice(words).upper()     #Here the word to be guessed is randomly selected

    word_letters = set(word)       #This creates the set of the letters of the word

    used_letters = set()        #This creates the set of the guessed letters

    #Here I create a label which will show the word to be guessed (letters that are not guessed yet are substituted with _)
    word_to_guess = Label(win, width=40, font="Raleway, 24")

    InfoLabel=Label(win, text='', font=('Helvetica, 18'))#This label will tell if the guessed letter 
                                    #is in the word or not, also will show whose player is the turn

    Wrong_guesses_label=Label(win, text=f"Wrong guesses=0", font=('Helvetica, 18'))  #This label will show the number of wrong guesses

    alphabet = list(string.ascii_uppercase)   #This creates the list of the letters of alphabet (in uppercase)
    current_word=str(get_current_word())
    word_to_guess["text"]=f"The Word to Guess ({len(word)} letters):   {current_word}"

    players=['Player 1', 'Player 2', 'Player 3']
    players_label=[]
    for n in range(3):
        players_label.append(Label(win, width=25,text=players[n], font="Raleway, 12",bg="white"))
    
    Wrong_guesses=0 
    
    #Here a Frame is created that will contain the buttons for the letters 
    LettersFrame=LabelFrame(win)
    LettersFrame.grid(row=1,column=1,padx=10)
    
    #Here the letter-buttons are defined and placed in the Frame we just created
    letter_buttons=[]    
    for letter in alphabet:
        letter_buttons.append(Button(LettersFrame, text=letter, padx=8, pady=7,))
    
    for k in range(13):
        letter_buttons[k].grid(row=2, column=k,padx=5,pady=5)

    for k in range(13,26):
        letter_buttons[k].grid(row=3, column=k-13,padx=5,pady=5)

#This defines the function that will clear the window
def clear_window():
   for widgets in win.winfo_children():
      widgets.destroy()

#This function when called will display the options to play again (1,2 or 3 players, or simulation mode). 
#Also displays the option to End/Quit
def play_again_options():
    Play_again_Frame=LabelFrame(win)
    Play_again_Frame.grid(row=6,column=0, columnspan=4, pady=20)
    Label(Play_again_Frame, text ="To play again choose an option below or click End to quit",font=('Helvetica, 16')).grid(row=0, column=0, columnspan=4, padx= 5, pady=20)
    Button(Play_again_Frame, text="1 player", font="Raleway, 14", padx=8, pady=7, command=lambda: single_player()).grid(row=1, column=0, padx= 10, pady=10)
    Button(Play_again_Frame, text="2 players", font="Raleway, 14", padx=8, pady=7, command=lambda: play(2)).grid(row=1, column=1, padx= 10, pady=10)
    Button(Play_again_Frame, text="3 players", font="Raleway, 14", padx=8, pady=7, command=lambda: play(3)).grid(row=1, column=2, padx= 10, pady=10)
    Button(Play_again_Frame, text="Computer Simulation Mode", font="Raleway, 14", padx=8, pady=7, command=lambda: simulation_mode()).grid(row=1, column=3, padx= 10, pady=10)
    Button(Play_again_Frame, text="END", font="Raleway, 14", padx=8, pady=7, command=lambda: quit()).grid(row=1, column=4, padx= 10, pady=10)

#THIS IS THE SECTION OF CODE FOR THE SINGLE PLAYER MODE
def single_player():
    
    clear_window()
    new_game()
    word_to_guess.grid(row=0, column=1, pady=20) 
      
    InfoLabel.grid(row=4, column=1, pady=20)
    InfoLabel["text"]=f"Try to guess the word, guessing a letter at a time by clicking on the corresponding button.\nThe chalenge is to get as less wrong guesses as you can.\nGetting no more than 5 wrong guesses is excelent, \n 6-7 is very good, 8-10 is good, more than 10 is not that good"
    Wrong_guesses_label.grid(row=5,column=1, pady=20)
    
    #Below I define what happens when the user clicks a letter-button in Single Player Mode
    for n in range(26):
        letter_buttons[n]["command"]=lambda letter=alphabet[n]: click(letter)

    def click(letter):    
        index = alphabet.index(letter)
        letter_buttons[index].destroy()
        global Wrong_guesses
        if letter in word:
            word_letters.remove(letter)
            used_letters.add(letter)
            current_word=str(get_current_word())
            word_to_guess["text"]=f"The Word to Guess ({len(word)} letters): {current_word}"
            InfoLabel.config(text=f'Good guess, keep going!')
            if len(word_letters)==0:
                InfoLabel.config(text=f'Hurray, you guessed the word!')
                file = open("Stats_Human_Players.csv", "a")
                file.write(f",{Wrong_guesses}")
                file.close()
                play_again_options()
        else:
            Wrong_guesses+=1
            InfoLabel["text"]=f"Wrong guess, letter {letter} is not in the word!\n continue with your next guess"
            Wrong_guesses_label["text"]=f"Wrong guesses={Wrong_guesses}" 



#THE NEXT SECTION CONTAINS THE CODE  FOR 2 OR 3 PLAYERS MODE
def play(num):    
    clear_window()    
       
    Pl_label=Label(win, text="Enter the Players' Names Below and then press the Start Button:", font="Raleway, 12")
    Pl_label.grid(row=0, column=0, padx= 10, pady=20)

    #Here I create the input fields for the players names   
    
    players_input=[]
    for n in range(num):
        players_input.append(Entry(win, width=25, font="Raleway, 12"))

    for n in range(num):
        players_input[n].grid(row=n+1, column=0, padx=40, pady=20)

    #Here, the start-button for this mode is created. Clicking on it will start the game
    button_start = Button(win, text="Start", font="Raleway, 12", padx=20, command=lambda: start())
    button_start.grid(row=5, column=0, padx=10, pady=20)
  
  
    # Here I define the start() function for the command in the start-button defined above.  
    def start():
        button_start.destroy()
        new_game()
        global players, players_label
        
        #Here we check if the users entered there names, then we change the players names accordingly,
        #otherwise, the default names Player 1, Player 2 or Player 3 will be kept
        for n in range(num):
            if players_input[n].get()!="":
                players[n]=players_input[n].get()
                players_label[n]["text"]=players_input[n].get()    
        
        for n in range(num):
            players_input[n].grid_forget()
            players_label[n].grid(row=n+1, column=0, padx=40, pady=20)
        
        Pl_label["text"]="Players' Names:"
        players_label[0]["bg"]="Yellow"
        
        global word_to_guess, Wrong_guesses_label, InfoLabel, current_player, players_index
        word_to_guess.grid(row=0, column=1, columnspan=13, pady=20)        
        
        Wrong_guesses_label.grid(row=5, column=0,pady=20)
        InfoLabel.grid(row=5,column=1,columnspan=13,pady=20)
        
        current_player = players[0]
        players_index=0
        InfoLabel.config(text=f"{current_player}'s turn")    

        for n in range(26):
            letter_buttons[n]["command"]=lambda letter=alphabet[n]: click(letter)   
          
      
   
    #This function defines the instructions for the command function in the letter-buttons
    def click(letter):    
        index = alphabet.index(letter)  #this gets the index of the letter in the alphabet to be used in the next line of code
        letter_buttons[index].destroy() #Here the corresponding letter-button is removed from screen
        global Wrong_guesses, players_index, current_player #declares that we are using the corresponding global variables,not local
        if letter in word:  #this checks if the letter is in the word and if it is, the following block of code is executed
            word_letters.remove(letter) #removes the letter from the set of word_letters
            used_letters.add(letter)  #adds the letter to the set of used letters
            current_word=str(get_current_word()) #gets the current word which will have all the correctly guessed letters
            word_to_guess["text"]=f"The Word to Guess ({len(word)} letters): {current_word}" #displays the guessed letters
            InfoLabel["text"]=f'Good guess {current_player}, keep going!' #informs the player that the guess was correct
            if len(word_letters)==0:   #This means that the word is guessed 
                InfoLabel["text"]=f'Hurray, {current_player} is the winner!' #declares the winner
                file = open("Stats_Human_Players.csv", "a")  #Opens the the csv file Human_Players_Stats.csv in append mode
                file.write(f",{Wrong_guesses}") #This writes the number of wrong guesses to the csv file
                file.close()  #closes the file
                if num == 3:  #For the '3 players' mode I record the index of the winning player)
                    file = open("Winners_humans_3players.csv", "a")
                    file.write(f",{players_index + 1}")  #instead of recording 0,1 or 2, I record 1,2 or 3 respectively
                    file.close()
                play_again_options()  #displays the options to play again or quit
                
        else:  #if the letter is not in the word then the following instructions are executed
            previous_player = players[players_index] #before changing the current player I need to store the previous player
            previous_players_index=players_index   #and it's index in the players list
            players_index=(players_index+1)%num #to change the current player, we first calculate its index in the list
            current_player = players[players_index]  #and then we use this index to change the current player
            InfoLabel["text"]=f"Wrong guess, {previous_player}!\n Letter {letter} is not in the word!\n It's now {current_player}'s turn!"
            players_label[previous_players_index]["bg"]="White" # previous player colour is changed back to white
            players_label[players_index]["bg"]="Yellow"   #highlights the current player           
            Wrong_guesses+=1  #increases the number of wrong guesses
            Wrong_guesses_label["text"]=f"Wrong guesses={Wrong_guesses}" #displays the updated number of wrong guesses



#THIS SECTION CONTAINS THE CODE FOR THE COMPUTER SIMULATION MODE

def simulation_mode():    
    clear_window()
    new_game()    
    Label(win, text="This is a simulation game:", font="Raleway, 12").grid(row=0, column=0, padx= 10, pady=20)
       
    word_to_guess.grid(row=0, column=1, columnspan=13, pady=20)     
    
    InfoLabel.grid(row=5,column=1,columnspan=13)
       
    #The next function defines the instructions for the simulation mode with time delays
    # It's execution is triggered in a separate thread so that the whole process can be watched. 
    #If the function is not executed in a separate thread, then it executes all the instructions 
    # without showing the whole process, but only displaying the result: the guessed word and the winner  
    
    
    def simulation():
        global players, current_player, players_index, k
        
        for n in range(3):
            players_label[n].grid(row=n+1, column=0, padx=40, pady=20)
            players_label[n]["text"]=players[n]
            players_label[n]["bg"]="White"
        
        current_player = players[0]
        players_index=0        
        available_letters=list(alphabet)
        InfoLabel["text"]=f"{current_player}'s turn"
        players_label[0]["bg"]="Green"
        Wrong_guesses_label.grid(row=5,column=0, pady=20)
        time.sleep(0.5)

        def next_guess():
            letter=random.choice(available_letters)            
            index = alphabet.index(letter)
            letter_buttons[index]["bg"]="Red"
            time.sleep(0.5)
            index = alphabet.index(letter)
            letter_buttons[index].destroy()
            available_letters.remove(letter)
            global Wrong_guesses, players_index, current_player, k
            if letter in word:
                current_player = players[players_index]
                word_letters.remove(letter)
                used_letters.add(letter)
                current_word=str(get_current_word())
                word_to_guess["text"]=f"The Word to Guess ({len(word)} letters): {current_word}"
                word_to_guess.grid(row=0, column=1, columnspan=13, pady=20)
                InfoLabel["text"]=f'Correct guess, {current_player} continues guessing!'
                if len(word_letters)==0:
                    InfoLabel["text"]=f'The word is guessed, {current_player} is the winner!'
                    file = open("Stats_Simulation_mode.csv", "a")
                    file.write(f",{Wrong_guesses}")
                    file.close()
                    file1 = open("Winners_Simulation_Mode.csv", "a")
                    file1.write(f",{players_index + 1}")   #instead of recording 0,1 or 2, I record 1,2 or 3 respectively
                    file1.close()
                    play_again_options()                    

            else:
                previous_players_index = players_index
                players_index=(players_index+1)%len(players)
                current_player = players[players_index]
                InfoLabel["text"]=f"Letter {letter} is not in the word!"
                time.sleep(0.5)
                InfoLabel["text"]=f"It's now {current_player}'s turn!"
                players_label[previous_players_index]["bg"]="White"
                players_label[players_index]["bg"]="Green"
                Wrong_guesses+=1
                Wrong_guesses_label["text"]=f"Wrong guesses={Wrong_guesses}" 
        while len(word_letters)>0:
            next_guess()
            time.sleep(0.5)    

    #Here the 'simulation' function is called in a separate thread
    x=threading.Thread(target=simulation, args=())
    x.start() 
    
win.mainloop()




