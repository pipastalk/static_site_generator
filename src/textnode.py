from enum import Enum
from typing import overload
from htmlnode import *
class TextType(Enum):
    #TODO Currently only includes inline text types
    # format: 0 = display_name, 1=markdown_open, 2=markdown_close, 3=html_open, 4=html_close, 5=category(inline/block/special) 
    
    # H1 = ("h1", "#", "\n", "<h1>", "</h1>", "inline")
    # H2 = ("h2", "##", "\n", "<h2>", "</h2>", "inline")
    # H3 = ("h3", "###", "\n", "<h3>", "</h3>", "inline")
    # H4 = ("h4", "####", "\n", "<h4>", "</h4>", "inline")
    # H5 = ("h5", "#####", "\n", "<h5>", "</h5>", "inline")
    # H6 = ("h6", "######", "\n", "<h6>", "</h6>", "inline")
    TEXT = ("text", None, None, None, None, None)
    BOLD = ("bold", "**", "**", "<strong>", "</strong>", "inline")
    ITALIC = ("italic", "_", "_", "<em>", "</em>", "inline")
    CODE = ("code", "`", "`", "<code>", "</code>", "inline")
    LINK = ("link", None, None, "<a>", "</a>", "special")
    IMAGE = ("image", None, None, "<img>", "</img>", "special")
    # QUOTE = ("quote", "> ", "None" "<blockquote>", "</blockquote>", "block")
    # PARAGRAPH = "paragraph"
    # UNORDERED_LIST = "unordered_list"
    # ORDERED_LIST = "ordered_list"
    # LIST_ITEM = "list_item"
    
    @property
    def display_name(self):
        return self.value[0]
    @property
    def markdown_open(self):
        return self.value[1]
    @property
    def markdown_close(self):
        return self.value[2]
    @property
    def html_open(self):
        return self.value[3]
    @property
    def html_close(self):
        return self.value[4]
    @property
    def category(self):
        return self.value[5]

class TextNode:
    @overload
    def __init__(self, text, text_type: TextType, url=None): ...
    @overload
    def __init__(self, text, text_type: str, url=None): ...
    def __init__(self, text, text_type, url=None):
        self.text = text
        if isinstance(text_type, TextType):
            self.text_type = text_type
        else:
            try:
                self.text_type = TextType(text_type)
            except ValueError:
                raise ValueError(f"Invalid text_type when creating a TextNode: {text_type!r}")
        self.url = url
    def __eq__(self, other):
        return (
            isinstance(other, TextNode)
            and self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )
    def __repr__(self):
        return(f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})")
    

