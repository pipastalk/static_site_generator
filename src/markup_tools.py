from htmlnode import HTMLNode, HTMLTags, LeafNode
from textnode import TextNode, TextType
import re

class MarkUpTools:

    def split_nodes_delimiter(old_nodes:TextNode, delimiter, text_type:TextType):
        new_nodes = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                new_nodes.append(old_node)
                continue
            text = old_node.text.split(delimiter)
            if len(text) % 2 == 0:
                raise ValueError("invalid markdown, formatted section not closed")
            for i in range(len(text)):
                snipet = text[i]
                if snipet == "":
                    continue
                if i % 2 == 1:
                    new_nodes.append(TextNode(snipet, text_type))
                else:
                    new_nodes.append(TextNode(snipet, TextType.TEXT))
        return new_nodes
    
    def text_node_to_html_node(text_node:TextNode) -> LeafNode:
        tag = None
        props = None
        match text_node.text_type:
            case TextType.TEXT:
                tag = HTMLTags.RAW_TEXT
            case TextType.BOLD:
                tag = HTMLTags.B
            case TextType.ITALIC:
                tag = HTMLTags.I
            case TextType.LINK:
                props = {"href": text_node.url}
                tag = HTMLTags.A
            case TextType.IMAGE:
                tag = HTMLTags.IMG
                props = {"src": text_node.url, "alt": text_node.text}
            case _:
                raise ValueError(f"Unsupported TextType for conversion to HTMLNode: {text_node.text_type!r}")
        return LeafNode(tag=tag, value=text_node.text, props=props)
    
    def extract_markdown_images(text):
        #return data = [(alt_text, image_source), ...]
        delimiter_pattern = r'!\[(.*?)\]\((.*?)\)'
        matches = re.findall(delimiter_pattern, text)
        if matches:
            for match in matches:
                if not match[0] and not match[1]:
                    raise ValueError(f"Image alt text and source URL are missing in {match}")
                elif not match[1]:
                    raise ValueError(f"Image source URL is missing in {match}")
                elif not match[0]:
                    pass #TODO change this to silent logging later
                    # raise ValueError(f"Image alt text is missing in {match}") 
            return matches
        return ValueError("No markdown images found")

    def extract_markdown_links(text):
        #return data = [(link, url), ...]
        delimiter_pattern = r'\[(.*?)\]\((.*?)\)'
        matches = re.findall(delimiter_pattern, text)
        if matches:
            for match in matches:
                if not match[0] and not match[1]:
                    raise ValueError(f"Link text and URL are missing in {match}")
                if not match[1]:
                    raise ValueError(f"Link URL is missing in {match}")
                if not match[0]:
                    raise ValueError(f"Link text is missing in {match}") 
            return matches
        return ValueError("No markdown images found")