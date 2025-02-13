import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import math
import sys

# Import sound module based on OS
if sys.platform.startswith("win"):
    import winsound  # Windows beep sound
else:
    import os  # Linux/macOS beep sound

# ---------------------------- CONSTANTS ------------------------------- #
WORK_MIN = 25  # Work session duration in minutes
SHORT_BREAK_MIN = 5  # Short break duration in minutes
LONG_BREAK_MIN = 15  # Long break duration in minutes
FONT_NAME = "Arial"
reps = 0
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Pomodoro Timer", fg="black")
    check_marks.config(text="")
    reps = 0

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    """Starts a new Pomodoro session and plays a buzzer sound."""
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        title_label.config(text="Long Break", fg="red")
        play_buzzer()  # Beep at the start of Long Break
        count_down(long_break_sec)
    elif reps % 2 == 0:
        title_label.config(text="Short Break", fg="blue")
        play_buzzer()  # Beep at the start of Short Break
        count_down(short_break_sec)
    else:
        title_label.config(text="Work", fg="green")
        play_buzzer()  # Beep at the start of Work session
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    minutes = math.floor(count / 60)
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"
    
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        play_buzzer()  # Beep when the timer ends
        start_timer()
        marks = "✔" * (reps // 2)
        check_marks.config(text=marks)

# ---------------------------- SOUND ALERT (BUZZER) ------------------------------- #
def play_buzzer():
    """Plays a beep sound when a session starts or ends."""
    if sys.platform.startswith("win"):  # Windows beep sound
        winsound.Beep(1000, 500)  # Frequency=1000Hz, Duration=500ms
    else:  # Linux/macOS beep sound
        os.system("echo -e '\a'")  # ASCII Bell character to trigger beep

# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro Timer")
window.config(padx=50, pady=25, bg="white")

# Title Label
title_label = tk.Label(text="Pomodoro Timer", font=(FONT_NAME, 20, "bold"), fg="black", bg="white")
title_label.grid(column=1, row=0)

# Load and Display Tomato Image
img = Image.open("tomato.png")  # Ensure the image is in the same folder
img = img.resize((200, 224), Image.LANCZOS)  # Resize for better display
tomato_img = ImageTk.PhotoImage(img)

canvas = tk.Canvas(width=200, height=224, bg="white", highlightthickness=0)
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Start Button
start_button = tk.Button(text="Start", font=(FONT_NAME, 12), command=start_timer, highlightthickness=0)
start_button.grid(column=0, row=2)

# Reset Button
reset_button = tk.Button(text="Reset", font=(FONT_NAME, 12), command=reset_timer, highlightthickness=0)
reset_button.grid(column=2, row=2)

# Check Marks
check_marks = tk.Label(font=(FONT_NAME, 14), fg="green", bg="white")
check_marks.grid(column=1, row=3)

window.mainloop()
