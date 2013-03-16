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

### writing

If you want to write your own bot, `bin/daneel-bot.py` is a good place to start.

Despite being `gevent` based, daneel still uses callback handlers, as they are a pretty standard way of dealing with the multiplexed, async nature of IRC.  Handlers receive a context object which looks like this:

```python
class Context(object):
    server    # current server object
    channel   # channel message was sent to, or None if N/A
    line      # raw line of this message
    sender    # sender of the message, eg. user!~username@hostmask.rr.com
    type      # type of message, eg. PRIVMSG
    target    # target of the message, eg. #channel
    msg       # the message text, eg. "Hello everyone!"
```

You can use `channel.say()` to send a message to the channel, or use `server.say(msg, to)` to reply to the sender.
Although gevent will not prevent the readloop from running while your plugins run, the handlers are all run in the same
thread and can block eachother;  spawn your own greenthreads if you need to do some networking that might take a while.

While handlers live at the server level, there are some helpers as well:

#### `privmsg(handler)`

A wrapper (or decorator) for a function which should only respond to PRIVMSG type messages.

#### `handle_on(handler, type=None, sender=None, target=None, msg=None)`

A generic handler wrapper which will filter out messages which do not match all of the established criteria.  For instance, you can use `handle_on(handler, type="NOTICE")` to have your handler only run on NOTICE functions.  The filters can take strings (at which point there is an `in` comparison) or callables which receive a string and return a booley value.  This means you can also do something like `handle_on(handler, type=lambda x: x != "PRIVMSG")` to handle all non-privmsg messages.

#### `channel.add_handler(handler)`

A convenience method which is equivalent to `channel.server.handlers.append(handle_on(handler, target=channel.name))`,
ie. only handle messages that go to this channel.

### interaction

Sometimes, your bot needs to have a kind of conversation with another user or with the server.  There is a simple
abstraction for this called `server.waitfor(...)`, which creates filters in the same way that `handle_on` does.  The
server connection step uses `waitfor` to connect and identify nicks before attempting to join any channels.  It's worth
noting that this will block your thread, so if you need to do this in a handler you should spawn a greenlet to continue
that conversation without blocking other handlers.

### TODO/INFO

* The server object installs its own handler, `server.ping`, which takes care of IRC's PING/PONG.
* Nearly any type of error will currently crash the bot, including disconnections.
* The `timeout` param for servers is not used, but should be used in the future by the ping handler to initiate a dc/rc
  sequence if it is exceeded.
* The entire bot code is currently only around ~200loc and can easily be read and understood by anyone who knows python,
  though reasoning about what might block and what won't can be more difficult.

