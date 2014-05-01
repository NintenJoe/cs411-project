#functions to decide if a deadline should be aggregated
#(by Tom)

from datetime import timedelta, datetime
import numpy as np

#transforms a list of datetimes to a list of integers
#representing those times and returns the new list
#the return list will be a numpy array
#(this representaion is the number of seconds
# since jan 1, 2014)
def transform_to_ints(deadlines):
    begining_of_time = datetime(2014, 1, 1)
    values = []
    for d in deadlines:
        delta = d - begining_of_time
        values.append(delta.seconds + 3600*24 * delta.days)
    return np.array(values)
    

#transforms a integer representation as from above
#back into a datetime and returns it
def transform_to_datetime(rep):
    begining_of_time = datetime(2014, 1, 1)
    delta = timedelta(np.floor(rep / (3600*24)), int(rep % (3600*24)))
    return begining_of_time + delta
    
#given a list of datetimes,
#returns an array of transformed datetimes
#which contains only the deadlines close to a
#discovered central value
def find_central_deadlines(deadlines):
    #calculate besic statics on the deadlines
    transformed_deadlines = np.array(transform_to_ints(deadlines))
    average = np.average(transformed_deadlines)
    deviation = np.std(transformed_deadlines)
    
    print sorted(transformed_deadlines.tolist())
    
    #get a list of just those within one standard deviation
    close_deadlines = []
    for d in transformed_deadlines:
        if d >= average - deviation and d <= average + deviation:
            close_deadlines.append(d)
    close_deadlines = np.array(close_deadlines)
    
    print sorted(close_deadlines.tolist())
    
    #repeat the process again, getting very close deadlines
    close_average = np.average(close_deadlines)
    close_deviation = np.std(close_deadlines)
    very_close_deadlines = []
    for d in close_deadlines:
        if d >= close_average - close_deviation and d <= close_average + close_deviation:
            very_close_deadlines.append(d)
    very_close_deadlines = np.array(very_close_deadlines)
    
    print sorted(very_close_deadlines.tolist())

    #todo: remove after internal aggregation fix
    return False
    return very_close_deadlines
    
#Decides if a deadline should be aggregated
#deadlines is a list of datetimes representing
#all the candidates for the deadline
#threshold is the number of deadlines that must
#lie in the center to cause aggregation
def should_aggregate(deadlines, threshold):
    center = find_central_deadlines(deadlines)
    return len(center) > threshold

#Aggregates a list of datetime deadlines
#returns the datetime deadline that is most
#likely to be the real dealine from this list
def aggregate(deadlines):
    center = find_central_deadlines(deadlines)
    deadline = max(set(center), key=center.tolist().count)

    return transform_to_datetime(deadline)
