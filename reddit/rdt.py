#!/usr/bin/env python3
import webbrowser
from .config import config
import praw

cfg = config()
client_id = cfg.get_clientid()
user_agent = cfg.get_useragent()
reddit = praw.Reddit(client_id = client_id,
                    client_secret = None,
                    user_agent = user_agent)
links = []
listed = False
listofsubmissions = []
listofcomments = []
listofsubreddits = []
countlist = 0
countcomments = 0
tempvar = 0
nextprevious = False
nextpreviousnormal = False
nextprevioussubreddits = False
commands = []

class rdt:

    def ls(move, subreddits, sort):

        def handleListCallType(type):
            global links
            global listed
            global listofsubmissions
            global countlist
            global listofsubreddits
            global nextprevious
            global nextpreviousnormal
            global nextprevioussubreddits
            nextpreviousnormal = False
            nextprevious = False
            nextprevioussubreddits = False
            temp = 0
            del links[:]
            del listofsubmissions[:]
            del listofsubreddits[:]
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
                listofsubmissions.append(listvals)

            for i in range(0,len(listofsubmissions)):
                if temp<10:
                    temp = temp + 1
                    print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), listofsubmissions[i].title))
                    print("{0:<5} \33[90m {1} \33[0m".format('', listofsubmissions[i].url))
                    print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(listofsubmissions[i].ups), str(listofsubmissions[i].num_comments)))
                    links.append(listofsubmissions[i].url)
            listed = True
            countlist = temp
            if len(listofsubmissions) >= 10:
                print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                nextpreviousnormal = True

        def handleMoreList(move):
            global links
            global listed
            global listofsubmissions
            global countlist
            global nextprevious
            global tempvar
            if move == 'next':
                temp = 0
                if listed == True and countlist<len(listofsubmissions):
                    for i in range(countlist,len(listofsubmissions)):
                        if temp < 10:
                            temp = temp + 1
                            print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), listofsubmissions[i].title))
                            print("{0:<5} \33[90m {1} \33[0m".format('', listofsubmissions[i].url))
                            print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(listofsubmissions[i].ups), str(listofsubmissions[i].num_comments)))
                            links.append(listofsubmissions[i].url)
                    countlist = countlist + temp
                    tempvar = temp
                    if countlist != len(listofsubmissions):
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                        nextprevious = True
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('previous'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))

            elif move == 'previous':
                if listed == True and countlist>10:
                    countlist = countlist-tempvar
                    for i in range(countlist-10,countlist):
                        print("\33[92m {0:<4} \33[0m {1}".format(str(i + 1), listofsubmissions[i].title))
                        print("{0:<5} \33[90m {1} \33[0m".format('', listofsubmissions[i].url))
                        print("{0:<5} \33[90m {1} Upvotes with {2} Comments \33[0m".format('', str(listofsubmissions[i].ups), str(listofsubmissions[i].num_comments)))
                        links.append(listofsubmissions[i].url)
                        tempvar = 10
                    if countlist>10:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next | previous'))
                        nextprevious = True
                    else:
                        print("\33[90m (\33[0m\33[93m {} \33[0m\33[90m) \33[0m".format('next'))
                else:
                    print("{0:<5} \33[31m {1} \33[5m".format('', 'No More Entries Available'))

        if move == sort == None and subreddits == False:
            handleListCallType('hot')
        elif move == None and subreddits == False and sort != None:
            handleListCallType(sort)
        elif (move == 'next' or move == 'previous') and subreddits == False and sort == None:
            if nextpreviousnormal == True:
                handleMoreList(move)
            else:
                print("{0:<5} \33[31m {1} \33[5m".format('', 'Nothing to Display'))

    def view(index, comments, more_comments):
        pass

    def search(input):
        pass
