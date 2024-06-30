# Defining a stack data structure to be used in the implementation.

class Stack:
    # Defining a Node class for the elements of the stack.
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            
    # Initializing the stack with a head pointer.
    def __init__(self):
        self.head = None

    # Checking if the stack is empty.
    def is_empty(self):
        return self.head is None

    # Method to push an element onto the stack.
    def push(self, data):
        new_node = self.Node(data)
        new_node.next = self.head
        self.head = new_node

    # Method to pop an element from the stack.
    def pop(self):
        if self.is_empty():
            return None
        popped = self.head
        self.head = self.head.next
        return popped.data

    # Method to peek the top element of the stack without removing it.
    def peek(self):
        if self.is_empty():
            return None
        return self.head.data

    # Method to display the elements of the stack.
    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> ")
            current = current.next
        print("None")
