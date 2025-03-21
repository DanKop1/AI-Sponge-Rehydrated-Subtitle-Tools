import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

# Conversion logic (unchanged)
def convert_ass_to_rich_text(ass_text):
    tag_mappings = {
        r"\\b1": "<b>",  r"\\b0": "</b>",
        r"\\i1": "<i>",  r"\\i0": "</i>",
        r"\\u1": "<u>",  r"\\u0": "</u>",
        r"\\s1": "<s>",  r"\\s0": "</s>",
    }

    color_pattern = re.compile(r"\\c&H([0-9A-Fa-f]{6})&")

    def color_replacement(match):
        hex_color = match.group(1)
        reversed_color = hex_color[4:6] + hex_color[2:4] + hex_color[0:2]
        return f'<color=#{reversed_color}>'

    font_size_pattern = re.compile(r"\\fs(\d+)")

    def replace_ass_tags(match):
        tag_content = match.group(1)
        modified_text = tag_content
        modified_text = color_pattern.sub(color_replacement, modified_text)
        modified_text = font_size_pattern.sub(r"<size=\1>", modified_text)
        for pattern, replacement in tag_mappings.items():
            modified_text = re.sub(pattern, replacement, modified_text)
        return modified_text

    ass_text = re.sub(r"{([^}]*)}", replace_ass_tags, ass_text)
    return ass_text

def process_ass_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        lines = file.readlines()

    processed_lines = []
    for line in lines:
        if line.startswith("Dialogue:"):
            parts = line.split(",", 9)
            if len(parts) == 10:
                parts[9] = convert_ass_to_rich_text(parts[9])
            processed_lines.append(",".join(parts))
        else:
            processed_lines.append(line)

    with open(output_file, "w", encoding="utf-8") as file:
        file.writelines(processed_lines)

# GUI Logic
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("ASS Files", "*.ass")])
    if file_path:
        input_path_var.set(file_path)

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_dir_var.set(folder_path)

def convert_file():
    input_path = input_path_var.get()
    output_dir = output_dir_var.get()

    if not input_path or not os.path.isfile(input_path):
        messagebox.showerror("Error", "Please select a valid .ass file.")
        return

    base_name = os.path.basename(input_path)
    name_only, ext = os.path.splitext(base_name)
    output_name = f"{name_only} rich 2{ext}"

    output_path = os.path.join(output_dir if output_dir else os.path.dirname(input_path), output_name)

    try:
        process_ass_file(input_path, output_path)
        messagebox.showinfo("Success", f"✅ Converted file saved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Conversion failed:\n{e}")

# GUI Setup
root = tk.Tk()
root.title("Dankop's .ass tags to Rich tags Text Converter")
root.geometry("500x280")
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

# Support text
tk.Label(root, text="Please contact Dankop on the AI Sponge Discord\nif there are any issues with the application in output or function", fg="gray").pack(pady=10)

root.mainloop()
