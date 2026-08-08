from Modules.Utils.utils import convert_file_to_list
from Modules.Utils.utils import getRightTimeTableNarabotka
from Modules.Utils.utils import prepare_folders
from Modules.Utils.utils import resultsFolder
from Modules.Utils.utils import get_NameForBERKUT
from Modules.Utils.utils import unique

from Modules.Utils.utils import getOrderedZones
from Modules.Utils.utils import getZonesindexes

from Modules.processing import processingTimeType
from Modules.processing import processingSpaceType

from Modules.DataBase import transientDataSet
from Modules.DataBase import transienSpaceDataSet

import math
import os

def calculateStress(coreZones, size=66) :
    stress_CF_name = ["2D_CladAxialStress", "2D_CladHoopStress", "2D_CladRadialStress"]
    number_for_delete = [size, size, size]
    some_parameter = 4 # связан с количеством 
    path_to_file = r'' + resultsFolder

    for zone in coreZones :
        zone_name = zone["name"]
        zone_tvel_name = zone["tvel"]["name"]
        file_name = ''

        print("calculate stress in "  + zone_name)

        path_to_file_in_zone = os.path.join(path_to_file, zone_name)

        dataList = []
        for i in range(len(stress_CF_name)) :
            object_name = getFileName(stress_CF_name[i], zone_name, zone_tvel_name)
            file_name = object_name + '.dat'
            dataList.append(convert_file_to_list(file_name, path_to_file_in_zone, number_for_delete[i], 0.0, False))

        data_1 = dataList[0]
        data_2 = dataList[1]
        data_3 = dataList[2]

        stress = []

        i = 0
        while i < len(data_1) :
            stress_line = [data_1[i][0]]
            for j in range(1, len(data_1[i]), some_parameter) :
                S = 0
                for k in range(some_parameter) :
                    s1 = data_1[i][j + k]
                    s2 = data_2[i][j + k]
                    s3 = data_3[i][j + k]
                    s_summ = s1 + s2 + s3
                    S_current = math.sqrt(1.5 * ((s1  - 2/3 * s_summ)**2 + (s2  - 2/3 * s_summ)**2) + (s3  - 2/3 * s_summ)**2)
                    S = max(S, S_current)

                stress_line.append(S)

            stress.append(stress_line)
            i += 1

        object_name = getFileName("stress_axial", zone_name, zone_tvel_name)
        #file_name =  r'' + resultsFolder + '\\' + object_name + '.dat'
        file_name =  os.path.join(path_to_file_in_zone, object_name + '.dat')
        file = open(file_name, "w")

        for line in stress :
            line_str = [str(item) + " " for item in line]
            line_str.append("\n")
            file.writelines(line_str)

        file.close()

def getFileName(resultsGroupName, zoneName, tvelName):
    return "BERKUT_" + resultsGroupName + "_" + zoneName + "_" + tvelName

def processingBERKUT_N(module_data, coreZones, stadyStateTime, linesPerFigure, DtPlot, myOut, MyCore):

    if module_data["StressRule"]["Calculating"] == "On":
        calculateStress(coreZones, module_data["StressRule"]["HeaderLines"])
    
    prepare_folders(module_data)

    module_name = module_data["module"]

    for resultsGroup in module_data["data"] :

        resultsGroupName = resultsGroup["name"]

        print("Processing " + module_name + ' ' + resultsGroupName)
        path_to_file = r'' + resultsFolder

        if resultsGroup["dataType"] =="time": # значит имеем только один график от времени

            file_pathFrac = os.path.join(module_name, resultsGroupName, "fraction.dat")
            fileoutFrac = open(file_pathFrac, "w")

            # отрисовываем данные по каждой зоне
            for zone in coreZones:
                zone_name = zone["name"]
                zone_tvel_name = zone["tvel"]["name"]

                path_to_file_in_zone = os.path.join(path_to_file, zone_name)

                file_name = ''
                object_name = getFileName(resultsGroupName, zone_name, zone_tvel_name) #getFileName(resultsGroupName, zone_name, zone["tvel"]["name"])
                file_name = object_name + '.dat'

                dataList = convert_file_to_list(file_name, path_to_file_in_zone, resultsGroup["HeaderLines"], 0.0, False)
                dataList = getRightTimeTableNarabotka(zone_name, zone_tvel_name, zone["ZoneAccidentStartTime"], True, dataList)

                #time_point = 28.51
                #if resultsGroupName[15:] == 'Cs134' or resultsGroupName[15:] == 'Cs137' or resultsGroupName[15:] == 'I131' or resultsGroupName[15:] == 'Kr85m' or resultsGroupName[15:] == 'Kr85m' or resultsGroupName[15:] == 'Xe133':
                #    i = 0
                #    while i < len(dataList):
                #        if dataList[i][0] > time_point and False:
                #            dataList[i][1] = dataList[i-1][1]
                #        i+=1


                max_value = 0.0
                for elem in dataList:
                    if elem[1] > max_value:
                        max_value = elem[1]
                fileoutFrac.write(zone_name + ' ' + str(max_value / dataList[0][1]) + '\n')

                data_to_plot = []
                data_to_plot.append(dataList)
                data_legends = []
                data_legends.append(resultsGroup["graphParameters"]["legend"])

                myData = transientDataSet(module_name, resultsGroupName)
                processingTimeType(resultsGroup, zone_name, object_name, data_to_plot, data_legends, module_name, myOut, myData)
                MyCore.addDataToZone(zone_name, myData, "time")

            fileoutFrac.close()

            haveRule = module_data.get("outputRule")
            ishydraulicGroups = False
            if haveRule: ishydraulicGroups = haveRule["type"] == "hydraulicGroups"
            if ishydraulicGroups:

                myOrderedZones =getOrderedZones(coreZones)
                myOrderedGroups = getZonesindexes(myOrderedZones)

                for orderedGroup in myOrderedGroups:
                    groupeName = module_data["outputRule"]["groupName"]
                    object_name_group = module_name + '_' + resultsGroupName + '_' + groupeName + '_' + str(orderedGroup)
                    data_to_plot = []
                    data_legends = []
                    for orderedZone in myOrderedZones:
                        if orderedGroup == orderedZone[0]:

                            zone_name = orderedZone[1] 
                            zone_tvel_name = orderedZone[2]
                            zone_accident_start_time = orderedZone[4]
                            file_name = ''
                            object_name = getFileName(resultsGroupName, zone_name, zone_tvel_name)
                            file_name = object_name + '.dat'

                            path_to_file_in_zone = os.path.join(path_to_file, zone_name)

                            dataList = convert_file_to_list(file_name, path_to_file_in_zone, resultsGroup["HeaderLines"], 0.0, False)
                            dataList = getRightTimeTableNarabotka(zone_name, zone_tvel_name, zone_accident_start_time, True, dataList)

                            time_point = 28.01
                            if resultsGroupName[15:] == 'Cs134' or resultsGroupName[15:] == 'Cs137' or resultsGroupName[15:] == 'I131' or resultsGroupName[15:] == 'Kr85m' or resultsGroupName[15:] == 'Kr85m' or resultsGroupName[15:] == 'Xe133':
                                i = 0
                                while i < len(dataList):
                                    if dataList[i][0] > time_point:
                                        dataList[i][1] = dataList[i-1][1]
                                    i+=1

                            data_to_plot.append(dataList)
                            data_legends.append("Зона" + ' ' + str(orderedZone[3]))
                    #hydr_zone_name = '_hydraulicZone_' +  str(orderedGroup)
                    hydr_zone_name = " гидравлическая. Номер " + str(orderedGroup)
                    myData = transientDataSet(module_name, resultsGroupName + " Группа номер " + str(orderedGroup))
                    processingTimeType(resultsGroup, hydr_zone_name, object_name_group, data_to_plot, data_legends, module_name, myOut, myData, add_resultsGroup_folder = '_' + groupeName)

        if resultsGroup["dataType"] =="space": # значит имеем только один график от времени
            for zone in coreZones:
                zone_name = zone["name"]
                zone_tvel_name = zone["tvel"]["name"]
                file_name = ''
                object_name = getFileName(resultsGroupName, zone_name, zone_tvel_name)

                path_to_file_in_zone = os.path.join(path_to_file, zone_name)

                file_name = object_name + '.dat'
                dataList = convert_file_to_list(file_name, path_to_file_in_zone, resultsGroup["HeaderLines"], 0.0, False)
                dataList = getRightTimeTableNarabotka(zone_name, zone_tvel_name, zone["ZoneAccidentStartTime"], True, dataList)
                lines_per_figure = linesPerFigure
                timeStepPlot = DtPlot
                myData = transienSpaceDataSet(module_name, resultsGroupName)
                processingSpaceType(resultsGroup, zone["name"], object_name, dataList, lines_per_figure, timeStepPlot, module_name, zone["tvel"]["grid"], myOut, myData)
                MyCore.addDataToZone(zone["name"], myData, "space")

