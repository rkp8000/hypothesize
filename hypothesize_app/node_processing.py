from __future__ import division, print_function
import os


def make_node_save_directory(path):
    """
    Make a new directory for saving nodes in.
    :param path: path to directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


def update_text_file(node, settings):
    """
    Update the text file corresponding to an updated node.
    :param node: node instance
    :param settings: models.Setting
    """
    node_save_directory = settings.objects.get(pk='NODE_SAVE_DIRECTORY').value
    path = os.path.join(node_save_directory, node.id)
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    with open('{}.md'.format(path), 'w') as f:
        f.write(node.text)