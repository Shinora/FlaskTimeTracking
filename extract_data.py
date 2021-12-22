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
    rows = data.to_numpy()
    for line in rows:
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
        path = "data/time/"+str(filename)
        if file_exist(path) != True:
            return x
        x+=1

def is_data_day(day):
    f = day
    filename = str(f)+".csv"
    path = "data/time/"+str(filename)
    return file_exist(path)

def daily_data(date):
    activities, times = extract_data_time_file("data/time/"+str(date)+".csv")
    return activities, times

def today_data():
    today = date.today()
    if is_data_day(today):
        activities, times = daily_data(date.today())
        return activities, times
    else:
        return [], []

def weekly_data():
    total_activities = []
    total_times = []
    valid_days = []

    days = [(date.today()-timedelta(days=x)).isoformat() for x in range(0, 6)]
    for day in days:
        if is_data_day(day):
            valid_days.append(day)

    for day in valid_days:
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
    valid_days = []
    days = [(date.today()-timedelta(days=x)).isoformat() for x in range(0, 30)]
    for day in days:
        if is_data_day(day):
            valid_days.append(day)

    for day in valid_days:
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
    valid_days = []

    days = [(date.today()-timedelta(days=x)).isoformat() for x in range(0, nb_days)]
    for day in days:
        if is_data_day(day):
            valid_days.append(day)

    for day in valid_days:
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


def weekly_data_activity(acitivity_code):
    days = [(date.today()-timedelta(days=x)).isoformat() for x in range(0, 6)]
    days = days[::-1]
    day_time = []
    for day in days:
        if not is_data_day(day):
            day_time.append(0)
        else:
            activities, times = daily_data(day)
            for activity in activities:
                if activity == acitivity_code:
                    idx = activities.index(activity)
                    day_time.append(times[idx])
    
    return days, day_time


def monthly_data_activity(acitivity_code):
    days = [(date.today()-timedelta(days=x)).isoformat() for x in range(0, 30)]
    days = days[::-1]
    day_time = []
    for day in days:
        if not is_data_day(day):
            day_time.append(0)
        else:
            activities, times = daily_data(day)
            for activity in activities:
                if activity == acitivity_code:
                    idx = activities.index(activity)
                    day_time.append(times[idx])
    
    return days, day_time
