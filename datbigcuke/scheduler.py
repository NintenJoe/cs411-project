#Functions for scheduling a meeting time for a group
#(by Tom)

from datetime import timedelta, datetime, date, time
import math

#returns a datetime or time representing the
#start of the m minute interval
#in which the given datetime or time t lies
def time_interval_start(t, m):
    minutes = int(m * math.floor(float(t.minute)/m))
    if(type(t) is datetime):
        return datetime(t.year, t.month, t.day, t.hour, minutes)
    if(type(t) is time):
        return time(t.hour, minutes)
    
#computes the possible meeting times
#group_members is a dictionary of members whose
#  keys are identifiers of the member
#  values are lists of 2-tuples,
#    containing a start time (datetime) and end time (datetime)
#  these tell when that group member is unavailable
#deadline is a datetime specifying before when the meeting must occur
#duration is a timedelta specifying how long the meeting should be
#off_limits_start and off_limits_end are times
#  which tell when the meeting should not be scheduled each day
#This function returns a list of 2-tuples describing possible meeting times
#  first value being the time of the meeting
#  second value being a list of group members
#    who are busy at some pointduring the meeting, if any
#  and this list is sorted first by time, then by availability
#
#Important assumptions:
#the off_limits time should cover a day change
#  if not, return an error list
#the earliest schedulable time is an hour from now
def schedule_meeting(group_members, deadline, duration, off_limits_start, off_limits_end):
    
    #check off_limits assumption    
    if(off_limits_start <= off_limits_end):
        return [(deadline, ['error: off limits times are bad'])]
        
    #m is the interval length, this must be 0 < m < 60
    m = 15

    midnight = time(0)
    
    #convert the given times to the intervals they are in
    overall_start = time_interval_start(datetime.now() + timedelta(hours=1, minutes=m), m)
    overall_end = time_interval_start(deadline, m)
    day_start = time_interval_start(off_limits_end, m)
    day_end = time_interval_start(off_limits_start, m)
    
    #create a structure that maps usable time intervals
    #to lists of members busy during that interval
    #and a similar structure that only has fully usable slots of length duration
    #this initializes all usable times to an empty list
    intervals = {}
    options = {}
    
    day = overall_start.date()
    while(day <= overall_end.date()):
        t = day_start
        end = day_end
        #start later on the first day, or end earlier on the last day, if necessary
        if(day == overall_start.date() and t < overall_start.time()):
            t = overall_start.time()
        if(day == overall_end.date() and overall_end.time() < end):
            end = overall_end.time()
            
        while(t < end):
            intervals[datetime.combine(day, t)] = []
            if((datetime.combine(day + timedelta(days=1), midnight) - duration) < datetime.combine(day, t)):
                t = (datetime.combine(day, t) + timedelta(minutes=m)).time()
                continue
            if((datetime.combine(day, t) + duration).time() <= end):
                options[datetime.combine(day, t)] = []
            t = (datetime.combine(day, t) + timedelta(minutes=m)).time()
            
        day = day + timedelta(days=1)
        
    #put busy group members in the appropriate intervals
    for member in group_members:
        for appointment in group_members[member]:
            t = time_interval_start(appointment[0], m)
            end = time_interval_start(appointment[1], m)
            while(t < end):
                if(t in intervals):
                    intervals[t].append(member)
                t = time_interval_start(t + timedelta(minutes=m), m)
                
    #use the intervals to fill the options with busy group members
    for option in options:
        t = option
        end = time_interval_start(option + duration, m)
        while(t < end):
            options[option] += intervals[t]
            t = t + timedelta(minutes=m)
        
    #zip the options into a sortable form
    option_tuples = []
    for option in options:
        option_tuples.append((len(set(options[option])), len(options[option]), option))
        
    #construct the result
    result = []
    for option in sorted(option_tuples):
        result.append((option[2], list(set(options[option[2]]))))
    
    return result
