"""
This script uploads all of the data and files from the old database into the new.
"""
from __future__ import division, print_function
from django.core.files import File
import os
import sqlite3 as lite
import traceback

from hypothesize_app import models

MAX_DOC_UPLOADS = 5
MAX_NODE_UPLOADS = 5
NODE_TYPES = {
    'document group': 'Group of documents.',
    'node group': 'Group of nodes.',
    'talk': 'Talk.',
}
NODE_TYPE_ID_CONVERSIONS = {
    'article_group': 'document group',
    'node_group': 'node group',
    'talk_notes': 'talk',
}
NUM_TO_ALPHA = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']


class Document(object):
    """
    :params row: sqlite3 row result

    "row" should be a tuple with the following elements: (id, title, journal, year, abstract, weblink, last_viewed, uploaded)
    """

    def __init__(self, row):
        self.id = row[0]
        self.title = row[1]
        self.journal = row[2]
        self.year = row[3]
        self.abstract = row[4]
        self.web_link = row[5]
        self.last_viewed = row[6]
        self.uploaded = row[7]

        assert len(self.id) > 0

        # change id formatting if underscores are present
        if self.id[-2] == '_':
            suffix = NUM_TO_ALPHA[int(self.id[-1])]
            self.id = self.id[:-2] + suffix

        self.doc = models.Document(
            id=self.id,
            title=self.title,
            publication=self.journal,
            year=self.year,
            abstract=self.abstract,
            web_link=self.web_link,
            last_viewed=self.last_viewed,
            uploaded=self.uploaded,
        )

    def attach_file(self, file_path):
        """
        Attach a file (typically a pdf).
        :param file_path: path to file
        """
        file_name = os.path.basename(file_path)

        with open(file_path) as f:
            self.doc.file.save(file_name, File(f), save=False)

    def upload_to_new_db(self):
        """
        Upload the document to the db.
        """
        self.doc.save()


class NodeType(object):
    """
    :params row: sqlite3 row

    "row" should be a tuple containing the following elements: (id, description)
    """

    def __init__(self, id, description):
        self.id = id
        self.description = description
        self.node_type = models.NodeType(
            id=self.id,
            description=self.description,
        )

    def upload_to_new_db(self):
        """
        Upload the node type to the new db.
        """
        self.node_type.save()


class Node(object):
    """
    :params row: sqlite3 row

    "row" should be a tuple containing the following elements: (id, type_id, text, last_viewed)
    """

    def __init__(self, row):
        self.id = row[0]
        self.text = row[1]
        self.last_viewed = row[2]

        self.node = models.Node(
            id=self.id,
            text=self.text,
            last_viewed=self.last_viewed,
        )

        self.type_id = NODE_TYPE_ID_CONVERSIONS.get(row[3], None)

        if self.type_id is not None:
            try:
                self.node.type = models.NodeType.object.get(pk=self.type_id)
            except Exception, e:
                print('Error assigning node type to node: "{}"'.format(e))

    def upload_to_new_db(self):
        """
        Upload the node to the new db.
        """
        self.node.save()


def migrate_old_database(db_path):

    messages_success = []
    messages_error = []
    # open database connection
    try:
        con = lite.connect(db_path)
    except Exception, e:
        messages_error.append('Connection error: "{}"'.format(e))

    # upload all documents
    try:
        with con:

            try:
                cur = con.cursor()
                cur.execute('SELECT id, title, journal, year, abstract, web_link, last_viewed, uploaded, file, '
                            'external_file_path FROM hypothesize_app_article')
            except Exception, e:
                messages_error.append('Cursor/SELECT error: "{}"'.format(e))
                messages_error.append(traceback.format_exc())

            doc_ctr = 0

            for row in cur.fetchall():
                doc_ctr += 1
                if doc_ctr >= MAX_DOC_UPLOADS:
                    break

                try:
                    doc = Document(row[:-2])

                    # open file
                    file_path = row[-2]
                    external_file_path = row[-1]

                    if file_path:
                        dir_name = os.path.dirname(db_path)
                        full_path = os.path.join(dir_name, 'media', file_path)
                    elif external_file_path:
                        full_path = external_file_path[7:]
                    else:
                        full_path = None

                    # attach file to document
                    if full_path is not None:
                        full_path = full_path.replace('%20', ' ')
                        doc.attach_file(full_path)

                    doc.upload_to_new_db()

                    messages_success.append('Document upload successful: "{}"'.format(doc.doc.id))

                except Exception, e:
                    messages_error.append('Document upload error: "{}"'.format(e))
                    messages_error.append(traceback.format_exc().replace('\n', '<br />'))

    except Exception, e:
        messages_error.append('Connection error: "{}"'.format(e))
        messages_error.append(traceback.format_exc())

    # add certain node types
    for id, description in NODE_TYPES.items():
        try:
            node_type = NodeType(id=id, description=description)
            node_type.upload_to_new_db()

            messages_success.append('Node type upload successful: "{}"'.format(node_type.id))
        except Exception, e:
            messages_error.append('Node type upload error: "{}"'.format(e))
            messages_error.append(traceback.format_exc())

    # upload all nodes
    try:
        with con:

            try:
                cur = con.cursor()
                cur.execute('SELECT id, text, last_viewed, type_id FROM hypothesize_app_node')
            except Exception, e:
                messages_error.append('Cursor/SELECT error: "{}"'.format(e))
                messages_error.append(traceback.format_exc())

            node_ctr = 0

            for row in cur.fetchall():
                node_ctr += 1
                if node_ctr >= MAX_NODE_UPLOADS:
                    break

                try:
                    node = Node(row)

                    node.upload_to_new_db()

                    messages_success.append('Node upload successful: "{}"'.format(node.node.id))

                except Exception, e:
                    messages_error.append('Node upload error: "{}"'.format(e))
                    messages_error.append(traceback.format_exc())

    except Exception, e:
        messages_error.append('Connection error: "{}"'.format(e))
        messages_error.append(traceback.format_exc())

    return messages_success, messages_error