from documenttonodes import markdown_to_blocks, block_to_block_type, BlockType 
from texttohtml import text_node_to_html_node, text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    top_level_child_nodes = []
    for block in blocks:
        block_level_child_nodes = block_tuple_to_text_nodes(block, block_to_block_type(block))
        top_level_child_nodes.append(block_level_child_nodes)

    return ParentNode("div", top_level_child_nodes)
    
def block_tuple_to_text_nodes(value, type):
    
    match type:
        case BlockType.CODE:
            return ParentNode("pre", [LeafNode("code", value.removeprefix("```").removesuffix("```").lstrip())])
    
        case BlockType.HEADING:
            level = 0   
            while value.startswith("#"):
                value = value.removeprefix("#")
                level += 1
            value = value.strip()
            return ParentNode(f'h{level}', list(map(text_node_to_html_node, text_to_textnodes(value))))            
    
        case BlockType.QUOTE:
            lines = value.split("\n")
            lines = list(map(lambda line: line.removeprefix("> "), lines))
            return ParentNode("blockquote", list(map(text_node_to_html_node, text_to_textnodes(" ".join(lines)))))

        case BlockType.PARAGRAPH:
            return ParentNode("p", list(map(text_node_to_html_node, text_to_textnodes(value.strip().replace("\n", " ")))))

        case BlockType.UNORDERED_LIST:
            return text_to_list(value, type)
        
        case BlockType.ORDERED_LIST:
            return text_to_list(value, type)

        case _:
            raise Exception("How did we even get here? The types were set.")
        
def text_to_list(text, type):
    lines = text.split("\n")
    lines = list(map(lambda line: line[2:] if type == BlockType.UNORDERED_LIST else line[3:], lines))
    return ParentNode("ul" if type == BlockType.UNORDERED_LIST else "ol",list(map(lambda line: ParentNode("li", list(map(text_node_to_html_node, text_to_textnodes(line)))), lines)))

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == BlockType.HEADING and block.startswith("# "):
            return block.removeprefix("# ").strip()
    raise Exception("Markdown does not have a title!")
            