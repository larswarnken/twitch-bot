import socket
import time
import re

HOST = "irc.twitch.tv"
PORT = 6667

TOKEN = "oauth:..."  # you can get your token from https://twitchapps.com/tmi/
NICKNAME = "..."  # all lowercase :)
CHANNEL = "..."  # all lowercase :)


start_time = time.time()
time_video = 0


def open_socket():
    socket_opened = socket.socket()
    socket_opened.connect((HOST, PORT))
    socket_opened.send(("PASS " + TOKEN + "\r\n").encode('utf-8'))
    socket_opened.send(("NICK " + NICKNAME + "\r\n").encode('utf-8'))
    socket_opened.send(("JOIN #" + CHANNEL + "\r\n").encode('utf-8'))
    return socket_opened


def send_message(socket_message, message_send):
    message_temp = "PRIVMSG #" + CHANNEL + " :" + message_send
    socket_message.send((message_temp + "\r\n").encode('utf-8'))
    print("Sent: " + message_temp)


def join_room(socket_to):
    read_buffering = ""
    loading = True
    while loading:
        read_buffering = read_buffering + socket_to.recv(2048).decode('utf-8')
        temp_message = read_buffering.split('\n')
        read_buffering = temp_message.pop()
        for chat_line in temp_message:
            # print(line)
            loading = loading_complete(chat_line)
    print("Successful connect")
    # send_message(s, "bot activated FeelsDankMan ")


def loading_complete(line_load):
    if "End of /NAMES list" in line_load:
        return False
    else:
        return True


def get_user(line_user):
    separate = line_user.split(":", 2)
    line_user = separate[1].split("!", 1)[0]
    return line_user


def get_message(line_message):
    separate = line_message.split(":", 2)
    try:
        message_split = separate[2]
    except Exception:
        message_split = "error"
    return message_split


s = open_socket()
join_room(s)
read_buffer = ""

run = True

while run:
    read_buffer = read_buffer + s.recv(2048).decode('utf-8')
    temp = read_buffer.split("\n")
    read_buffer = temp.pop()

    for line in temp:
        # print(line)
        if "PING :tmi.twitch.tv" in line:
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
            break

        user = get_user(line)
        message = get_message(line)
        print(user + ": " + message)

        # weirdchamp
        if "@{} WeirdChamp".format(NICKNAME) in message:
            send_message(s, "@" + user + " WeirdChamp")
            break
        if "{}, WeirdChamp".format(NICKNAME) in message:
            send_message(s, user + ", WeirdChamp")
            break
        if "{} WeirdChamp".format(NICKNAME) in message:
            send_message(s, user + " WeirdChamp")
            break
        if "{}, WeirdChamp".format(NICKNAME) in message:
            send_message(s, "@" + user + ", WeirdChamp")
            break

        # greeting back
        if "{} moin".format(NICKNAME) in message:
            send_message(s, user + " moin OkayChamp")
            break
        if "@{} hi".format(NICKNAME) in message:
            send_message(s, user + " hi :) /")
            break

        # copying emotes
        if "pokiDance" in message:
            send_message(s, "pokiDance")
            break
        if "cindyFloss" in message:
            send_message(s, "cindyFloss")
            break

        # copying user
        if user == 'yessayes':
            if bool(re.search('^!.+$', message))\
                    or bool(re.search('(?i)^kek.+$', message))\
                    or 'monteOpa' in message \
                    or 'ich ' in message:
                send_message(s, '{} nice try :)'.format(user))
            else:
                send_message(s, message)
