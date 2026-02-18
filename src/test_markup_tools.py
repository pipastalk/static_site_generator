import unittest
from unittest import result
from markup_tools import *
from textnode import TextNode, TextType
from blocknode import BlockType, BlockNode
class Test_Split_Nodes_Delimiter(unittest.TestCase):
    def test_markup_tool_functionality(self):
        node = TextNode("This is text with a `code block` and another `snippet` word", TextType.TEXT)
        new_nodes = MarkUpTools.split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and another ", TextType.TEXT),
            TextNode("snippet", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_splitting(self):
        node = TextNode("This is **bold** text and **strong** emphasis", TextType.TEXT)
        new_nodes = MarkUpTools.split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("strong", TextType.BOLD),
            TextNode(" emphasis", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_italic_splitting(self):
        node = TextNode("This is _italic_ text and _emphasis_ too", TextType.TEXT)
        new_nodes = MarkUpTools.split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text and ", TextType.TEXT),
            TextNode("emphasis", TextType.ITALIC),
            TextNode(" too", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_mixed_splitting(self):
        node = TextNode("This is **bold** and `code` with _italic_ text", TextType.TEXT)
        nodes_after_bold = MarkUpTools.split_nodes_delimiter([node], "**", TextType.BOLD)
        nodes_after_code = MarkUpTools.split_nodes_delimiter(nodes_after_bold, "`", TextType.CODE)
        final_nodes = MarkUpTools.split_nodes_delimiter(nodes_after_code, "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(final_nodes, expected_nodes)

    def test_unmatched_delimiter(self):
        node = TextNode("This is `unmatched code block text", TextType.TEXT)
        with self.assertRaises(ValueError):
            MarkUpTools.split_nodes_delimiter([node], "`", TextType.CODE)

    def test_text_node_to_html_node(self):
        rawTextNode = TextNode("This is a text node", TextType.TEXT)
        html_node = MarkUpTools.text_node_to_html_node(rawTextNode)
        self.assertEqual(html_node.tag.value, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsNone(html_node.props)
        boldTextNode = TextNode("Bold text", TextType.BOLD)
        html_node =  MarkUpTools.text_node_to_html_node(boldTextNode)
        self.assertEqual(html_node.tag.value, "b")
        self.assertEqual(html_node.value, "Bold text")
        self.assertIsNone(html_node.props)
        linkTextNode = TextNode("Link text", TextType.LINK, "https://example.com")
        html_node = MarkUpTools.text_node_to_html_node(linkTextNode)
        self.assertEqual(html_node.tag.value, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        imageTextNode = TextNode("Image alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = MarkUpTools.text_node_to_html_node(imageTextNode)
        self.assertEqual(html_node.tag.value, "img")
        self.assertEqual(html_node.value, "Image alt text")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Image alt text"})

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_link_missing(self):
        text = "[](http://example.com)"
        with self.assertRaises(ValueError):
            MarkUpTools.extract_markdown_links(text)

    def test_url_missing(self):
        text = "[Example]()"
        with self.assertRaises(ValueError):
            MarkUpTools.extract_markdown_links(text)

    def test_link_and_url_missing(self):
        text = "[]()"
        with self.assertRaises(ValueError):
            MarkUpTools.extract_markdown_links(text)

    def test_link_and_url_valid(self):
        text = "[Example](http://example.com)"
        result = MarkUpTools.extract_markdown_links(text)
        self.assertEqual(result, [("Example", "http://example.com")])

    def test_misformatted_markup_for_links(self):
        text = "[Example(http://example.com)"
        self.assertEqual(MarkUpTools.extract_markdown_links(text), [])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_image_missing(self):
        text = "![](http://example.com/image.png)"
        # Should not raise, just pass silently
        result = MarkUpTools.extract_markdown_images(text)
        self.assertEqual(result, [("", "http://example.com/image.png")])

    def test_url_missing(self):
        text = "![alt text]()"
        with self.assertRaises(ValueError):
            MarkUpTools.extract_markdown_images(text)

    def test_image_and_url_missing(self):
        text = "![]()"
        with self.assertRaises(ValueError):
            MarkUpTools.extract_markdown_images(text)

    def test_image_and_url_valid(self):
        text = "![alt text](http://example.com/image.png)"
        result = MarkUpTools.extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "http://example.com/image.png")])

    def test_misformatted_markup_for_image(self):
        text = "![alt text(http://example.com/image.png)"
        self.assertEqual(MarkUpTools.extract_markdown_images(text), [])

# Tests for split_nodes_link
class Test_Split_Nodes_Link(unittest.TestCase):
    def test_single_link(self):
        node = TextNode("This is a [link](http://example.com) in text", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "http://example.com"),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_link_type_passthrough(self):
        node = TextNode("already a link", TextType.LINK, "url")
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        self.assertEqual(result, [node])

    def test_no_links(self):
        node = TextNode("No links here", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        self.assertEqual(result, [node])
    def test_link_at_start(self):
        node = TextNode("[start](http://start.com) is the beginning", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        expected = [
            TextNode("start", TextType.LINK, "http://start.com"),
            TextNode(" is the beginning", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    def test_link_at_end(self):
        node = TextNode("This is the end [end](http://end.com)", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        expected = [
            TextNode("This is the end ", TextType.TEXT),
            TextNode("end", TextType.LINK, "http://end.com"),
        ]
        self.assertEqual(result, expected)
    def test_no_url_in_link(self):
        node = TextNode("This is a [link]() in text", TextType.TEXT)
        with self.assertRaises(ValueError):
            result = MarkUpTools.split_nodes_special(node, TextType.LINK)
    def test_no_link_text(self):
        node = TextNode("This is a [](http://example.com) in text", TextType.TEXT)
        with self.assertRaises(ValueError):
            result = MarkUpTools.split_nodes_special(node, TextType.LINK)
    def test_multiple_links(self):
        node = TextNode("[first](a.com) and [second](b.com)", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.LINK)
        expected = [
            TextNode("first", TextType.LINK, "a.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "b.com")
        ]
        self.assertEqual(result, expected)
# Tests for split_nodes_image
class Test_Split_Nodes_Image(unittest.TestCase):
    def test_single_image(self):
        node = TextNode("This is an ![alt](img.png) in text", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "img.png"),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    def test_no_alt_text(self):
        node = TextNode("This is an ![](img.png) in text", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        expected = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "img.png"),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    def test_image_at_start(self):
        node = TextNode("![start](img.png) is the beginning", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        expected = [
            TextNode("start", TextType.IMAGE, "img.png"),
            TextNode(" is the beginning", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    def test_image_at_end(self):
        node = TextNode("This is the end ![end](img.png)", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        expected = [
            TextNode("This is the end ", TextType.TEXT),
            TextNode("end", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(result, expected)
    def test_image_type_passthrough(self):
        node = TextNode("already an image", TextType.IMAGE, "img.png")
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        self.assertEqual(result, [node])
    def test_no_images(self):
        #error is handled inside function so it will return the original node
        node = TextNode("No images here", TextType.TEXT)
        result = MarkUpTools.split_nodes_special(node, TextType.IMAGE)
        self.assertEqual(result, [node])
        #TODO do I need this test anymore?

    def test_no_image_inside_multiple_images(self):
        node = TextNode("![a](a.png) and [![noImage]()", TextType.TEXT)
        with self.assertRaises(ValueError): 
            result = MarkUpTools.split_nodes_special([node], TextType.IMAGE)
    def test_multiple_images(self):
        node = TextNode("![a](a.png) and ![b](b.png) and this is a no alt text image ![](noalt.png)", TextType.TEXT)
        result = MarkUpTools.split_nodes_special([node], TextType.IMAGE)
        expected = [
            TextNode("a", TextType.IMAGE, "a.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "b.png"),
            TextNode(" and this is a no alt text image ", TextType.TEXT),
            TextNode("", TextType.IMAGE, "noalt.png")
        ]
        self.assertEqual(result, expected)


class Test_Text_To_Text_Nodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = MarkUpTools.text_to_text_nodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected_nodes)
class Test_Markdown_To_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = MarkUpTools.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
class TestBlockToBlockType(unittest.TestCase):
    def test_empty_block_raises(self):
        with self.assertRaises(ValueError):
            MarkUpTools.block_to_block_type("")
    def test_empty_blocks(self):
        with self.assertRaises(ValueError):
            MarkUpTools.block_to_block_type("#    ")
        with self.assertRaises(ValueError):
            MarkUpTools.block_to_block_type(">    ")
    def test_open_codeblock(self):
        with self.assertRaises(ValueError):
            MarkUpTools.block_to_block_type("``` I'm an unclosed codeblock")
    def test_headings(self):
        self.assertEqual(MarkUpTools.block_to_block_type("# Heading 1"), BlockType.H1)
        self.assertEqual(MarkUpTools.block_to_block_type("## Heading 2"), BlockType.H2)
        self.assertEqual(MarkUpTools.block_to_block_type("### Heading 3"), BlockType.H3)
        self.assertEqual(MarkUpTools.block_to_block_type("#### Heading 4"), BlockType.H4)
        self.assertEqual(MarkUpTools.block_to_block_type("##### Heading 5"), BlockType.H5)
        self.assertEqual(MarkUpTools.block_to_block_type("###### Heading 6"), BlockType.H6)

    def test_quote(self):
        self.assertEqual(MarkUpTools.block_to_block_type("> This is a quote"), BlockType.QUOTE)

    def test_unordered_list_item(self):
        self.assertEqual(MarkUpTools.block_to_block_type("- List item"), BlockType.UNORDERED_LIST_ITEM)

    def test_ordered_list_item(self):
        self.assertEqual(MarkUpTools.block_to_block_type("1. Ordered item"), BlockType.ORDERED_LIST_ITEM)

    def test_codeblock(self):
        self.assertEqual(MarkUpTools.block_to_block_type("```code with multiple lines \nof random stuff\n just to mess with you \n ddsadea```"), BlockType.CODEBLOCK)

    def test_no_match_returns_paragraph(self):
        self.assertEqual(MarkUpTools.block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)

class TestBlockToHTMLNodes(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = MarkUpTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = MarkUpTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_inline_bold_and_code(self):
        md = "hello **bold** world, `this is some code` hopefully that didn't break shit"
        node = MarkUpTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>hello <b>bold</b> world, <code>this is some code</code> hopefully that didn't break shit</p></div>",
        )

    def test_codeblock_with_and_without_trailing_newline(self):
        md1 = "```\n**def hello_world():**\n    print('Hello, world!')\n```"
        md2 = "```\n**def hello_world():**\n    print('Hello, world!')```"
        node1 = MarkUpTools.markdown_to_html_node(md1)
        node2 = MarkUpTools.markdown_to_html_node(md2)
        expected = "<div><pre><code>**def hello_world():**\n    print('Hello, world!')\n</code></pre></div>"
        self.assertEqual(node1.to_html(), expected)
        self.assertEqual(node2.to_html(), expected)

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item"
        node = MarkUpTools.markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>")

    def test_unordered_list(self):
        md = "- First item\n- Second item\n- Third item"
        node = MarkUpTools.markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><ul><li>First item</li><li>Second item</li><li>Third item</li></ul></div>")

    def test_errored_ordered_list(self):
        md = "1. First item\n4. Second item\n3. Third item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)

    def test_complex_markdown_all_features(self):
        md = """
# Heading 1

## Subheading 2

Paragraph with **bold** and _italic_ and `inline`

```
def fn():
    return True
```

1. First
2. Second

- Uno
- Dos

> A quoted line
"""
        node = MarkUpTools.markdown_to_html_node(md)
        expected = (
            "<div>"
            "<h1>Heading 1</h1>"
            "<h2>Subheading 2</h2>"
            "<p>Paragraph with <b>bold</b> and <i>italic</i> and <code>inline</code></p>"
            "<pre><code>def fn():\n    return True\n</code></pre>"
            "<ol><li>First</li><li>Second</li></ol>"
            "<ul><li>Uno</li><li>Dos</li></ul>"
            "<blockquote>A quoted line</blockquote>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected)

    def test_headings_with_inline_effects(self):
        md = """
# Heading with **bold** and `code`

## Another _italic_ heading
"""
        node = MarkUpTools.markdown_to_html_node(md)
        expected = (
            "<div>"
            "<h1>Heading with <b>bold</b> and <code>code</code></h1>"
            "<h2>Another <i>italic</i> heading</h2>"
            "</div>"
        )
        self.assertEqual(node.to_html(), expected)
    def test_quote_block(self):
        md = "> This is a quote\n> spanning multiple lines"
        node = MarkUpTools.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote spanning multiple lines</blockquote></div>",
        )
class Test_Error_Cases(unittest.TestCase):
    def test_text_node_to_html_node_unsupported(self):
        node = TextNode("some codeblock", TextType.CODEBLOCK)
        with self.assertRaises(ValueError):
            MarkUpTools.text_node_to_html_node(node)

    def test_split_nodes_special_unsupported_type(self):
        node = TextNode("no special", TextType.TEXT)
        with self.assertRaises(ValueError):
            MarkUpTools.split_nodes_special(node, TextType.TEXT)

    def test_block_to_block_type_empty_codeblock_raises(self):
        block = ""
        with self.assertRaises(ValueError):
            MarkUpTools.block_to_block_type(block)

    def test_list_block_to_html_nodes_unsupported_blocktype(self):
        with self.assertRaises(ValueError):
            MarkUpTools.list_block_to_html_nodes("- item", BlockType.PARAGRAPH)

    def test_list_block_to_html_nodes_invalid_unordered_item(self):
        # line does not start with '- ' (missing space)
        md = "- First item\n-Second item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)
    def test_malformed_lists(self):
        md = "1. First item\nSecond item without number\n3. Third item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)
            md = "1. First item\n- Second item without number\n3. Third item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)
        md = "- First item\nSecond item without number\n- Third item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)
        md = "1. First item\nSecond item without number\n3. Third item\n- Fourth item"
        with self.assertRaises(ValueError):
            MarkUpTools.markdown_to_html_node(md)
    #TODO BELOW - fix known bug where /n/n within a codeblock leads to invalid snippet parsing in markdown_to_blocks
    def DISABLED_test_codeblock_with_ending_newlines(self):
        
        md = """
```python
# Code block example
def foo():
    return "bar"
    
    # Trick Title in code block

```
"""
        #node = MarkUpTools.markdown_to_html_node(md)
        #html = node.to_html()
        #expected_html = "<div><pre><code>python\n# Code block example\ndef foo():\n    return \"bar\"\n    \n    # Trick Title in code block\n</code></pre></div>"
        #self.assertEqual(html, expected_html)

class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
This is a test paragraph with some **bold** and *italic* text.

## Subheading (H2)

- List item one
- List item two
- Nested item

# Main Title (H1)

### Details (H3)

1. First step
2. Second step

> This is a blockquote for testing.

#### Subsection (H4)

Inline code: `print("Hello, world!")`

```python
# Code block example
def foo():
    return "bar"
```
"""
        title = MarkUpTools.extract_title(md)
        self.assertEqual(title, "Main Title (H1)")

    def test_extract_title_codeblock_title(self):
        md = """
This is a test paragraph with some **bold** and *italic* text.

## Subheading (H2)

- List item one
- List item two
- Nested item

### Details (H3)

1. First step
2. Second step

> This is a blockquote for testing.

#### Subsection (H4)

Inline code: `print("Hello, world!")`

```python
# Code block example
def foo():
    return "bar"
    
    # Trick Title in code block
```

# Main Title (H1)
"""
        title = MarkUpTools.extract_title(md)
        self.assertEqual(title, "Main Title (H1)")

    def test_extract_title_two_titles(self):
        md = """
This is a test paragraph with some **bold** and *italic* text.

# Main Title (H1)

## Subheading (H2)

- List item one
- List item two
- Nested item


### Details (H3)

1. First step
2. Second step

> This is a blockquote for testing.

#### Subsection (H4)

Inline code: `print("Hello, world!")`

```python
# Code block example
def foo():
    return "bar"
    
    # Trick Title in code block
```

# Second Main Title (H1)
"""
        title = MarkUpTools.extract_title(md)
        self.assertEqual(title, "Main Title (H1)")

if __name__ == '__main__':
    unittest.main()
