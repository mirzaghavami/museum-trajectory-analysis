
# Will be Modify to adjust
# Example: Outputdir = 'D:/temp/'
Outputdir = ''
layers = iface.mapCanvas().layers()
for layer in layers:
    layerType = layer.type()
    if layerType == QgsMapLayer.VectorLayer:
        print (layer.name())
        QgsVectorFileWriter.writeAsVectorFormat( layer, Outputdir + layer.name() + ".shp", "utf-8", layer.crs(), "ESRI Shapefile" )