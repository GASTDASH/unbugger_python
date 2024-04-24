from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import ctypes
import re
import os
import traceback

# Increas Dots Per inch so it looks sharper
ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Setup Tkinter
root = Tk()
root.geometry('1000x800')
root.wm_title('Unbugger')

def file_open():
    file_name = filedialog.askopenfilename(filetypes = [('Python', '*.py')])
    
    print(file_name)
    if file_name or file_name != '':
        with open(file_name, 'r', encoding='utf-8') as f:
            file_string = ""
            for string in f.readlines():
                file_string += string
            editArea.delete('1.0', END)
            editArea.insert('1.0', file_string)
            changes()
            
def test(event=None):
    # with open('run.py', 'r', encoding='utf-8') as f:
    os.system('start cmd /K "python unbugger.py"')

# Debug the Programm
def debug(event=None):
    # Write the Content to the Temporary File
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    with open('run.py', 'r', encoding='utf-8') as f:
        try:
            exec(f.read())
        except:
            error_text = traceback.format_exc()
            print(error_text)
            
            finding_str = 'File "<string>", line '
            index = error_text.find(finding_str) + len(finding_str)
            
            line_number = str()
            for char in error_text[index:]:
                print(char)
                if char != ',':
                    line_number += char
                else:
                    break
            line_number = int(line_number)
            print(f"line_number = {line_number}")
            editArea.mark_set("insert", "%d.%d" % (line_number, 0))
            editArea.tag_add("sel", "%d.%d" % (line_number, 0), "%d.%d" % (line_number, 5))
            # print(f"index = {index}   |   error_text[index] = {error_text[index]}")
    # Start the File in a new CMD Window
    # os.system('start cmd /K "python unbugger.py"')
    # os.system('start cmd /K "python run.py"')

# Register Changes made to the Editor Content
def changes(event=None):
    global previousText

    # If actually no changes have been made stop / return the function
    if editArea.get('1.0', END) == previousText:
        return

    # Remove all tags so they can be redrawn
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Add tags where the search_re function found the pattern
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i+=1

    previousText = editArea.get('1.0', END) 

def search_re(pattern, text, groupid=0):
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches

def rgb(rgb):
    return "#%02x%02x%02x" % rgb


previousText = ''

# Define colors for the variouse types of tokens
normal = rgb((234, 234, 234))
keywords = rgb((234, 95, 95))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
font = 'Consolas 12'


# Define a list of Regex Pattern that should be colored in a certain way
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

# Make the Text Widget
# Add a hefty border width so we can achieve a little bit of padding
editArea = scrolledtext.ScrolledText(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief='raised',
    borderwidth=30,
    font=font
)

# scrollb = Scrollbar(command = editArea.yview)
# editArea['yscrollcommand'] = scrollb.set

# Place the Edit Area with the pack method
editArea.pack(
    fill=BOTH,
    expand=1
)

# Insert some Standard Text into the Edit Area
editArea.insert('1.0', """from argparse import ArgumentParser
from random import shuffle, choice
import string

# Setting up the Argument Parser
parser = ArgumentParser(
    prog='Password Generator.',
    description='Generate any number of passwords with this tool.'
)
""")

# Bind the KeyRelase to the Changes Function
editArea.bind('<KeyRelease>', changes)

# Bind Control + R to the exec function
root.bind('<Control-d>', debug)

root.option_add("*tearOff", FALSE)
menu = Menu()

file_menu = Menu()
file_menu.add_command(label = "Open", command = file_open)
file_menu.add_command(label = "Debug", command = debug)
file_menu.add_command(label = "Test", command = test)
menu.add_cascade(label = "File", menu = file_menu)

root.config(menu = file_menu)

changes()
root.mainloop()