from math import ceil
import os
import pandas as pd
import json 
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates

# Reading thread into pandas obj / dataframes which can later on be used however fit
event_name = 'charliehebdo'
follow_tuples = []
user_follow_dictionary = {}
user_follow_list = []
path_to_event = os.path.join('.', 'PhemeDataset', 'threads', 'en', event_name)
for filename in os.listdir(path_to_event):
    thread_id = filename
    path_to_thread = os.path.join(path_to_event,filename)
    assert (not os.path.isfile(path_to_thread)) # Assert that this is a directory, not file
    
    # TODO: Read in and parse who-follows-whom.dat
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
    
    # We used dictionary to make it easier to index via id
    # Now we can turn dictionary to list
    for u in user_follow_dictionary:
        user_dict = user_follow_dictionary[u]
        user_follow_list.append(user_dict)

    for u in user_follow_list:
        u['no_of_followers'] = len(u.get('followers'))

    user_follow_list = sorted(user_follow_list, key=lambda d: d['no_of_followers'], reverse=True)
    i = 0
    for u in user_follow_list:
        i += 1
        if i == 10: break
        print("===")
        print(u)
    exit()
    






