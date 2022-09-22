# Umuttepe Hava Botu

Publishes the weather conditions of Umuttepe and the live camera frames from kocaeliyiseyret.com on Twitter.

Uses Serverless Framework and deployed to Azure Function App.


**In prod. Twitter account: [@umuttepedehava](https://twitter.com/umuttepedehava)**

---

### Umuttepe

Kocaeli University's central campus is located in Umuttepe. Umuttepe is one of the places that have unstable weather conditions compared to Izmit Centre because of its 1276 feet (389 meters) altitude.

### Used Technologies & Libraries

- Serverless Framework
- OpenCV
- m3u8
- tweepy

### How the app works?

In v1, the app was refactored with Serverless Framework.
`OpenCV` helps to convert m3u8 stream segments to frames.
The tweet contains a weather summary from [umuttepe-hava.vercel.app/api/weather](https://umuttepe-hava.vercel.app/api/weather) and two frames from the live camera data from kocaeliyiseyret.com. Tweets are published using `tweepy`.

## Installation

umuttepe-hava-botu requires [Python](https://www.python.org) 3.8+ with dependencies to run. Also needed a Twitter Developer account.

Clone git repo

```sh
git clone https://github.com/sinanbekar/umuttepe-hava-botu
cd umuttepe-hava-botu
```

Rename .env.example to .env and edit Twitter Developer API keys.

Install the dependencies

```sh
yarn install
poetry install
```


For testing

```sh
poetry run test
```

## Deployment

To deploy to Azure, see: https://www.serverless.com/framework/docs/providers/azure/guide/quick-start
https://www.serverless.com/framework/docs/providers/azure/guide/credentials

```sh
yarn deploy # dev stage
yarn deploy --stage production # production
```

## Disclaimer

kocaeliyiseyret.com's contents are copyrighted by Kocaeli Metropolitan Municipality.
weather.com crawled data are also used in this project.

Use as only for **educational purposes**.
Use at **your own risk**.

## Contributing

Please feel free to share any ideas.

## License

MIT
