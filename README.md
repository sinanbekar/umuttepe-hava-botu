# Umuttepe Hava Botu
#### Umuttepe'de hava şu an nasıl ? - [@umuttepedehava](https://twitter.com/umuttepedehava)

Gets Umuttepe weather conditions and kocaeliyiseyret.com live camera frames, publishes on Twitter as a tweet. Currently hosting on Heroku Free Tier.

## Installation

umuttepe-hava-botu requires [Python](https://www.python.org) 3.6+ with dependencies to run. 
Uses Celery based task queues.

Clone Git repo
```sh
git clone https://github.com/sinanbekar/umuttepe-hava-botu
```

Rename .env.example to .env and edit Twitter Developer API keys.


Install the dependencies start the bot.

```sh
pip install -r requirements.txt
```

For testing, install requirements-dev.txt and run command pytest
```sh
pip install -r requirements-dev.txt
pytest
```


 ## Run
 Run umuttepe-hava-botu
 ```sh
umuttepe_hava_botu run
```


 ## TODO
 - Automatically change profile photo as weather related
 - Calculate live camera periodic turn timing and select unique angle with sampling
 - Dockerizing
 
 ## Backlog
 - Machine learning based live camera weather condition detection
 - Image processing for anonymizing (blurring pedestrians and license plates)
 Needed GPU powered cloud like Google Firebase (free trial) or Google Colab (totally free) for these 2 items so also needed implementation.
 - Real weather API (highest accuracy and free possible ☺)
 - More test coverage
 - Powerful logging

## Contributing

For now, feel free for sharing any idea.



## License

MIT
