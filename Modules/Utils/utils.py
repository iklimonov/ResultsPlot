import os          # для работы с операционной системой

import numpy as np
import json
from json import JSONEncoder
import codecs

try: set
except NameError: from sets import Set as set

import math

# для сглаживания
import pandas as pd
from statsmodels.tsa.holtwinters import SimpleExpSmoothing, Holt

import Modules.Utils.mySettings



resultsFolder = 'CalculationResults'
plotResultsFolder = 'PlotResults'
lineColors = ['black', 'red', 'green', 'blue', 'darkorange', 'crimson','DarkMagenta','DarkGoldenrod','LightSlateGray','LightSeaGreen','Moccasin']

#Открытие JSON файлов
def openJSON(file_name, folderWithPlotParameters):
    path_to_folder = ""
    if len(folderWithPlotParameters) > 0:
        path_to_folder +=folderWithPlotParameters + "\\"


    with codecs.open("Packages\\" + path_to_folder + file_name + ".json", "r", "utf-8") as read_file:
        jsonData = json.load(read_file)
        read_file.close()
        
        # Применяем параметры по умолчанию ко всем графикам
        if "defaultGraphParameters" in jsonData and "data" in jsonData:
            defaultParams = jsonData["defaultGraphParameters"]
            for graphData in jsonData["data"]:
                if "graphParameters" not in graphData:
                    graphData["graphParameters"] = {}
                # Объединяем параметры: индивидуальные заменяют параметры по умолчанию
                mergedParams = {**defaultParams, **graphData["graphParameters"]}
                graphData["graphParameters"] = mergedParams
        
        return jsonData


def exportCalculationParameters(mainParameters):  #PlotResults\
    #file_path = r'' + 'CalculationParameters' + '.js'
    file_path = os.path.join("PlotResults", 'CalculationParameters' + '.js')
    fileout = codecs.open(file_path, "w", "utf-8")
    mystr = 'var myCalcParameters = \''

    mystr += '{  "reactor": "'+mainParameters["reactor"]+'", "fuelType": "'+mainParameters["fuelType"]+'", "accident": "'+mainParameters["accident"]+'"}'

    mystr += '\';'
    fileout.write(mystr)
    fileout.write('\n')
    fileout.write("if (typeof myCalcParameters != 'undefined') {"+'\n')

    fileout.write('    CalcParametersData = JSON.parse(myCalcParameters);'+'\n')
    fileout.write('} else {'+'\n')
    fileout.write('    myCalcParameters = { reactor: "Лучший", fuelType: "хорошим", accident: "опасная"};'+'\n')
    fileout.write('}'+'\n')
    fileout.close()


def isTrueFalse(my_str):
    if my_str == None: return False
    if my_str == "Yes":
        return True
    return False

def isOn(my_str):
    if my_str == None: return False
    if my_str == "On":
        return True
    return False

#Преобразование файла в массив с данными
def convert_file_to_list(file_name, path_to_file, skiplines, time_shift, delete_stady_state):
        if len(path_to_file) != 0 : path_to_file = path_to_file + '/'
        file_path = r''+path_to_file + file_name
        if os.path.exists(file_path): filein = open(file_path, "r")      
        else: 
            print("ERROR: no file ",file_path)
            return []

        for i in range(skiplines):
            filein.readline()
        dataList = filein.readlines()                                      
        if not dataList: print("ERROR: reading from ",file_path," failed")
        filein.close()

        for i in range(len(dataList)):
            #dataList[i] = dataList[i].rstrip('\x00')
            dataList[i] = dataList[i].replace('\x00','')
            dataList[i] = dataList[i].split()            
            for j in range(len(dataList[i])):
                dataList[i][j] = float(dataList[i][j])
            dataList[i][0] = dataList[i][0] - time_shift

        if (delete_stady_state):
            i = 0
            list_len = len(dataList)
            while i < list_len :
                if dataList[i][0] < 0.0: 
                    dataList.pop(i)
                    i-=1
                list_len = len(dataList)
                i+=1

        if (Modules.Utils.mySettings.limitCalculationTime):
            i = 0
            list_len = len(dataList)
            while i < list_len :
                if dataList[i][0] > Modules.Utils.mySettings.endTime: 
                    dataList.pop(i)
                    i-=1
                list_len = len(dataList)
                i+=1

        if (Modules.Utils.mySettings.limitSpaceCalculationTime and len(dataList[0]) > 2):
            i = 0
            list_len = len(dataList)
            while i < list_len :
                if dataList[i][0] > Modules.Utils.mySettings.endTime: 
                    dataList.pop(i)
                    i-=1
                list_len = len(dataList)
                i+=1
        if (skiplines==1):

            for i in range(100):
                dataList[i][0] = 0.0 + i*0.1
            #dataList[0][0] = 0.0
            #dataList[1][0] = 0.1
            #dataList[2][0] = 0.2
            #dataList[3][0] = 0.3
            #dataList[4][0] = 0.4
            #dataList[5][0] = 0.5
            #dataList[6][0] = 0.6
            #dataList[7][0] = 0.7
            #dataList[8][0] = 0.8
            #dataList[9][0] = 0.9

        if len(dataList) == 0 : print('There is no data for' + file_name+'. Check stady-state time in input parameters or file with results.')
        return dataList



def getRightTimeTableNarabotka(zone_name, tvelName, time_shift, delete_stady_state, orig_data_list):

        #file_path = r'' + resultsFolder + '/' + "BERKUT_Time_" + zone_name + "_" + tvelName + ".dat"
        file_path = os.path.join(resultsFolder, zone_name, "BERKUT_Time_" + zone_name + "_" + tvelName + ".dat")
        if os.path.exists(file_path): 
            filein = open(file_path, "r")
        else: 
            print("ERROR: no file ",file_path)
            return []
        skiplines = 6
        for i in range(skiplines):
            filein.readline()
        dataList = filein.readlines()                                      
        if not dataList: print("ERROR: reading from ",file_path," failed")
        filein.close()

        right_time_table = []

        for i in range(len(dataList)):
            dataList[i] = dataList[i].split()
            for j in range(len(dataList[i])):
                dataList[i][j] = float(dataList[i][j])
            right_time_table.append(dataList[i][1] - time_shift) # положили наше сдвинутое время

        if len(right_time_table)!= len(orig_data_list):
            print("Different size of time table and data table for data in zone " + zone_name)
            exit()

        # подменяем время
        i = 0
        while i  <len(orig_data_list):
            orig_data_list[i][0] = right_time_table[i]
            i+=1

        # удаляем стационар
        if (delete_stady_state):
            i = 0
            list_len = len(orig_data_list)
            while i < list_len :
                if orig_data_list[i][0] < 0.0: 
                    orig_data_list.pop(i)
                    i-=1
                list_len = len(orig_data_list)
                i+=1
        if len(orig_data_list) == 0 :
            print('There is no data for ' + zone_name + '. Check stady-state time in input parameters or file with results.')
        return orig_data_list
###############################################################################
#Создание и очистка папок
def emptydir(top):
    if(top == '/' or top == "\\"):
        return
    else:
        for root, dirs, files in os.walk(top, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def processFolder(folder):
    if not os.path.exists(r''+folder+'/'): os.makedirs(r''+folder+'/')
    emptydir(folder)
    clearfolder = os.getcwd()+r'/'+folder+'/'
    for delfile in os.listdir(clearfolder):
        if os.path.exists(clearfolder+delfile): os.remove(clearfolder+delfile)
        else: print('No file: ',delfile)

def prepare_folders(module):
    #moduleFolder = module["module"]
    moduleFolder = os.path.join(plotResultsFolder, module["module"])
    processFolder(moduleFolder)

    for resultsGroup in module["data"] :
        #subfolder = moduleFolder + '/' + resultsGroup["name"]
        subfolder = os.path.join(moduleFolder, resultsGroup["name"])
        processFolder(subfolder)

        haveRule = module.get("outputRule")
        if haveRule:
            if resultsGroup["dataType"] =="time" and module["outputRule"]["type"] == "hydraulicGroups":
                #subfolder = moduleFolder + '/' + resultsGroup["name"]  + '_' + module["outputRule"]["groupName"]
                subfolder = os.path.join(moduleFolder, resultsGroup["name"]  + '_' + module["outputRule"]["groupName"])
                processFolder(subfolder)

###############################################################################
#Проверка существования файлов SAFR
def check_SAFR_Tvel_file(hs_name, zone_id, zone_name, input_file_name):
    file_path = r'' + resultsFolder + '/' + input_file_name + '_' + str(zone_id) + '_' + zone_name + '_' + hs_name + '_cell_information.csv'
    if os.path.exists(file_path): 
        return True

def check_SAFR_Canister_file(hs_name, zone_id, input_file_name):
    file_path = r'' + resultsFolder + '/' + input_file_name + '_' + hs_name + '_'  + str(zone_id) + '_cell_information.csv'
    if os.path.exists(file_path): 
        return True

def get_NameForBERKUT(file_name, zone_name,tvel_name):
    return 'BERKUT' + '_' + file_name + '_' +zone_name+'_'+tvel_name

def unique(s):
    """ Return a list of the elements in s in arbitrary order, but without
        duplicates. """
    # Try using a set first, because it's the fastest and will usually work
    try:
        return list(set(s))
    except TypeError:
        pass  # Move on to the next method
    # Since you can't hash all elements, try sorting, to bring equal items
    # together and then weed them out in a single pass
    t = list(s)
    try:
        t.sort( )
    except TypeError:
        del t  # Move on to the next method
    else:
        # the sort worked, so we're fine -- do the weeding
        return [x for i, x in enumerate(t) if not i or x != t[i-1]]
    # Brute force is all that's left
    u = [  ]
    for x in s:
        if x not in u:
            u.append(x)
    return u

def get_limits(myMin, myMax):

    def get_power(value):
        power = 0
        if (value != 0.0):
            power = math.log10(abs(value))
            if power >= 1.0 :
                power = int(power)
            else :
                power = math.floor(power)
        return power

    def get_low(value, power):
        if (value != 0.0):
            #power = get_power(value)
            
            order = 10**power

            first_number = math.floor(value / order)
            new_value = first_number * order

            if (value - new_value)==0.0:
                if value < 0.0: new_value *= 1.1 
                else: new_value *= 0.9
            return first_number * order
        return 0.0

    def get_high(value, power):
        if (value != 0.0):
            #power = get_power(value)
            
            order = 10**power

            first_number = math.floor(value / order) + 1
            new_value = first_number * order

            if (value - new_value)==0.0:
                if value < 0.0: new_value *= 0.9 
                else: new_value *= 1.1
            return new_value
        return 0.0

    diff = myMax - myMin
    dif_power = get_power(diff)
    #if diff > 10**dif_power :
        #dif_power+=1

    ###########
    if (myMin != 0.0):
        myMin = get_low(myMin, dif_power)
    else:
        myMin = -myMax * 0.01
    ######
    if (myMax != 0.0):
        myMax = get_high(myMax, dif_power)
    else:
        myMax = abs(myMin * 0.01)
    #############
        
    diff = myMax - myMin
    if diff == 0.0: 
        myMin = myMax - 0.1
        myMax = myMax + 0.1
    return [myMin, myMax]

def get_ticks(myMin, myMax):
    diff = myMax - myMin
    power = math.log10(diff)
    if power >= 1.0 :
        power = int(power)
    else :
        power = math.floor(power)

    if int(diff/(10**power)) == 1:
        power-=1

    yMaT = 10**power
    yMiT = yMaT / 10
    return [yMaT, yMiT]


def getOrderedZones(coreZones):

    myOrderedZones = []
                
    for zone in coreZones:
        myZone = []
        myZone.append(int(zone["plotGroup"]))
        myZone.append(zone["name"])
        myZone.append(zone["tvel"]["name"])
        myZone.append(zone["id"])
        myZone.append(zone["ZoneAccidentStartTime"])
        myOrderedZones.append(myZone)

    return myOrderedZones

def getZonesindexes(myOrderedZones):
    myOrderedGroups = []
    for zone in myOrderedZones:
        myOrderedGroups.append(zone[0])

    myOrderedGroups = unique(myOrderedGroups)
    return myOrderedGroups



def dataSmoothing(global_data):
    df = pd.DataFrame(global_data, columns=['time','data']).set_index('time')
    train = df.iloc[100:-10, :]
    test = df.iloc[-10:, :]
    train.index = pd.to_datetime(train.index)
    test.index = pd.to_datetime(test.index)
    pred = test.copy()

    model = SimpleExpSmoothing(np.asarray(train['data']))
    model._index = pd.to_datetime(train.index)

    fit1 = model.fit()
    pred1 = fit1.forecast(9)
    fit2 = model.fit(smoothing_level=.2)
    pred2 = fit2.forecast(9)
    fit3 = model.fit(smoothing_level=.5)
    pred3 = fit3.forecast(9)



def exponential_smoothing(global_data, alpha, breakPoint = -1):
    series = []
    startIndex = 0
    endIndex = len(global_data)
    if breakPoint > 0 :
        startIndex = breakPoint - 10
        endIndex = breakPoint + 10

    i = startIndex
    while i < endIndex:
        series.append(global_data[i][1])
        i+=1


    result = [series[0]] # first value is same as series
    for n in range(1, len(series)):
        result.append(alpha * series[n] + (1 - alpha) * result[n-1])

    i = startIndex
    while i < endIndex:
        global_data[i][1] = result[i - startIndex]
        i+=1

    return  global_data

def simple_smoothing(global_data, breakPoint, range):
    series = []

    startIndex = breakPoint - range
    endIndex = min(breakPoint + range, len(global_data))

    startValue = global_data[startIndex][0]
    endValue = global_data[endIndex-1][0]

    dif = global_data[endIndex-1][1] - global_data[startIndex][1]
    derivative = 0.0

    isLinear = False

    if dif == 0.0: 
        isLinear = True
    else:
        derivative = dif / (endValue - startValue)

    i = startIndex
    while i < endIndex:
        if isLinear:
            global_data[i][1] = global_data[startIndex][1]
        else:
            global_data[i][1] = global_data[i-1][1] + derivative * (global_data[i][0] - global_data[i-1][0])
        i+=1

    return  global_data

def get_max_from_data(dataList):
    if not (len(dataList) > 0): 
        print("Can not find max value for empty list")
        return None
    max_value = dataList[0][1]
    for data in dataList:
        if data[1] > max_value: max_value = data[1]

    return max_value


def reduceTimeTypeDataOutput(dataList, Dt):
    new_dataList = []
    if not (len(dataList) > 0): 
        print("Can not reduce time table for empty list")
        return dataList

    new_dataList.append(dataList[0])
    next_time_point = dataList[0][0] + Dt
    i = 1
    while i < len(dataList):
        if dataList[i][0] < next_time_point:
            i+=1
            continue
        new_dataList.append(dataList[i])
        next_time_point = dataList[i][0] + Dt
        i+=1
    return new_dataList


def get_derivatives(some_list):

    def derivative_second_order_bound_left(left, middle, right):
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = (right[0] - middle[0]) / (middle[0] - left[0])
        return (-ratio * (2.0 + ratio) * left[1] + (1.0 + ratio) * (1.0 + ratio) * middle[1] - right[1]) / h_right / (1.0 + ratio)

    def derivative_second_order_bound_right(left, middle, right):
        # передаются три точки: пары координата-значение
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = h_right / h_left
        unit_add_ratio = 1.0 + ratio
        return (ratio * ratio * left[1] - unit_add_ratio * unit_add_ratio * middle[1] + (2.0 * ratio + 1.0) * right[1]) / h_right / (1.0 + ratio)

    def derivative_second_order(left, middle, right):
        # передаются три точки: пары координата-значение
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = h_right / h_left
        ratio_square = ratio * ratio
        return (-ratio_square * left[1] + (ratio_square - 1.0) * middle[1] + right[1]) / h_right / (1.0 + ratio)

    if len(some_list) < 3:
        print("Can not find derivatives. Data list too short")
        exit()

    derivatives = []
    # первая точка
    new_par = [some_list[0][0], some_list[0][1]]
    new_par[1] = derivative_second_order_bound_left(some_list[0], some_list[1], some_list[2])
    derivatives.append(new_par)

    # центральные точки
    i=1
    while i < len(some_list)-1:
        new_par = [some_list[i][0], some_list[i][1]]
        new_par[1] = derivative_second_order_bound_left(some_list[i-1], some_list[i], some_list[i+1])
        derivatives.append(new_par)
        i+=1
    # последняя точка
    new_par = [some_list[i][0], some_list[i][1]]
    new_par[1] = derivative_second_order_bound_right(some_list[i-2], some_list[i-1], some_list[i])
    derivatives.append(new_par)

    return derivatives

def get_derivativesSeparate(points, values):

    def derivative_second_order_bound_left(left, middle, right):
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = (right[0] - middle[0]) / (middle[0] - left[0])
        return (-ratio * (2.0 + ratio) * left[1] + (1.0 + ratio) * (1.0 + ratio) * middle[1] - right[1]) / h_right / (1.0 + ratio)

    def derivative_second_order_bound_right(left, middle, right):
        # передаются три точки: пары координата-значение
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = h_right / h_left
        unit_add_ratio = 1.0 + ratio
        return (ratio * ratio * left[1] - unit_add_ratio * unit_add_ratio * middle[1] + (2.0 * ratio + 1.0) * right[1]) / h_right / (1.0 + ratio)

    def derivative_second_order(left, middle, right):
        # передаются три точки: пары координата-значение
        h_left = middle[0] - left[0]
        h_right = right[0] - middle[0]
        ratio = h_right / h_left
        ratio_square = ratio * ratio
        return (-ratio_square * left[1] + (ratio_square - 1.0) * middle[1] + right[1]) / h_right / (1.0 + ratio)

    if len(points) != len(values):
        print("Can not find derivatives. List size is not equal")
        exit()

    if len(points) < 3:
        print("Can not find derivatives. Data list too short")
        exit()

    derivatives = []
    # первая точка
    new_par_l = [points[0], values[0]]
    new_par_m = [points[1], values[1]]
    new_par_r = [points[2], values[2]]
    dif_value = derivative_second_order_bound_left(new_par_l, new_par_m, new_par_r)
    derivatives.append(dif_value)

    # центральные точки
    i=1
    while i < len(points)-1:
        new_par_l = [points[i-1], values[i-1]]
        new_par_m = [points[i], values[i]]
        new_par_r = [points[i+1], values[i+1]]
        dif_value = derivative_second_order_bound_left(new_par_l, new_par_m, new_par_r)
        derivatives.append(dif_value)
        i+=1
    # последняя точка
    new_par_l = [points[i-2], values[i-2]]
    new_par_m = [points[i-1], values[i-1]]
    new_par_r = [points[i], values[i]]
    dif_value = derivative_second_order_bound_right(new_par_l, new_par_m, new_par_r)
    derivatives.append(dif_value)

    return derivatives