import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode('p', None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()

    def test_to_html_with_multiple_childred(self):
        children = [LeafNode("b", "bold text"), LeafNode("i", "italic text")]
        parent_node = ParentNode('p', children)
        self.assertEqual(parent_node.to_html(), "<p><b>bold text</b><i>italic text</i></p>")

if __name__ == "__main__":
    unittest.main()