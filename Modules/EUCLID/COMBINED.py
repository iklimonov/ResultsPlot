from Modules.Utils.utils import convert_file_to_list
from Modules.Utils.utils import prepare_folders
from Modules.Utils.utils import resultsFolder

from Modules.processing import processingCombinedType


def processingCOMBINED(COMBINED_data, myOut, CommonData):
    
    prepare_folders(COMBINED_data)

    module_name = COMBINED_data["module"]

    for resultsGroup in COMBINED_data["data"] :

        resultsGroupName = resultsGroup["name"]

        print("Processing " + module_name + ' ' + resultsGroupName)
        path_to_file = r'' + resultsFolder
        file_name = ''
        object_name = module_name + '_' + resultsGroupName

        processingCombinedType(module_name, resultsGroup, object_name, CommonData, myOut)