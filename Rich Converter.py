import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

# GUI Functions
def browse_file():
    """Browse for an input .ass file"""
    file_path = filedialog.askopenfilename(filetypes=[("ASS Subtitle Files", "*.ass")])
    if file_path:
        input_path_var.set(file_path)

def browse_output_folder():
    """Browse for an output folder"""
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_dir_var.set(folder_path)

def convert_file():
    """Run the conversion process"""
    input_path = input_path_var.get()
    output_dir = output_dir_var.get()

    if not input_path or not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid .ass file.")
        return

    # Determine output path
    base_name = os.path.basename(input_path)
    name_only, ext = os.path.splitext(base_name)
    output_path = os.path.join(output_dir if output_dir else os.path.dirname(input_path), f"{name_only} converted{ext}")

    try:
        # Run the conversion function directly
        convert_ass_file(input_path, output_path)
        messagebox.showinfo("Success", f"✅ Converted file saved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Conversion failed:\n{e}")

def launch_gui():
    """Launch the GUI"""
    global input_path_var, output_dir_var

    root = tk.Tk()
    root.title("Dankop's .ASS to Rich Text Converter")
    root.geometry("500x320")
    root.resizable(False, False)

    input_path_var = tk.StringVar()
    output_dir_var = tk.StringVar()

    tk.Label(root, text="Select .ASS Subtitle File:").pack(pady=5)
    tk.Entry(root, textvariable=input_path_var, width=50).pack()
    tk.Button(root, text="Browse", command=browse_file).pack(pady=2)

    tk.Label(root, text="(Optional) Select Output Folder:").pack(pady=5)
    tk.Entry(root, textvariable=output_dir_var, width=50).pack()
    tk.Button(root, text="Browse", command=browse_output_folder).pack(pady=2)

    tk.Button(root, text="Convert", command=convert_file, bg="#4CAF50", fg="white", height=2, width=20).pack(pady=10)

    tk.Label(root, text="Please contact Dankop on the AI Sponge Discord\nif there are any issues with the application in output or function", fg="gray").pack(pady=10)

    root.mainloop()  # Start the GUI

# Conversion function (unchanged from convert_ass.py)
def convert_ass_file(input_file, output_file):
    """Reads an ASS subtitle file, converts it to Rich Text, and writes the modified output to a new file."""
    import re

    # Define mappings for tag replacements
    TAG_REPLACEMENTS = {
        r"\\s1": "<s>", r"\\s0": "</s>",  # Strikethrough
        r"\\b1": "<b>", r"\\b0": "</b>",  # Bold
        r"\\i1": "<i>", r"\\i0": "</i>",  # Italic
        r"\\u1": "<u>", r"\\u0": "</u>",  # Underline
        r"\\fnImpact": '<font="Impact SDF">',  # Font Impact
        r"\\c": "</color>",  # Color reset (Only where explicitly present)
        r"\\fs0": "</size>",  # Font size reset
    }

    def convert_bgr_to_rgb_with_fixed_alpha(match):
        """Convert BGR hex color (`HXXXXXX&`) to RGB format."""
        bgr = match.group(1)
        alpha = match.group(2) if match.group(2) else "FF"

        # Convert BGR to RGB
        rgb = bgr[4:6] + bgr[2:4] + bgr[0:2]

        # Flip Alpha if present
        if match.group(2):
            alpha = f"{255 - int(alpha, 16):02X}"

        return f"<color=#{rgb}{alpha}>"

    def convert_font_size(match):
        """Convert `\fsXX` (ASS font size) to `<size=XX>`."""
        return f"<size={match.group(1)}>"

    def process_ass_to_rich_text(ass_text):
        """Converts ASS tags to Rich Text equivalents."""
        ass_text = re.sub(r"{([^}]*)}", r"\1", ass_text)
        ass_text = re.sub(r"\\c&H([0-9A-Fa-f]{6})&(?:\\1a&H([0-9A-Fa-f]{2})&)?", convert_bgr_to_rgb_with_fixed_alpha, ass_text)
        ass_text = re.sub(r"\\fs(\d+)", convert_font_size, ass_text)

        for pattern, replacement in TAG_REPLACEMENTS.items():
            ass_text = re.sub(pattern, replacement, ass_text)

        return ass_text

    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    processed_lines = [process_ass_to_rich_text(line) if line.startswith("Dialogue:") else line for line in lines]

    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(processed_lines)

# Run GUI
if __name__ == "__main__":
    launch_gui()
