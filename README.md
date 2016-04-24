# README

*hypothesize* is a minimalistic academic note-taking application designed to keep your notes and ideas as close to the corpus of published literature as possible. To this end, it is based on the principle that referencing journal articles in notes and accessing them at a later time should require no more than a single click or a couple of keystrokes. Check out the video below to view *hypothesize* in action.

### Demo video

Insert demo video here.

### How *hypothesize* works

Structurally, *hypothesize* is nothing more than a glorified wiki. The *pages* that *hypothesize* links together, however, come in two varieties: documents and nodes. Documents are published journal articles, etc., usually represented with some meta information (title, authors, abstract, ...) and either a pdf file or a link to an external website. Nodes, on the other hand (named for their role in a network), are arbitrary text files, except that they can contain hyperlinks to documents as well as other nodes. Importantly, each document and each node is assigned a unique, unchanging ID. When composing a node, this allows unambiguous referencing of documents and other nodes through a simple, wiki-inspired syntax (e.g., "[[Smith1988]]" would link to journal article with the ID "Smith1988"). Each node can link to many documents and nodes, and each
document and node can be linked to by many nodes. This allows a much more flexible organization of ideas and
literature than, say, organizing documents in a hierarchy of directories, tagging documents with specific tags, or
attaching specific notes to specific documents.

You interface with *hypothesize* through the web browser. Because of this, you should find navigating its components quite natural and intuitive. For example, hyperlinks to nodes and documents are quite literally hyperlinks. Further, when composing nodes you can use all the standard markdown syntax, which gets rendered as cleanly formatted html by the browser, and you can include inline and block equations written in TeX by surrounding them with "$..$" (inline) or "$$...$$" (block).

*hypothesize* uses the web browser as its interface because it is powered by a local web server. Since the server is local, no internet connection is required to use it. However, because it is powered by a web server, using it across a network is quite natural. Thus, it is very easy to have *hypothesize* run on one computer while you access it on another. In this case it becomes automatically accessible by any mobile device with access to the internet, without installing any additional
 apps.

### List of advantages of using *hypothesize* to manage ideas and literature

* Allows flexible, wiki-like organization of ideas and published documents.
* Allows efficient referencing of documents and other nodes, and efficient navigating of the resulting wiki-like
network of documents and nodes. In fact, hypothesize is fully keyboard navigable (excepting a couple of bugs that are
 being ironed out).
* Is easily accessible remotely or on mobile devices.
* Plays nicely with other software. For example, you can keep the entire application and all your documents and nodes
 in a version-controlled Dropbox folder (note, however, that typical version-control systems are not ideal for storing
  large collections of pdfs, so those should probably be backed up in a different way).
* Uses a web browser as its interface. This allows it to take advantage of all the technologies built into a web
browser. One browser extension, for example, that makes *hypothesize* super
slick is *gleebox*, which enables lightning fast keyboard navigation among hyperlinks on a webpage. The browser also makes it very easy for other users to customize their experience through extra css and javascript.
* Is free and open source and not trying to make any money!

### To download and start hypothesize on your local computer

1. Clone the repository (`git clone https://github.com/rkp8000/hypothesize2`).
2. Set your username and password in the file 'hypothesize/settings.py'. To do this, uncomment the lines `# BASICAUTH_USERNAME = 'my_username'` and `# BASICAUTH_PASSWORD = 'my_password'` and fill in what you want your username and password to be. You can also store your username and password in the environment variables 'HYPOTHESIZE_USER' and 'HYPOTHESIZE_PATH'. Note: **neither of these passwords are securely stored since they're stored in plain text, so don't use the same password you use for anything important!**
3. *Optional*: create and activate a virtual environment. [Click for instructions on how to do this](https://virtualenv.pypa.io/en/latest/).
4. Install the relevant requirements: `pip install -r requirements.txt`.
5. Make sure you are in the root directory of the repository and make the database migrations: `python manage.py makemigrations`. Then make the database: `python manage.py migrate`. This will create a database called db.sqlite3, which is where all your data will be stored.
6. Start the server: `python manage.py runserver`. This starts the server and connects it to port 8000 by default. To specify a specific port user: `python manage.py runserver host:port`, e.g., `python manage.py runserver 0.0.0.0:9000`.
7. Navigate to 'localhost:8000/hypothesize' to begin (substitute a different port number if you started the server on a different port). Here you will be asked to enter a username and password. The defaults are 'user' and 'pass',
respectively, but these can be changed in the file hypothesize/settings.py.
8. Begin sciencing!

### How to upload a document

Click on 'add new document'. Fill in the form with as much information as you please and click save, including a file
 (e.g., a pdf) if you have it.

  To add authors to the document, enter them in the 'author text' field, separated by semi-colons (e.g.,
 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul').

 The document will be automatically be assigned a *document ID* consisting of the first word of the author text and the year of publication. For example, if a document has the author text 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul' and the year 2004, the document ID will become Smith2004. If the assigned ID is already taken, the ID will be augmented with a capital letter. E.g., if Smith2004 is taken, the article will be assigned Smith2004A. Each document can be uniquely referenced using its ID.

### How to create a new node

Nodes are very simple. They have an ID, a type, and text. To add a new node, click 'add new node'.

Pick whatever you like for the node ID, as long as it hasn't been used before. Like the document ids, a node id
allows you to uniquely reference the node.

Node types help you organize your nodes by category. For example, you might have a node type for talks/lectures, a
node type for notes about a specific article, a node type for algorithm details, etc. To add a new node type, click
on 'edit node types'. See below for full list of recommended node types.

The rest of the node is simply text that gets rendered to html upon saving. Node text is fully markdown compatible.
For example, you can specify a size-3 header with '### my header', italics with '*my text in italics*', etc. For a
full catalog of markdown syntax, see ...

Importantly, in addition to markdown, there also exists simple syntax for linking to documents and other nodes.
Document links are specified as '[[Smith2004]]', etc. Node links are specified as '((my other node))'. If you can't
quite remember the ids of the documents or nodes, hypothesize will help out a little. Once the node is saved, the
links will be rendered as hyperlinks.

You can also include equations in your nodes by surrounding them with '$...$' for inline equations or '$$...$$' for
equations that get their own line. These will be typeset using the MathJax library, which requires an internet
connection.

In addition to being store in a database, nodes are also stored in a folder called 'nodes', located in the
*hypothesize* directory you downloaded. This way you can version control your work more easily.

### Examples of useful node types

* talk: for taking notes in markdown and TeX during seminars
* meeting notes: for taking notes in a meeting
* document notes: for taking notes on a single document
* document group: for compiling a collection of links to related documents
* node group: for compiling a collection of links to related nodes
* code outline: for outlining code to be used in a project

## Running hypothesize on a remote server

Since hypothesize is powered by a web server, this means it can take advantage of all the technologies associated
with web servers, the most important being the ability to run it on one computer while accessing it on another. Doing
 this is super easy. On the computer on which you wish to run hypothesize (for example a computer in your lab that is
  always on, or on some other remote server -- call this the host computer), simply `cd` into the directory and at the
  command prompt enter `python manage.py runserver 0.0.0.0:8000` (replacing "8000" by whichever port you'd like to run it on, though 8000 is a
  good default). Then, on any computer with a web browser that's connected to the internet, simply navigate to the ip
   of the host computer, followed by the port number and '/hypothesize'. E.g., if the host's IP is d-121-55-191-111
   .mydomain.com, navigate to d-121-55-191-111.mydomain.com:8000/hypothesize.

## Contributing to hypothesize

This project is completely open source and nonprofit and all that good stuff. My motivation for making it was that
I wanted a piece of minimalistic software that allowed me to efficiently navigate through hundreds to thousands of
scientific documents stored on my local machine, as well as my notes about those documents or about other projects.
I've put enough time into it
 to make it at least reasonably
functional. That said, I really have no idea what I'm doing. I've tried to follow best practices when possible and
done what I can to make it work, but I would love some more help. Therefore, if you are interested in contributing
to this project you should feel free to open issues and pull requests.