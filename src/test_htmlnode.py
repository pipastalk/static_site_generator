import unittest
from htmlnode import HTMLNode, HTMLTags, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_init(self):
        allActiveNode = HTMLNode(tag="div", value="Content", children=[], props={"id": "main"})
        self.assertEqual(allActiveNode.tag, HTMLTags.DIV)
        self.assertEqual(allActiveNode.value, "Content")
        self.assertEqual(allActiveNode.children, [])
        self.assertEqual(allActiveNode.props, {"id": "main"})
        allNoneNode = HTMLNode(tag=None, value=None, children=None, props=None)
        self.assertIsNone(allNoneNode.tag.value)
        self.assertIsNone(allNoneNode.value)
        self.assertIsNone(allNoneNode.children)
        self.assertIsNone(allNoneNode.props)
    def test_props_to_html(self):
        #region valid values props test
        propTestNode = HTMLNode(tag="a", value="link", props={"href": "#", "class": "btn"})
        expected_html_string = ' href="#" class="btn"'
        props_html = propTestNode.props_to_html()
        self.assertEqual(props_html, expected_html_string)
        #endregion
        #region None key/value tests
        blankValueNode = HTMLNode(tag="a", value="link", props={"href": "#", "class": None})        
        with self.assertRaises(ValueError):
            blankValueNode.props_to_html()
        blankKeyNode = HTMLNode(tag="a", value="link", props={"href": "#", None: "btn"})
        with self.assertRaises(ValueError):
            blankKeyNode.props_to_html()
        #endregion
    def test_to_html_not_implemented(self):
        node = HTMLNode(tag="div", value="Content", children=[], props={"id": "main"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leafnode_init(self):
        leaf = LeafNode(tag="span", value="Sample text", props={"style": "color:red;"})
        self.assertEqual(leaf.tag, HTMLTags.SPAN)
        self.assertEqual(leaf.value, "Sample text")
        self.assertIsNone(leaf.children)
        self.assertEqual(leaf.props, {"style": "color:red;"})
        with self.assertRaises(TypeError):
            leafWithChildren = LeafNode(tag="span", value="Sample text", children = [], props={"style": "color:red;"})
    
    def test_leafnode_to_html(self):
        leaf = LeafNode(tag="span", value="Sample text", props={"style": "color:red;"})
        expected_html = '<span>Sample text</span>'
        self.assertEqual(leaf.to_html(), expected_html)
        noneTagLeaf = LeafNode(tag=None, value="Sample text", props={"style": "color:red;"})
        expected_html_none_tag = 'Sample text'
        self.assertEqual(noneTagLeaf.to_html(), expected_html_none_tag)
        noneValueLeaf = LeafNode(tag="span", value=None, props={"style": "color:red;"})
        with self.assertRaises(ValueError):
            noneValueLeaf.to_html()

class TestParentNode(unittest.TestCase):
    def test_parentnode_init(self):
        with self.assertRaises(TypeError):
            valueFilledAttemptParent = ParentNode(tag="div", value="Sample Text", children=LeafNode("span", "text"), props={"class": "container"})
        with self.assertRaises(ValueError):
            noneChildrenParent = ParentNode(tag="div", children=None, props={"class": "container"})
        parentNode = ParentNode(tag="div", children=[LeafNode("span", "text")], props={"class": "container"})
        self.assertEqual(parentNode.tag, HTMLTags.DIV)
        self.assertIsNone(parentNode.value)
        self.assertEqual(parentNode.children, [LeafNode("span", "text")])
        self.assertEqual(parentNode.props, {"class": "container"})
        
    def test_parentnode_to_html(self):
        noneTagParent = ParentNode(tag=None, children=[LeafNode("span", "text")], props={"class": "container"})
        with self.assertRaises(ValueError):
            noneTagParent.to_html()
        noneChildrenParent = ParentNode(tag="div", children=[LeafNode("span", "text")], props={"class": "container"})
        noneChildrenParent.children = None
        with self.assertRaises(ValueError):
            noneChildrenParent.to_html()
        with self.assertRaises(ValueError):
            emptyChildrenParent = ParentNode(tag="div", children=[], props={"class": "container"})
        emptyChildrenParent = ParentNode(tag="div", children=[LeafNode("span", "text")], props={"class": "container"})
        emptyChildrenParent.children = []
        with self.assertRaises(ValueError):
            emptyChildrenParent.to_html()
        singleChildParent = ParentNode(tag="div", children=[LeafNode("b", "bold")], props={"class": "container"})
        expected_html = '<div><b>bold</b></div>'
        self.assertEqual(singleChildParent.to_html(), expected_html)
        multiChildParent = ParentNode(tag="ul", children=[LeafNode("li", "Item 1"), LeafNode("li", "Item 2")], props={"id": "list"})
        expected_html_multi = '<ul><li>Item 1</li><li>Item 2</li></ul>'
        self.assertEqual(multiChildParent.to_html(), expected_html_multi)
        multiLevelParent = ParentNode(tag="div", children=[multiChildParent, LeafNode("p", "Paragraph")], props={"class": "wrapper"})
        expected_html_multi_level = '<div><ul><li>Item 1</li><li>Item 2</li></ul><p>Paragraph</p></div>'
        self.assertEqual(multiLevelParent.to_html(), expected_html_multi_level)
        
if __name__ == "__main__":
    unittest.main()
