from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import*
from PIL import Image, ImageTk
import pandas as pd
import os

# Load the CSV data into a pandas DataFrame with the specified semicolon delimiter
csv_file_path = 'Dossiers.csv'  # Replace with your actual CSV file path

def set_fullscreen_on_start(root):
    # root.attributes('-fullscreen', True)

    # getting screen width and height of display
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    # setting tkinter window size
    root.geometry("%dx%d" % (width, height))

def rgb_to_hex(rgb):
    """
    Convert an RGB tuple to a hexadecimal color code.
    """
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def apply_alternating_row_colors(tree):
    """
    Applies alternating row colors to the Treeview using RGB colors.
    """
    for i, item in enumerate(tree.get_children()):
        if i % 2 == 0:  # Even index rows
            tree.item(item, tags=('evenrow',))
        else:  # Odd index rows
            tree.item(item, tags=('oddrow',))

    # Define RGB color codes
    even_row_color = rgb_to_hex((231, 232, 233))  # Light Grey
    odd_row_color = rgb_to_hex((193, 233, 255))    # Light Blue

    # Define the tag configurations
    tree.tag_configure('evenrow', background=even_row_color)
    tree.tag_configure('oddrow', background=odd_row_color)

def check_time_and_close():
    now = datetime.now().time()
    start_time = now.replace(hour=12, minute=30, second=0, microsecond=0)
    end_time = now.replace(hour=13, minute=30, second=0, microsecond=0)

    if start_time <= now <= end_time:
        messagebox.showwarning("Attention", "L'application est fermée entre 12h30 et 13h30.")
        root.destroy()

def load_csv(file_path):
    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
    for encoding in encodings:
        try:
            return pd.read_csv(file_path, encoding=encoding, delimiter=';', on_bad_lines='skip')
        except (UnicodeDecodeError, pd.errors.ParserError):
            continue
    raise ValueError(f"Could not read the file with any of the tested encodings: {encodings}")

try:
    df = load_csv(csv_file_path)
except ValueError as e:
    messagebox.showerror("Error", f"Failed to read CSV file: {e}")
    exit()

desired_columns = [
    "Image",
    "Article",
    "Designation",
    "Rangement",
    "Stock reel",
    "Prix unitaire de vente",
    "Prix unitaire d'achat",
    "Famille article",
    "Autre designation",
    "Code fournisseur",
    "Référence fournisseur",
]

column_widths = {
    "Image": 10,
    "Article": 10,
    "Designation": 400,
    "Rangement": 70,
    "Stock reel": 50,
    "Prix unitaire de vente": 0,
    "Prix unitaire d'achat": 0,
    "Famille article": 40,
    "Autre designation": 250,
    "Code fournisseur": 0,
    "Référence fournisseur": 100,
}

# Modify the column names to include newlines for multi-row effect
multi_row_headings = {
    "Image": "Image",
    "Article": "Article",
    "Designation": "Designation",  # Example with newline
    "Rangement": "Rangement",
    "Stock reel": "Stock Reel",            # Example with newline
    "Prix unitaire de vente": "Prix de Vente",  # Example with multiple newlines
    "Prix unitaire d'achat": "Prix d'Achat",    # Example with multiple newlines
    "Famille article": "Famille",  # Example with newline
    "Autre designation": "Autre Designation",  # Example with newline
    "Code fournisseur": "Code Four",    # Example with newline
    "Référence fournisseur": "Ref Four"  # Example with newline
}

def update_treeview(data_frame):
    for row in tree.get_children():
        tree.delete(row)

    for index, row in data_frame.iterrows():
        image_file_name = str(row.get("Article", ""))
        image_display_text = "Voir l'Image" if image_file_name else "Pas d'Image"
        tree.insert("", "end", iid=index, values=[image_display_text, *[row.get(col, "") for col in desired_columns[1:]]])

    apply_alternating_row_colors(tree)

def search():
    query = search_var.get()
    if query:
        terms = query.lower().split()
        filtered_df = df[df.apply(lambda row: all(term in ' '.join(row.astype(str)).lower() for term in terms), axis=1)]
        update_treeview(filtered_df)
    else:
        update_treeview(df)

# def close_app():
#     root.destroy()

def on_cell_click(event):
    try:
        item_id = tree.selection()[0]
        column_id = tree.identify_column(event.x)
        photo_path = r"\\Svrsavs01\savsoft\GED\Photos\Identité_1"

        if column_id == "#1":
            item_index = tree.index(item_id)
            row_data = df.iloc[item_index]
            image_file_name = str(row_data.get("Article", ""))

            if not image_file_name:
                messagebox.showwarning("Warning", "No image file associated with this entry.")
                return

            image_path = os.path.join(photo_path, image_file_name, f"{image_file_name}.jpg")
            if os.path.exists(image_path):
                show_image(image_path, image_file_name)
            else:
                messagebox.showwarning("Warning", "Image file not found.")
    except IndexError:
        messagebox.showwarning("Warning", "No item selected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_image(image_path,image_file_name):
    try:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)

        image_window = tk.Toplevel(root)
        image_window.title(image_file_name)

        img_label = tk.Label(image_window, image=photo)
        img_label.image = photo
        img_label.pack()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load image: {e}")

def periodic_time_check():
    check_time_and_close()
    root.after(60000, periodic_time_check)

## -------------------Début de la présentation --------------------------------------------

root = tk.Tk()

img = PhotoImage(file='logo.png')
root.iconphoto(False, img)

root.title("LauncherStockMinelec")

set_fullscreen_on_start(root)

check_time_and_close()
periodic_time_check()

top_frame = tk.Frame(root)
top_frame.pack(side=tk.TOP, fill=tk.X)

# close_button = tk.Button(top_frame, text="Close", command=close_app)
# close_button.pack(side=tk.RIGHT, padx=5)

search_var = tk.StringVar()
search_entry = tk.Entry(top_frame, width=60, textvariable=search_var)
search_entry.pack(side=tk.LEFT, pady=10, padx=5)

search_button = tk.Button(top_frame, width=20, text="Rechercher", command=search)
search_button.pack(side=tk.LEFT, pady=5, padx=5)

tree_frame = tk.Frame(root)
tree_frame.pack(fill=tk.BOTH, expand=True)

vertical_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
horizontal_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)

tree = ttk.Treeview(tree_frame, columns=desired_columns, show='headings',
                    yscrollcommand=vertical_scrollbar.set,
                    xscrollcommand=horizontal_scrollbar.set)

vertical_scrollbar.config(command=tree.yview)
horizontal_scrollbar.config(command=tree.xview)

tree.grid(row=0, column=0, sticky='nsew')
vertical_scrollbar.grid(row=0, column=1, sticky='ns')
horizontal_scrollbar.grid(row=1, column=0, sticky='ew')

tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

#for column in desired_columns:
#    tree.heading(column, text=column)
#    tree.column(column, anchor="w", width=column_widths.get(column, 10))

for column in desired_columns:
    tree.heading(column, text=multi_row_headings.get(column, column))
    tree.column(column, anchor="w", width=column_widths.get(column, 10))

tree.bind("<ButtonRelease-1>", on_cell_click)

update_treeview(df)

root.mainloop()
