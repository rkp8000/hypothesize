"""
This script uploads all of the data and files from the old database into the new.
"""
from __future__ import division, print_function
from django.core.files import File
import os
import sqlite3 as lite

from hypothesize_app import models

MAX_DOC_UPLOADS = 5
MAX_NODE_UPLOADS = 0
NODE_TYPES_TO_UPLOAD = {
    'talk_notes': 'talk_notes',
    'node_group': 'node_group',
    'article_group': 'document_group'
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

    def __init__(self, row):
        self.id = row[0]
        self.description = row[1]

    def upload_to_new_db(self):
        """
        Upload the node type to the new db.
        """
        try:
            node_type = models.Document(
                id=self.id,
                description=self.description,
            )
            node_type.save()
        except Exception, e:
            print(
                'The following error occurred when uploading NodeType "{}": "{}"'.format(
                    self.id, e
                )
            )


class Node(object):
    """
    :params row: sqlite3 row

    "row" should be a tuple containing the following elements: (id, type_id, text, last_viewed)
    """

    def __init__(self, row):
        self.id = row[0]
        self.type_id = row[1]
        self.text = row[2]
        self.last_viewed = row[3]

    def upload_to_new_db(self):
        """
        Upload the node to the new db.
        """

        try:
            node_type = models.NodeType.object.get(pk=self.type_id)
            node = models.Node(
                id=self.id,
                type=node_type,
                text=self.text,
                last_viewed=self.last_viewed,
            )
            node.save()

        except Exception, e:
            print(
                'The following error occurred when uploading Node "{}": "{}"'.format(
                    self.id, e
                )
            )


def migrate_old_database(db_path):

    messages = []
    # open database connection
    try:
        con = lite.connect(db_path)
    except Exception, e:
        messages.append('Connection error: "{}"'.format(e))

    # upload all documents
    try:
        with con:

            try:
                cur = con.cursor()
                cur.execute('SELECT id, title, journal, year, abstract, web_link, last_viewed, uploaded, file, '
                            'external_file_path FROM hypothesize_app_article')
            except Exception, e:
                messages.append('Cursor/SELECT error: "{}"'.format(e))

            doc_ctr = 0

            for row in cur.fetchall():
                doc_ctr += 1

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
                except Exception, e:
                    messages.append('Document upload error: "{}"'.format(e))

                if doc_ctr >= MAX_DOC_UPLOADS:
                    break

    except Exception, e:
        messages.append('Connection error: "{}"'.format(e))

    return messages

    # upload certain node types

    # upload all nodes