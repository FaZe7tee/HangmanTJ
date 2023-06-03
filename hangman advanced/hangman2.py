import tkinter as tk
from tkinter import messagebox
import random
import os



# Global variables
current_user = None

high_scores = {}

# Function to handle the registration screen
def register_screen():
    global register_window
    register_window = tk.Toplevel(main_window)
    register_window.title("Register")
    register_window.geometry("300x250")

    global current_user
    global password
    global confirm_password
    current_user = tk.StringVar()
    password = tk.StringVar()
    confirm_password = tk.StringVar()

    # User input fields for current_user, password, and confirm password
    tk.Label(register_window, text="Please enter details below").pack()
    tk.Label(register_window, text="").pack()
    tk.Label(register_window, text="Username *").pack()
    tk.Entry(register_window, textvariable=current_user).pack()
    tk.Label(register_window, text="Password *").pack()
    tk.Entry(register_window, textvariable=password, show="*").pack()
    tk.Label(register_window, text="Confirm Password *").pack()
    tk.Entry(register_window, textvariable=confirm_password, show="*").pack()
    tk.Label(register_window, text="").pack()

    # Button to register the user
    tk.Button(register_window, text="Register", width=10, height=1, command=register_user).pack()

# Function to validate password requirements
def validate_password(password):
    if len(password) < 8:
        return False
    return True

# Function to register a new user
def register_user():
    username_info = current_user.get()
    password_info = password.get()
    confirm_password_info = confirm_password.get()

    # Check if any field is left empty
    if username_info == "" or password_info == "" or confirm_password_info == "":
        messagebox.showinfo("Error", "Please fill in all fields!")
        return

    # Validate password requirements
    if not validate_password(password_info):
        messagebox.showinfo("Error", "Password should be at least 8 characters long!")
        return

    # Check if the password matches the confirmed password
    if password_info != confirm_password_info:
        messagebox.showinfo("Error", "Password does not match!")
        return

    # Check if the logins.txt file exists
    if os.path.isfile("logins.txt"):
        with open("logins.txt", "r") as file:
            # Check if the chosen current_user already exists
            for line in file:
                if username_info == line.strip().split(",")[0]:
                    messagebox.showinfo("Error", "Username already exists!")
                    return

    # Write the current_user and password to the logins.txt file
    with open("logins.txt", "a") as file:
        file.write(username_info + "," + password_info + "\n")

    # Show a success message and close the registration window
    messagebox.showinfo("Success", "Registration successful!")
    register_window.destroy()

# Function to handle the login screen
def login_screen():
    global login_window
    login_window = tk.Toplevel(main_window)
    login_window.title("Login")
    login_window.geometry("300x250")

    global username_verify
    global password_verify
    username_verify = tk.StringVar()
    password_verify = tk.StringVar()

    # User input fields for current_user and password
    tk.Label(login_window, text="Please enter details below").pack()
    tk.Label(login_window, text="").pack()
    tk.Label(login_window, text="Username *").pack()
    tk.Entry(login_window, textvariable=username_verify).pack()
    tk.Label(login_window, text="Password *").pack()
    tk.Entry(login_window, textvariable=password_verify, show="*").pack()
    tk.Label(login_window, text="").pack()

    # Button to login
    tk.Button(login_window, text="Login", width=10, height=1, command=login_user).pack()

# Function to handle user login
def login_user():
    global current_user
    high_scores[current_user]=0
    username_info = username_verify.get()
    password_info = password_verify.get()

    # Check if any field is left empty
    if username_info == "" or password_info == "":
        messagebox.showinfo("Error", "Please fill in all fields!")
        return

    login_success = False

    # Check if the logins.txt file exists
    if os.path.isfile("logins.txt"):
        with open("logins.txt", "r") as file:
            # Check if the entered current_user and password match the records
            for line in file:
                user, password = line.strip().split(",")
                if username_info == user:
                    if password_info == password:
                        login_success = True
                        current_user = user
                        break
                    else:
                        messagebox.showinfo("Error", "Wrong password!")
                        return
            # Handle login success or failure
            if login_success:
                messagebox.showinfo("Success", "Login successful!")
                login_window.destroy()
                show_game_options()
            else:
                messagebox.showinfo("Error", "Username does not exist!")
    else:
        # If the logins.txt file doesn't exist, create one and repeat the login process
        with open("logins.txt", "a"):
            pass
        messagebox.showinfo("Info", "No users registered. Please register a new user.")

# Function to show game options after login
def show_game_options():
    global game_options_window
    game_options_window = tk.Toplevel(main_window)
    game_options_window.title("Game Options")
    game_options_window.geometry("300x250")

    # Buttons for play, view scores, and quit
    tk.Label(game_options_window, text="Game Options", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    tk.Label(game_options_window, text="").pack()
    tk.Button(game_options_window, text="Play New Game", height="2", width="30", command=start_game).pack()
    tk.Label(game_options_window, text="").pack()
    tk.Button(game_options_window, text="View High Scores", height="2", width="30", command=view_high_scores).pack()
    tk.Label(game_options_window, text="").pack()
    tk.Button(game_options_window, text="logout", height="2", width="30", command=logout).pack()
    tk.Label(game_options_window, text="").pack()

# Function to handle user logout
def logout():
    global current_user
    current_user = ""
    game_options_window.destroy()
    
#getting the secret_word
def load_secret_word():
    secret_word = []
    with open("secret_word.txt", "r") as file:
        for line in file:
            secret_word.append(line.strip())
    return secret_word

# Function to choose a random secret_word from a list
def choose_word(secret_word):
    import random
    return random.choice(secret_word)

# Function to start a new game
def start_game():
    global guessed_letters
    guessed_letters = set()
    global secret_word
    secret_word = load_secret_word()
    secret_word = choose_word(secret_word)
    global guessed_word
    guessed_word = ["_"] * len(secret_word)
    global attempts
    attempts = 7

    def update_display():
        word_label.config(text="Word: " + " ".join(guessed_word))
        attempts_label.config(text="Attempts remaining: " + str(attempts))
        guessed_label.config(text="Guessed letters: " + " ".join(sorted(guessed_letters)))

    def guess():
        global attempts
        guess = guess_entry.get()
        if guess.isalpha() and len(guess) == 1:
            if guess in guessed_letters:
                messagebox.showerror("Error", "You already guessed that letter.")
            elif guess in secret_word:
                guessed_letters.add(guess)
                for i, letter in enumerate(secret_word):
                    if letter == guess:
                        guessed_word[i] = guess
                update_display()
            else:
                guessed_letters.add(guess)
                attempts -= 1
                update_display()
        else:
            messagebox.showerror("Error", "Invalid input. Please enter a single letter.")
        guess_entry.delete(0, tk.END)
        
        if "".join(guessed_word) == secret_word:
            messagebox.showinfo("Success", f"Congratulations! You guessed the secret_word: {secret_word}")
    
            save_high_score()
            game_window.destroy()
            # entry_game(current_user)
        elif attempts == 0:
            messagebox.showinfo("Failure", f"Sorry, you ran out of attempts. The secret_word was: {secret_word}")
            save_high_score()
            game_window.destroy()
            # entry_game(current_user)
        # Guessing logic goes here

    # Create the game window
    game_window = tk.Toplevel(main_window)
    game_window.title("Hangman Game")
    game_window.geometry("300x250")

    word_label = tk.Label(game_window, text="Word: " + " ".join(guessed_word))
    word_label.pack()

    attempts_label = tk.Label(game_window, text="Attempts remaining: " + str(attempts))
    attempts_label.pack()

    guessed_label = tk.Label(game_window, text="Guessed letters: " + " ".join(sorted(guessed_letters)))
    guessed_label.pack()

    guess_entry = tk.Entry(game_window)
    guess_entry.pack()

    guess_button = tk.Button(game_window, text="Guess", command=guess)
    guess_button.pack()

# Function to save the user's high score
def save_high_score():
    global high_scores
    if os.path.isfile("scores.txt"):
        with open("scores.txt", "r") as file:
            high_scores = dict([line.strip().split(",") for line in file])
    
    if current_user in high_scores:
        if attempts > int(high_scores[current_user]):
            high_scores[current_user] = str(attempts)
    else:
        high_scores[current_user] = str(attempts)

    with open("scores.txt", "w") as file:
        for user, score in high_scores.items():
            file.write(user + "," + score + "\n")

# Function to view high scores
def view_high_scores():
    global high_scores_window
    high_scores_window = tk.Toplevel(main_window)
    high_scores_window.title("High Scores")
    high_scores_window.geometry("300x250")

    if os.path.isfile("scores.txt"):
        with open("scores.txt", "r") as file:
            high_scores = dict([line.strip().split(",") for line in file])
            sorted_scores = sorted(high_scores.items(), key=lambda x: int(x[1]))

            tk.Label(high_scores_window, text="High Scores", bg="blue", width="300", height="2",
                     font=("Calibri", 13)).pack()
            tk.Label(high_scores_window, text="").pack()

            for user, score in sorted_scores:
                tk.Label(high_scores_window, text=user + ": " + score).pack()
    else:
        tk.Label(high_scores_window, text="No high scores available.").pack()

    tk.Label(high_scores_window, text="").pack()
    tk.Button(high_scores_window, text="Close", width=10, command=high_scores_window.destroy).pack()

# Function to create the main window
def main_window_screen():
    global main_window
    main_window = tk.Tk()
    main_window.geometry("300x250")
    main_window.title("User Authentication")

    # Buttons for register, login, and quit
    tk.Label(main_window, text="User Authentication", bg="blue", width="300", height="2",
             font=("Calibri", 13)).pack()
    tk.Label(main_window, text="").pack()
    tk.Button(main_window, text="Register", height="2", width="30", command=register_screen).pack()
    tk.Label(main_window, text="").pack()
    tk.Button(main_window, text="Login", height="2", width="30", command=login_screen).pack()
    tk.Label(main_window, text="").pack()
    tk.Button(main_window, text="Quit", height="2", width="30", command=main_window.quit).pack()
    tk.Label(main_window, text="").pack()

    main_window.mainloop()

# Run the main window
main_window_screen()
