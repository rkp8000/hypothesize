# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from django.test import TestCase

import models


# AUTOMATED TESTS:

## document tests

### document processing

class DocumentProcessingTestCase(TestCase):

    def test_author_binding_with_example_author_string(self):

        pass

    def test_author_binding_with_no_author_string(self):

        pass

    def test_author_binding_with_author_string_with_bizarre_characters(self):

        pass

    def test_linked_documents_binding_with_basic_example(self):

        pass

    def test_linked_documents_binding_with_bad_linked_document_string(self):

        pass

    def test_base_key_is_made_correctly_for_standard_document(self):

        pass

    def test_base_key_is_made_correctly_with_no_author_or_year(self):

        pass

    def test_base_key_is_made_correctly_with_weird_author_names(self):

        pass

    def test_base_key_can_be_extracted_from_many_varieties_of_full_key(self):

        # key with no suffix

        # key with suffix

        pass

    def test_key_is_made_correctly_when_there_are_no_documents_with_same_base_key(self):

        pass

    def test_key_is_made_correctly_when_there_are_documents_with_same_base_key(self):

        # when no documents have been deleted

        # when the document with the original base key has been deleted

        # when the document with later conflicting keys have been deleted

        pass

    def test_google_scholar_url_is_built_correctly_with_standard_title(self):

        pass

    def test_google_scholar_url_is_build_correctly_with_title_with_weird_characters(self):

        pass


### document add

class DocumentAddTestCase(TestCase):

    def test_new_basic_document_is_stored_correctly(self):

        pass

    def test_several_documents_with_overlapping_base_keys_are_stored_correctly(self):

        pass


### document change

class DocumentChangeTestCase(TestCase):

    def test_basic_document_changing_works(self):

        pass

    def test_changing_document_base_key_components_doesnt_throw_error(self):

        pass

### document delete

class DocumentDeleteTestCase(TestCase):

    pass

### document search

class DocumentSearchTestCase(TestCase):

    pass

## thread tests

### thread processing

class ThreadProcessingTestCase(TestCase):

    def test_no_errors_when_linking_to_nonexistent_thread_or_document(self):

        pass

    def test_no_errors_when_linking_to_thread_with_weird_characters(self):

        pass

### thread add

class ThreadAddTestCase(TestCase):

    pass

### thread change

class ThreadChangeTestCase(TestCase):

    pass

### thread delete

class ThreadDeleteTestCase(TestCase):

    pass

### thread search

class ThreadSearchTestCase(TestCase):

    pass

## database backup tests

class DatabaseBackupTestCase(TestCase):

    pass

## crossref search tests

class CrossRefSearchTestCase(TestCase):

    pass


# USER INTERFACE TESTS

## document tests

# add two basic documents with different base keys
# doc 1: Smith, John; May, Sally; 1994
# doc 2: Smith, John; Q, Suzie; 1995
# make sure everything is saved correctly

# add new document with weird characters in all fields
# make sure everything is saved correctly and no error is thrown

# add new document with overlapping base key as first document
# Smith, John; Chen, Dizzy; 1994
# make sure document is saved with new key: Smith1994A

# change author and year of second document so that it conflicts with first document base key
# make sure a correct new document base key is generated: Smith1994B

# delete Smith1994A and add a new doc: Smith, John; Johnson, GG; 1994
# make sure it gets saved as Smith1994A

# delete Smith 1994 and add a new doc: Smith, John; Klaus, Johann; 1994
# make sure it gets saved as Smith1994

# add a few more documents
# doc 1: Smith, John; 1998, doc 2: Smith, John 1997
# delete Smith1994A and change Smith1998's year to 1994; make sure it gets saved as Smith1994A
# delete Smith1994 and change Smith1997's year to 1994; make sure it gets saved as Smith1994

#

## thread tests

## database backup tests

## crossref search tests

## messed up my_settings.py tests