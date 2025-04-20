import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')

class ImageSelectorApp:
    def __init__(self, root, folder_path):
        self.root = root
        self.folder_path = folder_path
        self.selected = set()
        self.image_buttons = {}
        # self.checkbox_icon = ImageTk.PhotoImage(Image.open("checkbox.png").resize((20, 20)))

        self.canvas = tk.Canvas(root)
        self.scroll_y = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.load_images()

        print_button = tk.Button(root, text="Print Selected", command=self.print_selected)
        print_button.pack(pady=10)

    def load_images(self):
        files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(IMAGE_EXTENSIONS)]
        for idx, file in enumerate(files):
            img_path = os.path.join(self.folder_path, file)
            image = Image.open(img_path).resize((100, 100))
            tk_image = ImageTk.PhotoImage(image)

            frame = tk.Frame(self.frame, bd=2, relief="groove")
            frame.grid(row=idx // 5, column=idx % 5, padx=5, pady=5)

            label = tk.Label(frame, image=tk_image)
            label.image = tk_image  # keep reference
            label.pack()
            label.bind("<Button-1>", lambda e, f=file, fr=frame: self.toggle_select(f, fr))

            self.image_buttons[file] = frame

    def toggle_select(self, filename, frame):
        if filename in self.selected:
            self.selected.remove(filename)
            frame.config(bg="SystemButtonFace")
        else:
            self.selected.add(filename)
            frame.config(bg="lightgreen")

    def print_selected(self):
        print("Selected files:")
        for f in self.selected:
            print(os.path.join(self.folder_path, f))

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Duplicate Image Selector")

    folder = filedialog.askdirectory(title="Select Folder with Images")
    if folder:
        app = ImageSelectorApp(root, folder)
        root.mainloop()
    else:
        print("No folder selected.")
