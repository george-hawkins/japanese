Archive Gemini chats
====================

This directory contains chats archived from Gemini.

**Update:** in the end, I wasn't too impressed by the Markdown produced by this process and instead started saving the HTML:

```
$ python fetch_share.py --no-markdown --no-preprocess https://gemini.google.com/share/6298bc9aa977 -v -o noun-verbs-adjectives.html
```

And then asking the Claude Code to produce a coherent structured document from the conversation and save it as Markdown. I even got it to create a slash-command so now within Claude Code, I can do:

```
> /chat-to-md my-chat.html
```

And it produces a corresponding `my-chat.md` file.

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
