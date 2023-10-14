import os
from dotenv import load_dotenv
from slack_bolt import App
from transformers import pipeline

load_dotenv()
print("Hello")

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

pipe = pipeline('text-classification',
                model='finiteautomata/bertweet-base-sentiment-analysis')


"""
License

This code snippet, written by Daniel Korth from TUM, is licensed
under the MIT License.

MIT License

Permission is hereby granted, free of charge, to any person
obtaining a copy of this code snippet and associated
documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above license notice and this permission notice shall be
included in all copies or substantial portions of the Software.

The Software is provided "as is", without warranty of any kind,
express or implied, including but not limited to the warranties
of merchantability, fitness for a particular purpose and
noninfringement. In no event shall the authors or copyright
holders be liable for any claim, damages or other liability,
whether in an action of contract, tort or otherwise, arising
from, out of or in connection with the Software or the use or
other dealings in the Software.

Any person wishing to distribute modifications to the Software
is encouraged to send the modifications to the original author,
Daniel Korth (contact information available at),
so that they can be incorporated into future versions of
the Software.

By using this code snippet, you agree to comply with the terms
and conditions of this license.
"""


def process(input_text):
    dictt = {'NEG': -1, 'NEU': 0, 'POS': 1}
    out = pipe(input_text)
    sentiment = out[0]['label']
    sentiment = dictt[sentiment]

    return sentiment


@app.event("message")
def handle_message(event, say):
    text = event["text"]
    say(f"You said: {text}")

    channel = event["channel"]
    timestamp = event["ts"]
    sentiment = process(text)

    if sentiment < 0:
        emoji = "rocket-down"
    elif sentiment > 0:
        emoji = "rocket"

    try:
        app.client.reactions_add(
            channel=channel,
            timestamp=timestamp,
            name=emoji
        )
    except Exception as e:
        print(f"Error adding reaction: {str(e)}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
