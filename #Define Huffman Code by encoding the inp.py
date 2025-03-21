#Define Huffman Code by encoding the input by the user

import heapq
from collections import Counter

#Node Class for Building Huffman Tree Nodes
class Node:
    def _init_(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def _lt_(self, other):
        return self.freq < other.freq
    
#Function to build Huffman Tree
def build_huffman_tree(text):
    from collections import Counter
    import heapq

    frequency = Counter(text)

    heap = [Node(freq, char) for char, freq in frequency.items()]

    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        merged = Node(left.freq + right.freq, left=left, right=right)

        heapq.heappush(heap, merged)

    return heap[0]

#Recursive function to generate Huffman Code
def create_codes(node, current_code="", codes={}):
    if node.char:
        codes[node.char] = current_code
        return

    create_codes(node.left, current_code + "0", codes)
    create_codes(node.right, current_code + "1", codes)

    return codes

def encode(text, codes):
    return ''.join(codes[char] for char in text)

def decode(encoded_text, codes):
    reverse_codes = {code:char for char, code in codes.item()}
    current_code = ""
    decoded_text = ""

    for bit in encoded_text:
        current_code += bit
        if current_code in reverse_codes:
            decoded_text += reverse_codes[current_code]
            current_code = ""
        return decoded_text
#User Interactive Program
import heapq
from collections import Counter

text = input("Enter the text you want to compress using Huffman Coding: ").upper()

frequency = Counter(text)

heap = [[freq, [char, ""]] for char, freq in frequency.items()]
heapq.heapify(heap)

while len(heap) > 1:
    lo = heapq.heappop(heap)
    hi = heapq.heappop(heap)

    for pair in lo[1:]:
        pair[1] = '0' + pair[1]

    for pair in hi[1:]:
        pair[1] = '1' + pair[1]

    heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
huffman_codes_list = sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))
huffman_dict = {char: code for char, code in huffman_codes_list}

print("\n Huffman Codes Generated: ")
for char, code in huffman_dict.items():
    print(f"{char}: {code}")

#Encode the input text
encoded_str = ''.join(huffman_dict[char] for char in text)
print(f"\nEncoded '{text}':{encoded_str}")

#Decoding the Huffman Coded Generated
decoded_text = ""
current_bits = ""
reverse_codes = {v: k for k, v in huffman_dict.items()}

#Travese through each bit
for bit in encoded_str:
    current_bits += bit
    if current_bits in reverse_codes:
        decoded_text += reverse_codes[current_bits]
        current_bits = ""
print(f"\nDecoded text: {decoded_text}")

if text == decoded_text:
    print("\nDecoding successful! Original text matches the decodede text.")
else:
    print("\nDecoding failed! Original does not match the decoded text.")