import unittest
from textnode import TextNode, TextType


class TestTextTypeEnum(unittest.TestCase):
    def test_enum_values_are_unique(self):
        text_types = list(TextType)
        values = [t.value for t in text_types]
        self.assertEqual(len(values), len(set(values)), "TextType values are not unique")
            
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        text_types = list(TextType)
        for text_type in text_types:
            enum_created_node = TextNode("Sample text", text_type)
            str_created_node = TextNode("Sample text", text_type.value)
            self.assertEqual(enum_created_node, str_created_node, "TextNodes created with enum and string TextType should be equal")
        
    def test_inequality(self):
        text_types = list(TextType)
        for i in range(0, len(text_types) - 1):
            tn1 = TextNode("Sample text", text_types[i])
            tn2 = TextNode("Sample text", text_types[i + 1])
            self.assertNotEqual(tn1, tn2, "TextNodes with different TextTypes should not be equal")
        
        #Test last with first of enum to complete the loop
        t1 = TextNode("Sample text", text_types[-1])
        t2 = TextNode("Sample text", text_types[0])
        self.assertNotEqual(t1, t2, "TextNodes with different TextTypes should not be equal")

    def test_url_initialization(self):
        tn_with_url = TextNode("Link text", TextType.LINK, "https://example.com")
        self.assertEqual(tn_with_url.url, "https://example.com", "URL should be set correctly when provided")
        
        tn_without_url = TextNode("Just text", TextType.TEXT)
        self.assertIsNone(tn_without_url.url, "URL should be None when not provided")
    
    def test_invalid_text_type(self):
        with self.assertRaises(ValueError, msg="Creating TextNode with invalid text_type should raise ValueError"):
            TextNode("Sample text", "invalid_type")
    

if __name__ == "__main__":
    unittest.main()