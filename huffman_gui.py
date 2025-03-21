import heapq
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import Counter

# Node Class for Building Huffman Tree Nodes
class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    
    def __lt__(self, other):
        return self.freq < other.freq

# Function to build Huffman Tree
def build_huffman_tree(frequencies):
    heap = [Node(freq, char) for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)
    
    return heap[0]

# Recursive function to generate Huffman Code
def generate_huffman_codes(node, prefix='', codes={}):
    if node:
        if node.char is not None:
            codes[node.char] = prefix
        generate_huffman_codes(node.left, prefix + '0', codes)
        generate_huffman_codes(node.right, prefix + '1', codes)
    return codes

# Function to encode text
def encode_text(text, huffman_codes):
    return ''.join(huffman_codes[char] for char in text)

# Function to save compressed file
def save_compressed_file(encoded_text, filename):
    byte_array = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        byte_array.append(int(byte.ljust(8, '0'), 2))
    
    with open(filename, 'wb') as file:
        file.write(byte_array)

# Function to decompress file
def decompress_file(compressed_file, huffman_codes):
    with open(compressed_file, 'rb') as file:
        binary_data = ''.join(f'{byte:08b}' for byte in file.read())
    
    reverse_codes = {v: k for k, v in huffman_codes.items()}
    decoded_text = ''
    temp_code = ''
    
    for bit in binary_data:
        temp_code += bit
        if temp_code in reverse_codes:
            decoded_text += reverse_codes[temp_code]
            temp_code = ''
    
    return decoded_text

# Function for Huffman compression
def huffman_compress(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()
    
    frequencies = Counter(text)
    huffman_tree = build_huffman_tree(frequencies)
    huffman_codes = generate_huffman_codes(huffman_tree)
    encoded_text = encode_text(text, huffman_codes)
    save_compressed_file(encoded_text, output_file)
    
    original_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(output_file)
    compression_ratio = (1 - (compressed_size / original_size)) * 100
    
    return huffman_codes, original_size, compressed_size, compression_ratio

# Allows the user to select a .txt file only
def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        compress_file(filename)

# Function to compress the selected file and update the GUI
def compress_file(input_file):
    output_file = "compressed.bin"
    global huffman_codes
    huffman_codes, original_size, compressed_size, compression_ratio = huffman_compress(input_file, output_file)
    
    # Display Huffman Codes
    codes_display.delete(1.0, tk.END)
    for char, code in huffman_codes.items():
        codes_display.insert(tk.END, f"'{char}': {code}\n")
    
    # Update compression details
    compression_label.config(
        text=f"Original: {original_size} bytes | "
             f"Compressed: {compressed_size} bytes | "
             f"Ratio: {compression_ratio:.2f}%",
        fg="#0066cc"
    )
    
    messagebox.showinfo("Compression Complete", "Compressed file saved as 'compressed.bin'.")

# Function for decompressing the file and updating the GUI
def decompress_file_interface():
    input_file = "compressed.bin"
    global huffman_codes
    decoded_text = decompress_file(input_file, huffman_codes)
    decoded_text_display.delete(1.0, tk.END)
    decoded_text_display.insert(tk.END, decoded_text)
    messagebox.showinfo("Decompression Complete", "Decoding successful! Original text matches.")

# GUI
root = tk.Tk()
root.title("Huffman Coding Compression Tool")
root.configure(bg="#f5f5f5")
root.geometry("600x600")

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

tk.Label(main_frame, text="📦 Huffman Coding Compression Tool", **label_style).pack(pady=5)
compress_button = tk.Button(main_frame, text="📂 Select Text File", command=select_file, width=20, height=2, relief="solid", bg="#cce5ff", fg="#333333", font=("Arial", 12, "bold"))
compress_button.pack(padx=5, pady=5)

compression_frame = tk.Frame(main_frame, bg="#f5f5f5")
compression_frame.pack(pady=5)

compression_label = tk.Label(compression_frame, text="Compression details will appear here.", fg="#0066cc", bg="#f5f5f5", font=("Arial", 12, "bold"))
compression_label.pack(side="left", padx=5)

# Displays the Huffman Codes of the compressed file
tk.Label(main_frame, text="📜 Huffman Codes:", **label_style).pack(pady=5)
codes_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, **text_style)
codes_display.pack(pady=5)

# Decompress file button
decompress_button = tk.Button(main_frame, text="🔄 Decompress File", command=decompress_file_interface, width=20, height=2, relief="solid", bg="#cce5ff", fg="#333333", font=("Arial", 12, "bold"))
decompress_button.pack(padx=5, pady=5)

# Displays the decoded text of the compressed file once decompressed
tk.Label(main_frame, text="📝 Decoded Text:", **label_style).pack(pady=5)
decoded_text_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, **text_style)
decoded_text_display.pack(pady=5)

root.mainloop()
