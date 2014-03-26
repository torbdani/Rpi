#!/usr/bin/env python
import logging
from time import sleep
import math
from twython import Twython, TwythonError, TwythonRateLimitError
from LedStrip_WS2801 import *

logging.basicConfig(filename='twitterstuff.log', filemode='w', level=logging.INFO)
logger = logging.getLogger('twitterstuff')

APP_KEY = 'jxDTVb48GLsNaTGpbSXiqw'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAABVnUQAAAAAAkTIHHrPYkohQadEgr98dD6HqDhA%3DG1u649C4sXPM5tWUd9fDefsNY59uTTd6pAd04Jp6Xe9NQTt3ye'

hashtag = '#python OR #java OR #dotnet'
ledStrip = LedStrip_WS2801(25)


def main():
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    latest_id = twitter.search(q=hashtag, result_type='recent')['statuses'][1]['id']

    while 1:
        logger.debug("Looking for new tweets")
        try:
            result = twitter.search(q=hashtag, result_type='recent', since_id=latest_id)
            statuses = result['statuses']

            if len(statuses) > 0:
                contains_python = False
                contains_java = False
                contains_net = False
                tweet = statuses[0]
                latest_id = tweet['id']
                logger.info("New tweet!")

                hashtags = tweet['entities']['hashtags']
                for hashtag_ in hashtags:
                    if hashtag_['text'].lower() == 'python':
                        contains_python = True
                    if hashtag_['text'].lower() == 'java':
                        contains_java = True
                    if hashtag_['text'].lower() == 'dotnet':
                        contains_net = True

                if contains_python and contains_java and contains_net:
                    antialisedPoint(ledStrip, [255, 0, 0], 0.5, 0.3, 0.01)
                    antialisedPoint(ledStrip, [0, 255, 0], 0.5, 0.3, 0.01)
                    antialisedPoint(ledStrip, [0, 0, 255], 0.5, 0.3, 0.01)
                elif contains_python:
                    logger.info("Python!")
                    antialisedPoint(ledStrip, [0, 255, 0], 0.5, 0.3, 0.1)
                elif contains_java:
                    logger.info("JAVA!")
                    antialisedPoint(ledStrip, [0, 0, 255], 0.5, 0.3, 0.1)
                elif contains_net:
                    logger.info(".NOT!")
                    antialisedPoint(ledStrip, [255, 0, 0], 0.5, 0.3, 0.1)

            sleep(6)

        except (TwythonError, TwythonRateLimitError) as e:
            logger.warning('Error querying twitter')
            logger.warning(e.msg)
            if hasattr(e, 'retry_after') and e.retry_after is not None:
                logger.warning('Got told to wait %s seconds before retrying', e.retry_after)
                sleep(e.retry_after)
            else:
                logger.warning('Trying to wait five minutes and see if that helps')
                sleep(300)


def mySin(a, min, max):
    return min + ((max - min) / 2.) * (math.sin(a) + 1)


def rainbow(a):
    intense = 255
    return [int(mySin(a, 0, intense)), int(mySin(a + math.pi / 2, 0, intense)), int(mySin(a + math.pi, 0, intense))]


def fillAll(ledStrip, color, sleeptime=0):
    for i in range(0, 25):
        ledStrip.setPixel(i, color)
        ledStrip.update()
        sleep(sleeptime)


def rainbowAll(ledStrip, times, sleeptime=0):
    for t in range(0, times):
        for i in range(0, ledStrip.nLeds):
            ledStrip.setPixel(i, rainbow((1.1 * math.pi * (i + t)) / ledStrip.nLeds))
        ledStrip.update()
        if sleeptime != 0:
            sleep(sleeptime)


def antialisedPoint(ledStrip, color, step, dscale, sleeptime=0):
    rr = color[0]
    gg = color[1]
    bb = color[2]
    screenOffset = int(1.0 / (step * dscale)) + 1
    for j in range(-screenOffset, int(ledStrip.nLeds / step + screenOffset)):
        for i in range(0, ledStrip.nLeds):
            delta = 1 - abs(i - j * step) * dscale
            if delta < 0: delta = 0
            ledStrip.setPixel(i, [int(delta * rr), int(delta * gg), int(delta * bb)])
        ledStrip.update()
        sleep(sleeptime)


if __name__ == '__main__':
    main()