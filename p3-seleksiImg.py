import os
from tkinter import Tk, Label, Button, Checkbutton, IntVar
from PIL import Image, ImageTk
import shutil
import csv

class ImageViewer:
    def __init__(self, root, image_folder):
        self.root = root
        self.image_folder = image_folder
        self.image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.current_index = 0
        self.idx = 1

        # Set background color of the root window
        root.configure(bg="#333333")  # You can adjust the hex color code as needed

        self.previous_button = Button(root, text="Previous", state="disabled", command=self.show_previous, bg="#555555", fg="white", width=15, height=2)
        self.previous_button.grid(row=1, column=0, padx=100)

        self.move_button = Button(root, text="Pindahkan", command=self.move_image, bg="#555555", fg="white", width=15, height=2)
        self.move_button.grid(row=0, column=1, pady=20, padx=80)

        self.delete_button = Button(root, text="Delete", command=self.delete_image, bg="#555555", fg="white", width=15, height=2)
        self.delete_button.grid(row=0, column=2, pady=20, padx=80)

        self.next_button = Button(root, text="Next", command=self.show_next, bg="#555555", fg="white", width=15, height=2)
        self.next_button.grid(row=1, column=3, padx=100)

        self.image_label = Label(root, bg="#333333")  # Set background color of the Label
        self.image_label.grid(row=1, column=0, columnspan=4, pady=20)

        self.filename_label = Label(root, text="", bg="#333333", fg="white")  # Label for displaying filename
        self.filename_label.grid(row=2, column=0, columnspan=4, pady=10)

        # Checkboxes
        self.checkbox_vars = [IntVar() for _ in range(6)]
        checkbox_titles = ["KepalaLeher", "Dada", "Full Sayap", "Paha Atas", "Paha Bawah", "Kaki"]

        for i, title in enumerate(checkbox_titles):
            checkbox = Checkbutton(root, text=title, variable=self.checkbox_vars[i], bg="#333333", fg="white")
            checkbox.grid(row=i + 3, column=0, pady=5)

        self.show_image()

    def show_image(self):
        if not self.image_files:
            # If there are no images left, disable all buttons
            self.previous_button["state"] = "disabled"
            self.next_button["state"] = "disabled"
            self.move_button["state"] = "disabled"
            self.delete_button["state"] = "disabled"
            self.filename_label.config(text="No images found.")
            return

        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
        img = Image.open(image_path)

        if img.height > 400:
            img = img.resize((int(img.width * (400 / img.height)), 400), Image.BICUBIC)
        else:
            img = img.resize((400, int(img.height * (400 / img.width))), Image.BICUBIC)

        tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=tk_img)
        self.image_label.image = tk_img

        # Update the filename label
        filename = f"Img-{self.idx}"
        self.filename_label.config(text=filename)

        self.update_buttons_state()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.show_image()

    def show_previous(self):
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.show_image()

    def move_image(self):
        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
        destination_folder = "baru"

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_filename = f"img-{self.idx}.png"
        destination_path = os.path.join(destination_folder, destination_filename)

        # Move the image only if the "Pindahkan" button is clicked
        shutil.move(image_path, destination_path)

        # Update the CSV file only if the image is successfully moved
        csv_file_path = os.path.join(os.path.dirname(self.image_folder), "moved_files.csv")
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write header if the file is newly created
            if os.path.getsize(csv_file_path) == 0:
                csv_writer.writerow(["nama_file"])

            csv_writer.writerow([destination_filename])

        # Increment index for the next image
        self.idx += 1

        # Reload image files after moving
        self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Show the next image
        self.show_next()

    def delete_image(self):
        if not self.image_files:
            return

        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])

        # Delete the image file
        os.remove(image_path)

        # Reload image files after deletion
        self.image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        # Show the next image or disable buttons if there are no images left
        if not self.image_files:
            self.previous_button["state"] = "disabled"
            self.next_button["state"] = "disabled"
            self.move_button["state"] = "disabled"
            self.delete_button["state"] = "disabled"
            self.filename_label.config(text="No images found.")
        else:
            # Show the next image
            self.show_next()

    def update_buttons_state(self):
        if self.current_index == 0:
            self.previous_button["state"] = "disabled"
        else:
            self.previous_button["state"] = "normal"

        if self.current_index == len(self.image_files) - 1:
            self.next_button["state"] = "disabled"
        else:
            self.next_button["state"] = "normal"

if __name__ == "__main__":
    root = Tk()
    root.title("Image Viewer")
    root.geometry("1200x800")  # Adjusted height to accommodate the filename label

    # Set the background color of the root window
    root.configure(bg="#333333")

    image_folder = "lama"  # Replace with your image folder
    if not os.path.exists(image_folder):
        print(f"Error: Folder '{image_folder}' not found.")
    else:
        image_viewer = ImageViewer(root, image_folder)
        root.mainloop()
