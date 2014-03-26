from twython import Twython

APP_KEY = 'jxDTVb48GLsNaTGpbSXiqw'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAABVnUQAAAAAAkTIHHrPYkohQadEgr98dD6HqDhA%3DG1u649C4sXPM5tWUd9fDefsNY59uTTd6pAd04Jp6Xe9NQTt3ye'

hashtag = '#python OR #java OR #dotnet'


def test():
    twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
    result = twitter.search(q=hashtag, result_type='recent')

    lol = result['statuses']
    entities_ = lol[0]['entities']
    hashtags = entities_['hashtags']
    contains_python = False
    contains_java = False
    contains_net = False
    for hashtag_ in hashtags:
        if hashtag_['text'].lower() == 'python':
            print('python!')
        if hashtag_['text'].lower() == 'java':
            print('java!')
        if hashtag_['text'].lower() == 'dotnet':
            print('net!')


if __name__ == '__main__':
    test()