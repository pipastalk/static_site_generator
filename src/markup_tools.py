import os
import re
from htmlnode import *
from textnode import TextNode, TextType
from blocknode import BlockType, BlockNode

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
            case TextType.CODE:
                tag = HTMLTags.CODE
            case TextType.QUOTE:
                tag = HTMLTags.BLOCKQUOTE
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
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = MarkUpTools.split_nodes_image(nodes)
        nodes = MarkUpTools.split_nodes_link(nodes)
        for tag in TextType:
            if tag.category != "inline":
                continue
            elif tag.markdown_close == None or tag.markdown_open == None:
                continue
            if tag.markdown_open == tag.markdown_close:
                nodes = MarkUpTools.split_nodes_delimiter(nodes, tag.markdown_open, tag)
            else:
                #TODO handle different opening and closing delimiters
                pass
        return nodes
    
    def markdown_to_blocks(text):
        lines = text.split("\n\n")
        blocks = []
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            blocks.append(line)
        return blocks
    
    def block_to_block_type(block):
        if block == "":
            raise ValueError("Empty block has no BlockType")
        for tag in BlockType:
            md = tag.markdown
            if md is None:
                continue
            if tag == BlockType.ORDERED_LIST_ITEM:
                pattern = r"^\d+\."
                if re.match(pattern, block):
                    return tag
            elif tag == BlockType.CODEBLOCK:
                if block.startswith(md) and block.endswith(md):
                    if block.split(md, 1)[1].strip() == "":
                        raise ValueError(f"Empty block, {tag.display_name} has no content {block!r}")
                    return tag
                elif block.startswith(md):
                    raise ValueError(f"Invalid markdown, codeblock is opened but never closed {block!r}")
            elif block[:len(md)] == md:
                if block.split(md, 1)[1].strip() == "":
                    raise ValueError(f"Empty block, {tag.display_name} has no content {block!r}")
                return tag
        return BlockType.PARAGRAPH
    
    def markdown_to_html_node(markdown):
        parent_div = ParentNode(HTMLTags.DIV, children=[])
        blocks = MarkUpTools.markdown_to_blocks(markdown)
        for block in blocks:
            block_type = MarkUpTools.block_to_block_type(block)
            if block_type == BlockType.CODEBLOCK:
                pre_wrapper = ParentNode(HTMLTags.PRE, children=[])
                #region stipping codeblock markdown and validating it is correct
                start_snip = block[0:3]
                if start_snip != BlockType.CODEBLOCK.markdown:
                    raise ValueError(f"Invalid codeblock markdown, expected opening delimiter {BlockType.CODEBLOCK.markdown!r} but got {start_snip!r} in block: {block!r}")
                end_snip = block[-3:]
                if end_snip != BlockType.CODEBLOCK.markdown:
                    raise ValueError(f"Invalid codeblock markdown, expected closing delimiter {BlockType.CODEBLOCK.markdown!r} but got {end_snip!r} in block: {block!r}")
                text = block[3:-3]
                if text.startswith("\n"):
                    text = text[1:]
                #endregion
                if not text.endswith("\n"):
                    text = text + "\n"
                codeblock_text_node = TextNode(text=text, text_type=TextType.CODE)
                pre_wrapper.children.append(MarkUpTools.text_node_to_html_node(codeblock_text_node))
                line_node = pre_wrapper
            elif block_type in [BlockType.ORDERED_LIST_ITEM, BlockType.UNORDERED_LIST_ITEM]:
                line_node = MarkUpTools.list_block_to_html_nodes(block, block_type)
            else:
                line_node = MarkUpTools.block_to_html_nodes(block, block_type)
            parent_div.children.append(line_node)
        return parent_div

    def block_to_html_nodes(block, block_type):
        # Helper function to convert a block of text into an HTMLNode based on its BlockType. Does not support CodeBlocks
        wrapper_node = None
        if block_type == BlockType.QUOTE:
            block = block.replace("\n> ", "\n")
        if block_type not in [BlockType.UNORDERED_LIST_ITEM, BlockType.ORDERED_LIST_ITEM] and block_type.markdown is not None:
            #Strips the markdown from the syntax specific cases removed such as list items.
            block = block[len(block_type.markdown):]
        block = block.replace("\n", " ")
        text_nodes = MarkUpTools.text_to_text_nodes(block)
        if len(text_nodes)  < 1:
            raise ValueError(f"Unexpected error, text_to_text_nodes returned empty list for block: {block!r}")
        for i in range(len(text_nodes)):
            if i == 0:
                wrapper_node = ParentNode(block_type.html_tag, children=[])
            leaf_node = MarkUpTools.text_node_to_html_node(text_nodes[i])
            wrapper_node.children.append(leaf_node)
        if wrapper_node is None:
            raise ValueError(f"Unexpected error, wrapper_node is None after processing block: {block!r}")
        return wrapper_node
    
    def list_block_to_html_nodes(block, block_type):
        if block_type == BlockType.ORDERED_LIST_ITEM:
            wrapper_node = ParentNode(HTMLTags.OL, children=[])
        elif block_type == BlockType.UNORDERED_LIST_ITEM:
            wrapper_node = ParentNode(HTMLTags.UL, children=[])
        else:
            raise ValueError(f"Unsupported BlockType for list_block_to_html_nodes: {block_type!r}")
        block_lines = block.split("\n")
        
        for i in range(len(block_lines)):
            snipet = block_lines[i]
            if snipet == "":
                continue
            if block_type == BlockType.ORDERED_LIST_ITEM:
                delimiter = f"{i+1}. "

                if not snipet.startswith(delimiter):
                    raise ValueError(f"Invalid ordered list item, expected to start with {delimiter!r} but got {snipet!r}")
                snipet = re.sub(delimiter, "", snipet)
                list_item_nodes = MarkUpTools.block_to_html_nodes(block=snipet, block_type=BlockType.ORDERED_LIST_ITEM)
            elif block_type == BlockType.UNORDERED_LIST_ITEM:
                delimiter = block_type.markdown
                if not snipet.startswith(delimiter):
                    raise ValueError(f"Invalid unordered list item, expected to start with {delimiter!r} but got {snipet!r}")
                snipet = re.sub(delimiter, "", snipet)
                list_item_nodes = MarkUpTools.block_to_html_nodes(block=snipet, block_type=BlockType.UNORDERED_LIST_ITEM)
            else:
                raise ValueError(f"Unsupported BlockType for list_block_to_html_nodes: {block_type!r}")
            wrapper_node.children.append(list_item_nodes)
        return wrapper_node

    def extract_title(markdown):
        node = MarkUpTools.markdown_to_blocks(markdown)
        for block in node:
            block_type = MarkUpTools.block_to_block_type(block)
            if block_type == BlockType.H1:
                text = block[len(BlockType.H1.markdown):]
                return text
        raise ValueError(f"No title found in markdown {markdown!r}") 

    def generate_page(from_path, template_path, dest_path):
        print(f"Generating page from {from_path} using template {template_path} and saving to {dest_path}")
        if not os.path.exists(from_path):
            raise FileNotFoundError(f"Source file not found: {from_path}")
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        #region destination path validation
        if os.path.exists(dest_path):
            raise FileExistsError(f"Destination file already exists: {dest_path}")
        if os.getcwd() not in os.path.abspath(dest_path):
            raise ValueError(f"Destination path must be within the current working directory: {dest_path}")
        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))    
        #endregion 
        with open(from_path, "r") as f:
            source_markdown = f.read()
        with open(template_path, "r") as f:
            template_html = f.read()
        source_html = MarkUpTools.markdown_to_html_node(source_markdown).to_html()
        source_title = MarkUpTools.extract_title(source_markdown)
        final_html = template_html.replace("{{ Content }}", source_html)
        final_html = final_html.replace("{{ Title }}", source_title)
        with open(dest_path, "w") as f:
            f.write(final_html)
        
#TODO Fix bug where inline text with image or links are not picked up as the correct htmlnode
#TODO Handle invalid src or href URLs inside split_nodes_special
#TODO Change to static tools properly