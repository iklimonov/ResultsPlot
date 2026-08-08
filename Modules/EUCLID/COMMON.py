from Modules.Utils.utils import convert_file_to_list
from Modules.Utils.utils import prepare_folders
from Modules.Utils.utils import resultsFolder

from Modules.processing import processingTimeType
from Modules.processing import processingSpaceType

from Modules.DataBase import transientDataSet
from Modules.DataBase import transienSpaceDataSet


def processingCOMMON(COMMON_data, stadyStateTime, linesPerFigure, DtPlot, myOut, commonDataBase):
    
    prepare_folders(COMMON_data)

    module_name = COMMON_data["module"]

    for resultsGroup in COMMON_data["data"] :

        resultsGroupName = resultsGroup["name"]

        print("Processing " + module_name + ' ' + resultsGroupName)
        path_to_file = r'' + resultsFolder
        file_name = ''
        object_name = module_name + '_' + resultsGroupName

        file_name = object_name + '.dat'

        if resultsGroup["dataType"] =="time": # значит имеем только один график от времени
            dataList = convert_file_to_list(file_name, path_to_file, resultsGroup["HeaderLines"], stadyStateTime, True)
            data_to_plot = []
            data_to_plot.append(dataList)
            data_legends = []
            data_legends.append(resultsGroup["graphParameters"]["legend"])

            myData = transientDataSet(module_name, resultsGroupName)
            processingTimeType(resultsGroup, "", object_name, data_to_plot, data_legends, module_name, myOut, myData)
            commonDataBase.addData(myData,"time")
            #
        else : print(resultsGroup["dataType"] + " are not supported for Commom data")