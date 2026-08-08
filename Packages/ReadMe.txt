inputCoreZones.json - параметры активной зоны для формирования имён выходных файлов и использование сетки аз и твэлов
{
    "id": 141,                                      //индекс зоны
    "name": "Zone_141",								//имя зоны
    "axialCellNumber": 87,							//количество ячеек в гидровлическом канале зоны
    "tvsNumber": 40,								//количество ТВС в зоне
    "grid": [],										//координаты центров ячеек гидравлического канала зоны
    "tvel": {
      "name": "TVEL_Rods",							//имя твэла в зоне
      "axialCellNumber": 55,						//количество ячеек твэла по высоте
      "radialCellNumberHole": 2,					//количество ячеек твэла для отверстия
      "radialCellNumberPellet": 10,					//количество ячеек твэла для таблеток
      "radialCellNumberGap": 1,						//количество ячеек твэла для газового зазора
      "radialCellNumberClad": 4,					//количество ячеек твэла для оболочки
      "grid": [ ]									//координаты центров ячеек твэла по высоте
    }
  }

mainParameters.json
{
  "reactor": "БН 1200",								//имя реактора
  "fuelType": "СНУП",								//тип топлива
  "accident": "UTOP",								//тип аварии
  "InputFileName": "BN1200_simple_utop",			//имя входного файла. Необходимо для формирования имён выходных файлов
  "stadyStateDuration": 400.0,						//количество секунд стационара. На это время будут сдвинуты все графики
  "BERKUT": {										//имя модуля или группы выходных данных || "BERKUT", "CORE", "SAFR", "DN3D", "FIRSTLOOP", "SECLOOP"
    "jsonFile": "BERKUToutputFiles",				// имя json файла с параметрами для обработки результатов
    "dataProcessing": "On",							//обрабатывать выходные данные для данных результатов расчёта или нет || "On", "Off"
    "linesPerFigure": 5,							//количество линий на одном графике. Не больше 6
    "DtPlot": 1.0									//Шаг вывода для графиков с данными в определённый момент времени
	},
	// параметры для остальных модулей заполняются аналогично приведённому примеру с модулем "BERKUT"
  "CORE": {
  },
  "SAFR": {
  },
  "DN3D": {
  },
  "FIRSTLOOP": {
  },
  "SECLOOP": {
  }
}

 // файлы типа json с параметрами для обработки данных 
BERKUToutputFiles.json
DN3DoutputFiles.json
COREoutputFiles.json
FIRSTLOOPoutputFiles.json
SECLOOPoutputFiles.json

//Для вышеуказанных групп выходных данных используются следующий способ задания параметров
{
  "module": "CORE", 							// имя модуля. Используется для формирования имён выходных файлов данного модуля
  "title": "Активная зона", 					// имя модуля для отображения в html документе
  "data": [										// список параметров для различных выходных результатов
    
	{
      "dataType": "time",						// тип графика || "time" - график от времени, "space" - график по пространству
      "name": "CoolantMassFluxInletInZone",		// основная часть имени входного файла. Используется для формирования имён выходных файлов данного модуля
      "title": "Расход на входе АЗ",			// имя группы результатов для отображения в html документе
      "HeaderLines": 8,							// количество первых строк в файле подлежащих удалению
      "graphParameters": {						// параметры для построения графика
        "userGridX": "No",						// использовать пользовательские настройки для оси OX || "Yes" - используются пользовательские параметры сетки указанные ниже, "No" - параметры сетки насчитываются автоматически
        "userGridY": "Yes",						// использовать пользовательские настройки для оси OY || "Yes" - используются пользовательские параметры сетки указанные ниже, "No" - параметры сетки насчитываются автоматически
        "RelativeToStadyState": "Yes",			// Относительные результаты. Данные делятся на значение в стационаре (в 0.0 секунду с учётом сдвига)
        "xMin": 0,								// Параметры сетки. Минимальная граница по X
        "xMax": 100,							// Параметры сетки. Максимальная граница по X
        "yMin": 0,								// Параметры сетки. Минимальная граница по Y
        "yMax": 2,								// Параметры сетки. Максимальная граница по Y
        "xLabel": "Время, с",					// Подпись оси OX
        "yLabel": "Массовый расход, отн. ед.",	// Подпись оси OY
        "legend": "EUCLID/V2",					// Легенда
        "legendPosition": "best",				// Положение легенды на графике ||  #['best' | 'upper right' | 'upper left' | 'lower left' | 'lower right' | 'right' | 'center left' | 'center right' | 'lower center' | 'upper center' | 'center']
        "title": "Зависимость расхода",			// Подпись рисунка
        "xMajorTicks": 10,						// Большие деления сетки по оси OX
        "xMinorTicks": 2,						// Малые деления сетки по оси OX
        "yMajorTicks": 0.5,						// Малые деления сетки по оси OY
        "yMinorTicks": 0.1,						// Большие деления сетки по оси OY
        "xMultiplicator": 1,					// Множитель для данные по оси OX
        "yMultiplicator": 1						// Множитель для данные по оси OY
      }
    },
}




//Параметры для обработки результатов SAFR

SAFRoutputFiles.json

{
  "module": "SAFR",								// имя модуля. Используется для формирования имён выходных файлов данного модуля
  "title": "Модуль разрушения",					// имя модуля для отображения в html документе
  "materials": [								// список материалов
    {
      "name": "UPN",							// имя материала
      "type": "fuel",							// тип материала		|| fuel, gas, structure
      "colorSolid": "green",					// цвет материала в твёрдой фазе
      "colorLiquid": "pink"						// цвет материала в жидкой фазе
    },
  ],
  "parameters": {								// параметры для отрисовки карты
    "sizeAxial": 853,							// количество пикселей по высоте
    "sizeRadial": 765,							// количество пикселей по ширине
    "Length": 2.33498,							// длина твэла
    "innerRadius": 0.0,							// внутренняя граница твэла
    "externalRadius": 0.0046,					// внешняя граница твэла в номинале
    "freeSpaceAxial": 42,						// количество пикселей по высоте для области с именами материалов
    "freeSpaceRadial": 125						// количество пикселей по ширине возле правой границы. Используется для движения материалов и карты температур
  },
  "data": [										// список параметров для различных выходных результатов. Можно менять параметр "title"
    {
      "dataType": "map",
      "name": "LiquidMap",
      "graphParameters": {
        "title": "Распределение расплава в зоне "
      }
    },
    {
      "dataType": "map",
      "name": "TemperatureMap",
      "graphParameters": {
        "title": "Распределение температуры в зоне "
      }
    },
    {
      "dataType": "time",
      "name": "LiquidMass",
      "graphParameters": {
        "title": "Масса расплава в твэле от времени. Зона "
      }
    },
    {
      "dataType": "time",
      "name": "MaxTemperature",
      "graphParameters": {
        "title": "Максимальная температура топлива в твэле от времени. Зона "
      }
    }
  ],
  "liquidMap": {
    "dataType": "map",
    "name": "LiquidMap",
    "title": "Карта расплава",
    "graphParameters": {
      "title": "Распределение расплава. Зона "
    }
  },
  "temperatureMap": {
    "dataType": "map",
    "name": "TemperatureMap",
    "title": "Карта температур",
    "graphParameters": {
      "title": "Распределение температуры. Зона "
    }
  },
  "liquidMass": {	// список параметров для графиков типа "time". Описание приведено выше
    "dataType": "time",
    "title": "Масса расплава",
    "name": "LiquidMass",
    "HeaderLines": 2,
    "graphParameters": {
      "userGridX": "No",
      "userGridY": "No",
      "RelativeToStadyState": "No",
      "xMin": 0,
      "xMax": 100,
      "yMin": 0,
      "yMax": 400,
      "xLabel": "Время, с",
      "yLabel": "Масса, кг",
      "legend": "EUCLID/V2",
      "legendPosition": "upper left",
      "title": "Масса расплава в твэле от времени в зоне ",
      "xMajorTicks": 5,
      "xMinorTicks": 1,
      "yMajorTicks": 100,
      "yMinorTicks": 10,
      "xMultiplicator": 1,
      "yMultiplicator": 1
    }
  },
  "maxTemperature": { // список параметров для графиков типа "time". Описание приведено выше
    "dataType": "time",
    "name": "MaxTemperature",
    "title": "Температура материалов",
    "HeaderLines": 7,
    "graphParameters": {
      "userGridX": "No",
      "userGridY": "No",
      "RelativeToStadyState": "No",
      "xMin": 0,
      "xMax": 100,
      "yMin": 0,
      "yMax": 4000,
      "xLabel": "Время, с",
      "yLabel": "Температура, К",
      "legend": "EUCLID/V2",
      "legendPosition": "upper left",
      "title": "Максимальная температура в твэле от времени в зоне ",
      "xMajorTicks": 5,
      "xMinorTicks": 1,
      "yMajorTicks": 200,
      "yMinorTicks": 50,
      "xMultiplicator": 1,
      "yMultiplicator": 1
    }
  }
}