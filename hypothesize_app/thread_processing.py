from __future__ import division, print_function, unicode_literals
import os
import re

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from django.core.urlresolvers import reverse
import markdown

DOCUMENT_LINK_PATTERN = r'\[\[(.*?)\]\]'
THREAD_LINK_PATTERN = r'\(\((.*?)\)\)'
DOCUMENT_LINK_PATTERN_FULL = r'\[\[.*?\]\]'
THREAD_LINK_PATTERN_FULL = r'\(\(.*?\)\)'


def make_thread_save_directory(path):
    """
    Make a new directory for saving threads in.
    :param path: path to directory
    """

    if not os.path.exists(path):

        os.makedirs(path)


def get_invalid_key_characters(key):
    """
    Make sure the thread key includes only characters in the thread key character whitelist.
    :param key: thread key
    :return: list of characters not in whitelist
    """

    return set([char for char in key if char not in settings.THREAD_KEY_CHARACTER_WHITELIST])


def check_for_invalid_components(key):
    """
    Make sure all components of the key contain the minimal required characters.
    :param key: thread key
    :return: True if key is invalid, False otherwise
    """

    for c in key.split('/'):

        if c == '':

            return True

        if not any([ch in settings.THREAD_KEY_COMPONENT_REQUIRED_CHARACTERS for ch in c]):

            return True

    return False


def key_is_invalid(key):
    """
    Check if thread key is invalid
    :param key: thread key
    :return: False if key is valid, otherwise invalid key error message
    """

    if not key:

        return '(error: you must provide a key)'

    # make sure key is valid

    invalid_chars = ['"' + char + '"' for char in get_invalid_key_characters(key)]

    if invalid_chars:

        invalid_str = ', '.join(invalid_chars)

        return '(error: the characters {} cannot be used in a key)'.format(invalid_str)

    # make all components of thread key have minimum required characters

    if check_for_invalid_components(key):

        return '(error: that key not valid)'

    return False


def update_text_file(thread):
    """
    Update the text file corresponding to an updated thread.
    :param thread: thread instance
    """

    thread_save_directory = settings.THREAD_SAVE_DIRECTORY

    make_thread_save_directory(thread_save_directory)

    path = os.path.join(thread_save_directory, thread.key)

    if not os.path.exists(os.path.dirname(path)):

        os.makedirs(os.path.dirname(path))

    with open('{}.md'.format(path), 'w') as f:

        f.write(thread.text.encode('utf8'))

    return True


def extract_linked_objects(text, document_model, thread_model):
    """
    Extract all of the linked objects from a thread's text.
    :param text: text
    :param document_model: models.Document
    :param thread_model: models.Thread
    :return: linked documents list, linked threads list
    """

    # extract documents

    document_links = re.findall(DOCUMENT_LINK_PATTERN, text)
    document_keys = [link.split('|')[0].strip() for link in document_links]

    documents = [document_model.objects.filter(key=document_key).first() for document_key in document_keys]
    documents = [document for document in documents if document is not None]

    # extract thread links

    thread_links = re.findall(THREAD_LINK_PATTERN, text)
    thread_keys = [link.split('|')[0].strip() for link in thread_links]

    # get all linked threads, creating them first if they don't exist

    threads = []

    for thread_key in thread_keys:

        # skip if key invalid

        if key_is_invalid(thread_key):

            continue

        # otherwise...

        thread = thread_model.objects.filter(key=thread_key).first()

        if not thread:

            thread = thread_model(key=thread_key)
            thread.save()

        threads.append(thread)

    return documents, threads


def bind_linked_objects(thread, document_model, thread_model):
    """
    Bind all documents and threads linked to by a thread to that thread.

    :param thread: thread
    :param document_model: models.Document
    :param thread_model: models.Thread
    """

    documents, threads = extract_linked_objects(thread.text, document_model, thread_model)

    thread.documents.clear()
    thread.documents.add(*documents)

    thread.threads.clear()

    thread.threads.add(*threads)


def document_link_to_html(match):
    """
    Convert document link pattern to html.
    :param match: regular expression match
    :return: html for link to document
    """

    fragments = match.group()[2:-2].split('|', 1)

    document_key = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:document_detail', args=(document_key.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkkey="document-{}">{}</a>'.format(
        url, document_key, text_to_display)

    return html


def thread_link_to_html(match):
    """
    Convert thread link pattern to html.
    :param match: regular expression match
    :return:
    """

    fragments = match.group()[2:-2].split('|', 1)

    thread_key = fragments[0]

    if len(fragments) == 1:

        text_to_display = fragments[0]

    elif len(fragments) == 2:

        text_to_display = fragments[1]

    try:

        url = reverse('hypothesize_app:thread_detail', args=(thread_key.strip(),))

    except NoReverseMatch:

        url = '#'

    html = '<a href="{}" class="internal-link" data-linkkey="thread-{}">{}</a>'.format(
        url, thread_key, text_to_display)

    return html


def text_to_md(text):
    """
    Convert thread text to markdown, parsing all of the links.
    :param text: thread text
    :return thread markdown
    """

    # replace document links and thread links in text with markdown

    temp = re.compile(DOCUMENT_LINK_PATTERN_FULL).sub(document_link_to_html, text)
    md = re.compile(THREAD_LINK_PATTERN_FULL).sub(thread_link_to_html, temp)

    return md


def text_to_html(text):
    """Convert thread text to html."""

    # convert internal links to html

    md = text_to_md(text)
    html = markdown.markdown(md)

    return html


def make_tab_complete_options(document_model, thread_model):
    """
    Generate a list of things that can be tab completed.
    :param document_model: models.Document,
    :param thread_model: models.Thread
    :return list of strings for tab completion
    """

    document_strings = [str(doc_key) for doc_key in document_model.objects.values_list('key', flat=True)]
    thread_strings = [str(thread_key) for thread_key in thread_model.objects.values_list('key', flat=True)]

    return document_strings + thread_strings