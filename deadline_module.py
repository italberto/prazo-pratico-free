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
    deadline_init = datetime.datetime(int(deadlines['init']['year']), int(deadlines['init']['month']), int(deadlines['init']['day']), int(deadlines['init']['hour']), int(deadlines['init']['min']))
    deadline_end  = datetime.datetime(int(deadlines['end']['year']), int(deadlines['end']['month']), int(deadlines['end']['day']), int(deadlines['end']['hour']), int(deadlines['end']['min']))

    hours_total = (deadline_end - deadline_init).days

    time_actual = datetime.datetime.now() - datetime.timedelta(hours=3)

    hours_restant = (deadline_end - time_actual).days


    percent = 100.0 - ((hours_restant * 100.0) / hours_total)

    if percent > 100:
        return 100.0
    elif percent < 0:
        return 0.0
    return percent
