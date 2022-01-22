import os
import re

import requests
from dotenv import load_dotenv

load_dotenv()
IFTTT_KEY = os.environ["IFTTT_KEY"]


def run(settings, message):

    actions = settings.actions
    keywords = [a["keyword"] for a in actions]
    command = re.sub(r"<@!?\d+>[ ]?", "", message.content).strip()
    search_regex = "^({})".format("|".join(keywords))
    keyword = re.findall(search_regex, command, flags=re.IGNORECASE)
    keyword = keyword[0].lower() if keyword else None
    message_out = None

    if keyword:
        action = actions[keywords.index(keyword)]
        url = "https://maker.ifttt.com/trigger/{}/with/key/{}".format(
            action["action"],
            IFTTT_KEY,
        )
        requests.get(url)
        message_out = action["reply"]

    else:
        message_out = "Keyword %s not understood. Available keywords: %s" % (
            keyword,
            ", ".join(keywords),
        )

    return message_out
