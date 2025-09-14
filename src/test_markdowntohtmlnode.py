import unittest
from markdowntohtmlnode import markdown_to_html_node, extract_title

class MarkdownProcessing(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading_variations(self):
        md = """
# Heading 1

## Heading 2 with **bold**

###    Heading 3 with spaces

#### Heading 4

##### Heading 5

###### Heading 6
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2 with <b>bold</b></h2><h3>Heading 3 with spaces</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>"
        )

    def test_mixed_inline_content(self):
        md = """
This paragraph has **bold**, *italic*, `code`, and even a [link](https://example.com) all together!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This paragraph has <b>bold</b>, <i>italic</i>, <code>code</code>, and even a <a href=\"https://example.com\">link</a> all together!</p></div>"
        )

    def test_list_with_inline_markdown(self):
        md = """
* First item with **bold** text
* Second item with *italic* text
* Third item with `code` text

1. Ordered item with **bold**
2. Another ordered item with [link](https://boot.dev)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item with <b>bold</b> text</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code> text</li></ul><ol><li>Ordered item with <b>bold</b></li><li>Another ordered item with <a href=\"https://boot.dev\">link</a></li></ol></div>"
        )

    def test_multiline_quote(self):
        md = """
> This is a quote
> with **bold** text
> and multiple lines
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text and multiple lines</blockquote></div>"
        )

    def test_empty_and_complex_mix(self):
        md = """
# Main Title

This is a paragraph.

> A wise quote

```
def hello():
    print("world")
```

* List item
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Title</h1><p>This is a paragraph.</p><blockquote>A wise quote</blockquote><pre><code>def hello():\n    print(\"world\")\n</code></pre><ul><li>List item</li></ul></div>"
        )

    def test_heading_extraction(self):
        md = """
# Heading 1

## Heading 2 with **bold**

###    Heading 3 with spaces

#### Heading 4

##### Heading 5

###### Heading 6
"""
        title = extract_title(md)
        self.assertEqual(title, "Heading 1")

    def test_heading_extraction_lacking(self):
        md = """
## Heading 2 with **bold**

###    Heading 3 with spaces

#### Heading 4

##### Heading 5

###### Heading 6
"""
        with self.assertRaises(Exception) as context:
            title = extract_title(md)

    def test_heading_extraction_deeper(self):
        md = """
## Heading 2 with **bold**

###    Heading 3 with spaces

#### Heading 4

# Heading 1

##### Heading 5

###### Heading 6
"""
        title = extract_title(md)
        self.assertEqual(title, "Heading 1")        

if __name__ == "__main__":
    unittest.main()