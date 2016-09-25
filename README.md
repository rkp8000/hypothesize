# README

*hypothesize* is a combined note-taking and reference-management app designed for the efficient synthesis of new ideas informed by scholarly literature. Its wiki-like structure enables you to flexibly organize and cross-reference your notes and journal articles and to nimbly navigate among them without ever losing track of where you came from. *hypothesize* is free to all to download and welcomes contributions from those interested in developing it further.

## To download and start hypothesize on your local computer

1. Clone the repository onto your local computer (`git clone https://github.com/rkp8000/hypothesize2`) and cd into it (`cd hypothesize2`).
2. Create a virtual environment: `virtualenv env`. (Note that this may give you problems if you have the current version of [conda](http://conda.pydata.org/docs/) installed, in which case you should make a virtual environment using conda itself.)
3. Activate the virtual environment (`source env/bin/activate`) and install the relevant requirements: `pip install -r requirements.txt`.
4. Start the server: `python manage.py runserver`. 
5. Open any web browser and navigate to "localhost:8000/hypothesize".
6. To stop *hypothesize* enter CTRL + c in the terminal window in which the server is running.

## Basic usage

### Documents and threads

*hypothesize* uses two kinds of objects: *documents* and *threads*. Documents are typically published journal articles or reports, and threads are text files for your notes and organization that get rendered into simple webpages when you save them. You can search, browse, or add new documents on the *document search page* and you can search, browse, or add new threads on the *thread search page*.

![Alt Text](https://github.com/rkp8000/hypothesize_resources/blob/master/tutorial/rec1.gif?raw=true)

### Keys

So that they can be unambiguously referenced, each thread and each document must have its own key, or unique label. Thread keys are simply the title of the thread's text file and document keys are the last name of first author combined with the publication year (e.g., Shannon1948). 

### Linking threads and documents

Within the text of a thread you can reference documents *inline* by surrounding the document key by double square brackets, e.g., "...it was shown in [[Shannon1948]] that a logarithmic measure of information was a very useful quantity...". In this way, one thread can reference many documents and one document can be referenced by many threads.

When you save the thread to render it as a webpage, "[[Shannon1948]]" becomes a hyperlink that when clicked expands into a small inline box containing the metadata for the article (such as its publication and abstract) and a link to the primary source (such as a local pdf or an external website). 

Threads can also reference other threads using double parentheses e.g., "...information theory and ((dynamical systems theory)) became major players in theoretical neuroscience...". When you edit a thread and start typing out the key for a document or thread reference, *hypothesize* will try to guess which key you're thinking of so you don't have to remember the exact spelling or phrasing. When a thread reference is saved and rendered it similarly becomes a hyperlink that when clicked opens up the referenced thread inline with the original one.

Inline navigation through your wiki-like network of threads and documents makes it so you never have to switch or reload tabs when moving among related objects, so you never lose track of where you are.

### Thread flexibility

Because threads are just text files with inline links to documents and other threads, they are extremely flexible. For example, you can use a thread as notes about a journal article in relation to other articles, as notes about several articles, as simply a list of related articles, as notes about a general idea that references journal articles or other ideas, as notes about a talk or seminar, as a list of related threads, as a list of talks or seminars (e.g., when attending a conference), as an outline for code, or as anything else you might think of.

In addition to threads containing inline links to other documents and threads, documents and threads also always show the other threads that link *to* them, so that you can easily navigate upstream as well.

## Advanced usage

### Document creation

One nice thing about hypothesize is that when adding a new document you don't have to type in all the metadata yourself. If you instead just type in a guess at the title you can click "attempt to fill in article metadata using CrossRef" to fill in the rest of the form. Note, however, that this does not fill in the abstract (work on this is in progress) or the PDF file.

Although this wasn't mentioned above, documents can also link to other documents. To create a link between two documents, simply edit the document that is doing the linking and type in a list of document keys that you want it to link to in the "downstream documents" text box. As before, you don't need to know the whole key; *hypothesize* will try to guess the rest you've entered. When you view a document, you will see the documents that that document links to, as well as all the documents that link to it.

### Advanced thread editing

When linking to documents or threads from within a thread, if you do not want the text of the rendered hyperlink to be the document/thread key, you can replace it with anything you like using the ```|```. For example, ```[[Shannon1948|Shannon's paper on information theory]]``` would get rendered as [Shannon's paper on information theory](https://github.com/rkp8000/hypothesize) but would link to the document with key "Shannon1948". Similarly, ```((dynamical systems theory|another mathematical perspective))``` would get rendered as [another mathematical perspective](https://github.com/rkp8000/hypothesize) but would link to the thread with the key "dynamical systems theory".

In addition to the special syntax for linking to documents and threads, the text of a thread admits numerous other syntactical shortcuts. Most notably, threads are completely Markdown compatible. For instance: ```*this text in italics*``` gets rendered as *this text in italics* and ```[my link](https://github.com/rkp8000/hypothesize)``` gets rendered as [my link](https://github.com/rkp8000/hypothesize). Check out this [Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet) to see what else you can do with Markdown.

You can also include TeX equations in a thread's text file, which get nicely typeset when you save and render the thread. You can include an inline equation by surrounding it with single $'s and a block equation by surrounding it with $$'s. For instance, ```$y = \sum_i x_i$``` would get rendered inline and ```$$y = \sum_i x_i$$``` would get rendered in its own block. At this point, equation typesetting will only work if you have an internet connection, since it is done by remotely loading the [MathJax](https://www.mathjax.org) javascript library.

### Backing up your database and restoring from a backup

You can backup your database by clicking the "back up database" link on either the document or thread search page. By default, database backups will get stored inside a directory called "backups" that lives inside the main *hypothesize* folder but you can specify an alternative path by editing the ```DATABASE_BACKUP_DIRECTORY``` setting in the file ```hypothesize/my_settings.py``` to path on your computer. Note that backing up the database in this way does not back up the files associated with documents, since they will generally take up a significant amount of memory. It only backs up all of your document metadata and all of your threads.

To restore from an old backup, simply copy the backup file that you want to restore to the main hypothesize directory and change its name to ```db.sqlite3``` (you will have to remove the old one first, so be sure you know what you're doing!).

### Setting a username and password

You can set up simple authentication for hypothesize (so that you have to enter a username and password in order to access your documents and threads) by changing the ```USERNAME``` and ```PASSWORD``` settings in ```hypothesize/my_settings.py```. Note that this is not at all secure at this point, since the username and password are stored as plain text, so it is not advisable to use it to protect any confidential information.

### Running hypothesize on a different port

By default *hypothesize* runs on port 8000. This is why you navigate to "localhost:*8000*/hypothesize" to access the application's browser interface. If you don't wish to use that port you can specify another when you start the server. For example, ```python manage.py runserver localhost:8080``` will run *hypothesize* on port 8080 and you can access the application by navigating to "localhost:8080/hypothesize" in your web browser.

### Running hypothesize on a remote server

Running *hypothesize* on a remote server is also very easy. On the host computer (e.g., a lab computer that remains on and has a static IP address) simply start *hypothesize* using ```python manage.py runserver 0.0.0.0:8000```. Then, on any computer with a web browser that's connected to the internet, simply navigate to the ip of the host computer, followed by the port number and '/hypothesize'. E.g., if the host is usually accessed through "mycomputer.myuniversity.edu", navigate to "mycomputer.myuniversity.edu:8000/hypothesize".

### Keyboard navigability

*hypothesize* is mostly keyboard navigable. One of its future goals is to be entirely keyboard navigable, so that editing notes and searching through articles can be done as efficiently as possible. In order to get the most out of *hypothesize* in its current incarnation, I recommend installing the [GleeBox](http://thegleebox.com) browser extension, which allows you to quickly jump between a website's hyperlinks without having to lift your hands from the keyboard.

# Contributing to hypothesize

This project is completely open source and free for all to use and modify. My motivation for making it was that I wanted a piece of minimalistic software that allowed me to efficiently navigate through thousands of scientific documents stored on my local machine, as well as my notes about those documents or about other projects. I've tried to make it at least reasonably functional and to follow best practices when possible, but that said, I really have very little idea what I'm doing, and I would love some more help. Therefore, if you are interested in contributing to this project you should feel free to open issues and pull requests.

Happy sciencing!
