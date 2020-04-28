# Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

wordlist = load_words()

def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    boolean = 0
    for x in secret_word:
        for n in letters_guessed:
            if x == n:
                boolean += 1
                break
            
    return boolean == len(secret_word)

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guessed_word = ""
    for x in secret_word:
        count = 0
        for n in letters_guessed:
            if x == n:
                guessed_word += x
                count += 1
                break
        if count == 0:
            guessed_word += '_ '
        
    return guessed_word

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    available_letters = string.ascii_lowercase
    for x in available_letters:
        for n in letters_guessed:
            if x == n:
                available_letters = available_letters.replace(x,'')
    
    return available_letters

def hangman(secret_word):
    
    n_guesses = 6
    n_correct_guesses = 0
    n_warnings = 3
    letters_guessed = ''
    letter = ' '

    print('---------------')
    print("Welcome to the game Hangman!\nI am thinking of a word that is",len(secret_word), "letters long.")
    print('---------------')

    while (not is_word_guessed(secret_word, letters_guessed)) and n_guesses != 0 and n_warnings != 0:
        print("You have",n_guesses,"guesses left.\nAvailable letters: ")
        print(get_available_letters(letters_guessed))
        print("---------------\nPlease, guess a letter: ")
        letter = str(input())
                    
        while letter not in string.ascii_letters:
            n_warnings -= 1
            print("Warning!!! You have to input a letter.")
            print(n_warnings, "more warnings left.")
            letter = str(input())
            if n_warnings == 0:
                print("lose the game")
                
        while letter in letters_guessed:
            print("The letter has already been guessed.\nPlease try again")
            letter = str(input())
        
        if letter in string.ascii_uppercase:
            letter = string.ascii_lowercase[string.ascii_uppercase.index(letter)]
        
        if letter in secret_word:
            print("True!")
            n_correct_guesses += 1
            n_guesses += 1  #in every other case, you do lose a guees; this compensates for that if you got it right
        else:
            print("False...")
        
        letters_guessed += letter
        print(get_guessed_word(secret_word, letters_guessed))
        n_guesses -= 1
        print(n_guesses)
        print('-------------')
    
    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        print("Congratulations, you won!")
        print("Your score:",n_guesses * n_correct_guesses)
    else:
        print("You lost...\n...the word was",secret_word)

# -----------------------------------

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(' ','')
    if len(my_word) != len(other_word):
        return False
    for x in range(len(my_word)):
            if (my_word[x] in string.ascii_lowercase) and my_word[x] != other_word[x]:
                return False
            
    return True            
                
def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    hint_wordlist = []
    for x in wordlist:
        if match_with_gaps(my_word, x):
            hint_wordlist.append(x)
            
    return hint_wordlist

def hangman_with_hints(secret_word):
    
    n_guesses = 6
    n_correct_guesses = 0
    n_warnings = 3
    letters_guessed = ''
    letter = ' '

    print('---------------')
    print("Welcome to the game Hangman!\nI am thinking of a word that is",len(secret_word), "letters long.")
    print('---------------')

    while (not is_word_guessed(secret_word, letters_guessed)) and n_guesses != 0 and n_warnings != 0:
        print("You have",n_guesses,"guesses left.\nAvailable letters: ")
        print(get_available_letters(letters_guessed))
        print("---------------\nPlease, guess a letter: ")
        letter = str(input())
        
        if letter == '*':
            print(show_possible_matches(get_guessed_word(secret_word, letters_guessed)))
            continue
            
        while letter not in string.ascii_letters:
            n_warnings -= 1
            print("Warning!!! You have to input a letter.")
            print(n_warnings, "more warnings left.")
            letter = str(input())
            if n_warnings == 0:
                print("lose the game")
                
        while letter in letters_guessed:
            print("The letter has already been guessed.\nPlease try again")
            letter = str(input())
        
        if letter in string.ascii_uppercase:
            letter = string.ascii_lowercase[string.ascii_uppercase.index(letter)]
        
        if letter in secret_word:
            print("True!")
            n_correct_guesses += 1
            n_guesses += 1  #in every other case, you do lose a guees; this compensates for that if you got it right
        else:
            print("False...")
        
        letters_guessed += letter
        print(get_guessed_word(secret_word, letters_guessed))
        n_guesses -= 1
        print(n_guesses)
        print('-------------')
    
    if get_guessed_word(secret_word, letters_guessed) == secret_word:
        print("Congratulations, you won!")
        print("Your score:",n_guesses * n_correct_guesses)
    else:
        print("You lost...\n...the word was",secret_word)

    
#secret_word = choose_word(wordlist)
#hangman(secret_word)

#to disable hints, comment the two lines below and uncomment the two lines above
    
secret_word = choose_word(wordlist)
hangman_with_hints(secret_word)