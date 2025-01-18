ChatGPT
=======

I created the current directory and set up things like so:

```
$ mkdir chatgpt
$ cd chatgpt
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install --upgrade pip
$ pip install requests
$ echo api-key.txt > .gitignore
```

I then went to <https://platform.openai.com/account/api-keys> and created an API key (I called it "Japanese Key" and left any other key properties unchanged).

I copied the key value into `api-key.txt`.

I got ChatGPT to create the script in [`request-kana.py`](request-kana.py).

The script reads the prompt for ChatGPT from the file `prompt.txt` so, I created that file and added my desired prompt to it.

But running the script just resulted in the error:

```
The model `gpt-4` does not exist or you do not have access to it.
```

It turns out (see [here](https://help.openai.com/en/articles/7102672-how-can-i-access-gpt-4-gpt-4-turbo-gpt-4o-and-gpt-4o-mini)) that you have to made a payment of at least $5 to be able to access the OpenAI API even if you intend to stay within the free tier.

So, I went to <https://platform.openai.com/settings/organization/billing/overview> and first clicked _Add payment details_ to add my credit card details.

It then asked me to _configure payment_, so I entered $5 and turned off automatic recharge.

I could then run it like so:

```
$ python request-kana.py 
```
