from twython import Twython, TwythonError
from lxml import html
import string
import random
import requests
import json


def build_tweet():
    # select a random letter
    letter = random.choice(string.ascii_lowercase)
    # build URL from alphabetical index page
    url = "https://www.ligatus.org.uk/lob/alphabetical/" + letter
    # fetch alphabetical list page for this letter
    page = requests.get(url, timeout=5.000)
    # success
    if page.status_code == 200:
        # find out how many terms
        tree = html.fromstring(page.content)
        items = tree.xpath('//td[@class="views-field views-field-title active"]')
        no_of_concepts = len(items)
        # pick a random one
        concept_no = random.randint(1, no_of_concepts)
        # get the link to the concept
        concept_url = items[concept_no].xpath('./a/@href')
        # get the concept id from the link
        concept_id = concept_url[0][13:]
        # fetch item page
        concept_json = requests.get("http://data.ligatus.org.uk/sparql?query=define%20sql%3Adescribe-mode%20%22CBD%22%20%20DESCRIBE%20%3Chttp%3A//w3id.org/lob/concept/" + concept_id + "%3E&output=application/rdf%2Bjson", timeout=5.000)
        # success
        if concept_json.status_code == 200:
            # get json from Ligatus
            data = json.loads(concept_json.content)
            # get the english label if it exists
            for pref_label in data['http://w3id.org/lob/concept/' + concept_id]['http://www.w3.org/2004/02/skos/core#prefLabel']:
                if pref_label['lang'] == "en":
                    pref_label_value = pref_label['value']
            # get the english scope note if it exists TODO: fix protocol in data.ligatus.org.uk to include https
            for scope_note in data['http://w3id.org/lob/concept/' + concept_id]['http://www.w3.org/2004/02/skos/core#scopeNote']:
                if scope_note['lang'] == "en":
                    scope_note_value = scope_note['value']
            try:
                scope_note_value
                pref_label_value
                # build the tweet
                lob_tweet = pref_label_value + "\n\n" + scope_note_value + "\n\nhttps://w3id.org/lob/concept/" + concept_id
                if len(lob_tweet) > 280:
                    len_reduce = 280 - len(lob_tweet)
                    lob_tweet = pref_label_value + "\n\n" + scope_note_value[:len_reduce - 3] + "...\n\nhttps://w3id.org/lob/concept/" + concept_id
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