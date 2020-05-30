from os import system, name
from time import sleep
from playsound import playsound
from random import randint
import pathlib


def makename():
    return

def randomsong():
# Look at amount of songs
    songs = []
    song = ""
    amount_of_songs = 0
    for path in pathlib.Path("songs").iterdir():
        amount_of_songs += 1
        songs.append(path)

    songnumber = randint(0,amount_of_songs -1)
    
    song = songs[songnumber]
    playsound(song)

    return song

def playmusic():
    # playsound(randomsong())
    randomsong()
    return

# https://www.geeksforgeeks.org/clear-screen-python/
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def main():
    name = input("What is your username?\n")
    clear()
    print(f"Hello {name}!")
    sleep(1)
    clear()
    playmusic()
    return


if __name__ == '__main__':
    main()
