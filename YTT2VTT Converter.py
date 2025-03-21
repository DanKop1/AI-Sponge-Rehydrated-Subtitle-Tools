import tkinter as tk
from tkinter import filedialog, messagebox
import os
import convert_ytt2vtt

def browse_file():
    """Open a file dialog to select a .ytt file"""
    file_path = filedialog.askopenfilename(filetypes=[("YouTube Timed Text", "*.ytt")])
    if file_path:
        entry_input_file.delete(0, tk.END)
        entry_input_file.insert(0, file_path)
        # Suggest an output file name based on input file
        suggested_output = os.path.splitext(os.path.basename(file_path))[0] + ".vtt"
        entry_output_file.delete(0, tk.END)
        entry_output_file.insert(0, suggested_output)

def browse_output_directory():
    """Open a directory selection dialog for the output file"""
    directory = filedialog.askdirectory()
    if directory:
        entry_output_directory.delete(0, tk.END)
        entry_output_directory.insert(0, directory)

def convert_file():
    """Convert the selected .ytt file to .vtt"""
    input_file = entry_input_file.get()
    output_file_name = entry_output_file.get()
    output_directory = entry_output_directory.get()
    keep_xml = var_keep_xml.get()

    if not input_file or not output_file_name or not output_directory:
        messagebox.showerror("Error", "Please select an input file, output file name, and output directory.")
        return

    output_file = os.path.join(output_directory, output_file_name)
    xml_file = os.path.splitext(output_file)[0] + ".xml"

    try:
        # Run the conversion using the existing script
        convert_ytt2vtt.convert_ytt_to_vtt(input_file, output_file)

        # Ensure XML file is deleted if not needed
        if not keep_xml:
            if os.path.exists(xml_file):
                try:
                    os.remove(xml_file)
                except Exception as e:
                    messagebox.showwarning("Warning", f"Could not delete XML file:\n{xml_file}\n{str(e)}")

        messagebox.showinfo("Success", f"Conversion completed! File saved as:\n{output_file}")

    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{str(e)}")

# Create GUI window
root = tk.Tk()
root.title("Dankop's YTT to VTT Converter")

# Input file selection
tk.Label(root, text="Select .ytt file:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_input_file = tk.Entry(root, width=50)
entry_input_file.grid(row=0, column=1, padx=5, pady=5)
btn_browse_input = tk.Button(root, text="Browse", command=browse_file)
btn_browse_input.grid(row=0, column=2, padx=5, pady=5)

# Output directory selection
tk.Label(root, text="Output Directory:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_output_directory = tk.Entry(root, width=50)
entry_output_directory.grid(row=1, column=1, padx=5, pady=5)
btn_browse_output = tk.Button(root, text="Browse", command=browse_output_directory)
btn_browse_output.grid(row=1, column=2, padx=5, pady=5)

# Output file name
tk.Label(root, text="Output .vtt File Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_output_file = tk.Entry(root, width=50)
entry_output_file.grid(row=2, column=1, padx=5, pady=5)

# Checkbox to keep XML file
var_keep_xml = tk.BooleanVar(value=False)
chk_keep_xml = tk.Checkbutton(root, text="Keep XML File", variable=var_keep_xml)
chk_keep_xml.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# Convert button
btn_convert = tk.Button(root, text="Convert", command=convert_file, bg="green", fg="white")
btn_convert.grid(row=4, column=1, padx=5, pady=10)

# Contact message
contact_label = tk.Label(root, text="Please contact Dankop on the AI Sponge Discord if there are any issues with the application in output or function", fg="gray")
contact_label.grid(row=5, column=0, columnspan=3, padx=5, pady=10)

# Run the GUI loop
root.mainloop()
