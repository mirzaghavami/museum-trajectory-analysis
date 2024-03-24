from Stop import *  # Note: Minimize wildcard imports
from qgis.core import QgsVectorLayer, QgsDataSourceUri

def load_table(uri, table_name, geometry_col):
    uri.setDataSource("public", table_name, geometry_col)
    vlayer = QgsVectorLayer(uri.uri(False), table_name, "postgres")
    QgsProject.instance().addMapLayer(vlayer)

# Database settings
db_settings = {
    "host": "localhost",
    "port": "5432",
    "database": "project_db",
    "user": "postgres",
    "password": "****",
}

geometry_col = "geom"
tables = ["outside_57", "outside_67", "outside_68", "person_57", "person_67", "person_68"]

# Construct the connection URI
uri = QgsDataSourceUri()
uri.setConnection(**db_settings)

# Load tables
for table in tables:
    load_table(uri, table, geometry_col)


