
# Introduction

This library provides a pure Python interface for the
`Messenger Bot API such as Facebook, Telegram, Slack.`. Feel free to add and contribute other.

In addition to the pure API implementation, this library features a number of high-level classes to
make the development of bots easy and straightforward.

# Learning by example
We believe that the best way to learn and understand this simple package is by example. 
So here are some examples for you to review [this url](https://github.com/python-bot/python-bot/tree/master/examples)

# Installing

**Python 3 required!**

>This framework assumes you are using Python 3. Get the latest version at
>Python's [download page](https://www.python.org/download/)


## Getting a copy of Python Bot's development version


The first step to contributing to Python Bot is to get a copy of the source code.
From the command line, use the ``cd`` command to navigate to the directory
where you'll want your local copy of Python Bot to live.

Download the Python Bot source code repository using the following command:

```
    $ git clone https://github.com/python-bot/python-bot.git
```

Now that you have a local copy of Python Bot.

## Using virtual environment

Create a new virtualenv by running:

```
    $ python3 -m venv ~/.virtualenvs/python-bot
```

The path is where the new environment will be saved on your computer.

>    On some versions of Ubuntu the above command might fail. Use the
>   ``virtualenv`` package instead, first making sure you have ``pip3``:

```

        $ sudo apt-get install python3-pip
        $ # Prefix the next command with sudo if it gives a permission denied error
        $ pip3 install virtualenv
        $ virtualenv --python=`which python3` ~/.virtualenvs/python-botdev
```

The final step in setting up your virtualenv is to activate it:

```
    $ source ~/.virtualenvs/python-botdev/bin/activate
```

The installed version of Python Bot is now pointing at your local copy.

## Contributing

Contributions of all sizes are welcome. You can also help by [reporting bugs](https://github.com/python-bot/python-bot/issues/new).

## License
You may copy, distribute and modify the software provided that modifications are described and licensed for free under [LGPL-3](https://www.gnu.org/licenses/lgpl-3.0.html). Derivatives works (including modifications or anything statically linked to the library) 
can only be redistributed under LGPL-3, but applications that use the library don't have to be.