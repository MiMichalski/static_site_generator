class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag              # string HTML tag name
        self.value = value          # string with value
        self.children = children    # list of HTMLNode objects
        self.props = props          # dictionary with HTML attributes

    def to_html(self):
        raise NotImplementedError("That's a parent class, don't use directly.")

    def props_to_html(self):
        attributes = " "
        if self.props is None:
            return attributes
        for key in self.props:
            attributes += f'{key}="{self.props[key]}" '
        return attributes

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props
    
    def __repr__(self):
        return f'Node: {self.tag}, {self.value}, {self.children}, {self.props}'