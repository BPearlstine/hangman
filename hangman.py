import random
import re
from saveGame import SaveGame

def searchSaves(name):
    with open("savedGames.csv") as forSearch:
        for row in forSearch:
            if  name in row:
                row = row.strip()
                game = row.split(",")
                name = game[0]
                wins = game[1]
                losses = game[2]
                print ("Welcome " + name + ", you have won " + wins + " and lost " + losses + " games so far!")
                return SaveGame(name,wins,losses)


def main ():
  name = ""
  dictionary = randomWord()
  print ("Do you want to try and guess one of ", len(dictionary), "words?")
  play = input("Enter [y/n]: ")
  play = str.lower(play)
  savedStart = input ("Do you want to open a saved game?[y/n]:")
  savedStart = str.lower(savedStart)
  if savedStart == "y":
      name = input("What is the name your game is saved under?: ")
      name = str.lower(name)
      currGame = searchSaves(name)
      gameStart(play, dictionary, currGame)
  else:
      name = input("Welcome to hangman! What is your name? ")
      name = str.lower(name)
      currGame = SaveGame(name,0,0)
      gameStart(play, dictionary, currGame)
  print ("Thanks for playing!")

def randomWord():
  #wordsEN is the list of all possible words
  wordlist_file = "wordsEn.txt"
  # open wordsEn to be read
  wordfile = open(wordlist_file, 'r')
  #read wordslist_file
  wordlist = wordfile.read()
  #convert wordslist_file to a string
  words = str(wordlist)
  #split into words
  dictionary = str.split(words)
  return dictionary

def gameStart(play, dictionary, currGame):
  #simple while loop game will stop on 'n'
  while play == 'y':
    letters, choice = playGame(dictionary)
    if len(letters) == 0:
        #length of letters = 0 means you've guessed the word, wins + 1
        currGame.changeWins()
        print ("Great game! you correctly guessed the word,", choice)
    else:
        # hangman = 6 no more guesses, you've lost, losses + 1
        currGame.changeLosses()
        print ("Sorry, you didn't guess it this time. The word was", choice)
    score = currGame.currentScore()
    print (score)
    saveQuery = input ("Would you like to save the game? [y/n]: ")
    if saveQuery == 'y':
        saveFile (currGame)
        print("your game has been saved!")
    play = input("Would you like to play again? [y/n]")
    play = str.lower(play)



def playGame(dictionary):
  #put a random word from dictionary into choice
  choice = random.choice(dictionary)
  #break choice into a list of the individual letters
  letters = list(choice)
  # hangman will be used to store the number of wrong guesses up to 6
  hangman = 0
  # dash will show the number of letters in the word choice
  # as each letter is guessed a '_' will be replaced by the correct letter
  dash = str('_') * len(choice)
  dash = list(dash)
  #just for testing remove print(choice) from final
  print (choice)
  print (dash)
  # keep looping for more guesses until all letters are guessed
  # or until all six incorrect guesses are used
  while len(letters) > 0 and hangman < 6:
      guess = input("What letter would you like to guess?: ")
      if guess in letters:
          #remove correctly guessed letter from list of needed letters
          letters = set(letters) - set(guess)
          list(letters)
          #find where the correctly guessed letter goes in the word choice
          for match in re.finditer(guess, choice):
              index = match.start()
              #replace '_' with guess in list dash
              dash[index] = guess
          print (dash)
          print ("Only", len(letters), "more letters to guess! You have ", 6 - hangman, "guesses left.")
      else:
          # else plus hangman so that your chances to guess go down
          hangman = hangman + 1
          chances = 6 - hangman
          print (dash)
          print("Sorry, that letters not in the word. You have ", chances, "guesses left!")
  return letters, choice

def saveFile (object):
    savedGames = "savedGames.csv"
    output_file = open (savedGames, 'a')
    strObj = str(object) + '\n'
    output_file.write (strObj)
    output_file.close()

main()
