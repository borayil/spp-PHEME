from math import ceil
import os
import pandas as pd
import json 
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates

# Read thread by thread
event_names = ['charliehebdo', 'ebola-essien', 'ferguson', 'germanwings-crash', 'ottawashooting',
'prince-toronto', 'putinmissing', 'sydneysiege']
event_names = ['charliehebdo']

for event_name in event_names:
    follow_tuples = []
    user_follow_dictionary = {}
    user_follow_list = []
    source_user_ids = []
    thread_dictionaries = []
    path_to_event = os.path.join('.', 'PhemeDataset', 'threads', 'en', event_name)

    # Store all source user ids
    for filename in os.listdir(path_to_event):
        thread_id = filename
        path_to_thread = os.path.join(path_to_event,filename)
        assert (not os.path.isfile(path_to_thread)) # Assert that this is a directory, not file
        # Read in source tweet ids 
        path_to_source_tweet = os.path.join(path_to_thread, 'source-tweets', filename + '.json')
        with open(path_to_source_tweet, 'r') as f:
            source_tweet = json.load(f)
            sid = source_tweet.get("user").get("id")
            if (not sid in source_user_ids):
                source_user_ids.append(str(id))

    for filename in os.listdir(path_to_event):
        thread_id = filename
        path_to_thread = os.path.join(path_to_event,filename)
        assert (not os.path.isfile(path_to_thread)) # Assert that this is a directory, not file
        
        # Read in annotation
        path_to_annotation = os.path.join(path_to_thread, 'annotation.json')
        with open(path_to_annotation, 'r') as f:
            annotation = json.load(f)
        
        # TODO: Read in retweets

        # TODO: Read in structure

        # Read in who-follows-whom.dat
        path_to_who_follows_whom = os.path.join(path_to_thread, 'who-follows-whom.dat')
        with open(path_to_who_follows_whom, 'r') as f:
            lines = f.readlines()
        for l in lines:
            str = l.split()
            user1 = str[0]
            user2 = str[1]

            # user1 follows user2
            follow_tuples.append((user1,user2))
        
        for t in follow_tuples:
            user1 = t[0]
            user2 = t[1]
            
            if user1 in user_follow_dictionary:
                user_follow_dictionary[user1].get('following').append(user2)
            else:
                user_follow_dictionary[user1] = {'id': user1, 'followers': [], 'following': [user2]}

            if user2 in user_follow_dictionary:
                user_follow_dictionary[user2].get('followers').append(user1)
            else:
                user_follow_dictionary[user2] = {'id': user2, 'followers': [user1], 'following': []}
            
            if (user1 in source_user_ids):
                user_follow_dictionary[user1]['is_source_user'] = True
            else:
                user_follow_dictionary[user1]['is_source_user'] = False
            if (user2 in source_user_ids):
                user_follow_dictionary[user2]['is_source_user'] = True
            else:
                user_follow_dictionary[user2]['is_source_user'] = False
        
        # We used dictionary to make it easier to index via id
        # Now we can turn dictionary to list
        for u in user_follow_dictionary:
            user_dict = user_follow_dictionary[u]
            user_follow_list.append(user_dict)
    
        # Read in source tweet(s) 
        path_to_source_tweet = os.path.join(path_to_thread, 'source-tweets', filename + '.json')
        with open(path_to_source_tweet, 'r') as f:
            source_tweet = json.load(f)
            new_created_at = datetime.strftime(datetime.strptime(source_tweet.get('created_at'), '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
            source_tweet['created_at'] = new_created_at
            
        
        # Read in reactions
        reactions = []
        path_to_reactions = os.path.join(path_to_thread, 'reactions')
        for filename in os.listdir(path_to_reactions):
            path_to_reaction = os.path.join(path_to_reactions, filename)
            with open(path_to_reaction, 'r') as f:
                reaction = json.load(f)
                
                
                created_at = reaction.get('created_at')
                # https://stackoverflow.com/questions/7703865/going-from-twitter-date-to-python-datetime-date
                new_created_at = datetime.strftime(datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
                reaction['created_at'] = new_created_at
                
                reactions.append(reaction)

                
        
        # Combine these in dictionary and add to list of dictionaries for each thread
        thread_dictionary = {
            'thread_id': thread_id, # same as source_tweet id
            'source_tweet': source_tweet,
            'no_of_reactions': len(reactions),
            'reactions': reactions,
            'annotation': annotation,
            # retweets
            # structure
            # who-follows-whom
            }
        thread_dictionaries.append(thread_dictionary)

    # Iterate all threads and combine all reactions into one
    all_reactions = []
    for t in thread_dictionaries:
        reactions = t.get("reactions")
        for r in reactions:
            all_reactions.append(r)


    all_reactions = sorted(all_reactions, key=lambda d: d['created_at'], reverse=False)
    start_time = all_reactions[0].get("created_at")
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = all_reactions[-1].get("created_at")
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    elapsed = end_time - start_time
    min_interval = 5
    number_of_intervals = ceil(elapsed / timedelta(minutes=min_interval))
    x_axis = [start_time + timedelta(minutes=x * min_interval) for x in range(number_of_intervals+1)]

    # Formulating y-axis
    y_axis = []

    curr_reaction_idx = 0
    count = 0
    for timestamp in x_axis:
        # check for out of bounds
        if curr_reaction_idx >= len(all_reactions):
            break
        while (datetime.strptime(all_reactions[curr_reaction_idx].get('created_at'), '%Y-%m-%d %H:%M:%S') <= timestamp):
            count += 1
            curr_reaction_idx += 1
            if curr_reaction_idx >= len(all_reactions):
                break
        y_axis.append(count)

    # Plot the axis
    plt.title(event_name)
    plt.xlabel("Timestamps")
    plt.ylabel("No. of reactions")
    # https://www.youtube.com/watch?v=_LWjaAiKaf8
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red' )
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(event_name)
    plt.close()
    print(event_name + " saved.")

    for u in user_follow_list:
        what = u.get("is_source_user")
        if what:
            print(what)
    exit()
    