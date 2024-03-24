# Import required libraries
from datetime import datetime
from qgis.core import *
import qgis.utils
import itertools


# Constants (Adjust as needed)
TIMESTAMP_FORMAT = '%Y/%m/%d %H:%M:%S.%f'

# ------------------ Helper Functions ------------------
def calculate_time_span(feature_i, feature_j):
    time_i = datetime.strptime(feature_i.attributes()[0], TIMESTAMP_FORMAT)
    time_j = datetime.strptime(feature_j.attributes()[0], TIMESTAMP_FORMAT)
    return time_j - time_i

def calculate_mean_coord(feature_i, feature_j):
    geom_i = feature_i.geometry().asPoint()
    geom_j = feature_j.geometry().asPoint()
    return QgsPoint((geom_i.x() + geom_j.x()) / 2, (geom_i.y() + geom_j.y()) / 2)

    
  
# ------------------ Main Algorithm ------------------
def stay_point_detection(layer_name, distance_threshold, time_threshold):
    layer = QgsProject.instance().mapLayersByName(layer_name)[0]
    stay_points = []

    features = layer.getFeatures()
    for i, feature_i in enumerate(features):
        for feature_j in itertools.islice(features, i + 1, None):
            distance = feature_i.geometry().distance(feature_j.geometry())
            if distance > distance_threshold:
                time_span = calculate_time_span(feature_i, feature_j)
                if time_span.seconds > time_threshold:
                    mean_coord = calculate_mean_coord(feature_i, feature_j)
                    arrival_time = feature_i.attributes()[0]
                    departure_time = feature_j.attributes()[0]
                    stay_points.append((mean_coord, arrival_time, departure_time))  # Store as tuple
                    break

    return stay_points



# ------------------ Usage Example ------------------
trajectory_layer = "person_67"  # Replace with your layer name
dist_thresh = 1.2
time_thresh = 30

stay_points = stay_point_detection(trajectory_layer, dist_thresh, time_thresh)

if not stay_points:  # Check if any stay points were found
    print("No stay point detected ")
    print(datetime.now())
else :
    # Display stay points on QGIS
    for geometry, arrival_time, departure_time in stay_points:
        geometry_layer = QgsVectorLayer(f"?query=SELECT ST_GeomFromText('{geometry.asWkt()}')",
                                        f"trajectory {trajectory_layer}, dist_thresh {dist_thresh} , time_thresh {time_thresh}",
                                        "virtual")
        geometry_layer.renderer().symbol().setSize(6)
        QgsProject.instance().addMapLayer(geometry_layer)
        print(datetime.now())
            

    
    