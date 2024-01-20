import tkinter as tk

def update_output():
    checked_boxes = [var.get() for var in checkboxes_vars]
    checked_titles = [titles[i] for i, checked in enumerate(checked_boxes) if checked]
    print("Checked titles:", checked_titles)

# List of titles A-F
titles = ['A', 'B', 'C', 'D', 'E', 'F']

# Create the main window
window = tk.Tk()
window.title("Checkbox Example")

# Create checkbox variables
checkboxes_vars = [tk.IntVar() for _ in titles]

# Create checkboxes and associate with variables
for i, title in enumerate(titles):
    checkbox = tk.Checkbutton(window, text=title, variable=checkboxes_vars[i], command=update_output)
    checkbox.pack(anchor='w')

# Run the Tkinter event loop
window.mainloop()
