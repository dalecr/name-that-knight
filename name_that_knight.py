''' name_that_knight.py
  --- A simple hangman game that I made to learn to use Tkinter
  --- Created by Connor Dale
'''

from random import randint
from tkinter import*
from PIL import ImageTk,Image

class Hangman(Frame):

	def __init__(self, master=None):

		super().__init__(master)

		master.title("Name That Knight")
		self.grid()
		
		# Picks a word at random
		self.word = []
		self.choose_word()
		self.displayList = []
		self.get_display_list() # parts of the word that the user sees
		self.strikes = 0  # number of incorrect guesses

		# Parts of the word that have been guessed are displayed
		self.displayWord = StringVar()
		self.update_display_word()
		knownLetters = Label(master, textvariable=self.displayWord)
		knownLetters.config(font=("Courier",42))
		knownLetters.grid(row=0, column=1, columnspan=100)

	# BUTTONS FOR ENTERING LETTERS
		self.buttonList = [] # contains all of the buttons for guessing letters
		letters = ["A","B","C","D","E","F","G","H","I","J","K","L","M",
			"N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
		r=1 # row position of button
		c=0 # column position of button
		for i in range(len(letters)):
			name = letters[i]
			button = Button(master, bg="White", text=name, width=5, height=1, relief=GROOVE,
                    command=lambda index=i, name=name: self.click_button(index,name))
			# draws the button
			if c<7:
				c+=1
			else:
				r+=1
				c=1
			button.grid(padx=2, pady=2, row=r, column=c) 
			
			# adds the new button to the list of buttons
			self.buttonList.append(button) 

		# make spacing consistent for alphabet buttons
		for col in range(1,7):
		    master.grid_columnconfigure(col, minsize=20)

		for row in range(1,4):
		    master.grid_rowconfigure(row, minsize=20)

	# BUTTONS FOR ENDING THE GAME/STARTING A NEW GAME
		self.replayButton = Button(master, bg="White", text="YES", width=5, height=2, relief=GROOVE,
                    command=lambda choice="yes": self.play_again(choice))
		self.endButton = Button(master, bg="White", text="NO", width=5, height=2, relief=GROOVE,
                    command=lambda choice="no": self.play_again(choice))

		# Label for end of game
		self.endMessage = StringVar()
		self.endMessage.set("Try to guess the knight's name!")
		self.endLabel = Label(master, textvariable=self.endMessage)
		self.endLabel.config(font=("Courier",20))
		self.endLabel.grid(row=6, column=1, columnspan=10)

	# BLACK KNIGHT IMAGE
		self.numKnights = 7 # the number of distinct images on file
		self.path = "knight_files/knight1.jpg"
		self.knight = ImageTk.PhotoImage(Image.open(self.path))
		self.displayImage = Label(master, image=self.knight)
		self.displayImage.grid(padx=0, pady=0, row=0, column=0, rowspan=50)


	def click_button(self,index,name):
		''' When the user clicks one of the lettered buttons, this
			function calls the check_guess function for that letter, then 
			deactivates and greys-out the button.
		---------------------------------------------------------------------------------------
				Inputs: index ----- the index of the button in self.buttonList
						name ------ the letter associated with the button
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		self.check_guess(name)
		self.buttonList[index].config(background="Grey")
		self.buttonList[index].config(state="disabled")


	def get_display_list(self):
		''' Generates a list of underscores to be displayed 
			in the game window, representing unguessed letters.
		---------------------------------------------------------------------------------------	
				Inputs: none
		---------------------------------------------------------------------------------------
				Outputs: displayList ---- a list with one item per letter in 
									the target word. Letters that have been 
									guessed are stored as themselves, otherwise
									they are represented by an underscore. All items 
									are set as underscores in this function.
		'''
		displayList = []
		for i in range(len(self.word)):
			displayList.append('_')
		self.displayList = displayList


	def update_display_word(self):
		''' When a letter is guessed correctly, the check_guess function calls this 
			function to update which parts of the target word are displayed.
		---------------------------------------------------------------------------------------
				Inputs: none
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		disp = ""
		for i in range(len(self.displayList)):
			disp+=self.displayList[i]
			disp+=" " # spaces between letters make display more readable
		self.displayWord.set(disp)


	def update_knight(self):
		''' When a letter is guessed incorrectly, the check_guess function calls this
			function to update the image of the Black Knight.
		---------------------------------------------------------------------------------------
				Inputs: none
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		num = self.strikes+1 # image name numbering starts at 1, not 0
		if num <= self.numKnights: # less than number of distinct images on file
			num = str(num) 
			self.path = ("knight_files/knight"+num+".jpg")
			self.knight = ImageTk.PhotoImage(Image.open(self.path))
			self.displayImage.configure(image=self.knight)


	def check_guess(self,guess):
		''' When the user clicks one of the lettered buttons, the click_button
			function calls the check_guess function to determine whether the letter
			associated with that button is a correct guess or not, and to call the 
			appropriate update function(s).
		---------------------------------------------------------------------------------------
				Inputs: guess ---- the letter that has been guessed
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		correct = False # the guess is incorrect until proven correct

		# checks the guess against each letter in the target word
		for i in range(len(self.word)):
			item = self.word[i]
			if item == guess:
				self.displayList[i] = item
				correct = True
		if correct == False: # guess matched no letters
			self.strikes+=1 # one more incorrect guess has occurred
			self.update_knight() # hacks off a limb

			if self.strikes >= self.numKnights: # no more hackable limbs
				self.game_over("loss") # ends the game as a loss
		else: # guess matched one or more letters
			self.update_display_word() # adds the guessed letter to the displayed word
			if "_" not in self.displayList: # user has guessed all of the letters
				self.game_over("win") # ends the game as a win


	def choose_word(self):
		''' When the game starts, this function selects a random word from
			a list of proper names taken from the Tain, the Mabinogion, Beowulf,
			and several Icelandic sagas.
		---------------------------------------------------------------------------------------
				Inputs: none
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		fname = "knight_files/ye_olde_names.txt" # file containing word choices
		f = open(fname) 
		allWords = f.read() # extract text
		f.close()
		wordOptions = allWords.split() # split text on spaces
		num = randint(0,len(wordOptions)-1)
		word = wordOptions[num] # randomly select a word
		wordlist = []
		for letter in word: # convert word to list of upper-case letters
			wordlist.append(letter.upper())
		self.word = wordlist


	def play_again(self,answer):
		''' Called by the buttons generated by the game_over function. Exits the
			program or starts a new game, depending on the user's choice of button.
		---------------------------------------------------------------------------------------
				Inputs: answer ---- "yes" or "no" - each associated with a button
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		if answer == "yes":
			# choose new word
			self.choose_word() 

			# reset strikes
			self.strikes = 0 

			# reset knight image
			self.update_knight()

			# reset displayed letters
			self.get_display_list() 
			self.update_display_word()

			# remove end of game buttons and message
			self.endMessage.set("Try to guess the knight's name!")
			self.replayButton.grid_forget() 
			self.endButton.grid_forget()

			# reset all alphabet buttons
			for button in self.buttonList:
				button.config(background="White")
				button.config(state="normal")
		else:
			exit()


	def game_over(self,condition):
		''' The check_guess function calls this function when the user's strikes
			exceed the limit. This	function displays a prompt and two buttons, and 
			allows the user to choose whether to exit the program or to start a new game.
		---------------------------------------------------------------------------------------
				Inputs: condition ----- "win" or "loss" determines the message 
										that is displayed
		---------------------------------------------------------------------------------------
				Outputs: none
		'''
		self.displayList = self.word
		correctWord = ""
		for i in range(len(self.word)):
	 		correctWord+=self.word[i]
		if condition == "win":
			message = "YOU WON!\nThe name was "+correctWord+"\nWant to play again?"
		else:
			message = "YOU LOST!\nThe name was "+correctWord+"\nWant to play again?"
		self.endMessage.set(message)
		self.endLabel.config(font=("Courier",20))
		self.endLabel.grid(row=6, column=1, columnspan=10)
		self.replayButton.grid(row=9, column=3)
		self.endButton.grid(row=9, column=5)
		


def main():
	''' The main function creates an object of the Hangman class
	---------------------------------------------------------------------------------------
			Inputs: none
	---------------------------------------------------------------------------------------
			Outputs: none
	'''
	root = Tk()
	win = Hangman(master=root)
	win.mainloop()


main()