from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib import dates
from math import ceil



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

    # Plot the axis
    file_name = event_name + rumour
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("(Accumulative) No. of reactions")
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color='red')
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")

    # Print out the peak time and peak value
    peak_time = x_axis[y_axis.index(max(y_axis))]
    peak_value = max(y_axis)
    print("Peak time: " + str(peak_time))
    print("Peak value: " + str(peak_value))


def plot_reactions(reactions, event_name, is_rumour_thread, rumour=""):

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

    # Plot the axis
    file_name = event_name + rumour
    plt.title(file_name)
    plt.xlabel("Timestamps")
    plt.ylabel("No. of reactions")
    color = 'red' if is_rumour_thread else 'blue'
    plt.plot_date(x_axis, y_axis, linestyle='solid', markersize=2, color=color)
    plt.gcf().autofmt_xdate()
    plt.tight_layout()
    plt.savefig(file_name)
    plt.close()
    print(file_name + "saved.")

    # Print out source tweet time
    first_time = x_axis[0]
    print("Source time: " + str(first_time))

    # Print out the peak time and peak value
    peak_time = x_axis[y_axis.index(max(y_axis))]
    peak_value = max(y_axis)
    print("Peak time: " + str(peak_time))
    print("Peak value: " + str(peak_value))

    # Print out time difference between first_time and peak_time
    time_diff = peak_time - first_time
    print("Time from source to peak: " + str(time_diff))


#  Plots given reactions with timestamps on given filename
#  Accumulative


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

        # Plot
        file_name = event_name + rumour
        plt.title(file_name)
        plt.xlabel("Timestamps")
        plt.ylabel("No. of reactions")
        plt.plot_date(x_axis, y_axis, linestyle='solid',
                      markersize=2, color='red')
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
        # Print out the peak time and peak value
        peak_time = x_axis[y_axis.index(max(y_axis))]
        peak_value = max(y_axis)
        print("Peak time: " + str(peak_time))
        print("Peak value: " + str(peak_value))


