import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import random

# Dictionary of words categorized by difficulty level and topics
words = {
    "beginner": {
        "fruits": ["apple", "pear", "peach", "figs", "grape"],
        "animals": ["cat", "dog", "bird", "fish", "lion"],
        "car companies": ["toyota", "ford", "honda", "nissan", "kia"],
        "countries": ["usa", "china", "japan", "india", "france"],
        "foods": ["pizza", "taco", "curry", "noodle", "rice"]
    },
    "moderate": {
        "fruits": ["banana", "cherry", "elder", "honey", "kiwis"],
        "animals": ["tiger", "bear", "monkey", "giraffe", "zebra"],
        "car companies": ["volkswagen", "bmw", "mercedes", "audi", "hyundai"],
        "countries": ["germany", "italy", "spain", "brazil", "australia"],
        "foods": ["sushi", "steak", "chicken", "fish", "burger"]
    },
    "expert": {
        "fruits": ["watermelon", "strawberry", "raspberry", "blueberry", "blackberry"],
        "animals": ["elephant", "kangaroo", "penguin", "koala", "rhinoceros"],
        "car companies": ["ferrari", "lamborghini", "porsche", "bentley", "rolls-royce"],
        "countries": ["argentina", "south africa", "south korea", "turkey", "poland"],
        "foods": ["lasagna", "falafel", "schnitzel", "tortilla", "cannelloni"]
    }
}

class WordGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Game")
        self.root.configure(bg='#f0f8ff')  # Light blue background
        
        self.level = tk.StringVar(value="beginner")
        self.guess = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title Label
        tk.Label(self.root, text="Word Game", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#000080").grid(row=0, column=0, columnspan=5, pady=(10, 10))
        
        # Level Selection
        level_frame = tk.Frame(self.root, bg="#e0f7fa", bd=2, relief="solid")
        level_frame.grid(row=1, column=0, columnspan=5, pady=(10, 10), padx=10, ipadx=10, ipady=10)
        
        tk.Label(level_frame, text="Choose a level:", font=("Helvetica", 14, "bold"), bg="#e0f7fa", fg="#006064").grid(row=0, column=0, pady=(10, 0), columnspan=3)
        
        levels = ["Beginner", "Moderate", "Expert"]
        level_combobox = ttk.Combobox(level_frame, textvariable=self.level, values=levels, state='readonly', font=("Helvetica", 12))
        level_combobox.grid(row=1, column=0, columnspan=3, pady=(10, 0), padx=(5, 5))
        level_combobox.set("Beginner")  # Default value
        
        # Custom Start Button
        tk.Button(level_frame, text="Start", command=self.start_game, font=("Helvetica", 12), bg="#87ceeb", fg="white", width=10).grid(row=2, column=0, columnspan=3, pady=(10, 10))
        
        # Game Display
        self.canvas = tk.Canvas(self.root, width=300, height=100, bg="#f0f8ff", highlightthickness=0)
        self.canvas.grid(row=2, column=0, columnspan=5, pady=(10, 10))
        
        self.hint_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f8ff")
        self.hint_label.grid(row=3, column=0, columnspan=5, pady=(10, 10))
        
        self.total_letters_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f8ff")
        self.total_letters_label.grid(row=4, column=0, columnspan=5, pady=(10, 10))
        
        # Unarranged Letters
        self.unarranged_letters_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f8ff")
        self.unarranged_letters_label.grid(row=5, column=0, columnspan=5, pady=(10, 10))
        
        # Guess Input
        input_frame = tk.Frame(self.root, bg="#e0f7fa", bd=2, relief="solid")
        input_frame.grid(row=6, column=0, columnspan=5, pady=(10, 10), padx=10, ipadx=10, ipady=10)
        
        tk.Label(input_frame, text="Enter a letter:", font=("Helvetica", 14), bg="#e0f7fa").grid(row=0, column=0, pady=(10, 0))
        tk.Entry(input_frame, textvariable=self.guess, font=("Helvetica", 14)).grid(row=0, column=1, pady=(10, 0), padx=(5, 5))
        
        tk.Button(input_frame, text="Submit", command=self.submit_guess, font=("Helvetica", 12), bg="#00796b", fg="#ffffff").grid(row=0, column=2, pady=(10, 0), padx=(5, 5))
        
        self.hint_canvas = tk.Canvas(self.root, width=300, height=100, bg="#f0f8ff", highlightthickness=0)
        self.hint_canvas.grid(row=7, column=0, columnspan=5, pady=(10, 10))
        
        self.tries_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f8ff")
        self.tries_label.grid(row=8, column=0, columnspan=5, pady=(10, 10))
        
        self.message_label = tk.Label(self.root, text="", font=("Helvetica", 14), bg="#f0f8ff")
        self.message_label.grid(row=9, column=0, columnspan=5, pady=(10, 10))
        
    def draw_star(self, x, y, size=20):
        points = [
            x, y - size,
            x + size * 0.588, y + size * 0.809,
            x - size * 0.951, y - size * 0.309,
            x + size * 0.951, y - size * 0.309,
            x - size * 0.588, y + size * 0.809
        ]
        return points

    def draw_hints(self):
        self.hint_canvas.delete("all")
        stars = self.hint_limit - self.hint_count
        for i in range(stars):
            x = 30 + i * 50
            y = 50
            star_id = self.hint_canvas.create_polygon(self.draw_star(x, y), fill="#ff69b4", outline="#ff69b4")
            self.hint_canvas.tag_bind(star_id, "<Button-1>", lambda event, star_id=star_id: self.give_hint(star_id))
        
    def start_game(self):
        self.level_choice = self.level.get().lower()
        self.word, self.category = self.choose_word(self.level_choice)
        self.guessed = "_" * len(self.word)
        self.guessed_letters = []
        self.tries = 10
        self.hint_count = 0
        self.hint_limit = 1 if self.level_choice == "beginner" else 2 if self.level_choice == "moderate" else 3
        
        self.update_display()
        self.draw_hints()
        
    def choose_word(self, level):
        if level not in words:
            messagebox.showerror("Error", "Invalid level. Please choose from beginner, moderate, or expert.")
            return None, None

        # Set word length ranges based on level
        if level == "beginner":
            min_length, max_length = 3, 5
        elif level == "moderate":
            min_length, max_length = 5, 7
        elif level == "expert":
            min_length, max_length = 8, 11
        else:
            min_length, max_length = 0, float('inf')

        # Filter words based on length criteria
        valid_words = []
        categories = list(words[level].keys())
        for category in categories:
            for word in words[level][category]:
                if min_length <= len(word) <= max_length:
                    valid_words.append((category, word))

        if not valid_words:
            messagebox.showerror("Error", f"No words found in the {level} level within the specified length range.")
            return None, None

        # Select a random category and word from filtered list
        category, word = random.choice(valid_words)
        return word, category
    
    def update_display(self):
        self.canvas.delete("all")
        for i, letter in enumerate(self.guessed):
            x0, y0 = 50 + i * 30, 20
            x1, y1 = x0 + 30, y0 + 30
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="#000080", fill="#ffb6c1", width=2)
            if letter != "_":
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=letter, font=("Helvetica", 16), fill="green")
            else:
                self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=letter, font=("Helvetica", 16), fill="#0000ff")
        
        self.hint_label.config(text=f"Hint: The word is related to {self.category}.")
        self.total_letters_label.config(text=f"Total letters: {len(self.word)}")
        self.tries_label.config(text=f"Tries left: {self.tries}")
        self.message_label.config(text="")
        self.unarranged_letters_label.config(text="Unarranged letters:")
        self.display_unarranged_letters()

    def display_unarranged_letters(self):
        self.canvas.delete("unarranged")
        unarranged_letters = random.sample(self.word, len(self.word))
        letters_str = ' '.join(unarranged_letters)
        self.canvas.create_oval(50, 160, 250, 200, outline="#ff0000", width=2, tags="unarranged", stipple="gray50")
        self.canvas.create_text(150, 180, text=letters_str, font=("Helvetica", 16), fill="#ff0000", tags="unarranged")
        
    def submit_guess(self):
        action = self.guess.get().lower()
        self.guess.set("")
        
        if len(action) != 1 or not action.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return
        
        if action in self.guessed_letters:
            self.message_label.config(text="You already guessed this letter.")
            return
        
        self.guessed_letters.append(action)
        
        if action not in self.word:
            self.tries -= 1
            self.message_label.config(text="This letter is not in the word.")
        else:
            self.guessed = "".join([char if char in self.guessed_letters else "_" for char in self.word])
        
        self.update_display()
        self.draw_hints()
        
        if "_" not in self.guessed:
            messagebox.showinfo("Congratulations", f"You guessed the word '{self.word}'!")
            self.start_game()
        
        if self.tries == 0:
            messagebox.showinfo("Game Over", f"Game over. The word was '{self.word}'.")
            self.start_game()
            
    def give_hint(self, star_id):
        if self.hint_count < self.hint_limit:
            available_indices = [i for i, x in enumerate(self.word) if x not in self.guessed_letters]
            if available_indices:
                hint_index = random.choice(available_indices)
                self.guessed_letters.append(self.word[hint_index])
                self.guessed = "".join([char if char in self.guessed_letters else "_" for char in self.word])
                self.hint_count += 1
                self.update_display()
                self.hint_canvas.delete(star_id)
                self.message_label.config(text=f"You have {self.hint_limit - self.hint_count} hints left.")
            else:
                self.message_label.config(text="No more hints available.")
        else:
            self.message_label.config(text="No more hints available.")

if __name__ == "__main__":
    root = tk.Tk()
    app = WordGameApp(root)
    root.mainloop()
