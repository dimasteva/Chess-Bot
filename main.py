import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from bot import ChessBot

class UI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Chess Bot 1.0")
        self.geometry("500x300")

        self.title_label = tk.Label(self, text="Chess Bot", font=("Helvetica", 16))
        self.title_label.pack(pady=(20, 30))

        self.form_frame = tk.Frame(self)
        self.form_frame.pack(padx=20, pady=10, fill=tk.X)

        self.setup_log_in()
    
    def setup_log_in(self):
        self.email_label = tk.Label(self.form_frame, text="Email/Username:", font=("Helvetica", 10))
        self.email_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.email_entry = tk.Entry(self.form_frame, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        self.password_label = tk.Label(self.form_frame, text="Password:", font=("Helvetica", 10))
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.password_entry = tk.Entry(self.form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        self.login_button = tk.Button(self.form_frame, text="Login", command=self.login)
        self.login_button.grid(row=3, column=1, columnspan=2, pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        bot = ChessBot(email, password, headless=True)
        if bot.login():
            messagebox.showinfo("Login Successful", "You have successfully logged in!")
            self.withdraw()
            bot.switch_to_normal_mode()
            bot.start()
        else:
            messagebox.showerror("Login Failed", "The email or password is incorrect. Please try again.")
            

def main():
    app = UI()
    app.mainloop()

if __name__ == "__main__":
    main()
