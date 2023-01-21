# NOTE: The use of str() to convert user ids is VERY IMPORTANT in this script.
# Most issued faced when checking / comparing ids was related to this, caused by how JSON files are loaded

from math import ceil
import os
import pandas as pd
import json
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates
from plotting import plot_reactions_accumulative, plot_reactions, plot_reactions_daily

# Plot
# Non-accumulative


#  Read thread by thread
event_names = ['charliehebdo', 'ebola-essien', 'ferguson', 'germanwings-crash', 'ottawashooting',
               'prince-toronto', 'putinmissing', 'sydneysiege']
event_names = ['charliehebdo', 'ferguson']

for event_name in event_names:
    # Go to initial dir
    follow_tuples = []
    user_follow_dictionary = {}
    user_follow_list = []
    source_user_ids = []
    thread_dictionaries = []
    path_to_event = os.path.join(
        '.', 'PhemeDataset', 'threads', 'en', event_name)

    # Store all source user ids
    for filename in os.listdir(path_to_event):
        thread_id = filename
        path_to_thread = os.path.join(path_to_event, filename)
        #  Assert that this is a directory, not file
        assert (not os.path.isfile(path_to_thread))
        # Read in source tweet ids
        path_to_source_tweet = os.path.join(
            path_to_thread, 'source-tweets', filename + '.json')
        with open(path_to_source_tweet, 'r') as f:
            source_tweet = json.load(f)
            sid = source_tweet.get("user").get("id")
            if (not sid in source_user_ids):
                source_user_ids.append(str(sid))

    for filename in os.listdir(path_to_event):
        thread_id = filename
        path_to_thread = os.path.join(path_to_event, filename)
        #  Assert that this is a directory, not file
        assert (not os.path.isfile(path_to_thread))

        #  Read in who-follows-whom.dat
        path_to_who_follows_whom = os.path.join(
            path_to_thread, 'who-follows-whom.dat')
        if (not os.path.isfile(path_to_who_follows_whom)):
            continue
        with open(path_to_who_follows_whom, 'r') as f:
            lines = f.readlines()
        for l in lines:
            string = l.split()
            user1 = string[0]
            user2 = string[1]

            #  user1 follows user2
            follow_tuples.append((user1, user2))

        for t in follow_tuples:
            user1 = t[0]
            user2 = t[1]
            if user1 in user_follow_dictionary:
                user_follow_dictionary[user1].get('following').append(user2)
            else:
                user_follow_dictionary[user1] = {
                    'id': user1, 'followers': [], 'following': [user2]}

            if user2 in user_follow_dictionary:
                user_follow_dictionary[user2].get('followers').append(user1)
            else:
                user_follow_dictionary[user2] = {
                    'id': user2, 'followers': [user1], 'following': []}

            if (user1 in source_user_ids):
                user_follow_dictionary[user1]['is_source_user'] = True
            else:
                user_follow_dictionary[user1]['is_source_user'] = False
            if (user2 in source_user_ids):
                user_follow_dictionary[user2]['is_source_user'] = True
            else:
                user_follow_dictionary[user2]['is_source_user'] = False

        # We use a dictionary to make it easier to index via id

        # Read in source tweet(s)
        path_to_source_tweet = os.path.join(
            path_to_thread, 'source-tweets', filename + '.json')
        with open(path_to_source_tweet, 'r') as f:
            source_tweet = json.load(f)
            new_created_at = datetime.strftime(datetime.strptime(source_tweet.get(
                'created_at'), '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
            source_tweet['created_at'] = new_created_at

        # Read in reactions
        reactions = []
        path_to_reactions = os.path.join(path_to_thread, 'reactions')
        for filename in os.listdir(path_to_reactions):
            path_to_reaction = os.path.join(path_to_reactions, filename)
            with open(path_to_reaction, 'r', encoding='utf-8') as f:
                reaction = json.load(f)

                created_at = reaction.get('created_at')
                # https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
                new_created_at = datetime.strftime(datetime.strptime(
                    created_at, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                reaction['created_at'] = new_created_at

                reactions.append(reaction)

        # Read in annotation
        annotation = None
        path_to_annotation = os.path.join(path_to_thread, 'annotation.json')
        with open(path_to_annotation, 'r') as f:
            annotation = json.load(f)

        # Combine these in dictionary and add to list of dictionaries for each thread
        thread_dictionary = {
            'thread_id': thread_id,  # same as source_tweet id
            'source_tweet': source_tweet,
            'no_of_reactions': len(reactions),
            'reactions': reactions,
            'annotation': annotation,
            'user_follow_dictionary': user_follow_dictionary,
        }
        thread_dictionaries.append(thread_dictionary)

    # Rank threads by most popular source tweets
    #  w.r.t. nr of total reactions AND nr of reactions who actually follow the user

    # w.r.t. nr of total reactions (highest to lowest)
    thread_dictionaries_by_reactions = sorted(
        thread_dictionaries, key=lambda d: d['no_of_reactions'], reverse=True)

    # w.r.t. nr of reactions following source
    thread_dictionaries_by_following = None
    # Label each thread with a count of nr of reactions who actually follow the source tweeter
    for t in thread_dictionaries:
        sid = t.get("source_tweet").get("user").get("id")
        curr_count = 0
        for r in t.get("reactions"):
            # Get reactee id
            rid = r.get("user").get("id")
            rid = str(rid)
            res = user_follow_dictionary.get(rid)

            # The reactee may not be within who-follows-whom
            if res is not None:
                # Check if reactee actually follows source
                if str(sid) in res.get("following"):
                    curr_count += 1
        t["nr_of_reactions_following_source"] = curr_count

    thread_dictionaries_by_following = sorted(
        thread_dictionaries, key=lambda d: d['nr_of_reactions_following_source'], reverse=True)

    # Iterate all threads and combine all reactions into one
    all_reactions = []
    for t in thread_dictionaries:
        reactions = t.get("reactions")
        for r in reactions:
            all_reactions.append(r)

    # plot_reactions(all_reactions, event_name)

    # TODO: Rumour vs non-rumour communities for this event
    rumour_reactions = []
    nonrumour_reactions = []
    for t in thread_dictionaries:
        reactions = t.get("reactions")
        if t.get("annotation").get("misinformation") == "1":
            for r in reactions:
                rumour_reactions.append(r)
        else:
            for r in reactions:
                nonrumour_reactions.append(r)

    plot_reactions_accumulative(
        nonrumour_reactions, event_name, rumour="-nonrumour-accumulative")
    plot_reactions_accumulative(
        rumour_reactions, event_name, rumour="-rumour-accumulative")

    # plot_reactions(nonrumour_reactions, event_name, rumour="-nonrumour")
    # plot_reactions(rumour_reactions, event_name, rumour="-rumour")

    plot_reactions_daily(nonrumour_reactions, event_name,
                         rumour="-nonrumour-daily")
    plot_reactions_daily(rumour_reactions, event_name,
                         rumour="-rumour-daily")

    #  Add source tweet amongst reactions, so first reaction is source tweet
    #  Get first 5 threads from thread_dictionaries_by_reactions by index
    thread_dictionaries_by_reactions = thread_dictionaries_by_reactions[:5]
    no = 1
    print('=== BY REACTIONS ===')
    for t in thread_dictionaries_by_reactions:
        # Note source time in report

        # For each thread t, get the reactions
        reactions = t.get("reactions")
        reactions.append(t.get("source_tweet"))
        plot_reactions(reactions, event_name,
                       rumour="-thread-" + t.get("thread_id") + "-top-reactions-no-"+str(no))
        no += 1

    #  Get first 5 threads from thread_dictionaries_by_following by index
    top5_thread_dictionaries_by_following = thread_dictionaries_by_following[:5]
    no = 1
    print('=== BY FOLLOWERS REACTIONS ===')
    for t in top5_thread_dictionaries_by_following:
        # Note source time in report
        # For each thread t, get the reactions
        reactions = t.get("reactions")
        reactions.append(t.get("source_tweet"))
        plot_reactions(reactions, event_name,
                       rumour="-thread-" + t.get("thread_id") + "-top-following-no-"+str(no))
        no += 1

    # 1. Explain sorting of threads (the top5s) in report AND code
    # 2. Label rumour vs nonrumour on reactions
    # (and plot on top of each other for all plots, like
    # add a paramater to plot_reactions functions true or false, which will denote rumour or not)
    # 3. MAYBE Seperate reactions plot function (scatter plot over time)
    # 4. For nodes with most followers thread, make their NetworkX Ego graph (centrality and degrees)
    # 5. zoom in plot for report
    # 6. When last activity occurs in event
    # 7. Use the other events, and compare / look for patterns
