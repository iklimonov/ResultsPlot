import os
import copy
import numpy as np
from Modules.myGraph import myGraph

from Modules.Utils.utils import getOrderedZones
from Modules.Utils.utils import getZonesindexes
from Modules.Utils.utils import processFolder
from Modules.Utils.utils import unique

from Modules.Utils.utils import dataSmoothing
from Modules.Utils.utils import exponential_smoothing
from Modules.Utils.utils import simple_smoothing
from Modules.Utils.utils import plotResultsFolder

from Modules.processing import processingTimeType


class transientDataSet():
    """description of class"""
    DataClass = ""
    Module = ""
    tData = []
    xData = []
    xLabel = ""
    yLabel = ""

    def __init__(self, ModuleName, DataName):
        self.Module = ModuleName
        self.DataClass = DataName

    def setTimeTable(self, tData):
        self.tData = list(tData)

    def setValueTable(self, xData):
        self.xData = list(xData)

    def getDataClass(self):
        return self.DataClass

    def getTimeTable(self):
         return list(self.tData)

    def getValueTable(self):
        return list(self.xData)

    def setXLabel(self, label):
        self.xLabel = label

    def setYLabel(self, label):
        self.yLabel = label

    def getXLabel(self):
        return self.xLabel

    def getYLabel(self):
        return self.yLabel

class transienSpaceDataSet():
    """description of class"""
    DataClass = ""
    Module = ""
    tData = []
    xMapData = []
    xMapSize = 0
    grid = []
    xLabel = ""
    yLabel = ""
    ###t[i] x[i] = [a1,a2,....]

    def __init__(self, ModuleName, DataName):
        self.Module = ModuleName
        self.DataClass = DataName

    def get_mapSize(self):
        return self.xMapSize

    def setTimeTable(self, tData):
        self.tData = list(tData)

    def setGrid(self, grid):
        self.grid = list(grid)
        self.xMapSize = len(self.grid)


    def setValueTable(self, xData):
        self.xMapData = list(xData)

    def getTimeTable(self):
         return list(self.tData)

    def getValueTable(self):
        return list(self.xMapData)

    def getGrid(self):
        return list(self.grid)

    def setXLabel(self, label):
        self.xLabel = label

    def setYLabel(self, label):
        self.yLabel = label

    def getXLabel(self):
        return self.xLabel

    def getYLabel(self):
        return self.yLabel


class zoneData():
    id = 0
    name =""
    axialCellNumber = 0
    NumberOfTVS = 0
    NumberOfTvels = 0

    transientData = []
    transientSpaceData = []
    def __init__(self, ZoneId, PlotGroup, ZoneName, ZoneAxialCellNumber, TVS_number, tvel_number):
        self.id = ZoneId
        self.plotGroup = PlotGroup
        self.name = ZoneName
        self.axialCellNumber = ZoneAxialCellNumber
        self.NumberOfTVS = TVS_number
        self.NumberOfTvels = tvel_number
        self.transientData = []
        self.transientSpaceData = []

    def addData(self, data, dataType):
        if dataType == "time" :
            self.transientData.append(data)
        if dataType == "space" :
            self.transientSpaceData.append(data)

    def getZoneId(self):
        return self.id

    def getDataByDataName(self, dataName):
        data_list = []
        for data in self.transientData:
            if dataName == data.DataClass:
                data_list.append(copy.copy(data))
        if len(data_list) > 0 : return data_list

        data_list = []
        for data in self.transientSpaceData:
            if dataName == data.DataClass:
                data_list.append(copy.copy(data))
        if len(data_list) > 0 : return data_list

        print("No data for " + dataName + " for " + self.name)
        return None


def get_graphParameters(CORE_data, graphName):
    for graphParameter in CORE_data["data"]:
        if graphParameter["name"] == graphName:
            return graphParameter
    return None


class CoreDataModule():   
    zones = []

    def __init__(self):
        self.zones = []

    def addZone(self, zone):
        self.zones.append(zone)

    def getZoneByName(self, zone_name):
        for zone in self.zones:
            if zone.name == zone_name :
                return zone


    def addDataToZone(self, zoneName, dataToZone, dataType):
        myZone = self.getZoneByName(zoneName)
        myZone.addData(dataToZone, dataType)

    def plotCombinedMaxTemperatureForTvel(self, berkut_module, berkut_data_group, safr_data_group, myOut):

        #berkut_data_group = "tvelMaxFuelTemperature"
        #safr_data_group = "MaxTemperature_fuel"

        myOrderedZones = []
                
        for zone in self.zones:
            myZone = []
            myZone.append(zone.plotGroup)
            myZone.append(zone.name)
            myOrderedZones.append(myZone)

        myOrderedGroups = []

        for zone in myOrderedZones:
            myOrderedGroups.append(zone[0])

        myOrderedGroups = unique(myOrderedGroups)

        #myOrderedZones = getOrderedZones(self.zones)
        #myOrderedGroups = getZonesindexes(myOrderedZones)

        dataForHZone = []
        legendForHZone = []
        idForHZone = []
        for orderedGroup in myOrderedGroups:
            dataForHZone.append([])
            legendForHZone.append([])
            idForHZone.append([])

        resultsGroup = None
        for gr in berkut_module["data"]:
            if gr["name"] == berkut_data_group:
                resultsGroup = copy.copy(gr)
                break

        resultsGroup["graphParameters"]["xMultiplicator"] = 1.0
        resultsGroup["graphParameters"]["yMultiplicator"] = 1.0
        resultsGroup["graphParameters"]["xAddendum"] = 0.0
        resultsGroup["graphParameters"]["yAddendum"] = 0.0

        module_name = "SAFR"

        resultsGroupName = resultsGroup["name"]
        subfolder = plotResultsFolder + '/' + module_name + '/' + resultsGroupName
        #subfolder = os.path.join(plotResultsFolder, module_name, resultsGroupName)
        processFolder(subfolder)


        for zone in self.zones:

            zone_name = zone.name

            print("Processing " + berkut_data_group + " in " + zone_name)

            #zoneHid = int(str(zone.id)[0])-1
            zoneHid = zone.plotGroup-1

            max_fuel_temp_safr = zone.getDataByDataName(safr_data_group)
            max_fuel_temp_berkut = zone.getDataByDataName(berkut_data_group)

            time_table_berkut = list(max_fuel_temp_berkut[0].getTimeTable())
            data_table_berkut = list(max_fuel_temp_berkut[0].getValueTable())

            global_dataEnd = []

            if max_fuel_temp_safr == None :
                global_data = []

                mergeIndex = 0
                #добавляем данные БЕРКУТ
                i = 0
                while i < len(time_table_berkut):
                    loc_data = [time_table_berkut[i],data_table_berkut[i]]
                    global_data.append(loc_data)
                    i+=1

                global_dataEnd = list(global_data)
            else:
                #####################################################################################################
                # у сафра может быть несколько материалов с топливом, которые появляются в разное время (диссоциация)
                # размерности списков температур могут быть разными для сафра
                Nmaterials = len(max_fuel_temp_safr)
                LengthMaterialsData = []

                indexOfLengthData = 0
                maxLength = 0
                i = 0
                while i < Nmaterials:
                    data_length = len(max_fuel_temp_safr[i].getValueTable())
                    if data_length > maxLength:
                        maxLength = data_length
                        indexOfLengthData = i
                    loc_data = [data_length, list(max_fuel_temp_safr[i].getTimeTable()), list(max_fuel_temp_safr[i].getValueTable())]
                    LengthMaterialsData.append(loc_data)
                    i+=1
            

                i = 0
                while i < Nmaterials:
                    if i != indexOfLengthData:
                        dataLengthOfi = LengthMaterialsData[i][0]
                        dataLengthOfCommon = LengthMaterialsData[indexOfLengthData][0]
                        segmentLength = min(dataLengthOfi, dataLengthOfCommon)
                        j = 1
                        while j <= segmentLength:
                            LengthMaterialsData[indexOfLengthData][2][dataLengthOfCommon - j] = max( LengthMaterialsData[indexOfLengthData][2][dataLengthOfCommon - j],  LengthMaterialsData[i][2][dataLengthOfi - j])
                            j+=1
                    i+=1


                time_table_safr = list(LengthMaterialsData[indexOfLengthData][1])
                data_table_safr = list(LengthMaterialsData[indexOfLengthData][2])


                #for data in max_fuel_temp_safr:
                #    i = 0
                #    data_table = data.getValueTable()
                #    while i < len(data_table):
                #        data_table_safr[i] = max(data_table_safr[i], data_table[i]) 
                #        i+=1
            
                ########################################################


                global_data = []

                mergeIndex = 0
                #добавляем данные БЕРКУТ
                i = 0
                while i < len(time_table_berkut):
                    if time_table_berkut[i] >= time_table_safr[0]:
                        mergeIndex = i - 1
                        break
                    else:
                        loc_data = [time_table_berkut[i],data_table_berkut[i]]
                        global_data.append(loc_data)
                    i+=1
                #добавляем данные САФР
                i = 0
                while i < len(time_table_safr):
                    loc_data = [time_table_safr[i],data_table_safr[i]]
                    global_data.append(loc_data)
                    i+=1
            
                #################### сглаживание ##################

                #global_data = dataSmoothing(global_data)
                #global_data = exponential_smoothing(global_data, 0.2) #, breakPoint = mergeIndex
                simple_smoothing(global_data, mergeIndex, 10)

                global_dataEnd = list(global_data)

                ###################################################

            object_name = module_name + '_' + resultsGroupName + '_' +zone_name

            dataForHZone[zoneHid].append(global_dataEnd)
            legendForHZone[zoneHid].append(zone_name)
            idForHZone[zoneHid].append(zone.id)

            data_to_plot = []
            data_to_plot.append(global_dataEnd)
            data_legends = []
            data_legends.append(resultsGroup["graphParameters"]["legend"])

            myData = transientDataSet(module_name, resultsGroupName)
            processingTimeType(resultsGroup, zone_name, object_name, data_to_plot, data_legends, module_name, myOut, myData)


        #######################
        #myOrderedZones =getOrderedZones(self.zones)
        #myOrderedGroups = getZonesindexes(myOrderedZones)

        groupeName = "hydraulicGroups"
        subfolder = plotResultsFolder + '/' + module_name + '/' + resultsGroupName + '_' + groupeName
        #subfolder = os.path.join(plotResultsFolder, module_name, resultsGroupName + '_' + groupeName)
        processFolder(subfolder)

        for orderedGroup in myOrderedGroups:
            if orderedGroup > len(dataForHZone) :
                break

            object_name_group = module_name + '_' + resultsGroupName + '_' + groupeName + '_' + str(orderedGroup)
            data_to_plot = []
            data_legends = []
            i = 0

            while i < len(dataForHZone[orderedGroup-1]):
                zone_name = legendForHZone[orderedGroup-1][i]
                file_name = ''
                object_name = module_name + '_' + resultsGroupName + '_' +zone_name
                data_to_plot.append(dataForHZone[orderedGroup-1][i])
                data_legends.append("Зона" + ' ' + str(idForHZone[orderedGroup-1][i]))
                i+=1
            #hydr_zone_name = '_hydraulicZone_' +  str(orderedGroup)
            hydr_zone_name = " гидравлическая. Номер " + str(orderedGroup)
            myData = transientDataSet(module_name, resultsGroupName + " гидравлическая. Номер " + str(orderedGroup))
            processingTimeType(resultsGroup, hydr_zone_name, object_name_group, data_to_plot, data_legends, module_name, myOut, myData, add_resultsGroup_folder = '_' + groupeName)



        #######################
        return True



    def plotCoreDataMap(self, graphName, dt_plot, CORE_data, myOut):

        print("Processing " + graphName + "MapInTime")
        graphParameter = get_graphParameters(CORE_data, graphName + "MapInTime")

        tvs_zones_name = graphParameter["tvsZoneNames"]
        axial_cell_center_zones= graphParameter["zoneAxialCellCenters"]

        colorBarScheme = graphParameter["graphParameters"]["colorBarScheme"]

        picture_title = graphParameter["graphParameters"]["colorBarScheme"]
        picture_xlabel = graphParameter["graphParameters"]["xLabel"]
        picture_ylabel = graphParameter["graphParameters"]["yLabel"]
        colorbar_label = graphParameter["graphParameters"]["colorBarLabel"]

        xMajorTicks = graphParameter["graphParameters"]["yMajorTicks"]
        xMinorTicks = graphParameter["graphParameters"]["yMinorTicks"]
        colorBarTicks = graphParameter["graphParameters"]["colorBarTicks"]

        isUserLimits = False
        if graphParameter["graphParameters"]["userLimits"] =="Yes":
            isUserLimits = True
        limitMin = graphParameter["graphParameters"]["limitMin"]
        limitMax = graphParameter["graphParameters"]["limitMax"]

        ##########################

        zone_ids = []
        for zone in self.zones:
            zone_ids.append(str(zone.getZoneId()))

        myData = self.zones[0].getDataByDataName(graphName)
        if len(myData) == 1: myData = myData[0] # в данном случае не должно быть одинаковых данных

        time_table = myData.getTimeTable()
        data_length = len(time_table)
        axialGrid = myData.getGrid()

        value_table_size = len(myData.getValueTable()[0])

        t = 0
        while t < data_length: # цикл по времени

            time = time_table[t]

            array_of_data = []
            for i in range(value_table_size):
                new_line = []
                array_of_data.append(new_line)

            for zone in self.zones:
                myData = zone.getDataByDataName(graphName)
                if len(myData) == 1: myData = myData[0] # в данном случае не должно быть одинаковых данных
                zone_data = myData.getValueTable()
                i=0
                while i < value_table_size:
                    array_of_data[i].append(zone_data[t][i])
                    i+=1

            array_of_data = np.array(array_of_data)

            picture_title = graphParameter["title"] + " в " + str(round(time,3)) + " секунду"
            output_name = graphName + "MapInTime" + "_" + str(round(time,3))
            output_path = plotResultsFolder + '/' +  CORE_data["module"] + "/" + graphName + "MapInTime"
            #output_path = os.path.join(plotResultsFolder, CORE_data["module"], graphName + "MapInTime")
            my_Graph = myGraph("1","2")
            my_Graph.plotColoredMap(array_of_data, zone_ids, tvs_zones_name, axialGrid, axial_cell_center_zones,
                       picture_title, picture_xlabel, picture_ylabel, colorbar_label, colorBarScheme,
                      xMajorTicks, xMinorTicks, colorBarTicks, isUserLimits, limitMin, limitMax,
                      output_name, output_path)

            pic_url = output_path + '/' + output_name + '.png'
            myOut.addFigure(CORE_data["module"],graphName + "MapInTime", graphParameter["title"] ,pic_url, picture_title)

            if dt_plot > 0.0:
                next_time = time + dt_plot
                current_time = time
                while current_time < next_time and t < data_length-1:
                    t+=1
                    current_time = time_table[t]
                if t!= data_length-1: t-=1

            t+=1

 
class commonDataModule():
    transientData = []
    transientSpaceData = []

    def __init__(self):
        self.transientData = []
        self.transientSpaceData = []

    def addData(self, data, dataType):
        if dataType == "time" :
            self.transientData.append(data)
        if dataType == "space" :
            self.transientSpaceData.append(data)

    def getDataByDataName(self,dataName):
        for data in self.transientData:
            if dataName == data.getDataClass():
                return data
        return None

    def plotTwoLines(self, graph_one, graph_two, module_data, myOut):


        #firs_graph = self.getDataByDataName(graph_one)
        #second_graph = self.getDataByDataName(graph_two)

        #lines = []

        #my_Line1 = myLine(firs_graph.getTimeTable(),firs_graph.getValueTable())
        #my_Line1.set_label("Расход в ПТО")
        #my_Line1.set_lineWidth(2)
        #my_Line1.set_color("black")
        #my_Line1.set_lineStyle("-")
        #lines.append(my_Line1)

        #my_Line2 = myLine(second_graph.getTimeTable(),second_graph.getValueTable())
        #my_Line2.set_label("Расход в а.з.")
        #my_Line2.set_lineWidth(2)
        #my_Line2.set_color("red")
        #my_Line2.set_lineStyle("-")
        #lines.append(my_Line2)


        #pathToFolder = module + '/' + resultsGroup["name"]

        #my_Graph.plot(lines ,object_name, pathToFolder)

        #pic_url = pathToFolder + '/' + object_name + '.png'
        #myOut.addFigure(module,resultsGroup["name"],resultsGroup["title"],pic_url,parameters["title"] + zone_name + add_to_title)

        return 0


class DataBase():
    Fuel = ""
    AccidentType = ""

    CoreData = None
    NeutronicsData = None
    FirstLoopData = None
    SecondLoopData = None

    def __init__(self, Fuel, AccidentType):
        self.Fuel = Fuel
        self.AccidentType = AccidentType

        self.CoreData = None
        self.NeutronicsData = []
        self.FirstLoopData = []
        self.SecondLoopData = []

    def set_CoreData(self, myCore):
        self.CoreData = myCore

    def set_NeutronicsData(self, myNeutronics):
        self.Neutronics.append(myNeutronics)

    def set_FirstLoopData(self, myFirstLoopData):
        self.FirstLoopData.append(myFirstLoopData)

    def set_SecondLoopData(self, mySecondLoopData):
        self.SecondLoopData.append(mySecondLoopData)