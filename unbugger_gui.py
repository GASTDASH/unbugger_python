import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
# import ctypes
import re
import os
import tkinter.messagebox
import traceback
import subprocess

#################
root = Tk()
root.geometry('1000x800')
root.wm_title('Unbugger GUI')
icon = PhotoImage(file='./icon.png')
root.tk.call('wm', 'iconphoto', root._w, icon)
#################

def file_open():
    '''
    Открытие файла
    '''

    file_name = filedialog.askopenfilename(filetypes = [('Python', '*.py')])
    print(file_name)
    
    # Чтение файла
    if file_name or file_name != '':
        with open(file_name, 'r', encoding='utf-8') as f:
            file_string = ""
            for string in f.readlines():
                file_string += string
            editArea.delete('1.0', END)
            editArea.insert('1.0', file_string)
            changes()
 
def test():
    '''
    Тестирование кода
    '''

    # Запись кода во временный файл
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))

    # Запуск тестов
    # os.system('start cmd /K "python unbugger.py"') # WINDOWS
    subprocess.call('konsole --noclose -e "python unbugger.py"', shell=True) # LINUX with KDE PLASMA

def debug():
    '''
    Дебагинг кода
    '''

    # Запись кода во временный файл
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(editArea.get('1.0', END))
        
    # Очищение от красных строк
    editArea.tag_delete("error")

    # Чтение файла для запуска
    with open('run.py', 'r', encoding='utf-8') as f:
        try:
            # Запуск кода
            exec(f.read(), globals())
        except:
            # Получение текста ошибки
            error_text = traceback.format_exc()
            print(error_text)
            
            # Проверка на принудительный выход из программы
            if error_text.find('SystemExit: 0') != -1:
                print("Принудительный выход из программы! Ошибок не найдено")
            else:
                # Поиск проблемной строки кода
                line_number = str()
                finding_str = 'File "<string>", line '
                index = 0
                while True:
                    line_number = str()
                    index = error_text.find(finding_str, index)
                    if index == -1:
                        break
                    index += len(finding_str)
                    for char in error_text[index:]:
                        if char != ',' and char != '\n':
                            line_number += char
                        else:
                            break
                    line_number = int(line_number)
                    print(f"line_number = {line_number}")
                    
                    editArea.mark_set("insert", "%d.%d" % (line_number, 0))
                    editArea.tag_add("error", "%d.%d" % (line_number, 0), 'insert lineend')
                    editArea.tag_config("error", background=error)
                
                tkinter.messagebox.showerror("Исключение", error_text)

def changes():
    '''
    Регистрация изменений, сделанных в окне редактирования кода
    '''

    global previousText
    
    # update_line_numbers(event=None)

    # Если не произошло изменений
    if editArea.get('1.0', END) == previousText:
        return

    # Удаление тегов для их нового добавления
    for tag in editArea.tag_names():
        editArea.tag_remove(tag, "1.0", "end")

    # Добавление тегов там где search_re найдёт нужные слова
    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', END)):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)

            i+=1

    previousText = editArea.get('1.0', END) 

def search_re(pattern, text, groupid=0):
    '''
    Поиск регулярных выражений (ключевых слов, комментариев, строк)
    '''
    
    matches = []

    text = text.splitlines()
    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):

            matches.append(
                (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
            )

    return matches

def rgb(rgb):
    '''
    Конвертация цветов
    '''

    return "#%02x%02x%02x" % rgb

def scroll(*args):
    '''
    Прокрутка кода
    '''

    editArea.yview(*args)

# def update_line_numbers(event):
#     line_numbers.delete(1.0, END)
#     for i in range(1, int(editArea.index('end').split('.')[0])):
#         line_numbers.insert(END, str(i) + '\n')
#     line_numbers.tag_configure("align", justify='right')
#     line_numbers.tag_add("align", 1.0, "end")

# Предыдущий текст
previousText = ''

# Определение цветов ключевых слов в коде #####
normal = rgb((234, 234, 234))
keywords = rgb((148, 131, 242))
comments = rgb((95, 234, 165))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
error = rgb((255, 35, 35))
###############################################
font = '"Consolas" 12'
###############################################

# Определение списка регулярных выржаний для паттернов для покраски слов
repl = [
    ['(^| )(False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ['\'.*?\'', string],
    ['#.*?$', comments],
]

# Номера строк слева
# line_numbers = Text(
#     root,
#     # width=4,
#     # padx=4,
#     # pady=4,
#     relief=RAISED,
#     borderwidth=15,
#     font=font,
# )
# line_numbers.pack(side=LEFT, fill=Y)


# Колесо прокрутки #############
scrollbar = Scrollbar(
    root,
    width=20
)
scrollbar.pack(
    side=RIGHT,
    fill=BOTH,
)
scrollbar.config(command=scroll)
################################


# Гланый редактор кода ################
editArea = Text(
    root,
    background=background,
    foreground=normal,
    insertbackground=normal,
    relief=RAISED,
    borderwidth=15,
    font=font,
    yscrollcommand=scrollbar.set
)
editArea.pack(
    side=LEFT,
    fill=BOTH,
    expand=True
)
editArea.insert('1.0',
"""from random import randint

# Test function
def print_random_number(digits: int):
    if digits > 0:
        print(randint(0, 10**digits))
    else:
        print("Digits must be bigger then 0")

print_random_number(3)
"""
)
editArea.bind('<KeyRelease>', changes)
################################


# Создание меню ################
root.option_add("*tearOff", FALSE)

menu = Menu()
file_menu = Menu()
file_menu.add_command(label = "Open", command = file_open)
file_menu.add_command(label = "Debug", command = debug)
file_menu.add_command(label = "Test", command = test)
menu.add_cascade(label = "File", menu = file_menu)

root.config(menu = file_menu)
################################

# root.bind('<Control-d>', debug)

changes()
root.mainloop()