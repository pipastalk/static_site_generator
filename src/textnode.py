from enum import Enum
from typing import overload
from htmlnode import *
class TextType(Enum):
    #TODO Currently only includes inline text types
    
    # H1 = ("h1", "#", "\n", "<h1>", "</h1>")
    # H2 = ("h2", "##", "\n", "<h2>", "</h2>")
    # H3 = ("h3", "###", "\n", "<h3>", "</h3>")
    # H4 = ("h4", "####", "\n", "<h4>", "</h4>")
    # H5 = ("h5", "#####", "\n", "<h5>", "</h5>")
    # H6 = ("h6", "######", "\n", "<h6>", "</h6>")
    TEXT = ("text", None, None, None, None)
    BOLD = ("bold", "**", "**", "<strong>", "</strong>")
    ITALIC = ("italic", "_", "_", "<em>", "</em>")
    CODE = ("code", "`", "`", "<code>", "</code>")
    LINK = ("link", None, None, "<a>", "</a>")
    IMAGE = ("image", None, None, "<img>", "</img>")
    # QUOTE = ("quote", "> ", "\n", "<blockquote>", "</blockquote>")
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
    

