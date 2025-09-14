import unittest

from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_plain_text(self):
        node = LeafNode("a", "test case")
        self.assertEqual(node.to_html(), "<a>test case</a>")

    def test_no_tag(self):
        node = LeafNode(None, "no tag")
        self.assertEqual(node.to_html(), "no tag")

    def test_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()

    def test_linklike(self):
        node = LeafNode("a", "Bite", {"href": "https://www.cos.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.cos.com">Bite</a>')

if __name__ == "__main__":
    unittest.main()