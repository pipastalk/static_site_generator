from enum import Enum
from htmlnode import HTMLTags
class BlockType(Enum):
    # FORMAT: (display_name, markdown_delimiter, html_open, html_close) 
    QUOTE = ("quote", "> ","<blockquote>", "</blockquote>", HTMLTags.QUOTE)
    PARAGRAPH = ("paragraph", None, "<p>", "</p>", HTMLTags.P)
    UNORDERED_LIST = ("unordered_list", None, "<ul>", "</ul>", HTMLTags.UL)
    UNORDERED_LIST_ITEM = ("list_item", r"- ", "<li>", "</li>", HTMLTags.LI)
    ORDERED_LIST = ("ordered_list", None, "<ol>", "</ol>", HTMLTags.OL)
    ORDERED_LIST_ITEM = ("list_item", r"^\d+\.", "<li>", "</li>", HTMLTags.LI) 
    PRE = ("pre", None, "<pre>", "</pre>", HTMLTags.PRE)
    CODEBLOCK = ("codeblock", "```", "<code>", "</code>", HTMLTags.CODEBLOCK)
    CODE = ("code", "`", "<code>", "</code>", HTMLTags.CODE)
    H1 = ("h1", "# ", "<h1>", "</h1>", HTMLTags.H1)
    H2 = ("h2", "## ", "<h2>", "</h2>", HTMLTags.H2)
    H3 = ("h3", "### ", "<h3>", "</h3>", HTMLTags.H3)
    H4 = ("h4", "#### ", "<h4>", "</h4>", HTMLTags.H4)
    H5 = ("h5", "##### ", "<h5>", "</h5>", HTMLTags.H5)
    H6 = ("h6", "###### ", "<h6>", "</h6>", HTMLTags.H6)
    
    @property
    def display_name(self):
        return self.value[0]
    @property
    def markdown(self):
        return self.value[1]
    @property
    def html_open(self):
        return self.value[2]
    @property
    def html_close(self):
        return self.value[3]
    @property
    def html_tag(self):
        return self.value[4]
class BlockNode:
    pass
    
#