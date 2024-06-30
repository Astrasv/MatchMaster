class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.prev = None

class Deque:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0
    
    def is_empty(self):
        return self.size == 0
    
    def add_front(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.next = self.front
            self.front.prev = new_node
            self.front = new_node
        self.size += 1
    
    def add_rear(self, value):
        new_node = Node(value)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            new_node.prev = self.rear
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
    
    def remove_front(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        value = self.front.value
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.front = self.front.next
            self.front.prev = None
        self.size -= 1
        return value
    
    def remove_rear(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        value = self.rear.value
        if self.front == self.rear:
            self.front = self.rear = None
        else:
            self.rear = self.rear.prev
            self.rear.next = None
        self.size -= 1
        return value
    
    def peek_front(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.front.value
    
    def peek_rear(self):
        if self.is_empty():
            raise Exception("Deque is empty")
        return self.rear.value
    
    def rotate_left(self):
        if self.size <= 1:
            return
        
        # Move the front element to the rear
        front_value = self.remove_front()
        self.add_rear(front_value)
    
    def range_queue(self,start,end):
        for node in range(start,end):
            self.add_rear(node)
            
# Define the Node and Deque classes (same as provided)

# Driver code
if __name__ == "__main__":
    # Create a deque instance
    deque = Deque()
    
    # Add elements from 1 to 5 to the front using range_queue
    deque.range_queue(1, 6)  # Adds 1, 2, 3, 4, 5 to the deque's front
    
    # Print the elements of the deque from front to rear
    print("Deque elements from front to rear:")
    current = deque.front
    while current:
        print(current.value, end=" ")
        current = current.next
    print()
    
    # Rotate the deque left
    print("Deque after rotating left:")
    deque.rotate_left()  # Moves 1 (front) to rear
    current = deque.front
    while current:
        print(current.value, end=" ")
        current = current.next
    print()
    
    # Add an element to the rear
    deque.add_rear(6)  # Adds 6 to the rear
    
    # Print the elements of the deque from front to rear
    print("Deque elements from front to rear after adding 6 to rear:")
    current = deque.front
    while current:
        print(current.value, end=" ")
        current = current.next
    print()
