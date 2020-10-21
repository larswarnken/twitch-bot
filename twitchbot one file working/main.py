import socket
import time

HOST = "irc.twitch.tv"
PORT = 6667

TOKEN = "oauth:..."  # you can get your token from https://twitchapps.com/tmi/
NICKNAME = "..."  # all lowercase :)
CHANNEL = "..."  # all lowercase :)


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




s = openSocket()
joinRoom(s)
readbuffer = ""

run = True

while run:
    readbuffer = readbuffer + s.recv(2048).decode('utf-8')
    temp = readbuffer.split("\n")
    readbuffer = temp.pop()

    for line in temp:
        #print(line)
        if "PING :tmi.twitch.tv" in line:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
            break

        user = getUser(line)
        message = getMessage(line)
        print(user + ": " + message)
        if "@{} WeirdChamp".format(NICKNAME) in message:
            sendMessage(s, "@" + user + " WeirdChamp")
            break
        if "{}, WeirdChamp".format(NICKNAME) in message:
            sendMessage(s, user + ", WeirdChamp")
            break
        if "{} WeirdChamp".format(NICKNAME) in message:
            sendMessage(s, user + " WeirdChamp")
            break
        if "{}, WeirdChamp".format(NICKNAME) in message:
            sendMessage(s, "@" + user + ", WeirdChamp")
            break
        if "{} moin".format(NICKNAME) in message:
            sendMessage(s, user + " moin OkayChamp")
            break
        if "@{} hi".format(NICKNAME) in message:
            sendMessage(s, user + " hi :) /")
            break
        if "pokiDance" in message:
            sendMessage(s, "pokiDance")
            break
        if "cindyFloss" in message:
            sendMessage(s, "cindyFloss")
            break



