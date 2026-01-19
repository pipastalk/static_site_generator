from enum import Enum
from typing import overload
from htmlnode import *
class TextType(Enum):
    H1 = "h1"
    H2 = "h2"
    H3 = "h3"
    H4 = "h4"
    H5 = "h5"
    H6 = "h6"
    # PARAGRAPH = "paragraph"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    # UNORDERED_LIST = "unordered_list"
    # ORDERED_LIST = "ordered_list"
    # LIST_ITEM = "list_item"
    QUOTE = "quote"
    
    
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
    

