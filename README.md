lob-bot-omy
===========

Twitter bot for the [Language of Bindings thesaurus](https://www.ligatus.org.uk/lob)

This Python script runs on a cron job to feed tweets to the [@LoB_bot_omy](https://twitter.com/LoB_bot_omy) twitter account.

It gets a random concept from [here](https://www.ligatus.org.uk/lob/lobotomy) it fetches its scope note and English preferred label as JSON.

It then trims and posts the tweet using the [Twython library](https://twython.readthedocs.io/en/latest/). 
