########################################################################
# Author: Roel de Jeu                                                  #
# Code from main.py is used aswell for some functions                  #
########################################################################

import socket
import time
from time import sleep
import threading
import pathlib
from random import randint

HOST = ''  # Standard loopback interface address (localhost)
PORT = 65434        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(10)

clientsockets = []

all_threads = []
has_thread = []

# Thread that connects all the clients to the server
def connect_clients():
    while True:
        conn, addr = s.accept()
        clientsockets.append(conn)
        print(f"Connection from {addr} established!")
        conn.send(bytes("You are connected!", "utf-8"))

# Makes the threads that reads the messages recieved from the threads for the
# different sockets
def make_subthreads():
    while True:
        for x in clientsockets:
            if x not in has_thread:
                has_thread.append(x)
                thread = threading.Thread(target=read_message, args=(x,))
                thread.start()
                all_threads.append(thread)

userinfo = [] # Basically a list containing the amount of points and name of a player i.e.: [[Roel, 10], [Gijs, 5]]
points = [] # A list containing players who scored a point on the song [[Roel], [Gijs], [Kent]]

# Reads the message from a socket in a process
def read_message(socket):
    while True:
        try:
            msg = socket.recv(1024)
            if len(msg) > 0:
                decode_message = msg.decode("utf-8")
                points.append(decode_message)
        except ConnectionResetError:
            break

client_connector = threading.Thread(target=connect_clients)
client_connector.start()

sub_threader = threading.Thread(target=make_subthreads)
sub_threader.start()

song_number = 0



"""
Gets a random song in the songs folder and plays it.
"""
amount_of_songs = 0
songs_played = []
songs = []
song = ""
amount_of_songs = 0

#Gets the amount of songs in the folder
for path in pathlib.Path("songs").iterdir():
    amount_of_songs += 1
    songs.append(path)

while True:
    # Gets a random song that has not yet been played
    songnumber = randint(0, amount_of_songs - 1)
    song = str(songs[songnumber])

    # Resets the songs played if all songs have been played
    if len(song) == len(songs_played):
        print("All songs have been played")
        songs_played = []

    while(song in songs_played):
        songnumber = randint(0, amount_of_songs - 1)
        song = str(songs[songnumber])

    songs_played.append(song)
    song.replace("\\", "/")

    # Send the song to the clients
    for x in clientsockets:
        x.send(bytes(song, "utf-8"))

    # Wait till the round is over.
    points = []
    sleep(22)

    # Go through points and see who got guesses first
    for x in points:
        has_name = True
        if len(userinfo) == 0:
            has_name = False

        for y in userinfo:
            if str(y[0]) == str(x):
                y[1] += 1
                break
            has_name = False

        if not has_name:
            userinfo.append([x, 1])

    # Gets rid of duplicates somehow still appearing
    temp = []
    for x in userinfo:
        if str(x[0]) in temp:
            userinfo.remove(x)
        else:
            temp.append(str(x[0]))

    got_point = []

    points_to_give = 3
    got_gold = ""
    got_silver = ""
    got_bronze = ""

    # Goes through the list of players who have gotten a point
    # If it has found a name twice, it will reward that player with gold/bronze/silver
    # If there are still points up for grab
    for x in points:
        if str(x) in got_point:
            if points_to_give == 3:
                got_gold = x
            elif points_to_give == 2:
                got_silver = x
            elif points_to_give == 1:
                got_bronze = x
            points_to_give -= 1
        else:
            got_point.append(str(x))

    # Actually adds the point to the user.
    for y in userinfo:
        if y[0] == str(got_gold):
            y[1] += 3
        elif y[0] == got_silver:
            y[1] += 2
        elif y[0] == got_bronze:
            y[1] += 3

    # Create a summary of everyones points and who got gold/silver/bronze in the round
    info = ""
    song = song.split("\\")[-1]
    song = song.replace(".mp3", "")
    song = song.replace("-", " - ")
    info += f"The song that just played was: {song}\n"
    for x in userinfo:
        info += f"{x[0]} is at {x[1]} point(s)!\n"

    if got_gold != "":
        info += f"{got_gold} achieved the gold medal this round!\n"
    if got_silver != "":
        info += f"{got_silver} achieved the silver medal this round!\n"
    if got_bronze != "":
        info += f"{got_bronze} achieved the bronze medal this round!\n"

    # Send this summary to the clients, also print it in the server
    print(info)
    for x in clientsockets:
        try:
            x.send(bytes(info, "utf-8"))
        except:
            pass
    sleep(5)







