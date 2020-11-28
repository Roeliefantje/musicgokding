########################################################################
# Author: Roel de Jeu                                                  #
# Code from main.py is used aswell for some functions                  #
########################################################################

import socket
from pydub import AudioSegment
from time import sleep
import time
from playsound import playsound
import os
import threading
from pyautogui import press
from random import randint
from difflib import SequenceMatcher

def clear():
    os.system('cls')
    sleep(2)

def matches(answer, question):
    if SequenceMatcher(None, answer.lower(), question.lower()).ratio() > 0.7:
        return True
    else:
        return False

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65434        # Port to listen on (non-privileged ports are > 1023)

clear()
print("Welcome to the binb we have at home, created by Roeliefantje")
print("Source code can by found at https://github.com/Roeliefantje/musicgokding/")
print("PLEASE TURN DOWN YOUR COMMAND PROMPT VOLUME AS IT IS QUITE LOUD")
sleep(2)
clear()

HOST_NEW = input("Enter IP here, no input = localhost\n")

if len(HOST_NEW) > 0:
    HOST = HOST_NEW

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

msg = ""
while len(msg) <= 0:
    msg = s.recv(1024)
    if len(msg) > 0:
        print(msg.decode("utf-8"))

name = input("What is your nickname?\n")
print(f"Welcome {name}")
sleep(1)

# If the string that got recieved by the server cant be played,
# the client will wait for a new string again.
failed = False
while True:
    # Wait for the next song to start and get the random song to be send.
    # Play that song for 20 seconds and let us guess
    if not failed:
        print("Waiting for the next round to start...")
        failed = False

    song = ""
    while len(song) <= 0:
        song = s.recv(1024)

    song = song.decode("utf-8")

    # Now uses pydub repos to create a 20 second snippet of a song
    # Then using the playsound repos to play the song.
    try:
        songfile = AudioSegment.from_mp3(song)
        # This would be a random number but I cant do that since the music wouldnt be sync between players
        # songduration = songfile.duration_seconds * 1000
        # songend = randint(20000, songduration)
        # songfile = songfile[songend-20000:songend]
        songfile = songfile[40000:60000]
        try:
            os.remove("temp.mp3")
        except OSError:
            pass

        songfile.export("temp.mp3", format="mp3")

        playsound('temp.mp3', False)
        print("Playing song...")
    except:
        failed = True
        continue

    songname = song.split("\\")[-1]
    songname = songname.replace('.mp3', '')
    answers = songname.split("-")
    timeout = time.time() + 20
    is_asking = True

    # Basically a function that presses enter for you to make sure the python
    # program doesnt hang on input() too long.
    # Only works if this is the focused window though.
    def press_enter():
        while is_asking:
            if time.time() > timeout:
                print("Please press enter to proceed.")
                press('enter')
                break

    # Start the thread that presses enter.
    enter_presser = threading.Thread(target=press_enter)
    enter_presser.start()

    while True:
        if len(answers) < 1:
            print("You have guessed both the title and the artist")
            print("Please wait till the round is over...")
            sleep(timeout - time.time())
            is_asking = False
            break
        guess = input("Take a guess!\n")
        if time.time() > timeout:
            print("No time left!")
            is_asking = False
            break
        for x in answers:
            if matches(guess, x):
                print("Thats right!")
                s.send(bytes(name, "utf-8"))
                answers.remove(x)

    clear()

    # Recieve the round info from the server and print it out.
    info = ""
    while len(info) <= 0:
        info = s.recv(1024)
    print(info.decode("utf-8"))
