#coding: utf-8
import datetime
import time

def calc_deadline_percent(deadlines):
    """
        #recieve a dictionary

        deadlines{
            'init' : deadline,
            'end'  : deadline,
            }

        #and return a percentage time of the time left
    """

    time_left = {}

    deadline_init = datetime.datetime(int(deadlines['init']['year']), int(deadlines['init']['month']), int(deadlines['init']['day']), int(deadlines['init']['hour']), int(deadlines['init']['min']))
    deadline_end  = datetime.datetime(int(deadlines['end']['year']), int(deadlines['end']['month']), int(deadlines['end']['day']), int(deadlines['end']['hour']), int(deadlines['end']['min']))

    days_total = ((deadline_end - deadline_init).total_seconds()/3600)/24

    time_actual = datetime.datetime.now() - datetime.timedelta(hours=3)

    days_restant = ((deadline_end - time_actual).total_seconds()/3600)/24

    percent = 100.0 - ((days_restant * 100.0) / days_total)

    if percent > 100:
        time_left['percent_time'] = 100
    elif percent <= 0:
        time_left['percent_time'] =  0
    else:
        time_left['percent_time'] =  int(percent)

    if days_restant < 0:
        time_left['days_left'] = 0
    if days_restant >= 0:
        if days_restant >= 1:
            time_left['days_left'] = int(days_restant)
        if days_restant < 1:
            time_left['days_left'] = round(days_restant, 2)

    return time_left
