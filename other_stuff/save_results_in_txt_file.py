import tkinter as tk
from tkinter import ttk
from subprocess import Popen, PIPE
import sys
import os


def run_program():
    if os.path.exists("./output.txt"):
        os.remove("./output.txt")
        print("File deleted successfully!")
    # Clear the text widget before running the program
    output_text.config(state=tk.NORMAL)
    output_text.delete('1.0', tk.END)
    output_text.config(state=tk.DISABLED)

    # Run the program and redirect stdout and stderr to a text file
    with open("output.txt", "w") as output_file:
        process = Popen([sys.executable, 'Pure_Aloha_Simulation.py'], stdout=output_file, stderr=PIPE, universal_newlines=True)
        stdout, stderr = process.communicate()

    # Display a message in the GUI to indicate where the output is saved
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, "Console output is saved to output.txt file.")
    output_text.config(state=tk.DISABLED)

    # Scroll the text widget to the bottom
    output_text.yview_moveto(1.0)

# Create the main window
root = tk.Tk()
root.title("Program Output")

# Configure a dark theme
style = ttk.Style(root)
style.theme_use('clam')  # Choose one of the available themes
root.configure(bg='#1e1e1e')  # Set background color    

# Create a text widget to display output
output_text = tk.Text(root, wrap=tk.WORD, bg='#1e1e1e', fg='white')
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
output_text.config(state=tk.DISABLED)  # Make the text widget read-only

# Create a vertical scroll bar
scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

# Button to run the program
run_button = ttk.Button(root, text="Run Program", command=run_program)
run_button.pack()

# Run the Tkinter event loop
root.mainloop()
