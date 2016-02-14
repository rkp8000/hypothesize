from __future__ import division, print_function
import os


def make_directory_if_not_exist(path):
    """
    Make a new directory at the given path if it does not already exist.

    :param path: path to new directory
    """
    if not os.path.exists(path):
        os.makedirs(path)


def update_text_file(node, root):
    """
    Update the text file that corresponds to a given node.
    :param node: node instance
    :return success code
    """
    path = os.path.join(root, node.id)
    return None