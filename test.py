import tkinter as tk
from tkinter import Scrollbar

class ScrollableText(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.text_widget = tk.Text(self, wrap=tk.NONE, **kwargs)
        self.vsb = Scrollbar(self, orient="vertical", command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.vsb.set)

        self.vsb.grid(row=0, column=1, sticky='ns')
        self.text_widget.grid(row=0, column=0, sticky='nsew')

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.text_widget.bind("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        self.text_widget.yview_scroll(-1*(event.delta//120), "units")


root = tk.Tk()
root.title("Synchronized Scrollbar Demo")

# Создаем фрейм
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)

# Создаем виджет для текста и номеров строк
text_widget = ScrollableText(frame, bg="white")
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

line_numbers_widget = tk.Text(frame, width=4, padx=4, pady=4, wrap='none')
line_numbers_widget.pack(side=tk.LEFT, fill=tk.Y)

# Создаем привязку прокрутки между текстовым виджетом и виджетом номеров строк
def on_text_scroll(*args):
    text_widget.vsb.set(*args)
    line_numbers_widget.yview_moveto(args[0])

text_widget.vsb.config(command=on_text_scroll)

root.mainloop()
