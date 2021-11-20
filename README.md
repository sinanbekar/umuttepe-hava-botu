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

**Rename .env.example to .env and edit Twitter Developer API keys.**


### Local

Install the dependencies

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


### Docker

For now, should only be used for development.

```sh
docker-compose run start
```

For testing
```sh
docker-compose run test
```

For production, additional changes needed in Docker files.

 ## TODO
 - Automatically change profile photo as weather related
 
 ## Backlog
 - Place various sensors to different locations near to Umuttepe and get weather conditions as highest accuracy

## Contributing

For now, feel free to sharing any idea.


## License

MIT
