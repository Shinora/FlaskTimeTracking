import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path


def extract_data_time_file(filename):
    activities = []
    times = []
    date_format = "%H:%M"
    data = pd.read_csv(filename)
    # reading the CSV file
    # displaying the contents of the CSV file
    print(data)
    rows = data.to_numpy()
    for line in rows:
        print(line[0], " ", line[1], " ", line[2])
        duration = datetime.strptime(line[1], date_format)-datetime.strptime(line[0], date_format)
        activity = line[2]
        if activity in activities:
            idx = activities.index(activity)
            times[idx]+=duration.seconds/3600
        else:
            activities.append(activity)
            times.append(duration.seconds/3600)

    return activities, times


def file_exist(path_to_file):
    return Path(path_to_file).is_file()
        
def max_prev_days():
    today = date.today()
    x = 1
    while True:
        f = (date.today()-timedelta(days=x)).isoformat()
        filename = str(f)+".csv"
        path = "data/"+str(filename)
        if file_exist(path) != True:
            return x
        x+=1
def is_data_today():
    today = date.today()
    f = today.isoformat()
    filename = str(f)+".csv"
    path = "data/"+str(filename)
    return file_exist(path)

def daily_data(date):
    activities, times = extract_data_time_file("data/"+str(date)+".csv")
    return activities, times

def today_data():
    if is_data_today():
        activities, times = daily_data(date.today())
        return activities, times
    else:
        return [], []

def weekly_data():
    total_activities = []
    total_times = []
    start = 0
    if is_data_today() == False:
        start=1
    if max_prev_days() > 6:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, 6)]
    else:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, max_prev_days())]

    for day in days:
        activities, times = daily_data(day)
        for activity in activities:
            idx2 = activities.index(activity)
            if activity in total_activities:
                idx = total_activities.index(activity)
                total_times[idx]+=times[idx2]
            else:
                total_activities.append(activity)
                total_times.append(times[idx2])
    
    return total_activities, total_times

def monthly_data():
    total_activities = []
    total_times = []
    start = 0
    if is_data_today() == False:
        start=1
    if max_prev_days() > 30:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, 30)]
    else:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, max_prev_days())]
    
    for day in days:
        activities, times = daily_data(day)
        for activity in activities:
            idx2 = activities.index(activity)
            if activity in total_activities:
                idx = total_activities.index(activity)
                total_times[idx]+=times[idx2]
            else:
                total_activities.append(activity)
                total_times.append(times[idx2])
    
    return total_activities, total_times

def last_days_data(nb_days):
    total_activities = []
    total_times = []
    start = 0
    if is_data_today() == False:
        start=1
    if max_prev_days() > nb_days:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, nb_days)]
    
    else:
        days = [(date.today()-timedelta(days=x)).isoformat() for x in range(start, max_prev_days())]
    
    for day in days:
        activities, times = daily_data(day)
        for activity in activities:
            idx2 = activities.index(activity)
            if activity in total_activities:
                idx = total_activities.index(activity)
                total_times[idx]+=times[idx2]
            else:
                total_activities.append(activity)
                total_times.append(times[idx2])
    
    return activities, times
