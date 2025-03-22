import heapq
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