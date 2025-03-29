import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Globalna lista przechowująca ścieżki wybranych obrazów
images_list = []

def crop_image(image_path, left, top, right, bottom):
    """The function crops the image according to the given pixel values."""
    image = Image.open(image_path)
    width, height = image.size
    # Obliczamy obszar przycięcia:
    crop_box = (left, top, width - right, height - bottom)
    if crop_box[2] <= crop_box[0] or crop_box[3] <= crop_box[1]:
        raise ValueError("The given crop values are too large, resulting in an incorrect crop area.")
    return image.crop(crop_box)

def select_images():
    """Feature that allows you to select multiple images via a dialog box."""
    filetypes = [
        ("Image files", "*.tif *.jpeg *.jpg *.png"),
        ("All files", "*.*")
    ]
    filenames = filedialog.askopenfilenames(title="Select images", filetypes=filetypes)
    if filenames:
        global images_list
        images_list = filenames
        image_paths_var.set("\n".join(filenames))

def select_folder():
    """Funkcja umożliwiająca wybór folderu zapisu."""
    folder = filedialog.askdirectory(title="Select save folder")
    if folder:
        save_folder_var.set(folder)

def crop_and_save():
    """The function crops each selected image and saves the result to the selected folder."""
    global images_list
    if not images_list:
        messagebox.showerror("Error", "No images selected!")
        return

    save_folder = save_folder_var.get()
    if not save_folder:
        messagebox.showerror("Error", "No save folder selected!")
        return

    try:
        left = int(entry_left.get())
        top = int(entry_top.get())
        right = int(entry_right.get())
        bottom = int(entry_bottom.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values ​​for trimming.")
        return

    errors = []
    successes = []
    for image_path in images_list:
        try:
            cropped = crop_image(image_path, left, top, right, bottom)
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
            new_filename = os.path.join(save_folder, f"{name}_cropped{ext}")
            cropped.save(new_filename)
            successes.append(new_filename)
        except Exception as e:
            errors.append(f"{os.path.basename(image_path)}: {e}")

    if successes:
        messagebox.showinfo("Success", "Cropped images saved successfully:\n" + "\n".join(successes))
    if errors:
        messagebox.showerror("Error", "There were errors while cropping the following images:\n" + "\n".join(errors))

# Główne okno aplikacji
root = tk.Tk()
root.title("AntPix")
root.iconbitmap(r"C:\Users\topgu\Desktop\Splotowe Sieci Neuronowe\antpix.ico")
root.geometry("800x600")

# Wczytanie obrazu tła i ustawienie go jako tło okna
bg_image = Image.open(r"C:\Users\topgu\Desktop\Splotowe Sieci Neuronowe\AntPix.png")
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Definicje stylów dla futurystycznego designu
bg_color_frame = "#222222"
label_style = {"bg": bg_color_frame, "fg": "#00ffea", "font": ("Segoe UI", 10)}
button_style = {"bg": "#444444", "fg": "#00ffea", "font": ("Segoe UI", 10, "bold"), "bd": 0, "relief": "flat",
                "activebackground": "#333333", "activeforeground": "#00ffee"}
entry_style = {"bg": "#333333", "fg": "#00ffea", "insertbackground": "#00ffea", "font": ("Segoe UI", 10)}

# Zmienne do przechowywania wybranych ścieżek
image_paths_var = tk.StringVar()
save_folder_var = tk.StringVar()

# Ramka na elementy interfejsu z futurystycznym designem
frame = tk.Frame(root, bg=bg_color_frame)
# Umieszczenie ramki na środku prawej strony okna z lekkim odstępem od krawędzi
frame.place(relx=1.0, rely=0.5, anchor="e", x=-20)

# Przycisk wyboru obrazów
btn_select_images = tk.Button(frame, text="Select images", command=select_images, **button_style)
btn_select_images.grid(row=0, column=0, sticky="w", padx=5, pady=5)

lbl_image_paths = tk.Label(frame, textvariable=image_paths_var, wraplength=400, **label_style)
lbl_image_paths.grid(row=0, column=1, padx=5, pady=5)

# Przycisk wyboru folderu zapisu
btn_select_folder = tk.Button(frame, text="Select save folder", command=select_folder, **button_style)
btn_select_folder.grid(row=1, column=0, sticky="w", pady=(5,0), padx=5)

lbl_save_folder = tk.Label(frame, textvariable=save_folder_var, wraplength=400, **label_style)
lbl_save_folder.grid(row=1, column=1, padx=5, pady=(5,0))

# Instrukcje oraz pola do wpisania wartości przycinania
lbl_instructions = tk.Label(frame, text="Enter the number of pixels to crop:", **label_style)
lbl_instructions.grid(row=2, column=0, columnspan=2, pady=(10,0), padx=5)

lbl_left = tk.Label(frame, text="Left:", **label_style)
lbl_left.grid(row=3, column=0, sticky="e", padx=5, pady=2)
entry_left = tk.Entry(frame, width=10, **entry_style)
entry_left.grid(row=3, column=1, sticky="w", padx=(5,0), pady=2)
entry_left.insert(0, "0")

lbl_top = tk.Label(frame, text="Up:", **label_style)
lbl_top.grid(row=4, column=0, sticky="e", padx=5, pady=2)
entry_top = tk.Entry(frame, width=10, **entry_style)
entry_top.grid(row=4, column=1, sticky="w", padx=(5,0), pady=2)
entry_top.insert(0, "0")

lbl_right = tk.Label(frame, text="Right:", **label_style)
lbl_right.grid(row=5, column=0, sticky="e", padx=5, pady=2)
entry_right = tk.Entry(frame, width=10, **entry_style)
entry_right.grid(row=5, column=1, sticky="w", padx=(5,0), pady=2)
entry_right.insert(0, "0")

lbl_bottom = tk.Label(frame, text="Down:", **label_style)
lbl_bottom.grid(row=6, column=0, sticky="e", padx=5, pady=2)
entry_bottom = tk.Entry(frame, width=10, **entry_style)
entry_bottom.grid(row=6, column=1, sticky="w", padx=(5,0), pady=2)
entry_bottom.insert(0, "0")

# Przycisk wykonania przycinania
btn_crop = tk.Button(frame, text="Crop images", command=crop_and_save, **button_style)
btn_crop.grid(row=7, column=0, columnspan=2, pady=(10,10), padx=5)

root.mainloop()
