import random

BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *
import pandas

current_card = {}
to_learn = {}
try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("./data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    current_card = random.choice(to_learn)
    website.after_cancel(flip_timer)
    french = current_card["French"]
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=french, fill="black")
    canvas.itemconfig(card_background, image=front)
    flip_timer = website.after(3000, func=flip)


def flip():
    english = current_card["English"]
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=english, fill="white")
    canvas.itemconfig(card_background, image=back)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("./data/words_to_learn.csv",index=False)
    next_card()

website = Tk()

website.title("Flashcard", )
website.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = website.after(3000, func=flip)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
front = PhotoImage(file="./images/card_front.png")
back = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=front)

card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(column=0, row=1)

right_image = PhotoImage(file="./images/right.png")
known_button = Button(image=right_image, highlightthickness=0, command=is_known)
known_button.grid(column=1, row=1)
next_card()
website.mainloop()
