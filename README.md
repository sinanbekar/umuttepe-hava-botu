# Umuttepe Hava Botu
Gets Umuttepe weather conditions and kocaeliyiseyret.com live camera frames, publishes on Twitter as a tweet. Currently hosting on Heroku Free Tier.

##### In prod. Twitter account:  [@umuttepedehava](https://twitter.com/umuttepedehava)
---
### Umuttepe
Kocaeli University's central campus is located in Umuttepe. Umuttepe is one of the places that have unstable weather conditions compared to Izmit Centre because of its 1276 feet (389 meters) altitude. 

### Used Technologies & Libraries
**OpenCV** (for capturing live stream frames)
**Celery** (for task queues)
**BeautifulSoup4** (for crawling weather data)
**Tweepy** (easy-to-use library for accessing the Twitter API)


### How the app works ?

Tweets include 2 jpeg frame from kocaeliyiseyret.com live camera data (m3u8) by OpenCV with random sampling (different camera angles) and the tweets also includes weather.com data that crawled with BeautifulSoup4. Celery tasks run periodically for tweeting and deleting old tweets. 



## Requirements & Installation

umuttepe-hava-botu requires [Python](https://www.python.org) 3.6+ with dependencies to run. Also needed Twitter Developer account.
Uses Celery based task queues. 

Clone Git repo
```sh
git clone https://github.com/sinanbekar/umuttepe-hava-botu
```

**Rename .env.example to .env and edit Twitter Developer API keys.**


# Local

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


# Docker

For now, should only be used for development.

```sh
docker-compose run start
```

For testing
```sh
docker-compose run test
```

For production, additional changes are needed in Docker files.

 ## TODO
 - Automatically change profile photo as weather-related
 
 ## Backlog
 - Place various sensors to different locations near Umuttepe and get weather conditions as highest accuracy

## Disclaimer

kocaeliyiseyret.com's contents are copyrighted by Kocaeli Metropolitan Municipality.
weather.com crawled data are also used in this project.

Use as only for **educational purposes**. 
Use at **your own risk**.


## Contributing

Please feel free to share any ideas.


## License

MIT
