from __future__ import division, print_function
import markdown
import os
import re

DOCUMENT_LINK_PATTERN = r'\[\[(.*?)\]\]'
NODE_LINK_PATTERN = r'\(\((.*?)\)\)'


def make_node_save_directory(path):
    """
    Make a new directory for saving nodes in.
    :param path: path to directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


def update_text_file(node, setting_model):
    """
    Update the text file corresponding to an updated node.
    :param node: node instance
    :param setting_model: models.Setting
    """
    node_save_directory = setting_model.objects.get(pk='NODE_SAVE_DIRECTORY').value
    path = os.path.join(node_save_directory, node.id)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open('{}.md'.format(path), 'w') as f:
        f.write(node.text)


def extract_linked_objects(text, document_model, node_model):
    """
    Extract all of the linked objects from a node's text.
    :param text: text
    :param document_model: models.Document
    :param node_model: models.Node
    :return: linked documents list, linked nodes list
    """

    # extract documents
    document_links = re.findall(DOCUMENT_LINK_PATTERN, text)
    document_ids = [link.split('|')[0].strip() for link in document_links]
    documents = [document_model.objects.get(pk=document_id) for document_id in document_ids]

    # extract node links
    node_links = re.findall(NODE_LINK_PATTERN, text)
    node_ids = [link.split('|')[0].strip() for link in node_links]
    nodes = [node_model.objects.get(pk=node_id) for node_id in node_ids]

    return documents, nodes


def bind_linked_objects(node, document_model, node_model):
    """
    Bind all of the documents and nodes that a node links to itself in the database.

    :param node: node
    :param document_model: models.Document
    :param node_model: models.Node
    """

    documents, nodes = extract_linked_objects(node.text, document_model, node_model)

    node.documents.clear()
    node.documents.add(*documents)
    node.nodes.clear()
    node.nodes.add(*nodes)


def text_to_md(text):
    """
    Convert node text to markdown, parsing all of the links.
    :param text: node text
    :return node markdown
    """
    # replace document links in text with markdown
    # replace node links in text with markdown
    md = text

    return md


def text_to_html(text):
    """Convert node text to html."""
    # convert internal links to
    md = text_to_md(text)
    html = markdown.markdown(md)
    return html