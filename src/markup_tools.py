from htmlnode import HTMLNode, HTMLTags, LeafNode
from textnode import TextNode, TextType
import re

class MarkUpTools:

    def split_nodes_delimiter(old_nodes:TextNode, delimiter, text_type:TextType) -> list[TextNode]:
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
    
    def extract_markdown_images(text): #return data = [(alt_text, image_source), ...]
        delimiter_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(delimiter_pattern, text)
        if matches:
            for match in matches:
                if not match[0] and not match[1]:
                    raise ValueError(f"{TextType.IMAGE.display_name.lower()} alt text and source URL are missing in {match}")
                elif not match[1]:
                    raise ValueError(f"{TextType.IMAGE.display_name.lower()} source URL is missing in {match}")
                elif not match[0]:
                    pass #TODO change this to silent logging later
                    # raise ValueError(f"{TextType.IMAGE.display_name.lower()} alt text is missing in {match}") 
            return matches
        return []
    
    def extract_markdown_links(text): #return data = [(link, url), ...]
        delimiter_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
        matches = re.findall(delimiter_pattern, text)
        if matches:
            for match in matches:
                if not match[0] and not match[1]:
                    raise ValueError(f"{TextType.LINK.display_name.lower()} text and URL are missing in {match}")
                if not match[1]:
                    raise ValueError(f"{TextType.LINK.display_name.lower()} URL is missing in {match}")
                if not match[0]:
                    raise ValueError(f"{TextType.LINK.display_name.lower()} text is missing in {match}") 
            return matches
        return []
    def split_nodes_link(old_nodes): #wrapper function
        return MarkUpTools.split_nodes_special(old_nodes, TextType.LINK)

    def split_nodes_image(old_nodes): #wrapper function
        return MarkUpTools.split_nodes_special(old_nodes, TextType.IMAGE)
    def split_nodes_special(old_nodes, text_type:TextType):
        if isinstance(old_nodes, TextNode):
            old_nodes = [old_nodes]
        new_nodes = []
        match text_type:
            case TextType.IMAGE:
                extractor = MarkUpTools.extract_markdown_images
            case TextType.LINK:
                extractor = MarkUpTools.extract_markdown_links
            case _:
                raise ValueError(f"Unsupported TextType for split_nodes_special: {text_type!r}")
        for node in old_nodes:
            text = node.text
            match node.text_type:
                case TextType.IMAGE:
                    new_nodes.append(node)
                case TextType.LINK:
                    new_nodes.append(node)
                case _:
                    matches = extractor(text)
                    if not matches:
                        new_nodes.append(node)
                    else:
                        match = matches[0]
                        special_text = match[0]
                        url = match[1]
                        match text_type:
                            case TextType.IMAGE:
                                delimiter = f"![{special_text}]({url})"
                            case TextType.LINK:
                                delimiter = f"[{special_text}]({url})"
                            case _:
                                raise ValueError(f"Unsupported TextType for split_nodes_special: {text_type!r}")    
                        parts = text.split(delimiter,1)
                        prefix_node = TextNode(parts[0], node.text_type) if parts[0] != "" else None
                        special_node = TextNode(special_text, text_type, url)
                        suffix_node = TextNode(parts[1], node.text_type) if parts[1] != "" else None
                        new_nodes.extend(filter(None, [prefix_node, special_node]))
                        if suffix_node is not None:
                            split_suffix_nodes = MarkUpTools.split_nodes_special([suffix_node], text_type)
                            new_nodes.extend(split_suffix_nodes)
        return new_nodes    
    
    def text_to_text_nodes(text):
        # "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [TextNode(text, TextType.TEXT)]
        for tag in TextType:
            if  tag.markdown_close == None or tag.markdown_open == None:
                continue
            if tag.markdown_open == tag.markdown_close:
                nodes = MarkUpTools.split_nodes_delimiter(nodes, tag.markdown_open, tag)
            else:
                #TODO handle different opening and closing delimiters
                pass
        nodes = MarkUpTools.split_nodes_image(nodes)
        nodes = MarkUpTools.split_nodes_link(nodes)
        return nodes
            
#
#TODO Handle invalid src or href URLs inside split_nodes_special