import re
import pandas as pd
from sqlite3 import Error

def petrel_formtops_read(tops_path = None,print_info = False):
    '''    
    Function to read Petrel Formation Top Export into Pandas dataframe

    Arguments:
    tops_path (float): full file location of selected tops file
    print_info (bool): print header locations and ID at runtime
    
    Returns:
    Pandas Dataframe containing and data columns from export

    Raises:
    Prints error if path incorrect

    Example:
    df = petrel_formtops_read(tops_path = "C:\\Test.txt",print_info = False)

    PRECONDITIONS: exported file is a valid Petrel tops  format.
    KJAGGS Apr 2025
    
    '''

    #Boolean operators are triggered at beginning and end of data identification
    header_open = False
    header_end = False
    data_start = 0
    header_cnt = 0

    #regex pattern matches to extract  units data from Tops file
    regexXyUnits = "^# Unit in X and Y direction:\\s?(\\w{1,2})"
    regexZUnits = "^# Unit in depth:\\s?(\\w{1,2})"


    regexTopsHeader = "^(.*)$"
    
    regexBeginHeader = "^BEGIN HEADER"
    regexEndHeader = "^END HEADER"

    #dictionary to host columns names
    DataIDDict = {}

    #read tops file
    try:
        TopsInput = open(tops_path, "r")
        #print (LasInput.read())
        for line in TopsInput:

            if re.search(regexXyUnits, line):
                match = re.search(regexXyUnits, line)
                if print_info == True:
                    print("X Y Units = %s" % match.group(1))

            if re.search(regexZUnits, line):
                match = re.search(regexZUnits, line)
                if print_info == True:
                    print("Z Units = %s" % match.group(1))
            
            if re.search(regexEndHeader, line):
                if print_info == True:
                    print("End Header Line = %s" % header_cnt)
                header_end = True
                data_start = header_cnt + 1
            
            if header_open == True and header_end == False:
                if re.search(regexTopsHeader, line):
                    match = re.search(regexTopsHeader, line)
                    if print_info == True:
                        print("Data Column = %s" % match.group(1))
                    DataIDDict[header_cnt] = match.group(1)

            if re.search(regexBeginHeader, line):
                if print_info == True:
                    print("Begin Header Line = %s" % header_cnt)
                header_open = True

            header_cnt += 1                  

    except Error as e:
        print(e)
        return None
    finally:

        TopsInput.close()

    df = pd.read_csv(tops_path,header=None,sep='\\s+' ,skiprows= data_start)
    columns_list = list(DataIDDict.values())
    df.columns = columns_list

    return df 