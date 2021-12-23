from twython import Twython, TwythonError
import requests
import json


def build_tweet():
    # set URL
    url = "https://www.ligatus.org.uk/lob/lobotomy"
    # fetch json
    concept_json = requests.get(url, timeout=5.000)
    # success
    if concept_json.status_code == 200:
        # get json from Ligatus
        data = json.loads(concept_json.content)
        # get the english label if it exists
        pref_label_value = data[0]['title']
        scope_note_value = data[0]['note']
        concept_uri = data[0]['uri']
        try:
            scope_note_value
            pref_label_value
            # build the tweet
            lob_tweet = pref_label_value + "\n\n" + scope_note_value + concept_uri
            if len(lob_tweet) > 280:
                len_reduce = 280 - len(lob_tweet)
                lob_tweet = pref_label_value + "\n\n" + scope_note_value[:len_reduce - 3] + "..." + concept_uri
            print(lob_tweet)
        except NameError:
            print("No english scopeNote of prefLabel for this concept")
            # try again with a new concept
            lob_tweet = build_tweet()

        return lob_tweet

# load credentials from json file which looks like twitter_keys_default.json
with open("twitter_keys.json", "r") as file:
    creds = json.load(file)
# add credentials to access API
twitter = Twython(creds['APP_KEY'], creds['APP_SECRET'], creds['OAUTH_TOKEN'], creds['OAUTH_TOKEN_SECRET'])

tweet = build_tweet()

try:
	twitter.update_status(status=tweet)
except TwythonError as e:
	print(e)