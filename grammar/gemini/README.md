Archive Gemini chats
====================

This directory contains chats archived from Gemini.

Python archiver
---------------

At the top-right of a Gemini chat are a stack of the dots, click this and select _Share conversation_ and use the resulting URL with the archiving tool here:

```
$ source venv/bin/activate
$ python fetch_share.py https://gemini.google.com/share/6298bc9aa977 -o noun-verbs-adjectives.md
```

Note that the fetching is quite slow, it can take several seconds, you can use `-v` to see what's going on.

Setup
-----

Create a Python `venv`:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
```

Install the necessary tools:

```
$ pip install playwright
$ playwright install chromium
$ pip install pypandoc beautifulsoup4
```
