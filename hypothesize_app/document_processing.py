from __future__ import division, print_function


def bind_linked_documents(document, document_model):
    """
    Parse a document's linked_documents_text field and bind the relevant documents to it.
    :param document: document
    :param document_model: models.Document
    """

    candidate_pks = [el.strip() for el in document.linked_document_text.split(';')]
    print(candidate_pks)
    linked_documents = [document_model.objects.get(pk=pk) for pk in candidate_pks if pk]


    document.linked_documents.clear()
    document.linked_documents.add(*linked_documents)