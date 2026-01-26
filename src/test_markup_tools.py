from unittest import result
from markup_tools import *
from textnode import TextNode, TextType
import unittest

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

if __name__ == '__main__':
    unittest.main()
