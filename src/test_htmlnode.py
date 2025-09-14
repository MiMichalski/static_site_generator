import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_1(self):
        node1 = HTMLNode("a")
        node2 = HTMLNode("a")
        self.assertEqual(node1, node2)

    def test_eq_2(self):
        node = HTMLNode(props={"url": "hoohle.com", "size": 5})
        self.assertEqual(node.props_to_html(), ' url="hoohle.com" size="5" ')
    
    # another note to self - naming two tests the same way tends to do wacky things
    def test_eq_3(self):
        node1 = HTMLNode(children={"aa": "test"})
        node2 = HTMLNode(children={"aa": "test"})
        self.assertEqual(node1, node2)

    def test_not_eq_1(self):
        node1 = HTMLNode(value="cos")
        node2 = HTMLNode("cos")
        self.assertNotEqual(node1, node2)

    # thought for later - name tests about what they do not just their id
    def test_to_html(self):
        node = HTMLNode('p', "test")
        with self.assertRaises(NotImplementedError) as context:
            node.to_html()


if __name__ == "__main__":
    unittest.main()