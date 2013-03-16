## daneel

Daneel is an irc [robot](http://en.wikipedia.org/wiki/R._Daneel_Olivaw).  He runs on a few rooms I'm in doing various things for me.

### commands

Currently, all daneel does is listen for URLs, fetch summaries for them, and print them out in the room.  Suggestions or
implementations for commands are welcome.

### installing

All you need is `gevent` and this repository;  daneel uses no other libraries.  If you are crazy, you can use:

    apt-get install gevent-python
    
But if you are a python programmer or a sane person,  you can install gevent with pip via:

    pip install gevent
    
The bulk of his IRC support is in `girc.py`, which is a very small gevent-based IRC library I wrote after irctk kept on failing to reconnect.  `girc` does not support reconnecting, but it will when daneel starts disconnecting :)

If you want to make your own daneel, look at `bin/daneel-bot.py`, which also gets installed as a script if you install
this repository.

