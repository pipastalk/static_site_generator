from enum import Enum
class BlockType(Enum):
    # FORMAT: (display_name, markdown_delimiter, html_open, html_close) 
    QUOTE = ("quote", "> ","<blockquote>", "</blockquote>")
    PARAGRAPH = ("paragraph", None, "<p>", "</p>")
    UNORDERED_LIST = ("unordered_list", "- ", "<ul>", "</ul>")
    ORDERED_LIST = ("ordered_list", None, "<ol>", "</ol>")
    ORDERED_LIST_ITEM = ("list_item", r"^\d+\.", "<li>", "</li>") 
    CODEBLOCK = ("codeblock", "```", "<code>", "</code>")
    H1 = ("h1", "# ", "<h1>", "</h1>")
    H2 = ("h2", "## ", "<h2>", "</h2>")
    H3 = ("h3", "### ", "<h3>", "</h3>")
    H4 = ("h4", "#### ", "<h4>", "</h4>")
    H5 = ("h5", "##### ", "<h5>", "</h5>")
    H6 = ("h6", "###### ", "<h6>", "</h6>")
    
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
    
class BlockNode:
    pass
    
#