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
    deadline_init = datetime.datetime(deadlines['init']['year'], deadlines['init']['month'], deadlines['init']['day'], deadlines['init']['hour'], deadlines['init']['min'])
    deadline_end  = datetime.datetime(deadlines['end']['year'], deadlines['end']['month'], deadlines['end']['day'], deadlines['end']['hour'], deadlines['end']['min'])

    hours_total = (deadline_end - deadline_init).days

    time_actual = datetime.datetime.now() - datetime.timedelta(hours=3)

    hours_restant = (deadline_end - time_actual).days


    percent = 100.0 - ((hours_restant * 100.0) / hours_total)

    if percent > 100:
        return 100.0
    return percent
