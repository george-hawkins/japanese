Claude
======

After trying GiNZA and OpenJTalk, I found Claude did far better even with Sonnet (Claude Code, running Opus 4.7, recommended Sonet as good enough for this task.

See [`book-annotation.md`](book-annotation.md) for a more cost-efficient approach than `claude_example.py`.

Quick HOWTO
-----------

Create a `venv`:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
```

Install `anthropic` and make sure you're Anthropic API key is setup:

```
(venv) $ pip install anthropic
(venv) $ export ANTHROPIC_API_KEY='sk-ant-api0...'
```

Mac Passwords is a convenient place to store these kinds of keys.

Now you can run the small sample:

```
$ python claude_example.py
```
