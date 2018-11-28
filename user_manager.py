import pprint
import tkinter as tk

from COMPANY_DATA import ALL_DATA
from USERS import user_data

TARGET_FILE_PATH = "USERS/user_data.py"
STOCK_CODES = [data.code for data in ALL_DATA]

DATA = user_data.DATA
del(user_data)

def update_tracked_stocks(username, *stocks):
    # Ensure that user is actually logged in
    for stock in stocks:
        if username in DATA and stock not in DATA[username] and stock in STOCK_CODES :
            DATA[username][1].append(stock)
    write_changes()


def _delete_user(username):
    DATA.pop(username)
    write_changes()

def make_user(username, password):
    try:
        assert username not in DATA
    except AssertionError:
        raise DuplicateUserError
    else:
        DATA[username] = (password, [])
        write_changes()

def login(username, password):
    if username in DATA:
        if password != DATA[username][0]:
            raise LoginError
        else:
            pass
    else:
        raise LoginError("Username not found.")

def login_as_guest():
    login("", "")
    
def write_changes():
    target_file = open(TARGET_FILE_PATH, "w")
    target_file.write("DATA = " + pprint.pformat(DATA))
    target_file.close()


class LoginError(Exception):
    def __init__(self, message="Invalid Credentials"):
        Exception.__init__(self)
        ErrorWindow(message)

class DuplicateUserError(Exception):
    def __init__(self, message="Error: User already exists"):
        Exception.__init__(self)
        ErrorWindow(message)


class ErrorWindow(tk.Tk):
    def __init__(self, message, width=400, height=200):
        tk.Tk.__init__(self)
        # self.grid_propagate(0)
        self["height"]=height
        self["width"]=width
        self.create_label(message)
        self.title("Error Window")
        self.resizable(False, False)
        self.mainloop()

    def create_label(self, message):
        self.label = tk.Label(master=self, text=message)
        self.label.pack(fill=tk.BOTH, expand=True)
    

