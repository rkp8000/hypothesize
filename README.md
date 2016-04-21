# README

Hypothesize is a browser-based software used to manage scientific documents and developing ideas. Most importantly, it features a robust note-taking framework that includes, among other things, wiki-like hyperlinking, note-taking in markdown, and embedded TeX equations (using the wonderful MathJax library).

## Demo video

Insert demo video here.

## To download and start hypothesize on your local computer

1. Clone the repository (`git clone https://github.com/rkp8000/hypothesize2`).
2. Set your username and password in the file 'hypothesize/settings.py'. To do this, uncomment the lines `# BASICAUTH_USERNAME = 'my_username'` and `# BASICAUTH_PASSWORD = 'my_password'` and fill in what you want your username and password to be. You can also store your username and password in the environment variables 'HYPOTHESIZE_USER' and 'HYPOTHESIZE_PATH'. Note: **neither of these passwords are securely stored since they're stored in plain text, so don't use the same password you use for anything important!**
3. *Optional*: create and activate a virtual environment. [Click for instructions on how to do this](https://virtualenv.pypa.io/en/latest/).
4. Install the relevant requirements: `pip install -r requirements.txt`.
5. Make sure you are in the root directory of the repository and make the database migrations: `python manage.py makemigrations`. Then make the database: `python manage.py migrate`. This will create a database called db.sqlite3, which is where all your data will be stored.
6. Start the server: `python manage.py runserver`. This starts the server and connects it to port 8000 by default. To specify a specific port user: `python manage.py runserver host:port`, e.g., `python manage.py runserver 0.0.0.0:9000`.
7. Navigate to 'localhost:8000/hypothesize' to begin (substitute a different port number if you started the server on a different port).
8. Begin sciencing!

## How to use hypothesize

Hypothesize is structured around a network of notes (called "nodes" because of their role in the network) and
scientific documents. Each node is at its heart a text file that can be rendered in a browser. Unlike normal text
files, however, nodes can link to scientific documents, as well as other nodes. Since everything takes place in the
browser, navigating a set of nodes and scientific documents is much like navigating a wiki.

### To start hypothesize

Hypothesize is an application that runs out of a personal web server. This means that to start it you will have to
navigate to the directory using the command line and enter 'python manage.py runserver'.

### To upload a document

Click on 'add new document'. Fill in the form with as much information as you please and click save, including a file
 (e.g., a pdf) if you have it.

  To add authors to the document, enter them in the 'author text' field, separated by semi-colons (e.g.,
 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul').

 The document will be automatically be assigned a *document id* consisting of the word of the author text and the year of publication. For example, if a document has the author text 'Smith, John D.; Winkelmann, Andreas; Erdos, Paul' and the year 2004, the document id will become Smith2004. If the assigned id is already taken, the id will be augmented with a capital letter. E.g., if Smith2004 is taken, the article will be assigned Smith2004A. Each document can be uniquely referenced using its id.

### To create a new node

Nodes are very simple. They have an id, a type, and text. To add a new node, click 'add new node'.

Pick whatever you like for the node id, as long as it hasn't been used before. Like the document ids, a node id
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

### Possible node types

* talk: for taking notes in markdown and TeX during seminars
* meeting notes: for taking notes in a meeting
* document notes: for taking notes on a single document
* document group: for compiling a collection of links to related documents
* node group: for compiling a collection of links to related nodes
* code outline: for outlining code to be used in a project

## Recommendations for making your experience really slick

1. Put the hypothesize directory in a Dropbox folder to sync it across computers.
2. Master your browser's hotkeys (opening links in same tab, opening links in a different tab, navigating between
tabs, etc.).
3. Install 'gleebox' for quickly searching and selecting hyperlinks.

These latter two suggestions make 'hypothesize' almost fully keyboard controllable.

## Running hypothesize on a remote server

One of the wonderful things about a browser-based software.

## Contributing to hypothesize

This project is completely open source and nonprofit and all that good stuff. My motivation for making it was that
I wanted a piece of minimalistic software that allowed me to efficiently navigate through hundreds to thousands of
scientific documents stored on my local machine. I've put enough time into it to make it at least reasonably
functional. That said, I really have no idea what I'm doing. I've tried to follow best practices when possible and
done what I can to make it work, but I would love some more help. Therefore, if you are interested in contributing
to this project you should feel free to open issues and pull requests.

I hope to keep the software as minimalist as possible, but that doesn't mean it can't improve!