import socket
import os
import glob
from time import localtime, strftime
from tkinter import *
import threading
import tkinter.scrolledtext as tkst
from tkinter import ttk
import time
import json
from pathlib import Path
from winsound import *
import EmoteWindowClass
import AccountWindowClass

current_path = os.path.dirname(os.path.abspath(__file__))

# sets up window
root = Tk()
root.title("Twitch Bot")
root.iconbitmap("1.ico")
root.configure(bg="#424242")
Grid.columnconfigure(root, 4, weight=1)
Grid.rowconfigure(root, 4, weight=1)

# creates a settings file if there's none
settings_file = Path("config.json")
if not settings_file.is_file():
    config = {"last_channel": "", 'send_confirmation_message': 0, "afk_mode": 0, "copy_emotes": 0, "copy_user": 0,
              "last_user": ""}
    with open('config.json', 'w') as f:
        json.dump(config, f)

# opens the save file
with open('config.json', 'r') as f:
    config = json.load(f)

# opens the account file
if settings_file.is_file():
    with open('account.json', 'r') as f:
        account_info = json.load(f)
    if account_info.get("account_name") == "" or account_info.get("token") == "":
        AccountWindowClass.AccountSettings()

# entry boy for the channel to connect with
channel_input = Entry(root, bg="#424242", fg="white")
channel_input.insert(0, config["last_channel"])
channel_input.bind("<Button-1>", (lambda event: channel_input.delete(0, "end")))
channel = str(channel_input.get())

# twitch server settings
HOST = "irc.twitch.tv"
PORT = 6667
TOKEN = str(account_info.get("token"))
NICKNAME = str(account_info.get("account_name"))
CHANNEL = str(channel_input.get())

# to play sounds
muted = False

# to play sounds
send_or_nah = True

# counter for sent messages
counter_sent = 0
counter_mentions = 0


# creates text files to save sent messages later
def create_text_file():
    try:
        os.mkdir(current_path + "/sent messages")
    except OSError:
        print("Creation of the directory s failed")
    else:
        print("Successfully created the directory")
    text_folder_path = current_path + "/sent messages"
    os.chdir(text_folder_path)
    file_list = []
    if len(os.listdir(text_folder_path)) == 0:
        f = open("1.txt", "w+")
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + "\n\n")
        f.close()
    else:
        for files in glob.glob("*.txt"):
            split = files.split(".")
            file_list.append(int(split[0]))
        file_list.sort()
        new_file_name = str(file_list[-1] + 1) + ".txt"
        f = open(new_file_name, "w+")
        f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + "\n\n")
        f.close()

    for files in glob.glob("*.txt"):
        split = files.split(".")
        file_list.append(int(split[0]))
    file_list.sort()
    global current_text_file
    current_text_file = str(file_list[-1]) + ".txt"
    print(current_text_file)


# sends a message to the twitch server or chat
def send_message(s, message, waiting_time):
    message_temp = "PRIVMSG #" + channel_input.get() + " :" + message
    time.sleep(waiting_time)
    s.send((message_temp + "\r\n").encode('utf-8'))
    print("Sent: " + message_temp)


# checks if connected
def loading_complete(line):
    if "End of /NAMES list" in line:
        return False
    else:
        return True


# gives back the user
def get_user(line):
    separate = line.split(":", 2)
    user = separate[1].split("!", 1)[0]
    return user


# gives back the message
def get_message(line):
    global output_str
    print("line-" + str(line))
    separate = line.split(":")
    try:
        message = separate[2]
        output_str = ''.join(c for c in message if c.isprintable())
    except:
        message = "error"
    return output_str


# adds sent message to text file
def add_sent_message(current_file, message):
    f = open(current_file, "a+")
    f.write(strftime("%H:%M:%S", localtime()) + ": " + str(message) + "\n")
    f.close()


# replies to a message in chat
def reply_message(user, message, reply, waiting_time):
    global counter_sent
    counter_sent += 1
    global s
    send_message(s, reply, waiting_time)
    add_sent_message(current_text_file, reply)
    sent_box.insert(INSERT,
                    strftime("[%H:%M:%S", localtime()) + f"] {user}: {message}\n-> replied with: {reply}\n\n")
    sent_box.see(END)
    # plays sound
    if not muted:
        pathy = current_path + "\\clearly.wav"
        PlaySound(pathy, SND_ASYNC)
    my_notebook.tab(sent_frame, text=f"Sent ({counter_sent})")


# connects to a twitch channel
def connect():
    global s
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send(("PASS " + TOKEN + "\r\n").encode('utf-8'))
    s.send(("NICK " + NICKNAME + "\r\n").encode('utf-8'))
    s.send(("JOIN #" + channel_input.get() + "\r\n").encode('utf-8'))

    global readbuffer
    readbuffer = ""
    Loading = True
    while Loading:
        readbuffer = readbuffer + s.recv(2048).decode('utf-8')
        temp = readbuffer.split('\n')
        readbuffer = temp.pop()
        for line in temp:
            print(line)
            Loading = loading_complete(line)
    print("Successful connect")
    label_status.config(text="connected", bg="green", fg="white")
    # plays sound
    path_con_sound = current_path + "\\bot_activated.wav"
    PlaySound(path_con_sound, SND_ASYNC)
    # sends confirmation in chat if selected in settings
    if send_conf.get() == 1:
        send_message(s, "bot activated FeelsDankMan", 0)
    # start time thread
    global start_time
    start_time = time.time()
    thread_time.start()


global start_time


# main stuff with commands
def go():
    # saves the current channel as pre-input for next use
    config["last_channel"] = channel_input.get()
    with open('config.json', 'w') as f:
        json.dump(config, f)

    # creates a logging text file
    create_text_file()

    # connects to input channel obviously
    connect()

    # stupid loop
    ja = 1
    while ja < 2:
        global readbuffer
        readbuffer = readbuffer + s.recv(2048).decode('utf-8')
        temp = readbuffer.split("\n")
        readbuffer = temp.pop()

        for line in temp:
            print(line)
            # responses to twitch server
            if "PING :tmi.twitch.tv" in line:
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
                print("PONG")
                break

            user = get_user(line)
            message = get_message(line)
            print(user + ": " + message)

            # checks if user stopped sending via checkbox
            if send_or_nah == True:
                # checks if my name is in a message
                if account_info["account_name"] in message:
                    global counter_mentions
                    counter_mentions += 1
                    my_notebook.tab(mentions_frame, text=f"Mentions ({counter_mentions})")
                    mentions_box.insert(INSERT, strftime("[%H:%M:%S", localtime()) + f"] {user}: {message}\n\n")
                    mentions_box.see(END)

                # inserts user and message in chatbox
                chat_box.insert(INSERT, strftime("[%H:%M:%S", localtime()) + f"] {user}: {message}\n")
                chat_box.see(END)

                # checks if user has afk mode on
                if afk_var.get() == 1 and account_info["account_name"] in message and "WeirdChamp" not in message:
                    reply = f"{user} bin grad afk FeelsDankMan"
                    reply_message(user, message, reply, 0)
                    break
                else:
                    # the classics
                    if message == "@" + account_info["account_name"] + " WeirdChamp":
                        reply = f"@{user} WeirdChamp"
                        reply_message(user, message, reply, 0)
                        break
                    if message == account_info["account_name"] + ", WeirdChamp":
                        reply = f"{user}, WeirdChamp"
                        reply_message(user, message, reply, 0)
                        break
                    if message == account_info["account_name"] + " WeirdChamp":
                        reply = f"{user} WeirdChamp"
                        reply_message(user, message, reply, 0)
                        break
                    if message == "@" + account_info["account_name"] + ", WeirdChamp":
                        reply = f"@{user}, WeirdChamp"
                        reply_message(user, message, reply, 0)
                        break

                    # general weirdchamp
                    if account_info["account_name"] in message and "WeirdChamp" in message:
                        reply = f"@{user} WeirdChamp was"
                        reply_message(user, message, reply, 0)
                        break

                    # greetings
                    if account_info["account_name"] + " moin" in message:
                        reply = f"{user} moin OkayChamp"
                        reply_message(user, message, reply, 2)
                        break
                    if account_info["account_name"] + " hi" in message:
                        reply = f"{user} hi :) /"
                        reply_message(user, message, reply, 2)
                        break

                    # checks if user has emote copy mode on
                    if copy_emotes_var.get() == 1:
                        emote_file_path = current_path + "/emotes.json"
                        with open(emote_file_path, 'r') as f:
                            emotes = json.load(f)
                        index = 0
                        for _ in emotes:
                            if message == emotes[index]:
                                reply_message(user, message, message, 3)
                                break
                            index += 1
                    # TODO: emote cooldown dings weil kann eh nicht so schnell schicken
                    # checks if user has user copy mode on
                    if copy_user_var.get() == 1:
                        print("copy user")
                        if user == str(copy_user_input.get()):
                            reply_message(user, message, message, 0)


def convert(seconds):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))


def update_time():
    for _ in range(86400):
        label_time.config(text=f"{convert(time.time() - start_time)}")
        # print(convert(time.time() - start_time))
        time.sleep(1)


# time thread
thread_time = threading.Thread(target=update_time)
thread_time.daemon = True


# saves all settings to settings file
def saving():
    config['send_confirmation_message'] = send_conf.get()
    config["afk_mode"] = afk_var.get()
    config["copy_emotes"] = copy_emotes_var.get()
    config["copy_user"] = copy_user_var.get()
    config["last_user"] = copy_user_input.get()
    with open('config.json', 'w') as f:
        json.dump(config, f)
    print(config['send_confirmation_message'])
    print(config['afk_mode'])
    print(config['copy_emotes'])
    print(config['copy_user'])

    update_afk()
    update_copy_emotes()
    update_copy_user()


# sound on or off
def toggle_mute():
    global muted
    if muted == False:
        muted = True
    else:
        muted = False
    print(muted)


# send messages or nah
def toggle_send():
    global send_or_nah
    if send_or_nah == False:
        send_or_nah = True
    else:
        send_or_nah = False


# updates afk banner
def update_afk():
    if afk_var.get() == 1:
        label_mode.config(text="afk")
    else:
        label_mode.config(text="normal")


# updates copy emotes banner
def update_copy_emotes():
    if copy_emotes_var.get() == 1:
        label_copy_emotes.config(text="yes")
    else:
        label_copy_emotes.config(text="no")


# updates copy user banner
def update_copy_user():
    if copy_user_var.get() == 1:
        label_copy_user.config(text=copy_user_input.get())
    else:
        label_copy_user.config(text="no")


# thread for main loop
thready = threading.Thread(target=go)
thready.daemon = True

# sets labels to saved options
if config["afk_mode"] == 0:
    mode1 = "normal"
else:
    mode1 = "afk"

if config["copy_emotes"] == 0:
    mode2 = "no"
else:
    mode2 = "yes"

if config["copy_user"] == 0:
    mode3 = "no"
else:
    mode3 = config["last_user"]

#
#
# top stuff
#
#
label_channel = Label(root, text="Channel: ", bg="#424242", fg="white")
button_run = Button(root, text="connect", padx=1, command=lambda: thready.start(), bg="#424242", fg="white",
                    activebackground="#424242", activeforeground="white")
#
box_sending = Checkbutton(root, text="stop sending", padx=1, command=toggle_send, bg="#424242", fg="white",
                          selectcolor="grey", activebackground="#424242", activeforeground="white")
#
box_mute = Checkbutton(root, text="mute", padx=1, command=toggle_mute, bg="#424242", fg="white", selectcolor="grey",
                       activebackground="#424242", activeforeground="white")
#
label_status_t = Label(root, text="Status:", bg="#424242", fg="white")
label_status = Label(root, text="disconnected", bg="red", fg="white", width=10)
#
#
# top stuff grid
label_channel.grid(row=0, column=0, padx=5, pady=10, sticky=W)
channel_input.grid(row=0, column=1, padx=5, ipady=3)
button_run.grid(row=0, column=2, padx=5, pady=3, sticky=W)
box_sending.grid(row=0, column=3, pady=5, sticky=W)
box_mute.grid(row=0, column=4, padx=5, pady=5, sticky=W)
label_status_t.grid(row=0, column=5, padx=0, sticky=E)
label_status.grid(row=0, column=6, padx=10)
#
#
#
# status bar
#
#
# frame
frame_bar = Frame(root, bg="#424242")
frame_bar.grid(row=2, column=0, columnspan=10, sticky=N + S + E + W)
#
# labels
label_mode_t = Label(frame_bar, text="Mode:", bg="#424242", fg="white")
label_mode = Label(frame_bar, text=mode1, width=5, bg="#424242", fg="white")
#
label_place1 = Label(frame_bar, text="", width=5, bg="#424242", fg="white")
#
label_copy_emotes_t = Label(frame_bar, text="copy emotes:", bg="#424242", fg="white")
label_copy_emotes = Label(frame_bar, text=mode2, width=5, bg="#424242", fg="white")
#
label_place2 = Label(frame_bar, text="", width=5, bg="#424242", fg="white")
#
label_copy_user_t = Label(frame_bar, text="copy user:", bg="#424242", fg="white")
label_copy_user = Label(frame_bar, text=mode3, width=10, bg="#424242", fg="white")

label_time_t = Label(frame_bar, text="Runtime:", bg="#424242", fg="white")
label_time = Label(frame_bar, text="00:00:00", width=10, bg="#424242", fg="white")
#
#
#
# status bar grid
Grid.columnconfigure(frame_bar, 7, weight=1)
#
label_mode_t.grid(row=1, column=0, padx=0, sticky=W)
label_mode.grid(row=1, column=1, padx=0, sticky=W)
#
label_place1.grid(row=1, column=2, padx=0, sticky=W)
#
label_copy_emotes_t.grid(row=1, column=3, padx=0, sticky=W)
label_copy_emotes.grid(row=1, column=4, padx=0, sticky=W)
#
label_place2.grid(row=1, column=5, padx=0, sticky=W)
#
label_copy_user_t.grid(row=1, column=6, padx=0, sticky=W)
label_copy_user.grid(row=1, column=7, padx=0, sticky=W)

label_time_t.grid(row=1, column=8, padx=0)
label_time.grid(row=1, column=9, padx=10)
#
#
#
# bottom stuff
#
#
# frame
#
frame_bottom = Frame(root)
frame_bottom.grid(row=4, column=0, columnspan=10, sticky=N + S + E + W)
# notebook
my_notebook = ttk.Notebook(frame_bottom)
my_notebook.pack(fill="both", expand=1)
#
# chat frame
#
chat_frame = Frame(my_notebook, bg="#424242")
chat_box = tkst.ScrolledText(master=chat_frame, wrap=WORD, width=90, height=30, font=("Calibri", 11), bg="#424242",
                             fg="white")
chat_box.pack(fill=BOTH, expand=True)
chat_box.bind("<Key>", lambda e: "break")
#
# sent messages frame
#
sent_frame = Frame(my_notebook, bg="#424242")
sent_box = tkst.ScrolledText(master=sent_frame, wrap=WORD, width=90, height=30, font=("Calibri", 11), bg="#424242",
                             fg="white")
sent_box.pack(fill=BOTH, expand=True)
sent_box.bind("<Key>", lambda e: "break")
#
# mentions frame
#
mentions_frame = Frame(my_notebook, bg="#424242")
mentions_box = tkst.ScrolledText(master=mentions_frame, wrap=WORD, width=90, height=30, font=("Calibri", 11),
                                 bg="#424242",
                                 fg="white")
mentions_box.pack(fill=BOTH, expand=True)
mentions_box.bind("<Key>", lambda e: "break")
#
#
# settings frame
#
# frame
#
settings_frame = Frame(my_notebook, bg="#424242")
label_warning = Label(settings_frame, text="can't save when connected because I'm too dumb to make it work",
                      bg="#424242", fg="white", padx=5, pady=5)
#
button_account_details = Button(settings_frame, text="Account Details",
                                command=lambda: AccountWindowClass.AccountSettings(), bg="#424242", fg="white",
                                activebackground="#424242", activeforeground="white")
#
checked_conf = config["send_confirmation_message"]
send_conf = IntVar(value=config['send_confirmation_message'])
checkbox_send_conf = Checkbutton(settings_frame, text="send connection message in chat", variable=send_conf,
                                 bg="#424242", fg="white", selectcolor="grey", padx=5, pady=5,
                                 activebackground="#424242", activeforeground="white")
#
checked_afk = config["afk_mode"]
afk_var = IntVar(value=config['afk_mode'])
box_afk = Checkbutton(settings_frame, text="afk mode", variable=afk_var, bg="#424242", fg="white", selectcolor="grey",
                      padx=5, pady=5, activebackground="#424242", activeforeground="white")
#
checked_copy_emotes = config["copy_emotes"]
copy_emotes_var = IntVar(value=config['copy_emotes'])
box_copy_emotes = Checkbutton(settings_frame, text="copy emotes", variable=copy_emotes_var, bg="#424242", fg="white",
                              selectcolor="grey", padx=5, pady=5, activebackground="#424242", activeforeground="white")
button_emotes = Button(settings_frame, text="choose...", command=lambda: EmoteWindowClass.EmoteSettings(), bg="#424242",
                       fg="white", activebackground="#424242", activeforeground="white")
#
checked_copy_user = config["copy_user"]
copy_user_var = IntVar(value=config['copy_user'])
box_copy_user = Checkbutton(settings_frame, text="copy a user", variable=copy_user_var, bg="#424242", fg="white",
                            selectcolor="grey", padx=5, pady=5, activebackground="#424242", activeforeground="white")
#
copy_user_input = Entry(settings_frame, bg="#424242", fg="white")
copy_user_input.insert(0, config["last_user"])
copy_user_input.bind("<Button-1>", (lambda event: copy_user_input.delete(0, "end")))
#
save_button = Button(settings_frame, text="save", command=saving, bg="#424242", fg="white", activebackground="#424242",
                     activeforeground="white")
#
# settings grid
#
label_warning.grid(row=0, column=0, columnspan=4, sticky=W)
button_account_details.grid(row=1, column=0, columnspan=3, sticky=W, padx=5)
checkbox_send_conf.grid(row=2, column=0, columnspan=3, sticky=W)
box_afk.grid(row=3, column=0, sticky=W)
box_copy_emotes.grid(row=4, column=0, sticky=W)
button_emotes.grid(row=4, column=1, sticky=W)
box_copy_user.grid(row=5, column=0, sticky=W)
copy_user_input.grid(row=5, column=1, sticky=W)
#
save_button.grid(row=6, column=0, padx=10, pady=10, sticky=W)
#
#
#
# grid bottom stuff
chat_frame.pack(fill="both")
sent_frame.pack(fill="both")
settings_frame.pack(fill="both")
#
# notebook tabs
#
my_notebook.add(chat_frame, text="Chat")
my_notebook.add(sent_frame, text="Sent Messages")
my_notebook.add(mentions_frame, text="Mentions")
my_notebook.add(settings_frame, text="Settings")

# for return key
channel_input.bind("<Return>", (lambda event: thready.start()))

root.mainloop()
