# ASS2YTT
import re
from tkinter import filedialog, Tk, messagebox
from xml.etree.ElementTree import Element, SubElement, ElementTree

def ass_time_to_milliseconds(ass_time):
    h, m, s = ass_time.split(":")
    s, cs = s.split(".")
    return (int(h) * 3600 + int(m) * 60 + int(s)) * 1000 + int(cs) * 10

def convert_ass_to_ytt(ass_path, ytt_path):
    with open(ass_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    dialogue_lines = [line for line in lines if line.strip().startswith("Dialogue:")]

    ytt = Element("timedtext")
    ytt.set("format", "3")
    body = SubElement(ytt, "body")

    for line in dialogue_lines:
        parts = line.strip().split(",", 9)
        if len(parts) < 10:
            continue
        start = parts[1]
        end = parts[2]
        text = parts[9]

        start_ms = ass_time_to_milliseconds(start)
        end_ms = ass_time_to_milliseconds(end)

        cleaned_text = re.sub(r"{.*?}", "", text).replace(r"\N", "\n").strip()

        p = SubElement(body, "p")
        p.set("t", str(start_ms))
        p.set("d", str(end_ms - start_ms))

        for segment in cleaned_text.split("\n"):
            if segment.strip():
                s = SubElement(p, "s")
                s.text = segment

    tree = ElementTree(ytt)
    tree.write(ytt_path, encoding="utf-8", xml_declaration=True)

def run_gui():
    root = Tk()
    root.withdraw()
    ass_path = filedialog.askopenfilename(title="Select .ass File", filetypes=[("ASS Subtitle", "*.ass")])
    if not ass_path:
        return

    ytt_path = filedialog.asksaveasfilename(title="Save as .ytt", defaultextension=".ytt", filetypes=[("YouTube Timed Text", "*.ytt")])
    if not ytt_path:
        return

    convert_ass_to_ytt(ass_path, ytt_path)
    messagebox.showinfo("Success", f"YTT file saved:\n{ytt_path}")

if __name__ == "__main__":
    run_gui()
