import unittest
from htmlnode import HTMLNode, HTMLTags

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_initialization_with_enum(self):
        node = HTMLNode(tag=HTMLTags.DIV, value="Hello", children=[], props={"class": "container"})
        self.assertEqual(node.tag, HTMLTags.DIV)
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "container"})

    def test_htmlnode_initialization_with_str_tag(self):
        node = HTMLNode(tag="span", value="World", children=None, props=None)
        self.assertEqual(node.tag, HTMLTags.SPAN)
        self.assertEqual(node.value, "World")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_htmlnode_repr(self):
        node = HTMLNode(tag="p", value="Text", children=[1, 2], props={"id": "pid"})
        rep = repr(node)
        self.assertIn("HTMLNode", rep)
        self.assertIn("p", rep)
        self.assertIn("Text", rep)
        self.assertIn("[1, 2]", rep)
        self.assertIn("'id': 'pid'", rep)

    def test_htmlnode_props_to_html(self):
        node = HTMLNode(tag="a", value="link", props={"href": "#", "class": "btn"})
        props_html = node.props_to_html()
        self.assertIn('href="#"', props_html)
        self.assertIn('class="btn"', props_html)
        self.assertTrue(props_html.strip().startswith('href') or props_html.strip().startswith('class'))

    def test_htmlnode_props_to_html_empty(self):
        node = HTMLNode(tag="ul")
        self.assertEqual(node.props_to_html(), "")

    def test_htmlnode_to_html_not_implemented(self):
        node = HTMLNode(tag="div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_htmlnode_invalid_tag_raises(self):
        with self.assertRaises(ValueError):
            HTMLNode(tag="notatag")


if __name__ == "__main__":
    unittest.main()
