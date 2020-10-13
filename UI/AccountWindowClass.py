from tkinter import *
import json
from pathlib import Path
import os
from tkinter import messagebox

current_path = os.path.dirname(os.path.abspath(__file__))

settings_file = Path(f"{current_path}/account.json")
if not settings_file.is_file():
    account_info = {"account_name": "", "token": ""}
    with open('account.json', 'w') as f:
        json.dump(account_info, f)

if settings_file.is_file():
    with open('account.json', 'r') as f:
        account_info = json.load(f)


class AccountSettings:
    def __init__(self):
        self.account_window = Tk()
        self.account_window.title("Account Details")
        self.account_window.geometry("500x500")
        self.account_window.configure(bg="#424242")

        # account name
        self.label_account_name = Label(self.account_window, text="Your account name: ", bg="#424242", fg="white")
        self.account_name_input = Entry(self.account_window, width=40, bg="#424242", fg="white")
        if account_info.get("account_name") != "":
            self.account_name_input.insert(0, account_info.get("account_name"))

        # token
        self.label_token = Label(self.account_window, text="Your token: ", bg="#424242", fg="white")
        self.token_input = Entry(self.account_window, width=40, bg="#424242", fg="white")
        if account_info.get("token") != "":
            self.token_input.insert(0, account_info.get("token"))
        self.label_token_info = Label(self.account_window,
                                      text="You can get your token from https://twitchapps.com/tmi/", bg="#424242",
                                      fg="white")

        # save button
        self.save_emotes_button = Button(self.account_window, text="save", command=lambda: self.save_account_details(),
                                         bg="#424242", fg="white", activebackground="#424242", activeforeground="white")

        # grid
        self.label_account_name.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.account_name_input.grid(row=0, column=1, padx=10, pady=10, sticky=W)

        self.label_token.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.token_input.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        self.label_token_info.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky=W)

        self.save_emotes_button.grid(row=10, column=0, padx=10, pady=10, sticky=W)

    def save_account_details(self):
        account_info["account_name"] = str(self.account_name_input.get())
        account_info["token"] = str(self.token_input.get())
        print(str(self.account_name_input.get()))
        print(str(self.token_input.get()))
        if self.account_name_input.get() == "" or self.token_input.get() == "":
            messagebox.showerror(title="Bruh", message="You have to fill in both boxes, dumbass")
            self.account_window.destroy()
            AccountSettings()
        elif " " in self.account_name_input.get() or " " in self.token_input.get():
            messagebox.showerror(title="Bruh", message="No Blankspaces, bruh")
            self.account_window.destroy()
            AccountSettings()
        elif self.token_input.get()[0:6] != "oauth:":
            messagebox.showerror(title="Bruh", message="token has to start with \"oauth:\" lol")
            self.account_window.destroy()
            AccountSettings()
        else:
            with open(f"{current_path}/account.json", 'w') as f:
                json.dump(account_info, f)
            self.account_window.destroy()
