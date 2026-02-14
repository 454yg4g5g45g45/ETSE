import os
from tkinter import Tk, filedialog

def fix_encoding(filepath):
    """
    Reads a file using a fallback system and saves it strictly as windows-1252.
    'errors=replace' handles characters that don't exist in the target encoding.
    """
    # Try reading as UTF-8 first (common source of errors), then CP-1252
    encodings_to_try = ['utf-8', 'cp1252', 'latin1']
    content = None

    for enc in encodings_to_try:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                content = f.read()
            break 
        except (UnicodeDecodeError, TypeError):
            continue

    # If all fail, read with 'replace' to force it through
    if content is None:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

    # Write back as strictly windows-1252 (ANSI)
    try:
        with open(filepath, 'w', encoding='cp1252', errors='replace') as f:
            f.write(content)
        print(f"Fixed: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Failed to write {filepath}: {e}")

def process_files(directory):
    target_exts = ('.txt', '.gfx', '.csv')
    count = 0
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(target_exts):
                # Ensure we skip .yml even if someone named it something weird
                if not file.lower().endswith('.yml'):
                    fix_encoding(os.path.join(root, file))
                    count += 1
    print(f"\nProcessing complete. {count} files updated to Windows-1252.")

def main():
    root = Tk()
    root.withdraw()
    print("Select the folder containing your EU4 mod files...")
    folder_selected = filedialog.askdirectory()
    
    if folder_selected:
        process_files(folder_selected)
    else:
        print("No folder selected. Exiting.")

if __name__ == "__main__":
    main()