# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from django.test import TestCase

import models


# Create your tests here.

class DocumentProcessingTestCase(TestCase):

    def test_get_primary_key_base_works_correctly_on_examples(self):

        pass


class DocumentChangingTestCase(TestCase):

    def test_basic_primary_key_is_created_correctly(self):
        """
        Make sure primary keys for documents combine first author last name and year.
        """

        doc = models.Document(
            publication='Nature',
            title='My title',
            author_text='Johnson, John; Smith, Steve',
            year=2005,
            abstract='This is pretty abstract.',
        )

        doc.save()

        self.assertEqual(doc.id, 'Johnson2005')

    def test_basic_overlapping_primary_keys_are_sorted_correctly(self):
        """
        Make sure if default primary key is already taken, A, B, etc., gets tagged onto new primary key.
        """

        doc_1 = models.Document(
            publication='Nature',
            title='My title',
            author_text='Johnson, John; Smith, Steve',
            year=2005,
            abstract='This is pretty abstract.',
        )

        doc_1.save()

        doc_2 = models.Document(
            publication='Nature Neuroscience',
            title='My title 2',
            author_text='Johnson, John; Smith, Steve',
            year=2005,
            abstract='This is pretty abstract.',
        )

        doc_2.save()

        doc_3 = models.Document(
            publication='Nature Cancer',
            title='My title 3',
            author_text='Johnson, John; Smith, Steve',
            year=2005,
            abstract='This is pretty abstract.',
        )

        doc_3.save()

        self.assertEqual(doc_1.id, 'Johnson2005')
        self.assertEqual(doc_2.id, 'Johnson2005A')
        self.assertEqual(doc_3.id, 'Johnson2005B')

    def test_primary_key_with_nonalpha_first_author_name_is_created_correctly(self):
        """
        Make sure if first author last name has spaces and periods, these are removed in the creation of
        the primary key.
        """

        doc = models.Document(
            publication='Nature',
            title='Some title',
            author_text='van Joseph Jr., Vierden; Doo, Yabadaba',
            year=2010,
            abstract='Beware the realm of abstract thought.'
        )

        doc.save()

        self.assertEqual(doc.id, 'VanJosephJr2010')

    def test_primary_key_with_accented_first_author_name_is_created_correctly(self):
        """
        Make sure that accents, etc., are removed from first author names when creating primary key.
        """

        doc = models.Document(
            publication='Nature',
            title='Some title',
            author_text='van Dübervéck Jr., Vierden; Doo, Yabadaba',
            year=2010,
            abstract='Beware the realm of abstract thought.'
        )

        doc.save()

        self.assertEqual(doc.id, 'VanDuberveckJr2010')

    def test_primary_key_defaults_work_if_name_or_year_not_given(self):
        """
        If the author name is not given, it should be replaced with Unknown. If the year is not given it should
        be replaced with 0000.
        """

        doc = models.Document(
            publication='Nature',
            title='My title',
            author_text='Johnson, John; Smith, Steve',
            abstract='This is pretty abstract.',
        )

        doc.save()

        self.assertEqual(doc.id, 'Johnson0000')

        doc = models.Document(
            publication='Nature',
            title='My title',
            year=2005,
            abstract='This is pretty abstract.',
        )

        doc.save()

        self.assertEqual(doc.id, 'Unknown2005')

    def test_authors_are_extracted_correctly_and_bound_to_document(self):
        """
        Make sure authors get bound to document after being extracted from author text.
        """

        doc = models.Document(
            publication='Nature',
            title='Some title',
            author_text='van Joseph Jr., Vierden; Doo, Yabadaba',
            year=2010,
            abstract='Beware the realm of abstract thought.'
        )

        doc.save()

        bound_author_ids = [author.id for author in doc.authors.all()]
        bound_author_ids_correct = ['van Joseph Jr., Vierden', 'Doo, Yabadaba']

        self.assertEqual(set(bound_author_ids), set(bound_author_ids_correct))

    def test_downstream_documents_are_extracted_correctly_and_bound_to_document(self):

        pass

    def test_downstream_documents_dont_raise_error_if_nonexistent(self):

        pass


class DocumentNodeMarkdownTestCase(TestCase):

    def test_markdown_is_converted_correctly(self):

        pass

    def test_markdown_is_converted_correctly_with_unfound_document(self):

        pass



# document add
## basic
## with weird author names
## with no authors
## with supplement
# document change
## basic
## with weird author names
## with supplement
## rearrange authors
# primary key overlap/absence issues


# node add
# node change
# primary key overlap/absence issues
# node text update with and without save directory declared