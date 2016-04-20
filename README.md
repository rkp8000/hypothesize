# README

Hypothesize is a browser-based software used to manage scientific documents and developing ideas. Most importantly, it features a robust note-taking framework that includes, among other things, wiki-like hyperlinking, note-taking in markdown, and embedded equations in TeX.

### To download and run hypothesize on your local computer

1. Clone the repository (`git clone https://github.com/rkp8000/hypothesize2').
2. Set your username and password in the file 'hypothesize/settings.py'. To do this, uncomment the lines `# BASICAUTH_USERNAME = 'my_username'` and `# BASICAUTH_PASSWORD = 'my_password'` and fill in what you want your username and password to be. You can also store your username and password in the environment variables 'HYPOTHESIZE_USER' and 'HYPOTHESIZE_PATH'. Note: **neither of these passwords are securely stored since they're stored in plain text, so don't use the same password you use for anything important!**
3. *Optional*: create and activate a virtual environment. [Click for instructions on how to do this](https://virtualenv.pypa.io/en/latest/).
4. Install the relevant requirements: `pip install -r requirements.txt`.
5. Make sure you are in the root directory of the repository and make the database migrations: `python manage.py makemigrations`. Then make the database: `python manage.py migrate`. This will create a database called db.sqlite3, which is where all your data will be stored.
6.  Start the server: `python manage.py runserver`. This starts the server and connects it to port 8000 by default. To specify a specific port user: `python manage.py runserver host:port`, e.g., `python manage.py runserver 0.0.0.0:9000`.
7. Navigate to 'localhost:8000/hypothesize' to begin (substitute a different port number if you started the server on a different port.
8. Begin sciencing!
