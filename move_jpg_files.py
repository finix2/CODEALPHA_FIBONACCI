import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil

class JPGMoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("JPG File Mover")
        self.root.geometry("500x300")

        # Source folder
        self.label_source = tk.Label(root, text="Source Folder:")
        self.label_source.pack(pady=10)
        self.entry_source = tk.Entry(root, width=50)
        self.entry_source.pack(pady=5)
        self.btn_browse_source = tk.Button(root, text="Browse", command=self.browse_source)
        self.btn_browse_source.pack(pady=5)

        # Destination folder
        self.label_dest = tk.Label(root, text="Destination Folder:")
        self.label_dest.pack(pady=10)
        self.entry_dest = tk.Entry(root, width=50)
        self.entry_dest.pack(pady=5)
        self.btn_browse_dest = tk.Button(root, text="Browse", command=self.browse_dest)
        self.btn_browse_dest.pack(pady=5)

        # Move button
        self.btn_move = tk.Button(root, text="Move JPG Files", command=self.move_jpg_files)
        self.btn_move.pack(pady=20)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_source.delete(0, tk.END)
            self.entry_source.insert(0, folder)

    def browse_dest(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_dest.delete(0, tk.END)
            self.entry_dest.insert(0, folder)

    def move_jpg_files(self):
        source_folder = self.entry_source.get()
        dest_folder = self.entry_dest.get()

        if not source_folder or not dest_folder:
            messagebox.showerror("Error", "Please select both source and destination folders.")
            return

        if not os.path.exists(source_folder):
            messagebox.showerror("Error", "Source folder does not exist.")
            return

        if not os.path.exists(dest_folder):
            try:
                os.makedirs(dest_folder)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create destination folder: {e}")
                return

        jpg_count = 0
        try:
            for filename in os.listdir(source_folder):
                if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
                    source_path = os.path.join(source_folder, filename)
                    dest_path = os.path.join(dest_folder, filename)
                    shutil.move(source_path, dest_path)
                    jpg_count += 1
            messagebox.showinfo("Success", f"Moved {jpg_count} JPG files to {dest_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = JPGMoverApp(root)
    root.mainloop()