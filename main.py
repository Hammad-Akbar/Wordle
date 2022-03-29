import random
from colorama import Fore, Back, Style
import os
import time
import requests
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), 'dictionary.env')
load_dotenv(dotenv_path)

token = os.getenv['DICTIONARY_KEY']

def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'): 
        command = 'cls'
    os.system(command)

def getWord(fileName):
  file = open(fileName, "r")
  lines = file.readlines()
  word = random.choice(lines)
  word = word.rstrip("\n")
  word = word.lower()
  return word

def addLetters():
  for i in range(5):
    if guess[i] == word[i]:
      letters.append(Back.GREEN + " " + guess[i] + " " + Style.RESET_ALL)
    elif guess[i] in word:
      letters.append(Style.BRIGHT + Back.YELLOW + " " + guess[i] + " " + Style.RESET_ALL)
    else:
      letters.append(Back.BLACK + " " + guess[i] + " " + Style.RESET_ALL)
  letters.append("\n")

print(
  Back.BLACK + "WORDLE\n" + 
  Back.BLACK + "Guess the word\n" +
  Back.YELLOW + " a " + 
  Back.BLACK + " r  i  s  e" + "\n" + 
  Back.BLACK + " t " + 
  Back.YELLOW + " r " + 
  Back.GREEN + " a  i " + 
  Back.BLACK + " n " + "\n" +
  Back.GREEN + " c  h  a  i  r " + 
  Back.BLACK + "\n\nBlack - wrong letter, wrong place\n" + 
  Back.YELLOW + "Yellow - right letter, wrong place\n" + 
  Back.GREEN + "Green - right letter, right place\n"
)

input(Back.BLACK + "Press any key to start " + Style.RESET_ALL)

word = getWord("words.txt")
letters = []
guess = ""
validWord = ""

for turn in range(6):
  clear()
  
  for letter in letters:
    print(letter, end = "")
    
  if guess == word:
    print("You guessed it!")
    break

  guess = input("Guess a 5 letter word: ")

  while guess != validWord:
    url = "https://dictionaryapi.com/api/v3/references/collegiate/json/{}?key={}".format(guess, token)
    response = requests.get(url)
    if response.status_code == 200:
      try:
        result = response.json()
        validWord = result[0]['meta']['id'][:5]
      except TypeError:
        print("\n🚨🚨🚨 WORD NOT IN WORDLIST 🚨🚨🚨")
        guess = input("Guess a 5 letter word: ") 
      
  while True:
    if len(guess) != 5:
      print("\n🚨🚨🚨 Please enter a 5 LETTER WORD 🚨🚨🚨")
      guess = input("Guess a 5 letter word: ")  
    else:
      break

  guess = guess.lower()
  addLetters()

print("The word was " + word)
