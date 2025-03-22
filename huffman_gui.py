import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from collections import Counter
import huffman_code

def encode_text(text, huffman_codes):
    try:
        return ''.join(huffman_codes[char] for char in text)
    
    # In case one of the characters trigger the encoding and creates an issue to encode the .txt file
    except KeyError:
        messagebox.showerror("Encoding Error", "There was an error encoding the text! Please ensure all characters are valid.")
        return ""

def save_compressed_file(encoded_text, filename):
    try:
        byte_array = bytearray()
        for i in range(0, len(encoded_text), 8):
            byte = encoded_text[i:i+8]
            byte_array.append(int(byte.ljust(8, '0'), 2))
        
        with open(filename, 'wb') as file:
            file.write(byte_array)

    # In case there was an issue saving the compressed file
    except Exception as e:
        messagebox.showerror("File Error", f"There was an error saving this compressed file! The error: {e}")

def decompress_file(compressed_file, huffman_codes):
    try:
        with open(compressed_file, 'rb') as file:
            binary_data = ''.join(f'{byte:08b}' for byte in file.read())
        
        reverse_codes = {v: k for k, v in huffman_codes.items()}
        decoded_text, temp_code = '', ''
        
        for bit in binary_data:
            temp_code += bit
            if temp_code in reverse_codes:
                decoded_text += reverse_codes[temp_code]
                temp_code = ''
        
        return decoded_text
    
    # In case the compressed file is not found
    except FileNotFoundError:
        messagebox.showerror("File Error", "Compressed file not found. Please compress a file first.")

        # In case there is an issue while decompressing the compressed file
    except Exception as e:
        messagebox.showerror("Decompression Error", f"There was an error decompressing the .txt file! The error: {e}")
    return ""

def huffman_compress(input_file, output_file):
    try:
        with open(input_file, 'r') as file:
            text = file.read()

        # To make sure the .txt file you choose actually has something in it    
        if not text:
            messagebox.showerror("File Error", "This .txt file is empty! Please make sure that there is something in the file!")
            return None, 0, 0, 0

        frequencies = Counter(text)
        huffman_tree = huffman_code.build_huffman_tree(frequencies)
        huffman_codes = huffman_code.generate_huffman_codes(huffman_tree)
        encoded_text = encode_text(text, huffman_codes)
        if not encoded_text:
            return None, 0, 0, 0
        
        save_compressed_file(encoded_text, output_file)
        
        original_size = os.path.getsize(input_file)
        compressed_size = os.path.getsize(output_file)
        compression_ratio = (1 - (compressed_size / original_size)) * 100
        
        return huffman_codes, original_size, compressed_size, compression_ratio
    
    # In case you try to select a "ghost" file
    # A file that should be there, but is not
    except FileNotFoundError:
        messagebox.showerror("File Error", "This .txt file was not found! Please make sure the file is there!")

        # In case an error occurs while compressing the .txt file
    except Exception as e:
        messagebox.showerror("Compression Error", f"Invalid file! Error during compression: {e}")
    return None, 0, 0, 0

def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filename:
        global selected_file
        selected_file = filename
        compress_file(filename)
    else:

        # When you don't select a .txt file and press Cancel on the File Explorer
        messagebox.showerror("File Selection Error", "You did not select a file! Please select a .txt file.")

def compress_file(input_file):
    output_file = "compressed.bin"
    global huffman_codes
    huffman_codes, original_size, compressed_size, compression_ratio = huffman_compress(input_file, output_file)
    
    if huffman_codes:
        codes_display.delete(1.0, tk.END)
        for char, code in huffman_codes.items():
            codes_display.insert(tk.END, f"'{char}': {code}\n")
        
        compression_label.config(
            text=f"Original: {original_size} bytes | Compressed: {compressed_size} bytes | Ratio: {compression_ratio:.2f}%",
            fg="#0066cc"
        )

        # Successfully compressed the .txt file
        messagebox.showinfo("Compression Complete", "Compressed file saved as 'compressed.bin'.")

def decompress_file_interface():
    global huffman_codes, selected_file

    # In case the compressed file you selected does not have data to be decompressed
    if not huffman_codes:
        messagebox.showerror("Decompression Error", "No compression data found. Compress a file first.")
        return
    
    # In case you attempt to decompress, but there is no .txt file selected
    if not selected_file:
        messagebox.showerror("File Error", "No .txt file was selected! Please select a .txt file before decompressing.")
        return
    decoded_text = decompress_file("compressed.bin", huffman_codes)
    decoded_text_display.delete(1.0, tk.END)
    decoded_text_display.insert(tk.END, decoded_text)

    # If the encoded text was successfully decoded
    messagebox.showinfo("Decompression Complete", "Decoding successful! Original text matches.")

# GUI
root = tk.Tk()
root.title("Huffman Coding Compression Tool")
root.configure(bg="#f5f5f5")
root.geometry("600x600")

main_frame = tk.Frame(root, bg="#f5f5f5", padx=20, pady=20)
main_frame.pack(expand=True)

# Huffman Coding Compression Tool title
tk.Label(main_frame, text="📦 Huffman Coding Compression Tool", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=5)

# Compression button
compress_button = tk.Button(main_frame, text="📂 Select Text File", command=select_file, width=20, height=2, relief="solid", bg="#cce5ff", fg="#333", font=("Arial", 12, "bold"))
compress_button.pack(padx=5, pady=5)

# Compression details
compression_label = tk.Label(main_frame, text="Compression details will appear here.", fg="#0066cc", bg="#f5f5f5", font=("Arial", 12, "bold"))
compression_label.pack(pady=5)

# Huffman Codes: 
tk.Label(main_frame, text="📜 Huffman Codes:", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=5)
codes_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, font=("Arial", 12))
codes_display.pack(pady=5)

# Decompression button
decompress_button = tk.Button(main_frame, text="🔄 Decompress File", command=decompress_file_interface, width=20, height=2, relief="solid", bg="#cce5ff", fg="#333", font=("Arial", 12, "bold"))
decompress_button.pack(padx=5, pady=5)

# Decoded Text: 
tk.Label(main_frame, text="📝 Decoded Text:", font=("Arial", 14, "bold"), bg="#f5f5f5", fg="#333").pack(pady=5)
decoded_text_display = scrolledtext.ScrolledText(main_frame, width=60, height=12, font=("Arial", 12))
decoded_text_display.pack(pady=5)

root.mainloop()
