from datetime import datetime, timedelta
from qgis.core import *
import qgis.utils
import itertools

from spd import *

# Define a function to merge the correspond indices of two lists
def merge(lst1, lst2):
    return [[a , b] for (a, b) in zip(lst1, lst2)]

def group_spd_based_on_time(layers , distThresh, timeThresh,stay_time_thresh):
    # For each layer the SPD is calculated and store in a list
    trajectories_spd = []
    for i in range(0,len(layers)):
        trajectories_spd.append(stay_point_detection(layers[i],dist_thresh,time_thresh))

    # If not find any SPD
    if len(trajectories_spd) == 0:
        return 1



    # separate geometries arrival time and leave time
    # Initialize variables
    geometries_spd = []
    arrival_time_spd = []
    leave_time_spd = []


    # Iterates over the trajectories_spd list and put each category in
    # its correspond list
    for i in range(0,len(trajectories_spd)):
        geometries_spd.append(trajectories_spd[i][0])
        for j in range(0,len(trajectories_spd)):
            if isinstance(trajectories_spd[i][j],datetime):
                arrival_time_spd.append(trajectories_spd[i][j])
                break
        leave_time_spd.append(trajectories_spd[i][j+1])


    # Compute the delta time in seconds for each trajectory
    # leave_time_spd - arrival_time_spd in corresponding list items
    delta_times = []
    for i in range(0,len(arrival_time_spd)):
        # The result will be a datetime.deltatime in python date time
        delta_times.append(leave_time_spd[i] -arrival_time_spd[i])


    # We need to get the property 'seconds' of deltatimes
    delta_times_seconds = []
    for i in range(0,len(delta_times)):
        delta_times_seconds.append(delta_times[i].seconds)



    # For each trajectory we need to compute the difference time between them
    timeDifference = []
    counter = 0
    sum = 0

    # The algorithm bellow illustrates how we can compute the difference of time between trajectories
    # Use cartesian product to subtract the time of each trajectory with the others in the list
    # Store a result of each time difference of trajectory with others in new list
    for p1,p2 in itertools.product(delta_times_seconds,repeat = 2):
        if counter == len(delta_times_seconds):
            counter = 0
        if counter < len(delta_times_seconds):
            sum = sum + abs(p1 - p2)
            counter = counter + 1
            if counter == len(delta_times_seconds):
                timeDifference.append(sum)
                sum = 0

    # Merge the correspond geometries with its time difference
    # Call the merge function that the output will be a merged list
    # The result will be a 2D List with the structure
    # [[geom object, time difference],[...],[...],[...],...,[...]]
    merge_g_t = []
    merge_g_t = merge(geometries_spd , timeDifference)

    # Extract the points with less than the stay time threshold
    result = []

    for i in range(0,len(merge_g_t)):
        for j in range(0,len(merge_g_t[i])):
            if (isinstance(merge_g_t[i][j],int)==True and merge_g_t[i][j] <= stay_time_thresh):
                    result.append(merge_g_t[i][j-1])
                    break

    return result

# Preliminaries to run the algorithm
trajectory_layers = ["person_57", "person_67", "person_68"]
dist_thresh = 1.2
time_thresh = 2 * 60
stay_time_thresh = 35
stp = []
stp = groupSPDBasedOnTime(trajectory_layers ,dist_thresh , time_thresh, stay_time_thresh )


# Check the result and show them as a layer in QGIS
if len(stp) <= 0:
    print("No stay point detected ")
else :
    # Extract only geometries, NOT timestamps and show them on QGIS
    for geometry in stp:
        
            geometry_Layer = QgsVectorLayer(f"?query=SELECT ST_GeomFromText('{geometry.asWkt()}')",
            f"trajectory {trajectory_layers}, dist_thresh {dist_thresh} ,
             time_thresh {time_thresh}, stay_time_thresh = {stay_time_thresh}", "virtual")
            geometry_Layer.renderer().symbol().setSize(6)
            QgsProject.instance().addMapLayer(geometry_Layer)
            
    