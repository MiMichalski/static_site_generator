import htmlnode

class ParentNode(htmlnode.HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be empty")
        if self.children is None:
            raise ValueError("Node must have at least one child node")
        output_string = ""
        for child in self.children:
            output_string += child.to_html()
        attributes = self.props_to_html()
        return f'<{self.tag}{attributes.rstrip()}>{output_string}</{self.tag}>'