from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING = "h"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleanup_blocks = []
    for block in blocks:
        if len(block) != 0:
            cleanup_blocks.append(block.strip())
    return cleanup_blocks

def block_to_block_type(block):
    match block[0]:
        case "#":
            for index in range(6):
                if block[index + 1] != "#" and block[index + 1] != " ":
                    return BlockType.PARAGRAPH
                return BlockType.HEADING
        case "`":
            if block.startswith("```") and block.endswith("```"):
                return BlockType.CODE
            return BlockType.PARAGRAPH
        case ">":
            lines = block.split("\n")
            for line in lines:
                if line[0] != ">":
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        case "-":
            lines = block.split("\n")
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "*":
            lines = block.split("\n")
            for line in lines:
                if not line.startswith("* "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        case "1":
            lines = block.split("\n")
            index = 1
            for line in lines:
                if not line.startswith(f"{index}. "):
                    return BlockType.PARAGRAPH
                index += 1
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH