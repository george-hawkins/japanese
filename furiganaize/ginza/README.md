spaCy with GiNZA
================

For accurate furigana, the state of the art in 2026, seems to be either doing things with a heavy-weight general AI model, like Gemini 3.1 Pro.

Or doing it with spaCy and GiNZA if you want a more process driven approach that's less susceptible to hallucination.

Currently, GiNZA has two main models:

* `ja_ginza` - a convolutional neural network (CNN) (size 50MiB, 1GiB RAM required).
* `ja_ginza_electra` - ELECTRA-base transformer (size 500MiB, at least 16GiB RAM recommended).

Both use [sudachi](https://github.com/WorksApplications/sudachi.rs/blob/develop/python/README.md) for tokenization and reading lookup.

Quick HOWTO
-----------

Create a `venv`:

```
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
```

Install `ginza` and `ja_ginza`:

```
(venv) $ pip install ginza ja_ginza
```

At the time of writing, this installed:

* spacy 3.8.14
* ginza and ja_ginza 5.2.0


`spaCy` introspects the GiNZA interface and has become stricter about types so something types `str` cannot take `None`.

So a small fix is needed to types used in the GinZA `make_compound_splitter` signature which can be applied so:

```
(venv) $ patch -p1 < ginza-compound-splitter.patch
```
 
Now you can run the small sample:

```
$ python ginza_example.py
```
