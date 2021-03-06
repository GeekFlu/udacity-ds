"""
Luis E Gonzalez

Links reviewed:
https://www.youtube.com/watch?v=t0Cq6tVNRBA
https://www.youtube.com/watch?v=HqPJF2L5h9U
http://homepages.math.uic.edu/~jan/mcs360/heaps_and_trees.pdf
"""
import sys


class HuffmanNode(object):
    """
    Huffman Node, this is not a generic Node so It wont work for a generic case
    """

    def __init__(self, letter='', frequency=0):
        self.left: HuffmanNode = None
        self.right: HuffmanNode = None
        self.letter: str = letter
        self.frequency: int = frequency
        self.code = None

    def __repr__(self):
        return f"HuffmanNode(letter={self.letter}, frequency={self.frequency})"

    def __str__(self):
        return f"HuffmanNode(letter={self.letter}, frequency={self.frequency})"


class MinHeap(object):
    """
    MIN Heap class
    """

    def __init__(self, initial_capacity=10):
        if initial_capacity is None or initial_capacity <= 0:
            raise ValueError("Priority Queue should have a valid capacity")
        self.heap = [None for i in range(initial_capacity)]
        self.elements = 0
        self.__capacity = initial_capacity

    def size(self):
        if self.heap is None:
            return 0
        return self.elements

    def peek(self):
        """It returns the root element of Min Heap. Time Complexity of this operation is O(1)"""
        if self.heap is None or len(self.heap) <= 0:
            return None
        return self.heap[0]

    def poll(self):
        """Always removes the minimum element from Min Heap.
           Time Complexity of this Operation is O(logn) as this operation needs
           to maintain the heap property after removing root."""
        # we remove element 0 from heap, since we are having in place all the elements en memory, we are going to swap root with last and keep track of the last element
        # to keep min heap we have to take the last element and move it from last to position 0
        # then we start comparing if least child is less than the root
        if self.heap is None or len(self.heap) <= 0:
            return None
        root_node = self.heap[0]
        is_there_elements = self.elements > 0
        if is_there_elements:
            keep_going_down = True
            self._swap(0, self.elements - 1)
            self.heap[self.elements - 1] = None
            # we heapify to min heap
            current_idx = 0
            self.elements -= 1
            while keep_going_down:
                left_child_idx = (2 * current_idx) + 1
                if left_child_idx <= self.elements - 1:
                    left_child = self.heap[left_child_idx]
                else:
                    left_child = None

                right_child_idx = (2 * current_idx) + 2
                if right_child_idx <= self.elements - 1:
                    right_child = self.heap[right_child_idx]
                else:
                    right_child = None

                # going left down if both are equal
                if self.elements == 2:
                    if self.heap[current_idx].frequency > left_child.frequency:
                        self._swap(left_child_idx, current_idx)
                        current_idx = left_child_idx
                    keep_going_down = False
                elif left_child is not None and right_child is not None and left_child.frequency <= right_child.frequency:
                    if self.heap[current_idx].frequency > left_child.frequency:
                        self._swap(left_child_idx, current_idx)
                        current_idx = left_child_idx
                    else:
                        keep_going_down = False
                elif left_child is not None and right_child is not None and right_child.frequency < left_child.frequency:
                    if self.heap[current_idx].frequency > right_child.frequency:
                        self._swap(right_child_idx, current_idx)
                        current_idx = right_child_idx
                    else:
                        keep_going_down = False
                else:
                    keep_going_down = False
        return root_node

    def insert(self, huffman_node: HuffmanNode):
        """
            Inserting a new node takes O(logn) time. We add a new node at the end of the tree.
            IF new node is greater than its parent, then we don’t need to do anything.
            Otherwise, we need to traverse up to fix the violated heap property by swapping.
            using:
            we are going to use an array so:
            to get left child = 2 * index
            to get right child = 2 * index + 1
            to get parent = index / 2 we take the integer part in case of decimal
           """
        self._ensure_capacity()
        if self.size() <= 0:
            self.heap[0] = huffman_node
        else:
            self.heap[self.elements] = huffman_node
            index_inserted = self.elements
            keep_climbing_up = True
            while keep_climbing_up:
                parent_idx = (index_inserted - 1) // 2
                if parent_idx >= 0 and self.heap[index_inserted].frequency < self.heap[parent_idx].frequency:
                    self._swap(index_inserted, parent_idx)
                    index_inserted = parent_idx
                else:
                    keep_climbing_up = False
        self.elements += 1

    def _ensure_capacity(self):
        if self.size() == self.__capacity:
            for _ in range(10):
                self.heap.append(None)
            self.__capacity = len(self.heap)

    def _swap(self, from_idx, with_idx):
        temp = self.heap[from_idx]
        self.heap[from_idx] = self.heap[with_idx]
        self.heap[with_idx] = temp


def huffman_encoding(data):
    """
    We will create the tree and encoded data
    :param data:
    :return:
    """
    if data is None or data.isspace() or len(data) <= 0:
        return None, None

    codes = get_frequency(data)
    priority_queue = create_priority_queue(codes)
    huffman_tree = None
    # Pop-out two nodes with the minimum frequency from the priority queue created in the above step.
    while priority_queue.size() > 0:

        element_1: HuffmanNode = priority_queue.poll()
        element_2: HuffmanNode = priority_queue.poll()

        # print(f"element = {element_1}")
        # print(f"element = {element_2}")

        new_frequency = 0

        if element_1 is not None:
            new_frequency += element_1.frequency
        if element_2 is not None:
            new_frequency += element_2.frequency

        huffman_tree = HuffmanNode("INTERNAL_NODE", new_frequency)

        if element_1 is not None and element_2 is None:
            huffman_tree.left = element_1
        elif element_1 is None and element_2 is not None:
            huffman_tree.left = element_2
        elif element_1.frequency < element_2.frequency:
            huffman_tree.left = element_1
            huffman_tree.right = element_2
        else:
            huffman_tree.left = element_2
            huffman_tree.right = element_1
        # we will stop when zero elements @ priority queue
        if priority_queue.size() > 0:
            priority_queue.insert(huffman_tree)

    # lets encode the string
    enc_holder = ""
    encoded_table = dict()
    encode_huffman_tree(huffman_tree, enc_holder, encoded_table)
    encoded_str = ""
    for letter in data:
        encoded_str += encoded_table.get(letter, "")

    return encoded_str, huffman_tree


def encode_huffman_tree(huffman_node: HuffmanNode, binary_code_holder, dictionary_words: dict):
    """
    Based on A huffman tree we will encode the data
    :param huffman_node: The root of the tree
    :param binary_code_holder:  This holder will be constructing the binary word until a leaf is reached
    :param dictionary_words: Dictionary to hold the final words in binary
    :return:
    """
    if huffman_node is not None:
        huffman_node.code = binary_code_holder
        # print(f"Huffman Node Code: {huffman_node.code} {huffman_node.frequency} {huffman_node.letter}")
        dictionary_words[huffman_node.letter] = dictionary_words.get(huffman_node.letter, "") + huffman_node.code
        encode_huffman_tree(huffman_node.left, binary_code_holder + "0", dictionary_words)
        encode_huffman_tree(huffman_node.right, binary_code_holder + "1", dictionary_words)


def huffman_decoding(encoded_word, root_huffman_node):
    """
        Steps to decode an encoded huffman word based on the huffman tree
        1. Declare a blank decoded string
        2. Pick a bit from the encoded data, traversing from left to right.
        3. Start traversing the Huffman tree from the root.
            If the current bit of encoded data is 0, move to the left child, else move to the right child of the tree if the current bit is 1.
            If a leaf node is encountered, append the (alphabetical) character of the leaf node to the decoded string.
    :param encoded_word: binary word
    :param root_huffman_node: root of the huffman tree
    :return: decoded word
    """
    decoded_str = ""
    current: HuffmanNode = root_huffman_node
    for bit_char in encoded_word:
        if bit_char == "0" and current.left is not None:
            current = current.left
        elif current.right is not None:
            current = current.right

        if current.left is None and current.right is None:
            decoded_str += current.letter
            current = root_huffman_node

    # print(f"decoded data = {decoded_str}")
    return decoded_str


def get_frequency(sentence):
    dictionary = dict()
    if sentence is None or len(sentence) == 0:
        return None
    for character in sentence:
        if dictionary.get(character) is None:
            dictionary[character] = 1
        else:
            dictionary[character] = dictionary.get(character) + 1
    return dictionary


def create_priority_queue(frequency_table: dict):
    """We will create a priority queue using a min heap"""
    if frequency_table is None or len(frequency_table.keys()) <= 0:
        return None
    pr_queue = MinHeap(len(frequency_table.keys()))
    for letter, frequency in frequency_table.items():
        new_node = HuffmanNode(letter, frequency)
        pr_queue.insert(new_node)
    return pr_queue


if __name__ == "__main__":
    # Step 1 determine frequency og each letter
    a_great_sentence = "AAAAAAABBBCCCCCCCDDEEEEEE"
    encoded_data, tree = huffman_encoding(a_great_sentence)

    print(f"The size of the data is: {sys.getsizeof(a_great_sentence)}")
    print(f"The content of the data is: {a_great_sentence}")
    print(f"The size of the encoded data is: {sys.getsizeof(int(encoded_data, base=2))}")
    print(f"The content of the encoded data is: {encoded_data}")

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}".format(sys.getsizeof(decoded_data)))
    print("The content of the encoded data is: {}".format(decoded_data))
