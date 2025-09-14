import unittest

from texttohtml import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_image(self):
        node = TextNode("alternative", TextType.IMAGE, "https://www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.test.com", "alt": "alternative"})

    def test_link(self):
        node = TextNode("anchor", TextType.LINK, "https://www.test.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor")
        self.assertEqual(html_node.props, {"href": "https://www.test.com"})

    def test_split_text_type(self):
        node = TextNode("A sentence without any delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result[0].text, "A sentence without any delimiters")

    def test_split_valid_pair(self):
        node = TextNode("a **b** c", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(f'{result[0].text_type.value}-{result[0].text} {result[1].text_type.value}-{result[1].text} {result[2].text_type.value}-{result[2].text}', "text-a  bold-b text- c")
    
    def test_split_valid_pair_start(self):
        node = TextNode("**a** b", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(f'{result[0].text_type.value}-{result[0].text} {result[1].text_type.value}-{result[1].text}', "bold-a text- b")

    def test_split_adjecent(self):
        node = TextNode("**a****b** c", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(f'{result[0].text_type.value}-{result[0].text} {result[1].text_type.value}-{result[1].text} {result[2].text_type.value}-{result[2].text}', "bold-a bold-b text- c")

    def test_split_lone_delimiter(self):
        node = TextNode("****", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            result = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_unmatched_delimiter(self):
        node = TextNode("**a b", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            result = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_list_multiple(self):
        nodes = [TextNode("Very bold node", TextType.BOLD), TextNode("Normal text node with **bold**", TextType.TEXT)]
        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(f'{result[0].text_type.value}-{result[0].text} {result[1].text_type.value}-{result[1].text} {result[2].text_type.value}-{result[2].text}', "bold-Very bold node text-Normal text node with  bold-bold")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is a text with a link [link](https://will.fill.later/asfd.ssa)")
        self.assertListEqual([("link", "https://will.fill.later/asfd.ssa")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links("This is a text with a link [link](https://will.fill.later/asfd.ssa) and [link2](https://will.fill.maybe/asfd.ssa)")
        #print(matches)
        self.assertListEqual([("link", "https://will.fill.later/asfd.ssa"), ("link2", "https://will.fill.maybe/asfd.ssa")], matches)

    def test_extract_markdown_image_empty(self):
        matches = extract_markdown_images("This is a text with nothing and I made no catch exceptions.")
        self.assertListEqual([], matches)

    def test_extract_markdown_image_from_link(self):
        matches = extract_markdown_images("This is a text with a link [link](https://will.fill.later/asfd.ssa) and [link2](https://will.fill.maybe/asfd.ssa)")
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_test_for_injection(self):
        node = TextNode("This contains a normal link ![image](https://s.sdfsg.css/hasdas.ppn) __img__", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_image([node])
    
    def test_split_images_test_incorrect_link(self):
        node = TextNode("This contains a normal link ![image](https://s.sdfsg.css/hasdas.ppn", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_link_test_image(self):
        node = TextNode("This contains a normal link ![image](https://s.sdfsg.css/hasdas.ppn)", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_valid(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
    def test_text_to_textnodes_smushed_input(self):
        input = "This is **text**_with italic_ words and `a bit of a code`**I am not adding links, that too much asserting**"
        nodes = text_to_textnodes(input)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode("with italic", TextType.ITALIC),
            TextNode(" words and ", TextType.TEXT),
            TextNode("a bit of a code", TextType.CODE),
            TextNode("I am not adding links, that too much asserting", TextType.BOLD)
            ]
        )
    

if __name__ == "__main__":
    unittest.main()