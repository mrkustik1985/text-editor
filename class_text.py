import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog as fd
import idlelib.colorizer as ic
import idlelib.percolator as ip
import re

start_size_screen = "1200x700"

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry(start_size_screen)
        self.filename = None

        self.create_title_file_name()

        self.create_last_action_title()

        self.create_find_and_replace_frame()

        self.create_main_menu()

        self.add_TEXT()

        self.add_hot_key()

    def info_about_text_editor(self, *args):
        messagebox.showinfo(
            "About text editor",
            " Это текстовый редактор!\n Тут вы можете писать текст, открывать и редактировать существующие файлы, и изменять текущие.\n Функционал горячих клавиш описан в другом окне:) Тут есть поддержка выделения текста совмещенная с перемещением по тексту\n",
        )

    def info_about_button(self, *args):
        messagebox.showinfo(
            "About tk.Button with editor and files",
            " Горячие клавиши и комбинацию к ним также можно найти в других окнах меню.\n cntrl+n - создать новый файл\n cntrl+o - открыть файл\n cntrl+s - сохранить, если не существует файла, то создать\n cntrl+a - сохранить файл как\n cntrl+e - выйти из редактора, перед выходом вас спросят сохранили ли вы файл\n",
        )

    def info_about_hot_keys(self, *args):
        messagebox.showinfo(
            "About Hot Keys",
            " cntrl+x - вырезать слово на котором находится курсор(также работает перед словом и сразу после него)\n cntrl+c - копировать выделенное\n cntrl+v - вставить выделенное\n cntrl+z - отменить последнее действие(редактрование слово, вставку и т.д)\n cntrl+p - удалить строку на которой находится курсор\n cntrl+u - удалить весь текст целиком",
        )

    def info_about_text_move(self, *args):
        messagebox.showinfo(
            "About movement fot text",
            " cntrl + -> курсор перемщается на 1 слово вправо\n cntrl + <- курсор перемщается на 1 слово влево\n fn + -> перемещается в конец строки\n fn + <- перемещается в начало строки\n",
        )

    def add_TEXT(self):
        self.text = tk.Text(
            self.root,
            font=("times new roman", 15, "bold"),
            bd=2,
            bg="black",
            fg="lime",
            padx=10,
            pady=10,
            wrap=tk.WORD,
            insertbackground="white",
            undo=True,
        )
        self.scrollbar = tk.Scrollbar(orient="vertical", command=self.text.yview)
        self.text["yscrollcommand"] = self.scrollbar.set
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text.pack(fill=tk.BOTH, expand=1)

    def make_highlighting(self):
      cdg = ic.ColorDelegator()
      cdg.idprog = re.compile(r'\s+(\w+)', re.S)
      cdg.tagdefs['MYGROUP'] = {'foreground': '#7F7F7F'} # ok
      cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000'} # ok
      cdg.tagdefs['KEYWORD'] = {'foreground': '#ff5c77'} # ok
      cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00'} 
      cdg.tagdefs['STRING'] = {'foreground': '#7F3F00'} # ok
      cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F'} # ok
      ip.Percolator(self.text).insertfilter(cdg)

    def create_title_file_name(self):
        self.title = tk.StringVar()
        self.title_bar = tk.Label(
            self.root,
            textvariable=self.title,
            font=("times new roman", 15, "bold"),
            bd=2,
            relief=tk.GROOVE,
        )
        self.title_bar.pack(side=tk.TOP, fill=tk.BOTH)
        self.is_open_file()

    def create_last_action_title(self):
        self.last_action = tk.StringVar()
        self.last_action_bar = tk.Label(
            self.root,
            textvariable=self.last_action,
            font=("times new roman", 15, "bold"),
            bd=4,
            relief=tk.GROOVE,
        )
        self.last_action_bar.pack(side=tk.BOTTOM, fill=tk.BOTH)
        self.last_action.set("welcome to text editor")

    def create_find_and_replace_frame(self):
        self.frame = tk.Frame(self.root)
        self.create_button_find()
        self.create_button_replace()
        self.frame.pack(side=tk.TOP, fill=tk.BOTH)

    def create_button_find(self):
        tk.Label(self.frame, text="Find").pack(side=tk.LEFT)
        self.edit_find = tk.Entry(self.frame)
        self.edit_find.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.edit_find.focus_set()
        self.find = tk.Button(self.frame, text="Find", command=self.find)
        self.find.pack(side=tk.LEFT)

    def create_button_replace(self):
        tk.Label(self.frame, text="Replace").pack(side=tk.LEFT)
        self.edit_replace = tk.Entry(self.frame)
        self.edit_replace.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.edit_replace.focus_set()
        self.replace = tk.Button(self.frame, text="Replace", command=self.find_replace)
        self.replace.pack(side=tk.LEFT)

    def create_file_menu(self):
        self.file_menu = tk.Menu(
            self.main_menu,
            font=("times new roman", 12, "bold"),
            activebackground="skyblue",
            tearoff=0,
        )
        self.file_menu.add_command(
            label="New", accelerator="Ctrl+N", command=self.new_file
        )
        self.file_menu.add_command(
            label="Open", accelerator="Ctrl+O", command=self.open_file
        )
        self.file_menu.add_command(
            label="Save", accelerator="Ctrl+S", command=self.save_file
        )
        self.file_menu.add_command(
            label="Save as", accelerator="Ctrl+A", command=self.first_save_file
        )
        self.file_menu.add_separator()
        self.file_menu.add_command(
            label="Exit", accelerator="Ctrl+E", command=self.exit
        )

    def create_help_menu(self):
        self.help_menu = tk.Menu(
            self.main_menu,
            font=("times new roman", 12, "bold"),
            activebackground="skyblue",
            tearoff=0,
        )
        self.help_menu.add_command(
            label="About Text Editor", command=self.info_about_text_editor
        )
        self.help_menu.add_command(label="About tk.Button", command=self.info_about_button)
        self.help_menu.add_command(
            label="About HotKeys", command=self.info_about_hot_keys
        )
        self.help_menu.add_command(
            label="About Movement fot text", command=self.info_about_text_move
        )

    def create_edit_menu(self):
        self.edit_menu = tk.Menu(
            self.main_menu,
            font=("times new roman", 12, "bold"),
            activebackground="skyblue",
            tearoff=0,
        )
        self.edit_menu.add_command(
            label="CutWord", accelerator="Ctrl+X", command=self.delete_currently_word
        )
        self.edit_menu.add_command(
            label="Copy", accelerator="Ctrl+C", command=self.copy
        )
        self.edit_menu.add_command(
            label="Paste", accelerator="Ctrl+V", command=self.paste
        )
        self.edit_menu.add_command(
            label="Cancel", accelerator="Ctrl+Z", command=self.cancel_action
        )
        self.edit_menu.add_command(
            label="DltCrntStr",
            accelerator="Ctrl+B",
            command=self.delete_currently_string,
        )
        self.edit_menu.add_separator()
        self.edit_menu.add_command(
            label="Undo", accelerator="Ctrl+U", command=self.undo
        )

    def create_main_menu(self):
        self.main_menu = tk.Menu(
            self.root, font=("times new roman", 12, "bold"), activebackground="skyblue"
        )
        self.root.config(menu=self.main_menu)
        self.create_help_menu()
        self.create_edit_menu()
        self.create_file_menu()
        self.main_menu.add_cascade(label="File", menu=self.file_menu)
        self.main_menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.main_menu.add_cascade(label="Help", menu=self.help_menu)

    def is_open_file(self):
        if self.filename != None:
            self.title.set(self.filename)
            t = self.filename[-2] + self.filename[-1]
            if t == "py":
                self.make_highlighting()
        else:
            self.title.set("Untitled")

    def new_file(self, *args):
        if self.filename != None:
            self.save_file()
        else:
            self.first_save_file()
        self.text.delete(1.0, tk.END)
        self.filename = None
        self.is_open_file()
        self.last_action.set("new file created")

    def open_file(self, *args):
        text_copy = self.text.get(1.0, tk.END)
        try:
            filetypes = (("All files", "*.*"), ("text files", "*.txt"))
            self.filename = fd.askopenfilename(
                title="Open a file", initialdir="/", filetypes=filetypes
            )
            if self.filename != None:
                self.text.delete(1.0, tk.END)
                for l in open(self.filename):
                    self.text.insert(tk.END, l)
                self.is_open_file()
                self.last_action.set("file opened")
            else:
                self.last_action.set("file is not opened")
        except Exception as e:
            pass

    def save_file(self, *args):
        text_copy = self.text.get(1.0, tk.END)
        try:
            if self.filename != None:
                with open(self.filename, "w") as f:
                    f.write(self.text.get(1.0, tk.END))
                self.last_action.set("file saved")
            else:
                op = messagebox.askyesno("your file is unnamed", "save it?")
                if op > 0:
                    self.first_save_file()
        except Exception as e:
            self.text.insert("1.0", text_copy)
            self.last_action.set("error of saved file")
            messagebox.showerror("ERROR", e)

    def first_save_file(self, *args):
        text_copy = self.text.get(1.0, tk.END)
        try:
            f = fd.asksaveasfilename(
                filetypes=(
                    ("All Files", "*.*"),
                    ("Text Files", "*.txt"),
                    ("Python Files", "*.py"),
                )
            )
            if f:
                self.filename = f
                f = open(self.filename, "w")
                f.write(self.text.get(1.0, tk.END))
                f.close()
            self.is_open_file()
            self.last_action.set("saved successfully")
        except Exception as e:
            self.text.insert("1.0", text_copy)
            self.last_action.set("error of saved file")
            messagebox.showerror("ERROR", e)

    def exit(self, *args):
        op = messagebox.askyesno("WARNING", "Your unsaved data may be lost!! Exit?")
        if op > 0:
            self.root.destroy()
        else:
            return

    def copy(self, *args):
        self.text.event_generate("<<Copy>>")

    def paste(self, *args):
        pass

    def undo(self, *args):
        try:
            self.text.delete(1.0, tk.END)
            self.last_action.set("Undone Successfully")
        except Exception as e:
            messagebox.showerror("Exception", e)


    def cancel_action(self, *args):
        self.text.edit_undo()

    def find_need_ind_of_line_and_txt(self):
        id_now = self.text.index("insert").split(".")
        txt = self.text.get(1.0, tk.END)
        self.text.delete(1.0, tk.END)
        txt = txt.split("\n")
        cnt = 0
        id_last_not_empty = 0
        cl = 0
        for i in txt:
            cl += 1
            if i != "" and i != "\n":
                id_last_not_empty = cl
        return (id_last_not_empty, txt[::], id_now[::])

    def delete_currently_string(self, *args):
        id_last_not_empty, txt, id_now = self.find_need_ind_of_line_and_txt()
        cnt = 0
        for l in txt:
            cnt += 1
            if cnt != int(id_now[0]) and cnt <= id_last_not_empty:
                self.text.insert(tk.END, l + "\n")

    def delete_currently_word(self, *args):
        id_last_not_empty, txt, id_now = self.find_need_ind_of_line_and_txt()
        id_in_row = int(id_now[1])
        id_row = int(id_now[0])
        row = 0
        for line in txt:
            row += 1
            if row > id_last_not_empty:
                break
            if row == id_row:
                y = line[:id_in_row].rfind(" ")
                x = line[id_in_row:].find(" ")
                if x == -1:
                    x = len(line)
                need_move_str = '\n'
                if row == id_last_not_empty:
                    need_move_str = ''
                self.text.insert(tk.END, line[: y + 1] + line[id_in_row + x :] + need_move_str)
            elif row < id_last_not_empty:
                self.text.insert(tk.END, line + "\n")
            elif row == id_last_not_empty:
                self.text.insert(tk.END, line)

    def find(self, *args):
        self.text.tag_remove("found", "1.0", tk.END)
        is_find_pressed = self.edit_find.get()
        if is_find_pressed:
            idx = "1.0"
            while 1:
                idx = self.text.search(is_find_pressed, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                # last index sum of current index and length of text
                lastidx = "% s+% dc" % (idx, len(is_find_pressed))
                self.text.tag_add("found", idx, lastidx)
                idx = lastidx
            self.text.tag_config("found", foreground="red")
        self.edit_find.focus_set()

    def find_replace(self, *args):
        self.text.tag_remove("found", "1.0", tk.END)
        is_pressed_find = self.edit_find.get()
        is_pressed_replace = self.edit_replace.get()
        if (
            is_pressed_find
            and is_pressed_replace
            and is_pressed_find != is_pressed_replace
        ):
            idx = "1.0"
            while 1:
                idx = self.text.search(is_pressed_find, idx, nocase=1, stopindex=tk.END)
                if not idx:
                    break
                lastidx = "% s+% dc" % (idx, len(is_pressed_find))
                self.text.delete(idx, lastidx)
                self.text.insert(idx, is_pressed_replace)
                lastidx = "% s+% dc" % (idx, len(is_pressed_replace))
                self.text.tag_add("found", idx, lastidx)
                idx = lastidx
            self.text.tag_config("found", foreground="green", background="yellow")
        self.edit_find.focus_set()
        self.edit_replace.focus_set()

    def add_hot_key(self):
        self.text.bind("<Control-e>", self.exit)
        self.text.bind("<Control-n>", self.new_file)
        self.text.bind("<Control-o>", self.open_file)
        self.text.bind("<Control-s>", self.save_file)
        self.text.bind("<Control-a>", self.first_save_file)
        self.text.bind("<Control-x>", self.delete_currently_word)
        self.text.bind("<Control-c>", self.copy)
        self.text.bind("<Control-v>", self.paste)
        self.text.bind("<Control-u>", self.undo)
        self.text.bind("<Control-z>", self.cancel_action)
        self.text.bind("<Control-b>", self.delete_currently_string)
