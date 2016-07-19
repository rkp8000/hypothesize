# README

*hypothesize* is a combined note-taking and reference-management app designed for the efficient synthesis of new ideas informed by scholarly literature. Its wiki-like structure enables you to flexibly organize and cross-reference your notes and journal articles and to nimbly navigate among them without ever losing track of where you came from. *hypothesize* is free to all to download and welcomes contributions from those interested in developing it further.
were..."

### To download and start hypothesize on your local computer

1. Clone the repository onto your local computer (`git clone https://github.com/rkp8000/hypothesize2`) and cd into it (`cd hypothesize2`).
2. Create a virtual environment: `virtualenv env`. (Note that this may give you problems if you have the current version of [conda](http://conda.pydata.org/docs/) installed, in which case you should make a virtual environment using conda itself.)
3. Activate the virtual environment (`source env/bin/activate`) and install the relevant requirements: `pip install -r requirements.txt`.
4. Start the server: `python manage.py runserver`. 
5. Open any web browser and navigate to "localhost:8000/hypothesize".

### Basic features

*hypothesize* is founded on a few basic principles.

#### Documents and topics

In *hypothesize* there are two kinds of objects: *documents* and *topics*. Documents are typically published journal articles or reports, and topics are text files for your notes and ideas that get rendered into simple webpages when you save them.

#### Keys

So that they can be unambiguously referenced, each topic and each document must have its own key, or unique label. Topic keys are simply the title of the topic's text file and document keys are the last name of first author combined with the publication year (e.g., Shannon1948). 

#### Linking topics and documents

Within the text of a topic you can reference documents *inline* by surrounding the document key by double square brackets, (e.g., "...it was shown in [[Shannon1948]] that a logarithmic measure of information was a very useful quantity..."). 

When you save the topic to render it as a webpage, [[Shannon1948]] becomes a hyperlink that when clicked expands into a small paragraph containing the metadata for the article (such as its publication and abstract) and a link to the primary source (such as a local pdf or an external website). In this way, one topic can reference many documents and one document can be referenced by many topics (and whenever a document's metadata is viewed it is accompanied by links to all the topics that reference it). 

Topics can also reference other topics by surrounding the topic key by double parentheses (e.g., "...information theory and ((dynamical systems theory)) became major players in theoretical neuroscience..."). When a topic reference is saved and rendered it similarly becomes a hyperlink that when clicked opens up the referenced topic inline with the original one.


### Advanced features

6. This starts the server and connects it to port 8000 by default. To specify a specific port user: `python manage.py runserver host:port`, e.g., `python manage.py runserver 0.0.0.0:9000`.
7. Navigate to 'localhost:8000/hypothesize' to begin (substitute a different port number if you started the server on a different port). Here you will be asked to enter a username and password. The defaults are 'user' and 'pass', respectively, but these can be changed in the file hypothesize/settings.py.
8. Begin sciencing!

### How to upload a document

Click on 'add new document'. Fill in the form with as much information as you please and click save, including a file
 (e.g., a pdf) if you have it.

  To add authors to the document, enter them in the 'author text' field, separated by semi-colons (e.g.,
 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul').

 The document will be automatically be assigned a *document ID* consisting of the first word of the author text and the year of publication. For example, if a document has the author text 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul' and the year 2004, the document ID will become Smith2004. If the assigned ID is already taken, the ID will be augmented with a capital letter. E.g., if Smith2004 is taken, the article will be assigned Smith2004A. Each document can be uniquely referenced using its ID.

### How to create a new node

Nodes are very simple. They have an ID, a type, and text. To add a new node, click 'add new node'.

Pick whatever you like for the node ID, as long as it hasn't been used before. Like the document ids, a node id allows you to uniquely reference the node.

Node types help you organize your nodes by category. For example, you might have a node type for talks/lectures, a node type for notes about a specific article, a node type for algorithm details, etc. To add a new node type, click on 'edit node types'. See below for full list of recommended node types.

The rest of the node is simply text that gets rendered to html upon saving. Node text is fully markdown compatible. For example, you can specify a size-3 header with '### my header', italics with '*my text in italics*', etc. For a full catalog of markdown syntax, see ...

Importantly, in addition to markdown, there also exists simple syntax for linking to documents and other nodes. Document links are specified as '[[Smith2004]]', etc. Node links are specified as '((my other node))'. If you can't quite remember the ids of the documents or nodes, hypothesize will help out a little. Once the node is saved, the links will be rendered as hyperlinks.

You can also include equations in your nodes by surrounding them with '$...$' for inline equations or '$$...$$' for equations that get their own line. These will be typeset using the MathJax library, which requires an internet connection.

In addition to being store in a database, nodes are also stored in a folder called 'nodes', located in the *hypothesize* directory you downloaded. This way you can version control your work more easily.

### Examples of useful node types

* talk: for taking notes in markdown and TeX during seminars
* meeting notes: for taking notes in a meeting
* document notes: for taking notes on a single document
* document group: for compiling a collection of links to related documents
* node group: for compiling a collection of links to related nodes
* code outline: for outlining code to be used in a project

## Running hypothesize on a remote server

Since hypothesize is powered by a web server, this means it can take advantage of all the technologies associated with web servers, the most important being the ability to run it on one computer while accessing it on another. Doing this is super easy. On the computer on which you wish to run hypothesize (for example a computer in your lab that is always on, or on some other remote server -- call this the host computer), simply `cd` into the directory and at the command prompt enter `python manage.py runserver 0.0.0.0:8000` (replacing "8000" by whichever port you'd like to run it on, though 8000 is a good default). Then, on any computer with a web browser that's connected to the internet, simply navigate to the ip of the host computer, followed by the port number and '/hypothesize'. E.g., if the host's IP is d-121-55-191-111.mydomain.com, navigate to d-121-55-191-111.mydomain.com:8000/hypothesize.

## Contributing to hypothesize

This project is completely open source and nonprofit and all that good stuff. My motivation for making it was that I wanted a piece of minimalistic software that allowed me to efficiently navigate through hundreds to thousands of scientific documents stored on my local machine, as well as my notes about those documents or about other projects. I've put enough time into it to make it at least reasonably functional. That said, I really have no idea what I'm doing. I've tried to follow best practices when possible and done what I can to make it work, but I would love some more help. Therefore, if you are interested in contributing to this project you should feel free to open issues and pull requests.
