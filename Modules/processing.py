import os
import math

#from Modules.DataBase import transientDataSet
#from Modules.DataBase import transienSpaceDataSet

import sys

from Modules.myGraph import myGraph
from Modules.myLine import myLine
from Modules.Utils.utils import lineColors
from Modules.Utils.utils import get_limits
from Modules.Utils.utils import get_ticks
from Modules.Utils.utils import isTrueFalse
from Modules.Utils.utils import plotResultsFolder
#печать картинок для type "time"

def processingTimeType(resultsGroup, zone_name, object_name, dataList, dataLegends, module, myOut, myData, add_to_title = '', add_resultsGroup_folder = '', useySciFormat = False):

    if len(dataList) == 0 : return

    minX_global = 1.e+35
    minY_global = 1.e+35

    maxX_global = -1.e+35
    maxY_global = -1.e+35

    parameters = resultsGroup["graphParameters"]

    lines = []
    ######################### обработка одной линии
    data_index = 0
    for data_line in dataList:

        if len(data_line) == 0 : continue

        t = []
        y = []

        stadyStateRatio = 1.0

        if isTrueFalse(parameters["RelativeToStadyState"]):
            # если уж деление на нуль, то пользователь сам виноват
            stadyStateRatio = 1.0 / ((data_line[0][1] + parameters["yAddendum"]) * parameters["yMultiplicator"])

        for i in range(len(data_line)):
            t.append((data_line[i][0] + parameters["xAddendum"]) * parameters["xMultiplicator"])
            y.append((data_line[i][1] + parameters["yAddendum"]) * parameters["yMultiplicator"] * stadyStateRatio)


        #my_Graph.set_Title(parameters["title"] + zone_name)

        #print(y)
        minX_global = min(minX_global,min(t))
        minY_global = min(minY_global,min(y))

        maxX_global = max(maxX_global,max(t))
        maxY_global = max(maxY_global,max(y))

        myData.setTimeTable(t)
        myData.setValueTable(y)
        myData.setXLabel(parameters["xLabel"])
        myData.setYLabel(parameters["yLabel"])

        my_Line = myLine(t,y)
        #my_Line.set_label(parameters["legend"])
        my_Line.set_label(dataLegends[data_index])
        my_Line.set_lineWidth(2)
        my_Line.set_color(lineColors[data_index])
        my_Line.set_lineStyle("-")

        lines.append(my_Line)
        data_index+=1
    ######################### обработка одной линии

 

    ################################## параметры графика
    my_Graph = myGraph(parameters["xLabel"],parameters["yLabel"])

    if isTrueFalse(parameters["axSciFormat"]):
        my_Graph.useSciFormatForAx()
    if isTrueFalse(parameters["aySciFormat"]) or useySciFormat:
        my_Graph.useSciFormatForAy()

    #if parameters["axScaleFormat"] != None:
    my_Graph.setScaleForAx(parameters.get("axScaleFormat", "linear"))
    my_Graph.setScaleForAy(parameters.get("ayScaleFormat", "linear"))


    xMaT = parameters["xMajorTicks"]
    xMiT = parameters["xMinorTicks"]
    yMaT = parameters["yMajorTicks"]
    yMiT = parameters["yMinorTicks"]

    if isTrueFalse(parameters["userGridX"]):
        my_Graph.set_xLimits(parameters["xMin"], parameters["xMax"])
    else: 
        #if parameters["userGridX"] == "No": # должно быть только 2 варианта
        myXmin = minX_global
        myXMax = maxX_global
        my_Graph.set_xLimits(myXmin, myXMax)

    if isTrueFalse(parameters["userGridY"]):
        if maxY_global > parameters["yMax"]:
            myLimits = get_limits(minY_global, maxY_global)
            myYmin = myLimits[0]
            myYmax = myLimits[1]
            my_Graph.set_yLimits(parameters["yMin"], myYmax)
        else:
            my_Graph.set_yLimits(parameters["yMin"], parameters["yMax"])
    else: 
        #if parameters["userGridX"] == "No": # должно быть только 2 варианта
        myYmin = minY_global
        myYmax = maxY_global

        myLimits = get_limits(myYmin, myYmax)
        myYmin = myLimits[0]
        myYmax = myLimits[1]
        my_Graph.set_yLimits(myYmin, myYmax)
        myTicks = get_ticks(myYmin, myYmax)
        yMaT = myTicks[0]
        yMiT = myTicks[1]
        
    my_Graph.set_xAxisTicks(xMaT, xMiT)
    my_Graph.set_yAxisTicks(yMaT, yMiT)

    my_Graph.set_LegendLocation(parameters["legendPosition"])

    pathToFolder = plotResultsFolder + '/' + module + '/' + resultsGroup["name"] + add_resultsGroup_folder
    #pathToFolder = os.path.join(plotResultsFolder, module, resultsGroup["name"] + add_resultsGroup_folder)
    pic_url = pathToFolder + '/' + object_name + '.png'
    #pic_url = os.path.join(pathToFolder, object_name + '.png')

    my_Graph.plot(lines ,object_name, pathToFolder)
    
    myOut.addFigure(module,resultsGroup["name"],resultsGroup["title"],pic_url,parameters["title"] + zone_name + add_to_title)

#печать картинок для type "space"
def processingSpaceType(resultsGroup, zone_name, object_name, dataList, lines_per_figure, timeStepPlot , module, xGrid, myOut, myData):

    if len(dataList) == 0 : return
    if timeStepPlot < 0.0 : timeStepPlot = 0.0
    x = xGrid
    #if module == "BERKUT":
    #    x = zone["tvel"]["grid"]
    #if module == "HYDRA":
    #    x = zone["grid"]

    parameters = resultsGroup["graphParameters"]

    for i in range(len(x)):
        x[i] = (x[i] + parameters["xAddendum"]) * parameters["xMultiplicator"]

    myData.setGrid(x)
        
    stadyStateRatios = []
    dataLineIndex = 0

    for i in range(len(dataList[dataLineIndex]) - 1):
        if isTrueFalse(parameters["RelativeToStadyState"]):
            # если уж деление на нуль, то пользователь сам виноват
            stadyStateRatios.append(1.0/((dataList[dataLineIndex][i + 1] + parameters["yAddendum"]) * parameters["yMultiplicator"]))
        else:
            stadyStateRatios.append(1.0)

    #############################################
    myData.setXLabel(parameters["xLabel"])
    myData.setYLabel(parameters["yLabel"])
    dataLineIndex = 0
    tt = []
    map = []
    while dataLineIndex < len(dataList):
        xl = []
        tt.append(dataList[dataLineIndex][0])
        for j in range(len(dataList[dataLineIndex]) - 1):
            xl.append((dataList[dataLineIndex][j + 1] + parameters["yAddendum"]) * parameters["yMultiplicator"] * stadyStateRatios[j])
        map.append(xl)
        dataLineIndex+=1
    myData.setTimeTable(tt)
    myData.setValueTable(map)
    #############################################

    dataLineIndex = 0
    while dataLineIndex < len(dataList):
        lines = []
        times = []
        myYmin = 1.e+35
        myYMax = 0
        for i in range(lines_per_figure):
            if dataLineIndex >=len(dataList): break
            time = round(dataList[dataLineIndex][0],4)

            y = []    
            for j in range(len(dataList[dataLineIndex]) - 1) :
                y.append((dataList[dataLineIndex][j + 1] + parameters["yAddendum"]) * parameters["yMultiplicator"] * stadyStateRatios[j])

            if isTrueFalse(parameters.get("yInvertData","No")) :
                y_min = sys.float_info.max
                for y_value in y :
                    if math.fabs(y_value) < 1e-14 :
                        continue
                    else :
                        y_min = min(math.fabs(y_value), y_min)

                # заменяем абсолютные нули на минимальные значения
                for y_index in range(len(y)) :
                    if math.fabs(y[y_index]) < 1e-14 :
                        y[y_index] = y_min

                    y[y_index] = 1.0 / y[y_index]
            
            #y = y * file["graphParameters"]["yMultiplicator"]
            min_value = min(y)
            max_value = max(y)

            myYmin = min(min_value,myYmin)
            myYMax = max(max_value,myYMax)




            my_Line = myLine(x,y)
            my_Line.set_label(str(time) + ' ' + parameters["legend"])
            my_Line.set_lineWidth(2)
            my_Line.set_color(lineColors[i])
            my_Line.set_lineStyle("-")

            lines.append(my_Line)
            times.append(time)

            if timeStepPlot>0.0 :
                current_time = dataList[dataLineIndex][0]
                next_time = current_time + timeStepPlot - 0.00001
                while current_time < next_time :
                    dataLineIndex+=1
                    if dataLineIndex >=len(dataList): break
                    current_time = dataList[dataLineIndex][0]
            else :
                dataLineIndex+=1

        my_Graph = myGraph(parameters["xLabel"],parameters["yLabel"])

        xMaT = parameters["xMajorTicks"]
        xMiT = parameters["xMinorTicks"]
        yMaT = parameters["yMajorTicks"]
        yMiT = parameters["yMinorTicks"]

        if isTrueFalse(parameters["axSciFormat"]):
            my_Graph.useSciFormatForAx()
        if isTrueFalse(parameters["aySciFormat"]):
            my_Graph.useSciFormatForAy()

        my_Graph.setScaleForAx(parameters.get("axScaleFormat", "linear"))
        my_Graph.setScaleForAy(parameters.get("ayScaleFormat", "linear"))

        if isTrueFalse(parameters["userGridX"]):
            my_Graph.set_xLimits(parameters["xMin"], parameters["xMax"])
        else: 
            myXmin = min(x)
            myXMax = max(x)
            my_Graph.set_xLimits(myXmin, myXMax)

        if isTrueFalse(parameters["userGridY"]):
            my_Graph.set_yLimits(parameters["yMin"], parameters["yMax"])
        else: 
            #myYmin = myYmin
            #myYMax = myYMax

            #if myYmin < 0.0: myYmin *= 1.1 
            #else: myYmin *= 0.9

            #if myYMax < 0.0: myYMax *= 0.9 
            #else: myYMax *= 1.1
        
            #diff = myYMax - myYmin
            #if diff == 0.0: 
            #    myYmin = myYMax - 0.1
            #    myYMax = myYMax + 0.1
            #    diff = 0.2

            #my_Graph.set_yLimits(myYmin, myYMax)

            #power = math.log10(diff)
            #if power >= 1.0 :
            #    power = int(power)
            #else :
            #    power = math.floor(power)

            #yMaT = 10**power
            #yMiT = yMaT / 5
            myLimits = get_limits(myYmin, myYMax)
            myYmin = myLimits[0]
            myYMax = myLimits[1]
            my_Graph.set_yLimits(myYmin, myYMax)
            myTicks = get_ticks(myYmin, myYMax)
            yMaT = myTicks[0]
            yMiT = myTicks[1]


        my_Graph.set_xAxisTicks(xMaT, xMiT)
        my_Graph.set_yAxisTicks(yMaT, yMiT)

        my_Graph.set_LegendLocation(parameters["legendPosition"])
        #my_Graph.set_Title(parameters["title"] + zone_name)

        pathToFolder = plotResultsFolder + '/' + module + '/' + resultsGroup["name"]
        #pathToFolder = os.path.join(plotResultsFolder, module, resultsGroup["name"])
        pic_file_name = object_name + '_time['+str(times[0])+'-'+str(times[len(times)-1])+']'
        my_Graph.plot(lines ,pic_file_name, pathToFolder)
        
        del my_Graph
        #module : module
        #resultsGroup : resultsGroup["name"]
        #picName : pic_file_name + '.png'
        pic_url = pathToFolder + '/' + pic_file_name + '.png'
        myOut.addFigure(module,resultsGroup["name"],resultsGroup["title"],pic_url,parameters["title"] + zone_name)

def processingCombinedType(module, combination_group, object_name, myData, myOut, add_to_title = ''):

    parameters = combination_group["graphParameters"]

    combinations = combination_group["combinations"]

    my_Graph = myGraph(parameters["xLabel"],parameters["yLabel"])
    
    xMaT = parameters["xMajorTicks"]
    xMiT = parameters["xMinorTicks"]
    yMaT = parameters["yMajorTicks"]
    yMiT = parameters["yMinorTicks"]

    if isTrueFalse(parameters["axSciFormat"]):
        my_Graph.useSciFormatForAx()
    if isTrueFalse(parameters["aySciFormat"]):
        my_Graph.useSciFormatForAy()

    my_Graph.setScaleForAx(parameters.get("axScaleFormat", "linear"))
    my_Graph.setScaleForAy(parameters.get("ayScaleFormat", "linear"))


    my_Graph.set_LegendLocation(parameters["legendPosition"])


    myXmin = 1e+35
    myXMax = 0.0
    myYmin = 1e+35
    myYMax = 0.0
    lines = []
    for combination in combinations:
        data = myData.getDataByDataName(combination["dataClass"])
   
        my_Line = myLine(data.getTimeTable(),data.getValueTable())
        my_Line.set_label(combination["legend"])
        my_Line.set_lineWidth(2)
        my_Line.set_color(combination["lineColor"])
        my_Line.set_lineStyle("-")
        lines.append(my_Line)

        myXmin = min(myXmin,min(data.getTimeTable()))
        myXMax = max(myXMax,max(data.getTimeTable()))
        myYmin = min(myYmin,min(data.getValueTable()))
        myYMax = max(myYMax,max(data.getValueTable()))



    if isTrueFalse(parameters["userGridX"]):
        my_Graph.set_xLimits(parameters["xMin"], parameters["xMax"])
    else: 
        my_Graph.set_xLimits(myXmin, myXMax)

    if isTrueFalse(parameters["userGridY"]):
        my_Graph.set_yLimits(parameters["yMin"], parameters["yMax"])
    else: 
        myLimits = get_limits(myYmin, myYMax)
        my_Graph.set_yLimits(myLimits[0], myLimits[1])
        myTicks = get_ticks(myLimits[0], myLimits[1])
        yMaT = myTicks[0]
        yMiT = myTicks[1]

    my_Graph.set_xAxisTicks(xMaT, xMiT)
    my_Graph.set_yAxisTicks(yMaT, yMiT)

    pathToFolder = plotResultsFolder + '/' + module + '/' + combination_group["name"]
    #pathToFolder = os.path.join(plotResultsFolder, module, combination_group["name"])

    my_Graph.plot(lines ,object_name, pathToFolder)

    pic_url = pathToFolder + '/' + object_name + '.png'
    myOut.addFigure(module, combination_group["name"], combination_group["title"], pic_url, parameters["title"] + add_to_title)