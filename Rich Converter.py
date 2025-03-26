import tkinter as tk
from tkinter import filedialog, messagebox
import os
import re

# GUI
def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("ASS Subtitle Files", "*.ass")])
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
    output_path = os.path.join(output_dir if output_dir else os.path.dirname(input_path), f"{name_only} converted{ext}")

    try:
        convert_ass_file(input_path, output_path)
        messagebox.showinfo("Success", f"✅ Converted file saved as:\n{output_path}")
    except Exception as e:
        messagebox.showerror("Error", f"❌ Conversion failed:\n{e}")

def launch_gui():
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

    root.mainloop()


def convert_font_name(match):
    font_name = match.group(1)
    if font_name.lower() == "impact":
        return '<font="Impact SDF">'
    return f'<font="{font_name}">'

def convert_color(match):
    bgr = match.group(1)
    rgb = bgr[4:6] + bgr[2:4] + bgr[0:2]
    return f"<color=#{rgb}>"

def convert_alpha(match):
    hex_alpha = match.group(1)
    flipped = 255 - int(hex_alpha, 16)
    return f"<alpha=#{flipped:02X}>"

def convert_font_size(match):
    return f"<size={match.group(1)}>"

TAG_REPLACEMENTS = {
    r"\\s1": "<s>", r"\\s0": "</s>",
    r"\\b1": "<b>", r"\\b0": "</b>",
    r"\\i1": "<i>", r"\\i0": "</i>",
    r"\\u1": "<u>", r"\\u0": "</u>",
    r"\\c": "</color>",
    r"\\fs0": "</size>",
    r"\\N": "<br>",
}

def process_ass_to_rich_text(text):
    def override_replacer(match):
        override = match.group(1)
        override = re.sub(r"\\fn([^\s\\]+)", convert_font_name, override, flags=re.IGNORECASE)
        override = re.sub(r"\\fs(\d+)", convert_font_size, override)
        override = re.sub(r"\\c&H([0-9A-Fa-f]{6})&", convert_color, override)
        override = re.sub(r"\\1a&H([0-9A-Fa-f]{2})&", convert_alpha, override)
        for pattern, replacement in TAG_REPLACEMENTS.items():
            override = re.sub(pattern, replacement, override)
        return override

    text = re.sub(r"{([^}]*)}", override_replacer, text)
    text = re.sub(r"\\fn([^\s\\]+)", convert_font_name, text, flags=re.IGNORECASE)
    for pattern, replacement in TAG_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
    return text

def convert_ass_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    processed_lines = [process_ass_to_rich_text(line) if line.startswith("Dialogue:") else line for line in lines]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(processed_lines)

if __name__ == "__main__":
    launch_gui()
