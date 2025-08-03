#Utility to scrape Dodo's voice commands, count them and order them by longest
#Pastebin address https://pastebin.com/raw/nY6fWpxi
import requests
import re
import signal
import sys
import time
import tkinter as tk
import tkinter.scrolledtext as st

url = "https://gist.githubusercontent.com/StampyDodo/19a563dfad9c9e6a6d1a3512346aaba4/raw/b93ce1c936f28837e8294f44461d8dcf2c0100d3/gistfile1.md"
response = None
commands = None
count = None
search = None

win = tk.Tk()
win.geometry("1920x1080")
win.title("DCS: Dodo Command Scraper")
win.columnconfigure(0, weight=1)
frame = tk.Frame(win)
frame.grid(row=0, column=0, sticky=tk.NE+tk.SW)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
outputText = st.ScrolledText(frame, height=50, width=200)
outputText.grid(row=0, column=0, pady=(20,10))
inputframe = tk.Frame(win)
inputframe.grid(row=1, column=0, pady=10)
inputframe.rowconfigure(0, weight=2)
commandcount = tk.Label(inputframe, width=20)
commandcount.grid(row=0, column=0)
inputfield = tk.Entry(inputframe, width=100)
inputfield.grid(row=0, column=1)

def refresh():
    global response 
    response = requests.get(url)
    global commands
    commands = re.findall("![\\w\\.]*", response.text)
    global count
    count = len(commands)
    commands.sort(key=lambda e: len(e))
    global outputText
    outputText.configure(state='normal')
    outputText.delete("1.0", tk.END)
    for x in commands:
        outputText.insert(tk.END, x+"\n")
    outputText.configure(state='disabled')
    outputText.see(tk.END)
    global commandcount
    commandcount.configure(text='Commands: '+str(count))

def searching(*args):
    global response
    global commands
    global inputfield
    categories = re.findall("([\\w[　 ]+]*:)[　 ]+([!\\w\\.[　 ]+]*)", response.text)
    search = inputfield.get()
    tmp = filter(lambda e: re.match(".*"+search+".*", e, re.IGNORECASE), commands)
    searched = list(tmp)
    for c in categories:
        if(re.match(".*"+search+".*", c[0], re.IGNORECASE)):
            extracommands = re.findall("![\\w\\.]*", c[1])
            for e in extracommands:
                if(e not in searched):
                    searched.append(e)
    searched.sort(key=lambda e: len(e))
    counted = len(searched)
    global outputText
    outputText.configure(state='normal')
    outputText.delete("1.0", tk.END)
    for x in searched:
        outputText.insert(tk.END, x+"\n")
    outputText.configure(state='disabled')
    outputText.see(tk.END)
    global commandcount
    commandcount.configure(text='Commands: '+str(counted))


def signal_handler(sig, frame):
    print("\nExiting...", flush=True)
    sys.exit(0)

def popup(event):
    try:
        menu.tk_popup(event.x_root, event.y_root)
    finally:
        menu.grab_release()

def copy():
    inp = outputText.get(tk.SEL_FIRST, tk.SEL_LAST)
    win.clipboard_clear()
    win.clipboard_append(inp)

menu = tk.Menu(win, tearoff=0)
menu.add_command(label='Copy', command=copy)
outputText.bind('<Button-3>', popup)  # Right-click bind

def select_line(event):
    index = event.widget.index(f"@{event.x},{event.y}")
    start = f"{index} linestart"
    end = f"{index} lineend"
    event.widget.tag_remove(tk.SEL, "1.0", "end")
    event.widget.tag_add(tk.SEL, start, end)
    # event.widget.see(index)
    copy()

outputText.bind("<Double-1>", select_line)

signal.signal(signal.SIGINT, signal_handler)
refresh()

# for x in commands:
#     outputText.insert(tk.END, x+"\n")

inputfield.bind("<Return>", searching)
inputbutton = tk.Button(inputframe, text="Search", command=searching)
inputbutton.grid(row=0, column=2)
refreshbutton = tk.Button(inputframe, text="Refresh", command=refresh)
refreshbutton.grid(row=0, column=3)
outputText.configure(state='disabled')
outputText.see(tk.END)
win.mainloop()