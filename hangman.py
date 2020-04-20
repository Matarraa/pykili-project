import random
import re

pictures = ['''
  
    +---+
    |   |
        |
        |
        |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
        |
        |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
    |   |
        |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
   /|   |
        |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
   /|\  |
        |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
 ^^^^^^^^^''','''

    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
 ^^^^^^^^^''']


rus_letters='абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

filename_w = 'russian_nouns.txt'
filename_d = 'russian_nouns_with_definition.txt'


def definition (filename_d):
    dictionary = {}
    with open(filename_d, encoding='utf-8') as file:
        text = file.readlines()
        for line in text:
            pair = re.search('([а-яё]+): (.+)', line)
            if pair:
                dictionary[pair.group(1)]= pair.group(2)
    return dictionary
            

def load_words(filename_w):
    with open(filename_w, encoding='utf-8') as file:
        words = file.read()
        wordlist = words.split()
    return wordlist


def choose_word(wordlist):
    return random.choice(wordlist)


def is_word_guessed(secret_word, letters_guessed):
    f=True
    i=0
    for letter in secret_word:
        if letter in letters_guessed:
            i+=1
    if(i!=len(secret_word)):
        f=False
    return f

    
def get_guessed_word(secret_word, letters_guessed):
    word_without_letters=''
    for letter in secret_word:
        if letter not in letters_guessed:
            word_without_letters = word_without_letters + '_ '
        else: 
            word_without_letters = word_without_letters + letter
    return word_without_letters


def get_available_letters(letters_guessed):
    available_letters = rus_letters
    b=''
    for letter in letters_guessed:
        available_letters = available_letters.replace(letter,b)
    return available_letters

  
def guess(g, gal):
    print('Вы можете ошибиться ещё ', str(g),' раз')
    print('Доступные буквы: ',gal, '\n')
    letter=str.lower(input('Введите букву: '))
    while True:
        if letter == 'подсказка':
            print('Увы, вы не можете использовать подсказку.\n')
            letter=str.lower(input('Введите букву: '))
        elif letter not in 'ёйцукенгшщзхъфывапролджэячсмитьбю':
            print('Пожалуйста, введите букву кириллицы')
            letter=str.lower(input('Введите букву: '))
        elif letter in 'ёйцукенгшщзхъфывапролджэячсмитьбю' and letter not in gal:
            print('Вы уже называли эту букву.')
            letter=str.lower(input('Введите букву: '))
        elif letter in gal and len(letter)==1:
            break 
    return letter


def number_of_hints(secret_word):
    if len(secret_word)<=5:
        hints = 1
    elif len(secret_word)>5 and len(secret_word)<=10:
        hints = 2
    else:
        hints = 3
    return hints
    

def guess_hint(g, gal):
    print('Вы можете ошибиться ещё ', str(g),' раз')
    print('Доступные буквы: ',gal, '\n')
    letter=str.lower(input('Введите букву: '))
    while True:
        if letter == 'подсказка':
            break
        elif letter not in 'ёйцукенгшщзхъфывапролджэячсмитьбю':
            print('Пожалуйста, введите букву кириллицы')
            letter=str.lower(input('Введите букву: '))
        elif letter in 'ёйцукенгшщзхъфывапролджэячсмитьбю' and letter not in gal:
            print('Вы уже называли эту букву.')
            letter=str.lower(input('Введите букву: '))
        elif letter in gal and len(letter)==1:
            break 
    return letter


def hint (secret_word, letters_guessed):
    not_guessed_letters = []
    word_without_letters = ''
    for letter in secret_word:
        if letter not in letters_guessed:
            not_guessed_letters.append(letter)
    hint = random.choice(not_guessed_letters)
    letters_guessed.append(hint)
    for letter in secret_word:
        if letter not in letters_guessed:
            word_without_letters = word_without_letters + '_ '
        else: 
            word_without_letters = word_without_letters + letter
    return word_without_letters


def hangman(secret_word):
    print('Добро пожаловать в игру "В И С Е Л И Ц А"!\n')
    print('Я загадал слово, которое содержит ',str(len(secret_word)),'букв.')
    print('_ '*len(secret_word))
    print(pictures[0])
    letters_guessed=[]
    gal=get_available_letters(letters_guessed)
    g=6
    while g>0:
        if is_word_guessed(secret_word, letters_guessed)==True:
            print('Вы выиграли!')
            dictionary = definition(filename_d)
            print(secret_word, '-', dictionary[secret_word])
            break
        letter=guess(g,gal)
        letters_guessed.append(letter)
        gal=get_available_letters(letters_guessed)
        if letter in secret_word:
            print('Хорошая попытка!\n')
            print(get_guessed_word(secret_word, letters_guessed))
            print(pictures[(6-g)])
        else:
            print('Этой буквы нет в загаданном слове.')
            print(get_guessed_word(secret_word, letters_guessed))
            g-=1
            print(pictures[(6-g)])
    if g==0:
        print('Увы, вы проиграли!')
        dictionary = definition(filename_d)
        print('Загаданное слово: ', secret_word, '\n')
        print(secret_word, '-', dictionary[secret_word], '\n')



def hangman_with_hints(secret_word):
    print('Добро пожаловать в игру "В И С Е Л И Ц А"!\n')
    print('Чтобы использовать подсказку, напишите: "подсказка".')
    print('Я загадал слово, которое содержит ',str(len(secret_word)),'букв.\n')
    print('_ '*len(secret_word))
    print(pictures[0])
    hints = number_of_hints(secret_word)
    letters_guessed=[]
    not_guessed_letters = []
    gal=get_available_letters(letters_guessed)
    g=6
    while g>0:
        if is_word_guessed(secret_word, letters_guessed)==True:
            print('Вы выиграли!')
            dictionary = definition(filename_d)
            print(secret_word, '-', dictionary[secret_word])
            break
        print('Количество доступных подсказок: ', hints)
        letter=guess_hint(g,gal)
        letters_guessed.append(letter)
        gal=get_available_letters(letters_guessed)
        if letter == 'подсказка':
            if hints > 0:
                print(hint(secret_word, letters_guessed))
                hints -= 1
                print(pictures[(6-g)])
            else:
                print('Вы не можете больше использовать подсказки.')
        elif letter in secret_word:
            print('Хорошая попытка!\n')
            print(get_guessed_word(secret_word, letters_guessed))
            print(pictures[(6-g)])
        else:
            print('Этой буквы нет в загаданном слове.')
            print(get_guessed_word(secret_word, letters_guessed))
            g-=1
            print(pictures[(6-g)])
    if g==0:
        print('Увы, вы проиграли!')
        dictionary = definition(filename_d)
        print('Загаданное слово: ', secret_word, '\n')
        print(secret_word, '-', dictionary[secret_word], '\n')


wordlist = load_words(filename_w)
 
answer='да'
secret_word = choose_word(wordlist)
while answer=='да':
    while True:
        answer1=str.lower(input('Вы хотите играть с подсказками?(да/нет) '))
        if answer1=='да':
            print('\n')
            hangman_with_hints(secret_word)
            break
        elif answer1=='нет':
            print('\n')
            hangman(secret_word)
            break
        else:
            continue
        
    answer=str.lower(input('Хотите сыграть еще раз? (да/нет)'))



