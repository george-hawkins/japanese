OpenJTalk
=========

OpenJTalk is a system that's used by TTS systems and so can handle things like 一階 becoming いっかい rather than いちかい.

But it falls down on things that GiNZA gets right.

Claude suggests using a hybrid of the two and asking an LLM like Gemini 3.1 Plus to adjudicate when the two disagree, i.e. only use the costly cloud option for sentences that you can't do locally.

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
(venv) $ pip install pyopenjtalk-plus pyopenjtalk-plus[onnxruntime]
```

Note: I installed [`pyopenjtalk-plus`](https://github.com/tsukumijima/pyopenjtalk-plus) rather than [`pyopenjtalk`](https://github.com/r9y9/pyopenjtalk). You don't have to change code when switching between the two, i.e. `import pyopenjtalk` works whether using the original or the `pyopenjtalk-plus` version.

Now you can run the small sample:

```
$ python openjtalk_example.py
```
