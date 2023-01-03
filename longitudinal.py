# NOTE: The use of str() to convert user ids is VERY IMPORTANT in this script.
# Most issued faced when checking / comparing ids was related to this, caused by how JSON files are loaded

from math import ceil
import os
import pandas as pd
import json 
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates

# Plot
# Non-accumulative
def plot_reactions(reactions, event_name, rumour=""):
    
    if len(reactions) <= 0:
        return
    assert (not event_name is None)

    # Plot rumour
    reactions = sorted(reactions, key=lambda d: d['created_at'], reverse=False)
    start_time = reactions[0].get("created_at")
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = reactions[-1].get("created_at")
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    elapsed = end_time - start_time
    min_interval = 10
    number_of_intervals = ceil(elapsed / timedelta(minutes=min_interval))
    x_axis = [start_time + timedelta(minutes=x * min_interval) for x in range(number_of_intervals+1)]

    # Formulating y-axis
    y_axis = []

    curr_reaction_idx = 0
    
    for timestamp in x_axis:
        count = 0
        # check for out of bounds
        if curr_reaction_idx >= len(reactions):
            break
        while (datetime.strptime(reactions[curr_reaction_idx].get('created_at'), '%Y-%m-%d %H:%M:%S') <= timestamp):
            count += 1
            curr_reaction_idx += 1
            if curr_reaction_idx >= len(reactions):
                break
        y_axis.append(count)

    # Plot the axis
    file_name = event_name + rumour
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("No. of reactions")
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red' )
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")
# Plots given reactions with timestamps on given filename
# Accumulative
def plot_reactions_accumulative(reactions, event_name, rumour=""):
    if len(reactions) <= 0:
        return
    assert (not event_name is None)

    # Plot rumour
    reactions = sorted(reactions, key=lambda d: d['created_at'], reverse=False)
    start_time = reactions[0].get("created_at")
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = reactions[-1].get("created_at")
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    elapsed = end_time - start_time
    min_interval = 10
    number_of_intervals = ceil(elapsed / timedelta(minutes=min_interval))
    x_axis = [start_time + timedelta(minutes=x * min_interval) for x in range(number_of_intervals+1)]

    # Formulating y-axis
    y_axis = []

    curr_reaction_idx = 0
    count = 0
    for timestamp in x_axis:
        # check for out of bounds
        if curr_reaction_idx >= len(reactions):
            break
        while (datetime.strptime(reactions[curr_reaction_idx].get('created_at'), '%Y-%m-%d %H:%M:%S') <= timestamp):
            count += 1
            curr_reaction_idx += 1
            if curr_reaction_idx >= len(reactions):
                break
        y_axis.append(count)

    # Plot the axis
    file_name = event_name + rumour
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("(Accumulative) No. of reactions")
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red' )
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")

def plot_reactions_daily(reactions, event_name, rumour=""):
    if len(reactions) <= 0:
        return
    assert (not event_name is None)

    # Plot
    reactions = sorted(reactions, key=lambda d: d['created_at'], reverse=False)
    start_time = reactions[0].get("created_at")
    start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end_time = reactions[-1].get("created_at")
    end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    
    curr_day = start_time
    curr_reaction_idx = 0
    while (True):

        # Stopping condition
        if (curr_day >= end_time):
            break

        # Get the end (add 24 hrs)
        end_day = curr_day + timedelta(days=1)
        elapsed = end_day - curr_day
        min_interval = 15
        number_of_intervals = ceil(elapsed / timedelta(minutes=min_interval))
        x_axis = [curr_day + timedelta(minutes=x * min_interval) for x in range(number_of_intervals+1)]
        y_axis = []

        for timestamp in x_axis:
            
            # Start from 0 between each time stamp
            count = 0

            # check for out of bounds
            if curr_reaction_idx >= len(reactions):
                y_axis.append(count)
                break
        
            while (datetime.strptime(reactions[curr_reaction_idx].get('created_at'), '%Y-%m-%d %H:%M:%S') <= timestamp):
                count += 1
                curr_reaction_idx += 1
                if curr_reaction_idx >= len(reactions):
                    break
            
            y_axis.append(count)
        
        while (len(y_axis)) < (len(x_axis)):
            y_axis.append(0)
        
        # Plot
        file_name = event_name + rumour
        plt.title(file_name)
        plt.xlabel("Timestamps")
        plt.ylabel("No. of reactions")
        plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red' )
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig(file_name + curr_day.strftime("%m-%d-%Y"))
        plt.close()
        print(file_name + "saved.")

        # Go to next day
        print(curr_day)
        curr_day += timedelta(days=1)
        print(curr_day)
        print("---")
            
# Read thread by thread
event_names = ['charliehebdo', 'ebola-essien', 'ferguson', 'germanwings-crash', 'ottawashooting',
'prince-toronto', 'putinmissing', 'sydneysiege']
event_names = ['charliehebdo']

for event_name in event_names:
    # Go to initial dir
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
                source_user_ids.append(str(sid))
    
    for filename in os.listdir(path_to_event):
        thread_id = filename
        path_to_thread = os.path.join(path_to_event,filename)
        assert (not os.path.isfile(path_to_thread)) # Assert that this is a directory, not file
        
        # Read in who-follows-whom.dat
        path_to_who_follows_whom = os.path.join(path_to_thread, 'who-follows-whom.dat')
        if (not os.path.isfile(path_to_who_follows_whom)):
            continue
        with open(path_to_who_follows_whom, 'r') as f:
            lines = f.readlines()
        for l in lines:
            string = l.split()
            user1 = string[0]
            user2 = string[1]

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
        
        # We use a dictionary to make it easier to index via id
    
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

        # Read in annotation
        annotation = None
        path_to_annotation = os.path.join(path_to_thread, 'annotation.json')
        with open(path_to_annotation, 'r') as f:
            annotation = json.load(f)
                
        
        # Combine these in dictionary and add to list of dictionaries for each thread
        thread_dictionary = {
            'thread_id': thread_id, # same as source_tweet id
            'source_tweet': source_tweet,
            'no_of_reactions': len(reactions),
            'reactions': reactions,
            'annotation': annotation,
            }
        thread_dictionaries.append(thread_dictionary)

    # Rank threads by most popular source tweets
    # w.r.t. nr of total reactions AND nr of reactions who actually follow the user
    
    # w.r.t. nr of total reactions (highest to lowest)
    thread_dictionaries_by_reactions = sorted(thread_dictionaries, key=lambda d: d['no_of_reactions'], reverse=True)
    
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

    thread_dictionaries_by_following = sorted(thread_dictionaries, key=lambda d: d['nr_of_reactions_following_source'], reverse=True)

    # Iterate all threads and combine all reactions into one
    all_reactions = []
    for t in thread_dictionaries:
        reactions = t.get("reactions")
        for r in reactions:
            all_reactions.append(r)
    plot_reactions(all_reactions, event_name)

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

    plot_reactions_accumulative(nonrumour_reactions, event_name, rumour="-nonrumour-accumulative")
    plot_reactions_accumulative(rumour_reactions, event_name, rumour="-rumour-accumulative")

    plot_reactions(nonrumour_reactions, event_name, rumour="-nonrumour")
    plot_reactions(rumour_reactions, event_name, rumour="-rumour")

    plot_reactions_daily(nonrumour_reactions, event_name, rumour="-nonrumour")
    plot_reactions_daily(rumour_reactions, event_name, rumour="-rumour")

    # Daily plot
    #plot_reactions_daily(nonrumour_reactions, event_name, rumour="-nonrumour")
    #plot_reactions_daily(rumour_reactions, event_name, rumour="-rumour")

    # TODO: Make use of these two sorted thread dictionaries for this event
    thread_dictionaries_by_following 
    thread_dictionaries_by_reactions 
    # select top 5 threads, when were the reactions after initial source tweet
    # do the same for top 5 threads
    
    # Currently, I combine all reactions into one then plot. Make a different script 
    # Do the reaction plotting thread by thread source tweet: checking how a source tweets timestamp effects amount of reactions
    # compare by visualisation and number
    # When was the peak for the tweet: an hour later? or 10 minutes
    # Peak: increases 


    