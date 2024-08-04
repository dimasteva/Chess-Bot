import tkinter as tk
from tkinter import ttk
from threading import Thread, Event

class UI(tk.Tk):
    def __init__(self, bot):
        self.bot = bot

        super().__init__()
        
        self.title("Chess Bot 1.0")
        self.geometry("500x500")

        # Frame za naslov
        title_frame = tk.Frame(self)
        title_frame.pack(fill="x")

        # Frame za ostatak GUI-a
        main_frame = tk.Frame(self)
        main_frame.pack(expand=True, fill="both")

        # Dodavanje naslova koristeći pack
        self.title_label = tk.Label(title_frame, text="Gamemodes", font=("Helvetica", 16))
        self.title_label.pack(pady=(20, 30))

        # Dodavanje ostalih widgeta koristeći grid
        options = ['Auto Detect Board', 'Grind Mode']
        self.combo = ttk.Combobox(main_frame, values=options, width=30, state='readonly')
        self.combo.grid(column=0, row=0, padx=20, pady=10)

        submit_button = tk.Button(main_frame, text="Submit", command=self.on_submit)
        submit_button.grid(column=1, row=0, padx=20, pady=10)

        self.stop_event = Event()
        self.bot_thread = None
    
    def on_submit(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.stop_event.set()
            self.bot_thread.join()
        
        self.stop_event.clear()

        selected_value = self.combo.get()

        play_again = False
        if selected_value == 'Auto Detect Board':
            self.bot_thread = Thread(target=self.bot.setup_auto_detect_board, args=(play_again, self.stop_event))
            self.bot_thread.start()
        elif selected_value == 'Grind Mode':
            self.bot_thread = Thread(target=self.bot.setup_grind_mode, args=(self.stop_event,))
            self.bot_thread.start()