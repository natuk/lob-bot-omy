lob-bot-omy
===========

Twitter bot for the [Language of Bindings thesaurus](https://www.ligatus.org.uk/lob)

This Python script runs on a cron job to feed tweets to the [@LoB_bot_omy](https://twitter.com/LoB_bot_omy) twitter account.

It selects a random letter from the [LoB alphabetical index](https://www.ligatus.org.uk/lob/alphabetical) and then a random number in the corresponding concepts for that letter.

It selects a concept based on the random number and fetches its scope note and English preferred label from the [LoB sparql endpoint](http://data.ligatus.org.uk/sparql) as JSON.

It then trims and posts the tweet using the [Twython library](https://twython.readthedocs.io/en/latest/). 