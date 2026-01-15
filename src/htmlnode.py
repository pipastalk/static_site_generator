from enum import Enum
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
    

