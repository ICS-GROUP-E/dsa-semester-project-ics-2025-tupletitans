import unittest

class TestTaskStack(unittest.TestCase):
    def test_push_pop(self):
        stack = TaskStack()
        stack.push("Task 1")
        stack.push("Task 2")
        self.assertEqual(stack.pop(), "Task 2")
        self.assertEqual(stack.pop(), "Task 1")