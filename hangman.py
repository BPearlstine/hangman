import random
import re
from saveGame import SaveGame
import sqlite3

#convert db to dict
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def searchSaves(name,play):
    try:
        #search db for correct row by name
        conn = sqlite3.connect('hangman.db')
        conn.row_factory = dict_factory
        c = conn.cursor()
        c.execute('SELECT * FROM game WHERE name=?', name)
        gameFile = c.fetchone()
        print ("Welcome ", gameFile['name'], " you have ", gameFile['wins'], " wins and ", gameFile['losses'], " losses.")
        conn.close()
        play = "y"
        return play

    except:
        pass
    else:
        print("Sorry that file doesn't exist, try again.")
        play = "n"
        return play



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

def gameStart(play, dictionary, name, newGame):
  wins = 0
  losses = 0
  #simple while loop game will stop on 'n'
  while play == 'y':
    letters, choice = playGame(dictionary)
    if len(letters) == 0:
        #length of letters = 0 means you've guessed the word, wins + 1
        wins = wins + 1
        print ("Great game! you correctly guessed the word,", choice)
    else:
        # hangman = 6 no more guesses, you've lost, losses + 1
        losses = losses + 1
        print ("Sorry, you didn't guess it this time. The word was", choice)
    print (name, "you currently have ", wins, "wins and ", losses, " losses!")
    saveQuery = input ("Would you like to save the game? [y/n]: ")
    if saveQuery == 'y':
        saveFile (name, wins, losses, newGame)
        print("your game has been saved!")
    play = input("Would you like to play again? [y/n]")
    play = str.lower(play)
  return play




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

def saveFile (name, wins, losses, newGame):

    conn = sqlite3.connect('hangman.db')
    c = conn.cursor()
    if newGame == False:
        c.execute("UPDATE game SET wins=wins+? WHERE name=?", (wins,name))
        c.execute("UPDATE game SET losses=losses+? WHERE name=?", (losses,name))
        conn.commit()
    else:
        c.execute("INSERT INTO game VALUES (?,?,?)", (name, wins, losses,))
        conn.commit()
    conn.close()


def main ():
  name = ""
  play = "y"
  while play == "y":
      dictionary = randomWord()
      print ("Let's play hangman!")
      savedStart = input ("Do you want to open a saved game?[y/n]:")
      savedStart = str.lower(savedStart)
      #check if using previously saved game
      if savedStart == "y":
          name = input("What is the name your game is saved under?: ")
          name = str.lower(name)
          nameTup = (name,)
          play = searchSaves(nameTup, play)
          newGame = False
          play = gameStart(play, dictionary, name, newGame)

      else:
          name = input("Welcome to hangman! What is your name? ")
          name = str.lower(name)
          newGame = True
          play = gameStart(play, dictionary, name, newGame)
  print ("Thanks for playing!")


main()
