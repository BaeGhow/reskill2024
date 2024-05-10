import glob
from osgeo import ogr

path = r"D:\test_1\test_data\*\*.shp"  #경로 설정
filenames=[]
for filename in glob.glob(path):  #glob.glob(path, recursive=True) 하위폴더도 찾음
    filenames.append(filename)
    
#shp파일 불러오기
sejong = QgsVectorLayer(filenames[0], '세종시', 'ogr')
store = QgsVectorLayer(filenames[1], '편의점', 'ogr')
school = QgsVectorLayer(filenames[2], '초등학교', 'ogr')

#QgsProject.instance().addMapLayer(sejong)
#QgsProject.instance().addMapLayer(conv)
#QgsProject.instance().addMapLayer(elem)

#좌표계 없는 shp파일 재투영
store1 = processing.run("native:reprojectlayer",
    {'INPUT':store, 'TARGET_CRS':'EPSG:5181', 'OUTPUT':'memory:'}
    )['OUTPUT']
    
school1 = processing.run("native:reprojectlayer",
    {'INPUT':school, 'TARGET_CRS':'EPSG:5181', 'OUTPUT':'memory:'}
    )['OUTPUT']

#세종시 기준 초등학교, 편의점 자료 추출
store_clip = processing.run("native:clip", {'INPUT':store1, 'OVERLAY':sejong, 'OUTPUT':'memory:'})['OUTPUT']
school_clip = processing.run("native:clip", {'INPUT':school1, 'OVERLAY':sejong, 'OUTPUT':'memory:'})['OUTPUT']


#세종시 각 초등학교 500m 범위 버퍼 생성
buffersize = QInputDialog.getInt(None, '버퍼', '크기를 입력하세요')[0]
school_buffer = processing.run("native:buffer", 
    {'INPUT':school_clip,'DISTANCE':buffersize,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,
    'DISSOLVE':False,'OUTPUT':'memory:'})['OUTPUT']

#QgsProject.instance().addMapLayer(sejong)
#QgsProject.instance().addMapLayer(store_clip)
#QgsProject.instance().addMapLayer(school_clip)
#QgsProject.instance().addMapLayer(school_buffer)

#500m 내 편의점 갯수 산출
store_count = processing.run("native:countpointsinpolygon", {
        'POLYGONS':school_buffer,
        'POINTS':store_clip,
        'WEIGHT':'',
        'CLASSFIELD':'',
        'FIELD':'NUMPOINTS',
        'OUTPUT':'memory:'})['OUTPUT']
#QgsProject.instance().addMapLayer(store_count)


#헥사 그리드생성
sejong_grid = processing.run("native:creategrid", {
    'TYPE': 4,
    'EXTENT':sejong,
    'HSPACING':500,
    'VSPACING':500,
    'HOVERLAY':0,
    'VOVERLAY':0,
    'CRS':'EPSG:5181',
    'OUTPUT':'memory:'})['OUTPUT']
#QgsProject.instance().addMapLayer(sejong_grid)

sejong_count = processing.run("native:countpointsinpolygon", {
        'POLYGONS':sejong_grid,
        'POINTS':store_clip,
        'WEIGHT':'',
        'CLASSFIELD':'',
        'FIELD':'NUMPOINTS',
        'OUTPUT':'memory:'})['OUTPUT']
#QgsProject.instance().addMapLayer(sejong_count)


sejong_grid_intersect = processing.run("native:extractbylocation", {
    'INPUT': sejong_count,
    'PREDICATE': 0,
    'INTERSECT': sejong,
    'OUTPUT': 'memory:'})['OUTPUT']
QgsProject.instance().addMapLayer(sejong_grid_intersect)
