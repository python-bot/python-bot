TODO list
========

Before merge features
-------------
##### Planned messenger support will text only (support for additional user data such as buttons, images, location, channels will be planned on next release, now you can access from BotRequest.extra)

Messenger   | Long polling   | Web hook        | Text mode
----------- | :------------: | :------:        | :--------:
Slack       | Partially done | -               | Not started
Telegram    | Not planned    | Partially done  | Partially done
Facebook    | -              | Partially done  | Partially done

##### Webhook handlers
- Pure python (Partially done)

##### DB storage
- Simple json storage (Partially done)
- MongoDB

Nice to have
-----------------
##### Python2 support
- rewrite all modules to be compatible with python2

##### DB storage
- MySQL

##### Webhook handlers (by priority)
- Flask
- Django
- Cherrypy

##### Messenger support (by priority)
- Skype
- Kik

##### Documentation
- comment all public methods (Follow style guide https://google.github.io/styleguide/pyguide.html)
- log debug information
- Sphinx documentation


##### Stats https://github.com/botanio/sdk#py or something like

##### Localization
- make all string translatable
- the same for datetime formats
- Localization support for Russian
