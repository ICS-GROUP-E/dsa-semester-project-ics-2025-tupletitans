import unittest
from src.TaskStack import TaskStack

class TestTaskStack(unittest.TestCase):
    def test_push_pop(self):
        stack = TaskStack()
        stack.push("Task 1")
        stack.push("Task 2")
        self.assertEqual(stack.pop(), "Task 2")
        self.assertEqual(stack.pop(), "Task 1")
        self.assertTrue(stack.is_empty())

    def test_peek(self):
        stack = TaskStack()
        stack.push("Task A")
        self.assertEqual(stack.peek(), "Task A")
        self.assertFalse(stack.is_empty())

    def test_empty_stack_behavior(self):
        stack = TaskStack()
        self.assertIsNone(stack.pop())
        self.assertIsNone(stack.peek())

if __name__ == "__main__":
    unittest.main()
