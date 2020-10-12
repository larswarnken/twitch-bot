from tkinter import *
from tkinter import scrolledtext as st
import json
from pathlib import Path
import os

# creates an emotes file if there's none
current_path = os.path.dirname(os.path.abspath(__file__))
settings_file = Path(f"{current_path}/emotes.json")
if not settings_file.is_file():
    emotes = []
    with open('emotes.json', 'w') as f:
        json.dump(emotes, f)


class EmoteSettings:
    def __init__(self):
        self.emote_window = Tk()
        self.emote_window.title("Emotes")
        self.emote_window.geometry("500x500")
        self.emote_window.configure(bg="#424242")

        # scrolled box thing
        self.scrollbox = st.ScrolledText(self.emote_window, font=("Calibri", 11), bg="#424242",
                                         fg="white")
        with open(f"{current_path}/emotes.json", 'r') as f:
            emotes = json.load(f)
        print(len(emotes))
        if len(emotes) != 0:
            index = 0
            for _ in emotes:
                self.scrollbox.insert(INSERT, f"{emotes[index]} \n")
                index += 1

        self.scrollbox.pack(fill=BOTH, expand=1)

        # save button
        self.save_emotes_button = Button(self.emote_window, text="save list", command=lambda: self.save_emotes(),
                                         bg="#424242", fg="white", activebackground="#424242", activeforeground="white")
        self.save_emotes_button.pack(pady=10)

    def save_emotes(self):
        emotes = []
        save_text = self.scrollbox.get("1.0", END)
        yes = save_text.split("\n")
        for i in yes:
            if i != "":
                print(i.partition(' ')[0])
                emotes.append(i.partition(' ')[0])
        print(emotes)
        with open(f"{current_path}/emotes.json", 'w') as f:
            json.dump(emotes, f)
        self.emote_window.destroy()
