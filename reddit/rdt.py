#!/usr/bin/env python3
import webbrowser
from .config import config
import praw, json
import pickle

cfg = config()
client_id = cfg.get_clientid()
user_agent = cfg.get_useragent()
reddit = praw.Reddit(client_id = client_id,
                    client_secret = None,
                    user_agent = user_agent)

class rdt:

    def ls(move, subreddits, sort):
        def handleListCallType(type):
            with open('reddit/variables.json', 'rb') as jsonf:
                dictvals = pickle.load(jsonf)
            jsonf.close()
            dictvals['nextpreviousnormal'] = "False"
            dictvals['nextprevioussubreddits'] = "False"
            del dictvals['links'][:]
            del dictvals['listofsubmissions'][:]
            del dictvals['listofsubreddits'][:]
            temp = 0
            if type == 'hot':
                submissions = reddit.front.hot(limit = 100)
            elif type == 'new':
                submissions = reddit.front.new(limit = 100)
            elif type == 'controversial':
                submissions = reddit.front.controversial(limit = 100)
            elif type == 'top':
                submissions = reddit.front.top(limit = 100)
            elif type == 'rising':
                submissions = reddit.front.rising(limit = 100)
            for listvals in submissions:
                dictvals['listofsubmissions'].append(listvals)

            for i in range(0,len(dictvals['listofsubmissions'])):
                if temp<10:
                    temp = temp + 1
                    print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubmissions'][i].title))
                    print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubmissions'][i].url))
                    print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(dictvals['listofsubmissions'][i].ups), str(dictvals['listofsubmissions'][i].num_comments)))
                    dictvals['links'].append(dictvals['listofsubmissions'][i].url)
            dictvals['listed'] = "True"
            dictvals['countlist'] = temp
            if len(dictvals['listofsubmissions']) >= 10:
                print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                dictvals['nextpreviousnormal'] = "True"
            with open('reddit/variables.json', 'wb') as f:
                pickle.dump(dictvals, f)
            f.close()

        def handleMoreList(move):
            with open('reddit/variables.json', 'rb') as jsonf:
                dictvals = pickle.load(jsonf)
            jsonf.close()
            if move == 'next':
                temp = 0
                if dictvals['listed'] == "True" and dictvals['countlist']<len(dictvals['listofsubmissions']):
                    for i in range(dictvals['countlist'],len(dictvals['listofsubmissions'])):
                        if temp < 10:
                            temp = temp + 1
                            print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubmissions'][i].title))
                            print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubmissions'][i].url))
                            print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(dictvals['listofsubmissions'][i].ups), str(dictvals['listofsubmissions'][i].num_comments)))
                            dictvals['links'].append(dictvals['listofsubmissions'][i].url)
                    dictvals['countlist'] = dictvals['countlist'] + temp
                    dictvals['tempvar'] = temp
                    if dictvals['countlist'] != len(dictvals['listofsubmissions']):
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('previous'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))

            elif move == 'previous':
                if dictvals['listed'] == "True" and dictvals['countlist']>10:
                    dictvals['countlist'] = dictvals['countlist'] - dictvals['tempvar']
                    for i in range(dictvals['countlist']-10,dictvals['countlist']):
                        print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubmissions'][i].title))
                        print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubmissions'][i].url))
                        print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(dictvals['listofsubmissions'][i].ups), str(dictvals['listofsubmissions'][i].num_comments)))
                        dictvals['links'].append(dictvals['listofsubmissions'][i].url)
                        dictvals['tempvar'] = 10
                    if dictvals['countlist'] > 10:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))
            with open('reddit/variables.json', 'wb') as f:
                pickle.dump(dictvals,f)
            f.close()

        def handleMoreSubreddits(move):
            with open('reddit/variables.json', 'rb') as jsonf:
                dictvals = pickle.load(jsonf)
            jsonf.close()
            if move == 'next':
                temp = 0
                if dictvals['listed'] == "True" and dictvals['countlist']<len(dictvals['listofsubreddits']):
                    for i in range(dictvals['countlist'],len(dictvals['listofsubreddits'])):
                        if temp < 10:
                            temp = temp + 1
                            print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubreddits'][i].display_name_prefixed+ " - "+dictvals['listofsubreddits'][i].title))
                            print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubreddits'][i].url))
                            print("{0:<5} \33[90m {1} subscribers\33[0m".format('', str(dictvals['listofsubreddits'][i].subscribers)))
                    dictvals['countlist'] = dictvals['countlist'] + temp
                    dictvals['tempvar'] = temp
                    if dictvals['countlist'] != len(dictvals['listofsubreddits']):
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('previous'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))

            elif move == 'previous':
                if dictvals['listed'] == "True" and dictvals['countlist']>10:
                    dictvals['countlist'] = dictvals['countlist'] - dictvals['tempvar']
                    for i in range(dictvals['countlist']-10,dictvals['countlist']):
                        print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubreddits'][i].display_name_prefixed+ " - "+dictvals['listofsubreddits'][i].title))
                        print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubreddits'][i].url))
                        print("{0:<5} \33[90m {1} subscribers\33[0m".format('', str(dictvals['listofsubreddits'][i].subscribers)))
                        dictvals['tempvar'] = 10
                    if dictvals['countlist'] > 10:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))
            with open('reddit/variables.json', 'wb') as f:
                pickle.dump(dictvals,f)
            f.close()

        with open('reddit/variables.json', 'rb') as jsonf:
            dictvals = pickle.load(jsonf)
        jsonf.close()

        if move == sort == None and subreddits == False:
            handleListCallType('hot')

        elif move == None and subreddits == False and sort != None:
            handleListCallType(sort)

        elif (move == 'next' or move == 'previous') and subreddits == False and sort == None:
            if dictvals['nextpreviousnormal'] == "True":
                handleMoreList(move)
            else:
                print("{0:<5} \33[31m {1} \33[5m".format('', 'Nothing to Display'))

        elif move == None and subreddits == True and sort == None:
            dictvals['nextpreviousnormal'] = False
            dictvals['nextprevioussubreddits'] = False
            temp = 0
            del dictvals['links'][:]
            del dictvals['listofsubmissions'][:]
            del dictvals['listofsubreddits'][:]
            subreddits = reddit.subreddits.popular(limit = 100)

            for listvals in subreddits:
                dictvals['listofsubreddits'].append(listvals)

            for i in range(0,len(dictvals['listofsubreddits'])):
                if temp<10:
                    temp = temp + 1
                    print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), dictvals['listofsubreddits'][i].display_name_prefixed+ " - "+dictvals['listofsubreddits'][i].title))
                    print("{0:<5} \33[90m {1} \33[0m".format('', dictvals['listofsubreddits'][i].url))
                    print("{0:<5} \33[90m {1} subscribers\33[0m".format('', str(dictvals['listofsubreddits'][i].subscribers)))
            dictvals['listed'] = "True"
            dictvals['countlist'] = temp
            if len(dictvals['listofsubreddits']) >= 10:
                print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                dictvals['nextprevioussubreddits'] = "True"
            with open('reddit/variables.json', 'wb') as f:
                pickle.dump(dictvals,f)
            f.close()

        elif (move == 'next' or move == 'previous') and subreddits == True and sort == None:
            if dictvals['nextprevioussubreddits'] == "True":
                handleMoreSubreddits(move)
            else:
                print("{0:<5} \33[31m {1} \33[5m".format('', 'Nothing to Display'))

    def view(index, comments, more_comments):
        pass

    def search(input):
        pass
