from __future__ import division, print_function, unicode_literals
import os
import re

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
import markdown

DOCUMENT_LINK_PATTERN = r'\[\[(.*?)\]\]'
TOPIC_LINK_PATTERN = r'\(\((.*?)\)\)'
DOCUMENT_LINK_PATTERN_FULL = r'\[\[.*?\]\]'
TOPIC_LINK_PATTERN_FULL = r'\(\(.*?\)\)'


def make_topic_save_directory(path):
    """
    Make a new directory for saving topics in.
    :param path: path to directory
    """

    if not os.path.exists(path):

        os.makedirs(path)


def update_text_file(topic):
    """
    Update the text file corresponding to an updated topic.
    :param topic: topic instance
    """

    topic_save_directory = settings.TOPIC_SAVE_DIRECTORY

    make_topic_save_directory(topic_save_directory)

    path = os.path.join(topic_save_directory, topic.id)

    if not os.path.exists(os.path.dirname(path)):

        os.makedirs(os.path.dirname(path))

    with open('{}.md'.format(path), 'w') as f:

        f.write(topic.text)

    return True


def extract_linked_objects(text, document_model, topic_model):
    """
    Extract all of the linked objects from a topic's text.
    :param text: text
    :param document_model: models.Document
    :param topic_model: models.Topic
    :return: linked documents list, linked topics list
    """

    # extract documents

    document_links = re.findall(DOCUMENT_LINK_PATTERN, text)
    document_ids = [link.split('|')[0].strip() for link in document_links]

    documents = [document_model.objects.filter(id=document_id).first() for document_id in document_ids]
    documents = [document for document in documents if document is not None]

    # extract topic links

    topic_links = re.findall(TOPIC_LINK_PATTERN, text)
    topic_ids = [link.split('|')[0].strip() for link in topic_links]

    topics = [topic_model.objects.filter(id=topic_id).first() for topic_id in topic_ids]
    topics = [topic for topic in topics if topic is not None]

    return documents, topics


def bind_linked_objects(topic, document_model, topic_model):
    """
    Bind all of the documents and topics that a topic links to itself in the database.

    :param topic: topic
    :param document_model: models.Document
    :param topic_model: models.Topic
    """

    documents, topics = extract_linked_objects(topic.text, document_model, topic_model)

    topic.documents.clear()
    topic.documents.add(*documents)

    topic.topics.clear()
    topic.topics.add(*topics)


def document_link_to_html(match):
    """
    Convert document link pattern to html.
    :param match: regular expression match
    :return: html for link to document
    """

    fragments = match.group()[2:-2].split('|', 1)

    document_id = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:document_detail', args=(document_id.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkpk="document-{}">{}</a>'.format(
        url, document_id, text_to_display)

    return html


def topic_link_to_html(match):
    """
    Convert topic link pattern to html.
    :param match: regular expression match
    :return:
    """

    fragments = match.group()[2:-2].split('|', 1)

    topic_id = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:topic_detail', args=(topic_id.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkpk="topic-{}">{}</a>'.format(
        url, topic_id, text_to_display)

    return html


def text_to_md(text):
    """
    Convert topic text to markdown, parsing all of the links.
    :param text: topic text
    :return topic markdown
    """

    # replace document links and topic links in text with markdown

    temp = re.compile(DOCUMENT_LINK_PATTERN_FULL).sub(document_link_to_html, text)

    md = re.compile(TOPIC_LINK_PATTERN_FULL).sub(topic_link_to_html, temp)

    return md


def text_to_html(text):
    """Convert topic text to html."""

    # convert internal links to html

    md = text_to_md(text)
    html = markdown.markdown(md)

    return html


def make_tab_complete_options(document_model, topic_model):
    """
    Generate a list of things that can be tab completed.
    :param document_model: models.Document,
    :param topic_model: models.Topic
    :return list of strings for tab completion
    """

    document_strings = [str(doc_id) for doc_id in document_model.objects.values_list('id', flat=True)]
    topic_strings = [str(topic_id) for topic_id in topic_model.objects.values_list('id', flat=True)]

    return document_strings + topic_strings