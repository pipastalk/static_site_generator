from enum import Enum
from unittest import case
class HTMLTags(Enum):
    DIV = "div"
    SPAN = "span"
    P = "p"
    A = "a"
    IMG = "img"
    UL = "ul"
    LI = "li"
    TABLE = "table"
    TR = "tr"
    TD = "td"
    TH = "th"
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    B = "b"
    I = "i"
    U = "u"
    RAW_TEXT = None # Special case for raw text nodes

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag if isinstance(tag, HTMLTags) else HTMLTags(tag)
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html method must be implemented by subclasses")
    def props_to_html(self):
        if not self.props:
            return ""
        props_str = " ".join(f' {key}="{value}"' for key, value in self.props.items())
        return props_str
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        tag = tag if isinstance(tag, HTMLTags) else HTMLTags(tag)
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value
        tag = f"<{self.tag.value}>"
        endtag = f"</{self.tag.value}>"
        return f"{tag}{self.value}{endtag}"
    def __repr__(self):
        return f"leafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node must have a valid tag")
        if self.children is None:
            raise ValueError("Parent node must have children")
        child_html = f"<{self.tag.value}>"
        for child in self.children:
            child_html += child.to_html()
        child_html += f"</{self.tag.value}>"
        return child_html