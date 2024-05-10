
my_gpkg = r'D:\test_1\test_data\test_a.gpkg'
school = f'{my_gpkg}|layername=XsDB_초등학교_POI_TM' #경로에 있는 것만 담아져 있음
store = f'{my_gpkg}|layername=XsDB_편의점_100M_TM'
sejong = QgsVectorLayer(f'{my_gpkg}|layername=sejong', 'ggg', 'ogr')

QgsProject.instance().addMapLayer(sejong)

#
#iface.addVectorLayer(sejong, "aa", "ogr")
#
  

