# Description: Main script for the longitudinal analysis and other visualizations of the Pheme dataset
import os
import networkx as nx
import json
import requests
import scipy # For matrix convertion error with networkx
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates
from plotting import plot_reactions_accumulative, plot_reactions, plot_reactions_daily, plot_ego_graph
import tarfile

#  All event names in PHEME dataset
ALL_EVENT_NAMES = ['charliehebdo', 'ebola-essien', 'ferguson', 'germanwings-crash', 'ottawashooting',
               'prince-toronto', 'putinmissing', 'sydneysiege']

# For all names, see above of this file (ALL_EVENT_NAMES)
# Decide on the event names to be used 
event_names = ['charliehebdo', 'ferguson', 'sydneysiege']
print('Using the following events: ' + str(event_names))

# Check if Pheme dataset is present
url = 'https://ndownloader.figshare.com/files/4988998'
target_path = 'phemerumourschemedataset.tar.bz2'
if (not os.path.isdir(os.path.join('.', 'PhemeDataset'))):
    # Download dataset, and unzip it.
    try:
        print('Pheme dataset not found in current directory. Downloading from ' + url)
        print('This may take a few minutes (129.89 MB to be downloaded and extracted)')
        response = requests.get(url, stream=True)
        file = tarfile.open(fileobj=response.raw, mode="r|bz2")
        file.extractall(path=".")
        # Rename the extracted directory
        os.rename('pheme-rumour-scheme-dataset', 'PhemeDataset')
        print('Pheme dataset downloaded and extracted successfully.')
    except Exception as e:
        print('Could not download and extract Pheme dataset. Please download it manually from ' + url + ' and extract it to the current directory. Then rename it to "PhemeDataset".')
        print('Error: ' + str(e))
    exit()
else:
    print('Pheme dataset found in current directory. Continuing...')

# Iterate over all events
for event_name in event_names:
    print('Processing event: ' + event_name)
    # Create output directory if it doesn't exist
    path_to_output = os.path.join('.', 'output')
    if (not os.path.isdir(path_to_output)):
        os.mkdir(path_to_output)
        

    # Create a new directory for the this events output if it doesn't exist
    path_to_output = os.path.join('.', 'output', event_name)
    if (not os.path.isdir(path_to_output)):
        os.mkdir(path_to_output)
    
    # Change into the output directory
    os.chdir(path_to_output)

    # Initialize our data structures
    follow_tuples = []
    user_follow_dictionary = {}
    user_follow_list = []
    source_user_ids = []
    thread_dictionaries = []

    # Formulate the path to the event
    path_to_event = os.path.join(
        '..', '..', 'PhemeDataset', 'threads', 'en', event_name)

    # Store all source user ids, for later use
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

    # Iterate over all threads
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

        # From follow tuples, create a dictionary of users and their followers and following
        # We use a dictionary to make it easier to index via id
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

        # Form the dictionary for the current thread being processed, using the above data that we have read in
        thread_dictionary = {
            'thread_id': thread_id,  # same as source_tweet id
            'source_tweet': source_tweet,
            'no_of_reactions': len(reactions),
            'reactions': reactions,
            'annotation': annotation,
            'user_follow_dictionary': user_follow_dictionary,
        }

        # Add this current thread's dictionary to the list collection of all threads, named thread_dictionaries
        thread_dictionaries.append(thread_dictionary)

    # Print out that we have read in all threads
    print("Read in all threads from JSON files :)")

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

    # Seperately plot rumour and nonrumour reactions
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

    # Name of folder to store upcoming plots
    folder_name = "accumulative"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)

    plot_reactions_accumulative(
        nonrumour_reactions, event_name, rumour="nonrumour-accumulative")
    plot_reactions_accumulative(
        rumour_reactions, event_name, rumour="rumour-accumulative")
    
    # Go back to parent folder
    os.chdir("..")

    # Name of folder to store upcoming plots
    folder_name = "interval"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)

    plot_reactions(nonrumour_reactions, event_name, rumour="nonrumour")
    plot_reactions(rumour_reactions, event_name, rumour="rumour")


    # Name of folder to store upcoming plots
    folder_name = "interval-top-5-by-reactions"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)
    #  Add source tweet amongst reactions, so first reaction is source tweet
    #  Get first 5 threads from thread_dictionaries_by_reactions by index
    top5_thread_dictionaries_by_reactions = thread_dictionaries_by_reactions[:5]
    no = 1
    print('=== BY REACTIONS ===')
    for t in top5_thread_dictionaries_by_reactions:
        # Note source time in report

        # For each thread t, get the reactions
        reactions = t.get("reactions")
        reactions.append(t.get("source_tweet"))
        plot_reactions(reactions, event_name,
                       rumour="top-reactions-no-"+str(no)+"-"+t.get("thread_id"))
        no += 1
    os.chdir("..")

    # Name of folder to store upcoming plots
    folder_name = "interval-top-5-by-following"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)
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
                       rumour="top-following-no-"+str(no)+"-"+t.get("thread_id"))
        no += 1
    os.chdir("..")

    # Go back to parent folder
    os.chdir("..")
    
     # Name of folder to store upcoming plots
    folder_name = "daily"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)

    plot_reactions_daily(nonrumour_reactions, event_name,
                         rumour="nonrumour-daily")
    plot_reactions_daily(rumour_reactions, event_name,
                         rumour="rumour-daily")

    # Go back to parent folder
    os.chdir("..")

    

    # Name of folder to store upcoming plots
    folder_name = "ego-graphs"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)

    # Name of folder to store upcoming plots
    folder_name = "ego-graphs-top-5-by-following"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)
    
    for t in top5_thread_dictionaries_by_following:
        plot_ego_graph(t, event_name)
    os.chdir("..")

    # Name of folder to store upcoming plots
    folder_name = "ego-graphs-top-5-by-reactions"
    # Create folder if it does not exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    os.chdir(folder_name)
    
    # Ego Graphs section 
    for t in top5_thread_dictionaries_by_reactions:
        plot_ego_graph(t, event_name)
    
    # Change back 2 directories to leave ego-graphs folder back to output/event_name
    os.chdir("..")
    os.chdir("..")

    
    # Change back 2 directories to leave output/event_name folder back to root
    os.chdir("..")
    os.chdir("..")

    print("Done processing " + event_name)
print("All events processed")
print("*** END ***")
