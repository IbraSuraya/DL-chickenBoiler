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
        self.idx = 700
        self.csv_headers = ["neckHead", "breast", "wing", "thigh", "feet"]
        self.checkbox_vars = [IntVar() for _ in range(6)]
        self.checkbox_list = []

        # Set background color of the root window
        root.configure(bg="#333333")  # You can adjust the hex color code as needed

        self.previous_button = Button(root, text="Previous", state="disabled", command=self.show_previous, bg="#555555", fg="white", width=15, height=2)
        self.previous_button.grid(row=1, column=0, padx=100)

        self.delete_button = Button(root, text="Delete", command=self.delete_image, bg="#555555", fg="white", width=15, height=2)
        self.delete_button.grid(row=0, column=1, pady=20, padx=80)

        self.move_button = Button(root, text="Pindahkan", command=self.move_image, bg="#555555", fg="white", width=15, height=2)
        self.move_button.grid(row=0, column=2, pady=20, padx=80)

        self.next_button = Button(root, text="Next", command=self.show_next, bg="#555555", fg="white", width=15, height=2)
        self.next_button.grid(row=1, column=3, padx=100)

        self.image_label = Label(root, bg="#333333")  # Set background color of the Label
        self.image_label.grid(row=1, column=0, columnspan=4, pady=20)

        self.filename_label = Label(root, text="", bg="#333333", fg="white")  # Label for displaying filename
        self.filename_label.grid(row=2, column=0, columnspan=4, pady=10)

        # Inside __init__ method
        self.checkbox_vars = [IntVar() for _ in self.csv_headers]

        # Checkboxes
        for i, title in enumerate(self.csv_headers):
            checkbox = Checkbutton(self.root, text=title, variable=self.checkbox_vars[i], command=lambda i=i: self.update_checkbox_value(i))
            self.checkbox_list.append(checkbox)
            checkbox.grid(row=i + 3, column=1, pady=5)

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
        # filename = f"Img-{self.idx}"
        filename = self.image_files[self.current_index]
        self.filename_label.config(text=filename[-10:]+f"{self.idx}")

        self.update_buttons_state()

    def show_next(self):
        self.current_index = (self.current_index + 1) % len(self.image_files)
        self.show_image()

    def show_previous(self):
        self.current_index = (self.current_index - 1) % len(self.image_files)
        self.show_image()

    def move_image(self):
        image_path = os.path.join(self.image_folder, self.image_files[self.current_index])
        destination_folder = "data\\fix"

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        destination_filename = f"img-{self.idx}.png"
        destination_path = os.path.join(destination_folder, destination_filename)

        # Move the image only if the "Pindahkan" button is clicked
        shutil.move(image_path, destination_path)

        # Mendapatkan nilai checkbox dan menyusunnya menjadi list
        checkbox_values = [var.get() for var in self.checkbox_vars]

        # Update the CSV file only if the image is successfully moved
        csv_file_path = os.path.join(os.path.dirname(self.image_folder), "multiLabel.csv")
        with open(csv_file_path, mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)

            # Write header if the file is newly created
            if os.path.getsize(csv_file_path) == 0:
                header_row = ["nama_file"] + self.csv_headers
                csv_writer.writerow(header_row)

            # Write data row
            data_row = [destination_filename] + checkbox_values
            csv_writer.writerow(data_row)

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
  
    # Inside your ImageViewer class
    def update_checkbox_value(self, index):
        checked_boxes = [var.get() for var in self.checkbox_vars]

if __name__ == "__main__":
    root = Tk()
    root.title("Image Viewer")
    root.geometry("1200x800")  # Adjusted height to accommodate the filename label

    # Set the background color of the root window
    root.configure(bg="#333333")

    image_folder = "data\\raw2"  # Replace with your image folder
    if not os.path.exists(image_folder):
        print(f"Error: Folder '{image_folder}' not found.")
    else:
        image_viewer = ImageViewer(root, image_folder)
        root.mainloop()
