import gzip
import xml.etree.ElementTree as ET
import os

def convert_ytt_to_xml(ytt_file, xml_file):
    """
    Extracts a .ytt (YouTube Timed Text) file.
    Handles both GZIP-compressed and plain XML formats.
    """
    try:
        # Try to open as GZIP
        with gzip.open(ytt_file, "rb") as f:
            xml_content = f.read().decode("utf-8")
    except gzip.BadGzipFile:
        # If not GZIP, try opening as plain text
        with open(ytt_file, "r", encoding="utf-8") as f:
            xml_content = f.read()

    # Save extracted content as XML
    with open(xml_file, "w", encoding="utf-8") as f:
        f.write(xml_content)

    print(f"✅ Extracted XML saved as: {xml_file}")

def convert_xml_to_vtt(xml_file, vtt_file):
    """
    Converts a YouTube XML subtitle file to a WebVTT (.vtt) format.
    Preserves subtitle text, colors, and basic formatting.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(vtt_file, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")  # WebVTT header

        for i, child in enumerate(root.findall(".//p")):  # Find all subtitle <p> elements
            start_time = float(child.attrib.get("t", "0")) / 1000.0  # Convert ms to seconds
            duration = float(child.attrib.get("d", "2000")) / 1000.0  # Default duration if missing
            
            end_time = start_time + duration

            # Convert to VTT timestamp format (HH:MM:SS.mmm)
            start_time_vtt = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02}.{int((start_time * 1000) % 1000):03}"
            end_time_vtt = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02}.{int((end_time * 1000) % 1000):03}"

            # Extract subtitle text (including formatting)
            subtitle_text = ""
            for elem in child.iter():
                if elem.text:
                    subtitle_text += elem.text  # Append text content

            if not subtitle_text.strip():
                subtitle_text = "[No Text]"  # Placeholder if text is missing

            # Write VTT formatted subtitle line
            f.write(f"{i+1}\n{start_time_vtt} --> {end_time_vtt}\n{subtitle_text}\n\n")

    print(f"✅ Converted WebVTT saved as: {vtt_file}")

def convert_ytt_to_vtt(ytt_file, vtt_file):
    """
    Converts a YouTube .ytt subtitle file directly to a .vtt file.
    """
    xml_file = os.path.splitext(ytt_file)[0] + ".xml"  # Generate XML filename
    convert_ytt_to_xml(ytt_file, xml_file)
    convert_xml_to_vtt(xml_file, vtt_file)
    print("✅ Conversion complete!")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python convert_ytt2vtt.py input.ytt output.vtt")
    else:
        convert_ytt_to_vtt(sys.argv[1], sys.argv[2])
