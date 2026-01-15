import unittest
from htmlnode import HTMLNode, HTMLTags, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):
    def test_leafnode_initialization(self):
        node = LeafNode("span", "Sample text", props={"style": "color:red;"})
        self.assertEqual(node.tag, HTMLTags.SPAN)
        self.assertEqual(node.value, "Sample text")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"style": "color:red;"})
    def test_leafnode_initialiaztion_none_tag(self):
        node = LeafNode(None, "Raw text")
        self.assertIsNone(node.tag.value)
        self.assertEqual(node.value, "Raw text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    def test_leafnode_repr(self):
        node = LeafNode("img", "image.png", props={"alt": "An image"})
        rep = repr(node)
        self.assertIn("leafNode", rep)
        self.assertIn("img", rep)
        self.assertIn("image.png", rep)
        self.assertIn("'alt': 'An image'", rep)

    def test_leaf_to_html_div(self):
        node = LeafNode("div", "Content")
        self.assertEqual(node.to_html(), "<div>Content</div>")
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

class test_parentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

#TODO Write better test cases for ParentNode and LeafNodes. Also test negative cases on these tests as I've not done so yet
if __name__ == "__main__":
    unittest.main()
