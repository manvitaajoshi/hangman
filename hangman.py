# -------------------IMPORT STATEMENT-------------------#
import pygame, sys, random

# -------------------PYGAME UI SETTING-------------------#
pygame.init()
screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load("rope.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("HANGMAN")

# -------------------FONT AND DISPLAY PICTURE-------------------#
background_img1 = pygame.image.load("jail.jpg")
background_img2 = pygame.image.load("black.png")
main_title = pygame.font.Font("Heaters.otf", 150)
main_page_text = main_title.render("HANGMAN", True, (255, 255, 255))
text1 = pygame.font.Font(("LEMONMILK-Regular.otf"), 40)
text2 = pygame.font.Font(("LEMONMILK-Regular.otf"), 20)
text3 = pygame.font.Font(("Please write me a song.ttf"), 40)
text4 = pygame.font.Font(("LEMONMILK-Light.otf"), 10)
text5 = pygame.font.Font(("LEMONMILK-Light.otf"), 30)

# -------------------LIST OF WORDS-------------------#
easy_words = "soup brick fork image snake thumb rabbit stale bear radio mango chocolate spider".split()
medium_words = "cookie memory fox puff common vowel adjective silver bridge sentence".split()
hard_words = "bandwagon blizzard microwave pneumonia vortex jukebox oxygen jazz exchange cobweb embezzle".split()

# -------------------DICTIONARY OF HINTS-------------------#
hint = {"soup": "Liquid food", "brick": "Related to buildings", "fork": "A type of cutlery",
        "image": "Facilitates easy data representation",
        "snake": "A reptile", "thumb": "One of the fingers", "rabbit": "An animal",
        "stale": "Related to freshness", "bear": "An animal",
        "radio": "A device whose mode of communication is through waves", "mango": "A fruit",
        "chocolate": "A decadent dessert", "spider": "An insect",
        "cookie": "Sweet baked food item", "memory": "Capacity to retain data", "fox": "An animal",
        "puff": "Relating to air or gaseous state substances",
        "common": "Repetitive", "vowel": "Present in alphabet series", "adjective": "A type of words",
        "silver": "A metal", "bridge": "Related to connections",
        "sentence": "A collection of certain objects in a meaningful manner",
        "bandwagon": "Cause of attraction or popularity",
        "blizzard": "Related to cold bad weather", "microwave": "An electrical gadget",
        "pneumonia": "A respiratory disease",
        "vortex": "A geographical phenomenon consisting of spirals", "jukebox": "A device related to music",
        "oxygen": "Essential for life",
        "jazz": "Music genre", "exchange": "A term related to trade", "cobweb": "Shelter made by an insect",
        "embezzle": "Act of committing a fraud"}


# -------------------BINARY SEARCH TREE-------------------#
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.data = key


def createNode(key):
    return Node(key)


def insert(root, p):
    if root.data < p.data:
        if root.right is None:
            root.right = p
        else:
            insert(root.right, p)
    else:
        if root.left is None:
            root.left = p
        else:
            insert(root.left, p)


def createBST(secretWord):
    key = secretWord[0]
    root = createNode(key)
    for key in secretWord[1:]:
        p = createNode(key)
        insert(root, p)
    return root


def search(root, req):
    if root is None:
        return False
    if req > root.data:
        return search(root.right, req)
    elif req < root.data:
        return search(root.left, req)
    else:
        return True


# -------------------MAIN PAGE-------------------#
# Show the front main page of the game for visual purposes.
def mainpage():
    run = True
    while run:
        screen.blit(background_img1, (90, 150))
        screen.blit(main_page_text, (220, 260))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    run = False
        pygame.display.update()


# -------------------INSTRUCTIONS-------------------#
# Displays the instructions of the game for the user.
def instruction():
    run = True
    while run:
        screen.blit(background_img1, (90, 150))
        text = text1.render("Instructions", True, (255, 255, 255))
        screen.blit(text, (260, 170))
        text = text3.render("Guess the secret word correctly by guessing", True, (255, 255, 255))
        screen.blit(text, (110, 300))
        text = text3.render("one letter at a time before the hangman kills.", True, (255, 255, 255))
        screen.blit(text, (110, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    run = False
        pygame.display.update()


# -------------------GET DIFFICULTY LEVEL-------------------#
# Takes input from the user regarding the difficulty level.
def selectlevel():
    run = True
    global guess_of_user
    guess = ''
    guess_of_user = ''
    while run:
        screen.blit(background_img1, (90, 150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                else:
                    guess += event.unicode
                    guess_of_user = guess
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and guess.isalnum():
                    run = False
        title = text1.render('Please select a level', True, (255, 255, 255))
        screen.blit(title, (150, 150))
        title = text3.render('1. Easy', True, (255, 255, 255))
        screen.blit(title, (350, 300))
        title = text3.render('2. Medium', True, (255, 255, 255))
        screen.blit(title, (350, 350))
        title = text3.render('3. Hard', True, (255, 255, 255))
        screen.blit(title, (350, 400))
        text = text1.render(guess, True, (255, 255, 255))
        screen.blit(text, (400, 480))
        title = text4.render("Hereon press SHIFT to continue", True, (255, 255, 255))
        screen.blit(title, (500, 520))
        pygame.display.update()


# -------------------GET THE GUESSED LETTER-------------------#
# Displays the hint and takes a single letter from the user as the guess.
def gamepage():
    run = True
    global user_guess
    user_guess = ''
    guess = ''
    while run:
        screen.blit(background_img2, (90, 50))
        title = text1.render('HINT', True, (255, 255, 255))
        screen.blit(title, (100, 150))
        title = text2.render(hints, True, (255, 255, 255))
        screen.blit(title, (100, 200))
        title = text1.render('Guess a letter!', True, (255, 255, 255))
        screen.blit(title, (235, 250))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT) and guess.isalnum() and len(
                        guess) == 1 and ((ord(guess)>=65 and ord(guess)<=90) or (ord(guess)>=97 and ord(guess)<=122)):
                    pygame.display.update()
                    run = False
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                else:
                    guess += event.unicode
                    user_guess = guess
        text = text1.render(guess, True, (255, 255, 255))
        screen.blit(text, (380, 350))
        pygame.display.update()


# -------------------SHOW THE STATUS-------------------#
# Displays the letters that are correctly guessed and wrongly guessed.
# Displays the chances left for the user to guess the word.
# Displays hangman pictures.
def status(chances):
    run = True
    guess = ''
    while run:
        screen.blit(background_img2, (90, 100))
        title = text1.render('YOUR STATUS:', True, (255, 255, 255))
        screen.blit(title, (100, 150))
        title = text2.render(dash1, True, (255, 255, 255))
        screen.blit(title, (100, 250))
        title = text1.render('Missed letters:', True, (255, 255, 255))
        screen.blit(title, (100, 350))
        title = text2.render(miss, True, (255, 255, 255))
        screen.blit(title, (100, 450))
        title = text2.render("Chances left: " + str(chances), True, (255, 255, 255))
        screen.blit(title, (530, 150))
        if chances == 6:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 5:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" O   |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 4:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" O   |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("  |    |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (560, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 3:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" 0    |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("/|     |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("       |", True, (255, 255, 255))
            screen.blit(title, (565, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 2:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" O    |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("/|\    |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("        |", True, (255, 255, 255))
            screen.blit(title, (560, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 1:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" O    |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("/|\    |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("/      |", True, (255, 255, 255))
            screen.blit(title, (565, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        if chances == 0:
            title = text1.render("+---+ ", True, (255, 255, 255))
            screen.blit(title, (560, 200))
            title = text1.render(" O    |", True, (255, 255, 255))
            screen.blit(title, (560, 250))
            title = text1.render("/|\    |", True, (255, 255, 255))
            screen.blit(title, (560, 300))
            title = text1.render("/ \    |", True, (255, 255, 255))
            screen.blit(title, (560, 350))
            title = text1.render("   ===", True, (255, 255, 255))
            screen.blit(title, (560, 400))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    pygame.display.update()
                    run = False
        pygame.display.update()


# -------------------GAME WON-------------------#
# Displays that the user has won the game along with the word accurately guessed by the user.
def game_won(secretWord):
    run = True
    while run:
        screen.blit(background_img1, (90, 150))
        title = text1.render('BRAVO...YOU WON!!!', True, (255, 255, 255))
        screen.blit(title, (190, 170))
        title = text2.render('As you correctly guessed,', True, (255, 255, 255))
        screen.blit(title, (250, 320))
        title = text2.render('the secret word was: ' + secretWord, True, (255, 255, 255))
        screen.blit(title, (250, 360))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    pygame.display.update()
                    run = False
        pygame.display.update()


# -------------------GAME LOST-------------------#
# Displays that the user has lost the game along with the secret word which was supposed to be guessed.
def game_lost(secretWord, correctLetters):
    run = True
    while run:
        screen.blit(background_img1, (90, 150))
        title = text1.render('OOPS!!! YOU LOST :(', True, (255, 255, 255))
        screen.blit(title, (190, 170))
        title = text2.render('The secret word was: ' + secretWord, True, (255, 255, 255))
        screen.blit(title, (250, 320))
        title = text2.render('The correct letters you guessed are: ' + correctLetters, True, (255, 255, 255))
        screen.blit(title, (180, 360))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT):
                    pygame.display.update()
                    run = False
        pygame.display.update()


# -------------------CALL THE FUNCTIONS-------------------#
# Asks the user whether to restart or not.
def replay():
    run = True
    global play_again
    input = ''
    play_again = ''
    while run:
        screen.blit(background_img1, (90, 150))
        title = text5.render('Do you wish to play again?', True, (255, 255, 255))
        screen.blit(title, (175, 150))
        title = text5.render('Press ENTER to restart.', True, (255, 255, 255))
        screen.blit(title, (200, 320))
        title = text5.render('Press ESCAPE to exit.', True, (255, 255, 255))
        screen.blit(title, (220, 370))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False
                    return True
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
        text = text1.render(input, True, (255, 255, 255))
        screen.blit(text, (380, 350))
        pygame.display.update()


# -------------------CALL THE FUNCTIONS-------------------#
# This function returns a random word from the passed list of strings.
def getRandomWord(wordList):
    wordIndex = random.randint(0, len(wordList) - 1)
    return wordList[wordIndex]


mainpage()
instruction()
while True:
    # Setting some strings as empty. Here the user guesses would be added.
    miss = ""
    missedLetters = ''
    correctLetters = ''
    dash = ""
    selectlevel()
    # Difficulty level which the user wants.
    lvl = int(guess_of_user)
    # Keep asking again until the user enters a valid difficulty level.
    while True:
        if (lvl == 1 or lvl == 2 or lvl == 3):
            break
        else:
            selectlevel()
            lvl = int(guess_of_user)
    # Assign the list of words based on the difficulty.
    if lvl == 1:
        words = easy_words
    elif lvl == 2:
        words = medium_words
    elif lvl == 3:
        words = hard_words

    # Get a random word from the list.
    secretWord = getRandomWord(words)
    root = createBST(secretWord)
    hints = str(hint[secretWord])
    win = 0
    chances = 6
    while True:
        miss = ""
        dash = ""
        dash1 = ""
        gamepage()
        # If the guessed letter is in the BST and not already guessed, add it to the correctLetters string.
        if search(root, str(user_guess).lower()) is True and str(user_guess).lower() not in correctLetters:
            num = secretWord.count(user_guess)
            for i in range(num):
                correctLetters += user_guess
        # If the guessed letter is not in the BST and not already guessed, add it to the missedLetters string.
        elif search(root, str(user_guess).lower()) is not True and str(user_guess).lower() not in missedLetters:
            missedLetters += user_guess
            chances -= 1
            win += 1
        blanks = '_' * len(secretWord)
        for letter in missedLetters:
            miss += letter
        # Replace blanks with correctly guessed letters.
        for i in range(len(secretWord)):
            if secretWord[i] in correctLetters:
                blanks = blanks[:i] + secretWord[i] + blanks[i + 1:]
        # Show the secret word with spaces in between each letter.
        for letter in blanks:
            dash += letter
        for i in dash:
            dash1 = dash1 + i + " "
        status(chances)
        # When the secretWord is equal to the correctLetters, game is over and user wins.
        if len(secretWord) == len(correctLetters):
            break
        # If the user has used all the chances and not guessed the word, game is over and user loses.
        if chances == 0:
            break
    # Display the accurate results (win/lose)
    if chances != 0:
        game_won(secretWord)
    else:
        game_lost(secretWord, correctLetters)
    # If the user doesn't wish to replay, break. Else, go on.
    if replay() is not True:
        break
