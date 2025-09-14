import htmlnode

class LeafNode(htmlnode.HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return f'{self.value}'
        attributes = self.props_to_html()
        return f'<{self.tag}{attributes.rstrip()}>{self.value}</{self.tag}>'