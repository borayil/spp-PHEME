from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates
from math import ceil
import os
import networkx as nx
from math import sqrt

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
    x_axis = [start_time + timedelta(minutes=x * min_interval)
              for x in range(number_of_intervals+1)]

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

    # Outputting the files
    file_name = rumour

    # Make output directory
    path_to_output = os.path.join(".", file_name)

    # Create output directory if it does not exist
    if (not os.path.isdir(path_to_output)):
        os.mkdir(path_to_output)
    os.chdir(path_to_output)

    # Save the plot
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("(Accumulative) No. of reactions")
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")

    # Create a text file with the same name as the plot
    with open(file_name + ".txt", "w") as f:
        first_time = x_axis[0]
        peak_time = x_axis[y_axis.index(max(y_axis))]
        peak_value = max(y_axis)
        time_diff = peak_time - first_time
        last_activity_time = x_axis[y_axis.index(1)]
        f.write("Time interval used: " + str(min_interval) + " minutes" + "\n")
        print("Time interval used: " + str(min_interval) + " minutes")
        f.write("First time: " + str(first_time) + "\n")
        f.write("Peak time: " + str(peak_time) + "\n")
        f.write("Peak value: " + str(peak_value) + "\n")
        f.write("Last activity time: " + str(last_activity_time) + "\n")
        f.write("Time from source to peak: " + str(time_diff) + "\n")
        print("Source time: " + str(first_time))
        print("Peak time: " + str(peak_time))
        print("Peak value: " + str(peak_value))
        print("Last activity time: " + str(last_activity_time))
        print("Time from source to peak: " + str(time_diff))

    # Go back one directory
    os.chdir("..")
    
    # Print art denoting end
    print("====================================")


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
    min_interval = 5
    number_of_intervals = ceil(elapsed / timedelta(minutes=min_interval))
    x_axis = [start_time + timedelta(minutes=x * min_interval)
              for x in range(number_of_intervals+1)]

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

    # Outputting the files
    file_name = rumour

    # Make output directory
    path_to_output = os.path.join(".", file_name)

    # Create output directory if it does not exist
    if (not os.path.isdir(path_to_output)):
        os.mkdir(path_to_output)
    os.chdir(path_to_output)

    # Save the plot
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("No. of reactions")
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")

    # Create a text file with the same name as the plot
    with open(file_name + ".txt", "w") as f:
        first_time = x_axis[0]
        peak_time = x_axis[y_axis.index(max(y_axis))]
        peak_value = max(y_axis)
        time_diff = peak_time - first_time
        last_activity_time = x_axis[y_axis.index(1)]
        f.write("Source time: " + str(first_time) + "\n")
        f.write("Time interval used: " + str(min_interval) + " minutes" + "\n")
        print("Time interval used: " + str(min_interval) + " minutes")
        f.write("Peak time: " + str(peak_time) + "\n")
        f.write("Peak value: " + str(peak_value) + "\n")
        f.write("Last activity time: " + str(last_activity_time) + "\n")
        f.write("Time from source to peak: " + str(time_diff) + "\n")
        print("Source time: " + str(first_time))
        print("Peak time: " + str(peak_time))
        print("Peak value: " + str(peak_value))
        print("Last activity time: " + str(last_activity_time))
        print("Time from source to peak: " + str(time_diff))


    # Go back one directory
    os.chdir("..")

    # Print art denoting end
    print("====================================")


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
        x_axis = [curr_day + timedelta(minutes=x * min_interval)
                  for x in range(number_of_intervals+1)]
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
        
        # Init this days file name
        file_name = rumour + curr_day.strftime("%m-%d-%Y")

        # Make output directory
        path_to_output = os.path.join(".", file_name)

        # Create output directory if it does not exist
        if (not os.path.isdir(path_to_output)):
            os.mkdir(path_to_output)
        os.chdir(path_to_output)

        # Plot
        plt.title(file_name)
        plt.xlabel("Timestamps")
        plt.ylabel("No. of reactions")
        plt.plot_date(x_axis, y_axis, linestyle='solid',
                      markersize=2, color='red')
        plt.gcf().autofmt_xdate()
        plt.tight_layout()
        plt.savefig(file_name)
        plt.close()

        # Go to next day
        curr_day += timedelta(days=1)

        # Go back one directory
        os.chdir("..")

def plot_ego_graph(thread, event_name, k=0.4, scale=2, iterations=215):


        # Draw NetworkX Ego graph for each thread

        # Start by reading who-follows-whom.dat with built in read_edgelist function
        thread_id = thread.get("thread_id")
        path_to_who_follows_whom = os.path.join('..', '..', '..', '..','PhemeDataset', 'threads', 
        'en',event_name,thread_id,'who-follows-whom.dat')
        
        if (not os.path.isfile(path_to_who_follows_whom)):
            return
        g = None
        g = nx.read_edgelist(path_to_who_follows_whom, create_using=nx.Graph(), nodetype=int)
        
        plt.axis('off')

        # Make networkx graph bigger
        #plt.figure(figsize=(12,12))



        # Draw ego graph where source is the center and node size is proportional to centrality
        source_id = thread.get("source_tweet").get("user").get("id")
        source_id = source_id

        # Get centrality for sizing
        centrality = nx.degree_centrality(g)
        centrality = [min(1 + (v * 500), 3000) for v in centrality.values()]

        # Create color map
        color_map = []
        for node in g:
            if node == source_id:
                color_map.append('green')
            else: 
                color_map.append('#1f78b4')
        
        # Set layout
        sp = nx.spring_layout(g, k=k, scale=scale, iterations=iterations)
       
        nx.draw_networkx_nodes(g, pos=sp,
        node_color=color_map,
        node_size=centrality,
        edgecolors = 'black')

        nx.draw_networkx_edges(g, pos=sp, node_size=centrality,
        arrows=False, width=0.3, edge_color='brown', alpha=0.8)
        save_name = 'ego-graph-' + thread_id + '.png'

        # Set title of plot to thread_id and number of nodes and edges
        plt.title(thread_id + " (" + str(g.number_of_nodes()) + " nodes, " + str(g.number_of_edges()) + " edges)")

        
        plt.savefig(save_name, dpi=250)
        plt.clf()

        # Print that plot has been saved
        print("Saved " + save_name)


