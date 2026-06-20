import tkinter as tk
from tkinter import ttk
import random
import string

from analyzer import analyze_password


def check_password():
    password = password_entry.get()

    result = analyze_password(password)

    if result["strength"] == "Weak":
        strength_label.config(
            text="Strength: Weak",
            fg="red"
        )
        strength_bar["value"] = 33

    elif result["strength"] == "Medium":
        strength_label.config(
            text="Strength: Medium",
            fg="orange"
        )
        strength_bar["value"] = 66

    else:
        strength_label.config(
            text="Strength: Strong",
            fg="green"
        )
        strength_bar["value"] = 100

    entropy_label.config(
        text=f"Entropy: {result['entropy']} bits"
    )

    if result["common"]:
        common_label.config(
            text="⚠ Common Password Detected",
            fg="red"
        )
    else:
        common_label.config(
            text="✓ Not a Common Password",
            fg="green"
        )

    checks_label.config(
        text=
        f"Uppercase: {'✔' if result['upper'] else '✘'}\n"
        f"Lowercase: {'✔' if result['lower'] else '✘'}\n"
        f"Numbers: {'✔' if result['digit'] else '✘'}\n"
        f"Special: {'✔' if result['special'] else '✘'}"
    )

    suggestions_text.delete("1.0", tk.END)

    if result["suggestions"]:
        for item in result["suggestions"]:
            suggestions_text.insert(
                tk.END,
                f"• {item}\n"
            )
    else:
        suggestions_text.insert(
            tk.END,
            "Excellent password!"
        )


def toggle_password():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


def generate_password():
    characters = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = "".join(
        random.choice(characters)
        for _ in range(16)
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


root = tk.Tk()
root.title("Password Strength Analyzer")
root.geometry("550x650")
root.resizable(False, False)

title = tk.Label(
    root,
    text="Password Strength Analyzer",
    font=("Arial", 18, "bold")
)
title.pack(pady=15)

password_label = tk.Label(
    root,
    text="Enter Password:"
)
password_label.pack()

password_entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12),
    show="*"
)
password_entry.pack(pady=5)

show_var = tk.BooleanVar()

show_checkbox = tk.Checkbutton(
    root,
    text="Show Password",
    variable=show_var,
    command=toggle_password
)
show_checkbox.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

analyze_button = ttk.Button(
    button_frame,
    text="Analyze Password",
    command=check_password
)
analyze_button.grid(
    row=0,
    column=0,
    padx=10
)

generate_button = ttk.Button(
    button_frame,
    text="Generate Password",
    command=generate_password
)
generate_button.grid(
    row=0,
    column=1,
    padx=10
)

strength_label = tk.Label(
    root,
    text="Strength:",
    font=("Arial", 12, "bold")
)
strength_label.pack(pady=5)

strength_bar = ttk.Progressbar(
    root,
    orient="horizontal",
    length=300,
    mode="determinate"
)
strength_bar.pack(pady=5)

entropy_label = tk.Label(
    root,
    text="Entropy:"
)
entropy_label.pack(pady=5)

common_label = tk.Label(
    root,
    text="",
    font=("Arial", 10, "bold")
)
common_label.pack(pady=5)

checks_label = tk.Label(
    root,
    text="",
    justify="left",
    font=("Arial", 11)
)
checks_label.pack(pady=10)

suggestion_label = tk.Label(
    root,
    text="Suggestions",
    font=("Arial", 12, "bold")
)
suggestion_label.pack()

suggestions_text = tk.Text(
    root,
    height=8,
    width=45
)
suggestions_text.pack(pady=10)

root.mainloop()