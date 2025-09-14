from textnode import TextNode, TextType
from leafnode import LeafNode
import re

def text_node_to_html_node(text_node : TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid tag")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) == 1:
            new_nodes.append(old_node)
            continue
        elif len(parts) % 2 == 0:
            raise Exception("Unmatched delimiter")
        odd = True
        for part in parts:
            if len(part) == 0:
                odd = not odd
                continue
            if odd:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
            odd = not odd
    if len(new_nodes) == 0:
        raise Exception("The node is either empty or contain just delimiters")
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.+?)\]\((.+?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.+?)\]\((.+?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if text.find('__img__') > 1:
            raise Exception("Possible injection detected!")
        images = extract_markdown_images(text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            text = text.replace(f'![{image[0]}]({image[1]})', '|__img__|')
        strips = text.split('|')
        index = 0
        for strip in strips:
            if len(strip) == 0:
                continue
            if strip == '__img__':
                new_nodes.append(TextNode(images[index][0], TextType.IMAGE, images[index][1]))
                index += 1
            else:
                new_nodes.append(TextNode(strip, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        text = node.text
        if text.find('__link__') > 1:
            raise Exception("Possible injection detected!")
        links = extract_markdown_links(text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            text = text.replace(f'[{link[0]}]({link[1]})', '|__link__|')
        strips = text.split('|')
        index = 0
        for strip in strips:
            if len(strip) == 0:
                continue
            if strip == '__link__':
                new_nodes.append(TextNode(links[index][0], TextType.LINK, links[index][1]))
                index += 1
            else:
                new_nodes.append(TextNode(strip, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    starting_node = TextNode(text, TextType.TEXT)
    extracted_links = split_nodes_link([starting_node])
    extracted_images = split_nodes_image(extracted_links)
    extracted_bold = split_nodes_delimiter(extracted_images, "**", TextType.BOLD)
    extracted_italic_1 = split_nodes_delimiter(extracted_bold, "_", TextType.ITALIC)
    extracted_italic_2 = split_nodes_delimiter(extracted_italic_1, "*", TextType.ITALIC)
    extracted_code = split_nodes_delimiter(extracted_italic_2, "`", TextType.CODE)
    return extracted_code