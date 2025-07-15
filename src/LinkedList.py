class Node:
    def _init_(self, data):
        self.data = data
        self.next = None

class TaskLinkedList:
    def _init_(self):
        self.head = None

    def insert(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, key):
        temp = self.head
        prev = None
        while temp and temp.data != key:
            prev = temp
            temp = temp.next
        if temp:
            if prev:
                prev.next = temp.next
            else:
                self.head = temp.next

    def search(self, key):
        temp = self.head
        while temp:
            if temp.data == key:
                return True
            temp = temp.next
        return False

    def display(self):
        tasks = []
        temp = self.head
        while temp:
            tasks.append(temp.data)
            temp = temp.next
        return tasks
