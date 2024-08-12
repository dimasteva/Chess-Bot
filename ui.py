import tkinter as tk
from tkinter import ttk, messagebox
from threading import Thread, Event

class UI(tk.Tk):
    def __init__(self, bot):
        self.bot = bot

        super().__init__()
        
        self.title("Chess Bot 1.0")
        self.geometry("600x500")
        self.iconbitmap('chess_icon.ico')

        title_frame = tk.Frame(self)
        title_frame.pack(fill="x")

        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        self.title_label = tk.Label(title_frame, text="Gamemodes", font=("Helvetica", 16))
        self.title_label.pack(pady=(20, 30))

        options = ['Auto Detect Board', 'Grind Mode']
        self.combo = ttk.Combobox(main_frame, values=options, width=30, state='readonly')
        self.combo.grid(column=0, row=0, padx=20, pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.on_combo_select)

        submit_button = tk.Button(main_frame, text="Submit", command=self.on_submit)
        submit_button.grid(column=1, row=0, padx=20, pady=10)

        self.status_label = tk.Label(main_frame, text="Waiting for match to finish...", font=("Helvetica", 11))
        self.status_label.grid(column=2, row = 0, padx=20, pady=10)
        self.status_label.grid_forget()

        self.grind_frame = tk.Frame(main_frame)
        self.dont_include = False

        self.listbox_vars = {}
        self.time_options = {
            'Bullet': [
                "Don't include",
                '30 sec',
                '20 sec | 1',
                '1 min',
                '1 | 1',
                '2 | 1'
            ],
            'Blitz': [
                "Don't include",
                '3 min',
                '5 min',
                '5 | 5',
                '5 | 2',
                '3 | 2'
            ],
            'Rapid': [
                "Don't include",
                '10 min',
                '15 | 10',
                '20 min',
                '30 min',
                '60 min',
                '10 | 5'
            ],
            #'Daily': [
            #    "Don't include",
            #    '1 day',
            #    '2 days',
            #    '3 days',
            #    '5 days',
            #    '7 days',
            #    '14 days'
            #]
        }

        for i, mode in enumerate(self.time_options.keys()):
            tk.Label(self.grind_frame, text=mode).grid(row=i, column=0, sticky='w')
            listbox = tk.Listbox(self.grind_frame, selectmode=tk.MULTIPLE, height=len(self.time_options[mode]), exportselection=False)
            listbox.grid(row=i, column=1, padx=10, pady=5)
            for option in self.time_options[mode]:
                listbox.insert(tk.END, option)
            listbox.select_set(0)
            listbox.bind("<<ListboxSelect>>", lambda event, mode=mode: self.on_listbox_select(event, mode))
            self.listbox_vars[mode] = listbox

        self.grind_frame.grid(column=0, row=1, columnspan=2, padx=20, pady=10)
        self.grind_frame.grid_remove()

        self.stop_event = Event()
        self.bot_thread = None

    def on_listbox_select(self, event, mode):
        listbox = event.widget
        selected_indices = listbox.curselection()

        if 0 in selected_indices:
            if len(selected_indices) == 2:
                if self.dont_include:
                    listbox.selection_clear(selected_indices[1])
                    self.dont_include = False
                else:
                    listbox.selection_clear(0)
                    self.dont_include = True
            else:
                for index in selected_indices:
                    listbox.selection_clear(index)
        else:
            listbox.selection_clear(0)

        if len(listbox.curselection()) == 0:
            listbox.select_set(0)


    def on_combo_select(self, event):
        selected_value = self.combo.get()
        if selected_value == 'Grind Mode':
            self.grind_frame.grid()
        else:
            self.grind_frame.grid_remove()

    def on_submit(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.status_label.grid(column=2, row = 0, padx=20, pady=10)
            self.update_idletasks()
            self.stop_event.set()
            self.bot_thread.join()

        self.stop_event.clear()
        self.status_label.grid_forget()
        self.update_idletasks()
        selected_value = self.combo.get()

        if selected_value == 'Auto Detect Board':
            self.bot_thread = Thread(target=self.bot.setup_auto_detect_board, args=(False, self.stop_event))
            self.bot_thread.start()
        elif selected_value == 'Grind Mode':
            selected_options = {mode: [self.listbox_vars[mode].get(i) for i in self.listbox_vars[mode].curselection()] 
                                for mode in self.time_options}
            filtered_options = {
            key: [value for value in values if value != "Don't include"]
            for key, values in selected_options.items()
            if "Don't include" not in values or len(values) > 1
            }

            if not filtered_options:
                messagebox.showinfo('Error', 'You need to select at least one game mode')
                return

            self.bot_thread = Thread(target=self.bot.setup_grind_mode, args=(self.stop_event, filtered_options))
            self.bot_thread.start()

