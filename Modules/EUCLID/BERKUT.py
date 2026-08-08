from Modules.Utils.utils import convert_file_to_list
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

def processingBERKUT(module_data, coreZones, stadyStateTime, linesPerFigure, DtPlot, myOut, MyCore):
    
    prepare_folders(module_data)

    module_name = module_data["module"]

    for resultsGroup in module_data["data"] :

        resultsGroupName = resultsGroup["name"]

        print("Processing " + module_name + ' ' + resultsGroupName)
        path_to_file = r'' + resultsFolder

        if resultsGroup["dataType"] =="time": # значит имеем только один график от времени

            # отрисовываем данные по каждой зоне
            for zone in coreZones:
                zone_name = zone["name"]
                file_name = ''
                object_name = get_NameForBERKUT(resultsGroupName, zone_name,zone["tvel"]["name"])
                file_name = object_name + '.dat'

                dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"],stadyStateTime,True)
                data_to_plot = []
                data_to_plot.append(dataList)
                data_legends = []
                data_legends.append(resultsGroup["graphParameters"]["legend"])

                myData = transientDataSet(module_name, resultsGroupName)
                processingTimeType(resultsGroup, zone_name, object_name, data_to_plot, data_legends, module_name, myOut, myData)
                MyCore.addDataToZone(zone_name, myData, "time")

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
                            file_name = ''
                            object_name = get_NameForBERKUT(resultsGroupName, zone_name, zone_tvel_name)
                            file_name = object_name + '.dat'

                            dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"],stadyStateTime,True)
                            data_to_plot.append(dataList)
                            data_legends.append("Зона" + ' ' + str(orderedZone[3]))
                    #hydr_zone_name = '_hydraulicZone_' +  str(orderedGroup)
                    hydr_zone_name = " гидравлическая. Номер " + str(orderedGroup)
                    myData = transientDataSet(module_name, resultsGroupName + " гидравлическая. Номер " + str(orderedGroup))
                    processingTimeType(resultsGroup, hydr_zone_name, object_name_group, data_to_plot, data_legends, module_name, myOut, myData, add_resultsGroup_folder = '_' + groupeName)

        if resultsGroup["dataType"] =="space": # значит имеем только один график от времени
            for zone in coreZones:
                file_name = ''
                object_name = get_NameForBERKUT(resultsGroupName,zone["name"],zone["tvel"]["name"])

                file_name = object_name + '.dat'
                dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"],stadyStateTime,True)
                lines_per_figure = linesPerFigure
                timeStepPlot = DtPlot
                myData = transienSpaceDataSet(module_name, resultsGroupName)
                processingSpaceType(resultsGroup, zone["name"], object_name, dataList, lines_per_figure, timeStepPlot, module_name, zone["tvel"]["grid"], myOut, myData)
                MyCore.addDataToZone(zone["name"], myData, "space")

