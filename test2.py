import tkinter as tk
root = tk.Tk()

file1data = ("ciao\n"*100)

S1 = tk.Scrollbar(root)
S1.grid(row=0, column=1,sticky=tk.N + tk.S + tk.E + tk.W)
template1 = tk.Text(root, height=25, width=50,wrap=tk.NONE, yscrollcommand=S1.set)
template1.grid(row=0, column=0)
template1.insert(tk.END, file1data)
S1.config(command=template1.yview)

S2 = tk.Scrollbar(root)
S2.grid(row=0, column=3,sticky=tk.N + tk.S + tk.E + tk.W)
template2 = tk.Text(root, height=25, width=50, wrap=tk.NONE, yscrollcommand=S2.set)
template2.grid(row=0, column=2)
template2.insert(tk.END, file1data)
S2.config(command=template2.yview)

def sync_scroll(*args):
    template1.yview(*args)
    template2.yview(*args)
    
S1.config(command=sync_scroll)
S2.config(command=sync_scroll)

tk.mainloop()