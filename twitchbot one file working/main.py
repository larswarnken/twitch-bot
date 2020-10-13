import socket
import time
import math

HOST = "irc.twitch.tv"
PORT = 6667
TOKEN = "oauth:fbjtch47fdxco4picpesndaz1nc9hh"
NICKNAME = "lars_99"
CHANNEL = "papaplatte"


start_time = time.time()
time_video = 0


def openSocket():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(("PASS " + TOKEN + "\r\n").encode('utf-8'))
    s.send(("NICK " + NICKNAME + "\r\n").encode('utf-8'))
    s.send(("JOIN #" + CHANNEL + "\r\n").encode('utf-8'))
    return s


def sendMessage(s, message):
    messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
    s.send((messageTemp + "\r\n").encode('utf-8'))
    print("Sent: " + messageTemp)


def joinRoom(s):
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(2048).decode('utf-8')
        temp = readbuffer.split('\n')
        readbuffer = temp.pop()
        for line in temp:
            # print(line)
            Loading = loadingComplete(line)
    print("Successful connect")
    # sendMessage(s, "bot activated FeelsDankMan ")



def loadingComplete(line):
    if ("End of /NAMES list" in line):
        return False
    else:
        return True


def getUser(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


def getMessage(line):
    separate = line.split(":", 2)
    try:
        message = separate[2]
    except:
        message = "error"
    return message




def time_convert(sec):

    global time_video

    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60

    print("Time Lapsed = {0}:{1}:{2}".format(int(hours),int(mins),math.floor(sec)))

    time_video = "Film Zeit: {0}:{1}:{2}".format(int(hours),int(mins),math.floor(sec))







s = openSocket()
joinRoom(s)
readbuffer = ""

ja = 1

while ja < 2:
    readbuffer = readbuffer + s.recv(2048).decode('utf-8')
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    for line in temp:
        # print(line)
        if "PING :tmi.twitch.tv" in line:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
            break

        user = getUser(line)
        message = getMessage(line)
        # print(user + ": " + message)
        if "you suck" in message:
            sendMessage(s, "no you suck")
            break
        if "@lars_99 WeirdChamp" in message:
            sendMessage(s, "@" + user + " WeirdChamp")
            break
        if "lars_99, WeirdChamp" in message:
            sendMessage(s, user + ", WeirdChamp")
            break
        if "lars_99 WeirdChamp" in message:
            sendMessage(s, user + " WeirdChamp")
            break
        if "@lars_99, WeirdChamp" in message:
            sendMessage(s, "@" + user + ", WeirdChamp")
            break
        if "lars_99 moin" in message:
            sendMessage(s, user + " moin OkayChamp")
            break
        if "@lars_99 hi" in message:
            sendMessage(s, user + " hi :) /")
            break
        if "pokiDance" in message:
            sendMessage(s, "pokiDance")
            break
        if "cindyFloss" in message:
            sendMessage(s, "cindyFloss")
            break



        if 'zeit?' in message or 'Zeit?' in message:
            print('time')
            end_time = time.time()
            time_lapsed = end_time - start_time + 3630
            time_convert(time_lapsed)
            sendMessage(s, '@ ' + user + ' ' + time_video + ' plus minus paar sekunden')
            break