import unittest
from documenttonodes import markdown_to_blocks, block_to_block_type
from documenttonodes import BlockType

class MarkdownProcessing(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_multiline_blank(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_block_to_block(self):
        block = "This is a random text inside the block."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_code(self):
        block = """```I'll just copy something here.\nPARAGRAPH = "p"\nHEADING = "h"\nCODE = "code"\nQUOTE = "quote"\nUNORDERED_LIST = "ul"\nORDERED_LIST = "ol"```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_code_defective(self):
        block = """```I'll just copy something here.\nPARAGRAPH = "p"\nHEADING = "h"\nCODE = "code"\nQUOTE = "quote"\nUNORDERED_LIST = "ul"\nORDERED_LIST = "ol"``"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_heading(self):
        block = "### This is a title of 3rd tier"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_quote(self):
        block = ">This will work the first time\n>Trust me"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_unordered_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_unordered_list_defective(self):
        block = "- This is a list\n- with items\n-third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
    
    def test_block_to_block_ordered_list_defective(self):
        block = "1. First item\n2. Second item\n3.Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    # It worked the first time, so... it likely contains a hidden bug/feature that will help us later

if __name__ == "__main__":
    unittest.main()