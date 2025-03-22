import heapq
from collections import Counter
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

# -------------------------------
# Huffman Tree Node Definition
# -------------------------------
class Node:
    """Node class for Huffman Tree"""
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

# -------------------------------
# Huffman Encoding Functions
# -------------------------------
def build_huffman_tree(frequencies):
    """Builds Huffman Tree based on character frequencies"""
    heap = [Node(freq, char) for char, freq in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(node, prefix='', codes={}):
    """Generates Huffman codes by traversing the tree"""
    if node:
        if node.char is not None:
            codes[node.char] = prefix
        generate_huffman_codes(node.left, prefix + '0', codes)
        generate_huffman_codes(node.right, prefix + '1', codes)
    return codes

#-------------------------------------------------------------------------------

def encode_text(text, huffman_codes):
    """Encodes text using Huffman codes"""
    try:
        return ''.join(huffman_codes[char] for char in text)
    
    # In case one of the characters trigger the encoding and creates an issue to encode the .txt file
    except KeyError:
        messagebox.showerror("Encoding Error", "There was an error encoding the text! Please ensure all characters are valid.")
        return ""


def save_compressed_file(encoded_text, filename):
    """Saves encoded binary text to a file"""
    try:
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            byte_array.append(int(byte.ljust(8, '0'), 2))

        with open(filename, 'wb') as file:
            file.write(byte_array)
    
    # In case there was an issue saving the compressed file
    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("File Error", f"There was an error saving this compressed file! The error: {e}")


def decompress_file(compressed_file, huffman_codes, progress_callback=None):
    """Reads a compressed file and decodes it using Huffman codes"""

    try:
        with open(compressed_file, 'rb') as file:
            binary_data = file.read()

        if progress_callback:
            progress_callback(30)

        binary_str = ''.join(f'{byte:08b}' for byte in binary_data)

        if progress_callback:
            progress_callback(60)

        reverse_codes = {v: k for k, v in huffman_codes.items()}
        decoded_text = ''
        temp_code = ''
        for bit in binary_str:
            temp_code += bit
            if temp_code in reverse_codes:
                decoded_text += reverse_codes[temp_code]
                temp_code = ''

        if progress_callback:
            progress_callback(100)

        return decoded_text
    
    # In case the compressed file is not found
    except FileNotFoundError:
        messagebox.showerror("File Error", "Compressed file not found. Please compress a file first.")

    # In case there is an issue while decompressing the compressed file
    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Decompression Error", f"There was an error decompressing the .txt file! The error: {e}")
    return ""

def huffman_compress(input_file, output_file, progress_callback=None):
    """Main function to handle Huffman compression and return stats"""
    with open(input_file, 'r') as file:
        text = file.read()

    # Checks to see if the .txt file is empty
    if not text:
        messagebox.showerror("Error", "This .txt file is empty. Please choose a valid .txt file.")
        return None, None, None, None

    if progress_callback:
        progress_callback(10)

    frequencies = Counter(text)
    if progress_callback:
        progress_callback(30)

    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)
    if progress_callback:
        progress_callback(50)

    encoded_text = encode_text(text, huffman_codes)
    if progress_callback:
        progress_callback(70)

    save_compressed_file(encoded_text, output_file)
    if progress_callback:
        progress_callback(100)

    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    compression_ratio = (1 - (compressed_size / original_size)) * 100

    return huffman_codes, original_size, compressed_size, compression_ratio

# -------------------------------
# GUI Interaction Functions
# -------------------------------
def select_file():
    """Prompts user to select a .txt file for compression"""
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        compress_file(filename)

    # When you don't select a .txt file and press Cancel on the File Explorer
    if not filename:
        messagebox.showerror("Error", "A .txt was not file selected. Please select a valid .txt file.")
        return

def compress_file(input_file):
    """Compresses the selected file and displays progress and results"""
    output_file = "compressed.bin"

    # Create progress window
    progress_win, progress_bar = show_progress_window("Compressing File...")

    def update_progress(percent):
        progress_bar['value'] = percent
        progress_bar.update_idletasks()
    try:
        global huffman_codes
        huffman_codes, original_size, compressed_size, compression_ratio = huffman_compress(
            input_file, output_file, progress_callback=update_progress
        )

        progress_win.destroy()

        # Display Huffman Codes
        codes_display.delete(1.0, tk.END)
        for char, code in huffman_codes.items():
            codes_display.insert(tk.END, f"'{char}': {code}\n")

        compression_label.config(
            text=f"Original: {original_size} bytes | "
                f"Compressed: {compressed_size} bytes | "
                f"Ratio: {compression_ratio:.2f}%",
            fg="#0066cc"
        )

        # Successfully compressed the .txt file
        messagebox.showinfo("Compression Complete", "Compressed file saved as 'compressed.bin'.")

    # In case an issue occurs during compression
    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Compression Error", f"An error occurred during compression: {str(e)}")


def decompress_file_interface():
    """Handles the decompression process and updates the GUI"""
    input_file = "compressed.bin"

    progress_win, progress_bar = show_progress_window("Decompressing File...")

    def update_progress(percent):
        progress_bar['value'] = percent
        progress_bar.update_idletasks()

    try:
        global huffman_codes
        decoded_text = decompress_file(input_file, huffman_codes, progress_callback=update_progress)

        progress_win.destroy()

        decoded_text_display.delete(1.0, tk.END)
        decoded_text_display.insert(tk.END, decoded_text)

        # If the encoded text was successfully decoded
        messagebox.showinfo("Decompression Complete", "Decoding successful! Original text matches.")

    # In case an issue occurs during decompression
    except Exception as e:
        progress_win.destroy()
        messagebox.showerror("Decompression Error", f"An error occurred during decompression: {str(e)}")

def show_progress_window(title):
    """Creates a separate progress bar window"""
    progress_win = tk.Toplevel(root)
    progress_win.title(title)
    progress_win.geometry("400x100")
    progress_win.resizable(False, False)
    progress_win.grab_set()  # Modal

    label = tk.Label(progress_win, text=title, font=("Arial", 12))
    label.pack(pady=10)

    progress = ttk.Progressbar(progress_win, orient="horizontal", mode="determinate", length=300)
    progress.pack(pady=5)

    return progress_win, progress

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Huffman Coding Compression Tool")
root.configure(bg="#f5f5f5")
root.geometry("600x800")

main_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
main_frame.pack(expand=True)

label_style = {
    "bg": "#f5f5f5",
    "fg": "#333333",
    "font": ("Arial", 14, "bold")
}

text_style = {
    "bg": "white",
    "fg": "#333333",
    "font": ("Arial", 12)
}

# Title and File Selection
tk.Label(main_frame, text="📦 Huffman Coding Compression Tool", **label_style).pack(pady=5)
compress_button = tk.Button(
    main_frame, text="📂 Select Text File", command=select_file,
    width=20, height=2, relief="solid", bg="#cce5ff", fg="#333333", font=("Arial", 12, "bold")
)
compress_button.pack(padx=5, pady=5)

# Compression Stats
compression_frame = tk.Frame(main_frame, bg="#f5f5f5")
compression_frame.pack(pady=5)
compression_label = tk.Label(
    compression_frame, text="Compression details will appear here.",
    fg="#0066cc", bg="#f5f5f5", font=("Arial", 12, "bold")
)
compression_label.pack(side="left", padx=5)

# Huffman Code Display
tk.Label(main_frame, text="📜 Huffman Codes:", **label_style).pack(pady=5)
codes_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, **text_style)
codes_display.pack(pady=5)

# Decompress Button
decompress_button = tk.Button(
    main_frame, text="🔄 Decompress File", command=decompress_file_interface,
    width=20, height=2, relief="solid", bg="#cce5ff", fg="#333333", font=("Arial", 12, "bold")
)
decompress_button.pack(padx=5, pady=5)

# Decoded Text Display
tk.Label(main_frame, text="📝 Decoded Text:", **label_style).pack(pady=5)
decoded_text_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, **text_style)
decoded_text_display.pack(pady=5)

# Run GUI
root.mainloop()
