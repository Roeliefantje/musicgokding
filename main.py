########################################################################
# THIS IS AN OUTDATED VERSION THAT DID NOT WORK WITH SERVERS YET!      #
# IF YOU WANNA LOOK AT THE ACTUAL CODE LOOK AT client.py AND hostex.py #
# Authors: Roel de Jeu & Gijsveld                                      #
########################################################################

from os import system, name
from time import sleep
import time
from random import randint
import pathlib
from pydub import AudioSegment #IF we dont want everyone to have to install mmfepg we might have to do this while adding songs to the directory.
# Might just make a python program that takes every song in a folder and just gets a random 20 second snippet
from playsound import playsound


points = 0
name = ""
songs_played = []
amount_of_songs = 1

def startguess(song):
    global points
    global name
    songname = song.split("\\")[-1]
    songname = songname.replace('.mp3', '')
    answers = songname.split("-")
    timeout = time.time() + 20
    while True:
        if time.time() > timeout:
            break
        if len(answers) < 1:
            print("You have guessed both the title and the artist")
            print("Please wait till the round is over")
            sleep(timeout - time.time())
            break
        guess = input("Take a guess!\n")
        for x in answers:
            if x == guess:
                points += 1
                answers.remove(x)

    if points == 1:
        print(f"{name} is at {points} point!")
    else:
        print(f"{name} is at {points} points!")


def makename():
    return

def randomsong():
    """
    Gets a random song in the songs folder and plays it.
    """
    global amount_of_songs
    global songs_played
    # Look at amount of songs
    songs = []
    song = ""
    amount_of_songs = 0
    for path in pathlib.Path("songs").iterdir():
        amount_of_songs += 1
        songs.append(path)

    songnumber = randint(0, amount_of_songs - 1)

    song = str(songs[songnumber])
    while(song in songs_played):
        songnumber = randint(0, amount_of_songs - 1)
        song = str(songs[songnumber])

    songs_played.append(song)
    song.replace("\\", "/")

    return song


def playmusic():
    # Now uses pydub repos to create a 20 second snippet of a song
    # Then using the playsound repos to play the song.
    song = randomsong()
    songfile = AudioSegment.from_mp3(song)
    songfile = songfile[:20000]
    songfile.export("temp.mp3", format="mp3")

    playsound('temp.mp3', False)
    return song

# https://www.geeksforgeeks.org/clear-screen-python/
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

def main():
    global amount_of_songs
    global songs_played
    global name
    global points
    name = input("What is your username?\n")
    clear()
    print(f"Hello {name}!")
    sleep(1)
    clear()
    while(amount_of_songs > len(songs_played)):
        song = playmusic()
        startguess(song)
    print("All songs have been played!")
    if points != 1:
        print(f"Congratulations {name} on scoring {points} points!")
    else:
        print(f"Unlucky {name} on scoring {points} point!")

    return


if __name__ == '__main__':
    main()
