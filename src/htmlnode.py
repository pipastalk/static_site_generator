from enum import Enum
from typing import overload
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
    PRE = "pre"
    CODEBLOCK = "codeblock"
    CODE = "code"
    QUOTE = "blockquote"
    OL = "ol" #TODO add support for ordered lists in markdown_to_html_node
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
        props_str = ""
        if not self.props:
            return props_str # Return empty string if no props
        for key, value in self.props.items():
            if key is None or value is None:
                raise ValueError(f"props key and value cannot be None \n{self.props!r}")
            props_str += f' {key}="{value}"'
        return props_str
    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
    def __eq__(self, other):
        return (
            isinstance(other, LeafNode) and
            self.tag == other.tag and
            self.value == other.value and
            self.props == other.props
        )

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        tag = tag if isinstance(tag, HTMLTags) else HTMLTags(tag)
        super().__init__(tag=tag, value=value, children=None, props=props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is HTMLTags.RAW_TEXT:
            return self.value
        tag = f"<{self.tag.value}>"
        endtag = f"</{self.tag.value}>"
        return f"{tag}{self.value}{endtag}"
    def __repr__(self):
        return f"leafNode(tag={self.tag!r}, value={self.value!r}, props={self.props!r})"

class ParentNode(HTMLNode):
    @overload
    def __init__(self, tag, children: list, props=None): ...
    def __init__(self, tag, children, props=None):
        if not isinstance(children, list):
            raise ValueError("ParentNode children must be a list")
        if children is None:
            raise ValueError("ParentNode children cannot be None")
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag is HTMLTags.RAW_TEXT:
            raise ValueError("Parent node must have a valid tag")
        if not self.children:
            raise ValueError("Parent node must have children")
        child_html = f"<{self.tag.value}>"
        for child in self.children:
            child_html += child.to_html()
        child_html += f"</{self.tag.value}>"
        return child_html