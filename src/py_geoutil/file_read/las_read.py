#python imports
import re
import pandas as pd


def readlasfile(las_path = None,print_info = True):

    '''
    Subroutine to read .Las format file and return data as Pandas dataframe
    Inputs path referenced to input Las file
    Outputs = Pandas dataframe rows = number data points in depth, columns = no of individual log curves                                                                                        
    Kevin Jaggs June 2018                                                                                
    (string)=>(pandas dataframe)
    Preconditions: 
    1) Inpath file name has been formatted to include \\ backslash escape prior to folder 
    2) Las file exists!
    3) Las file is in the correct format
    '''  
    #print(path)

    #Boolean operator is triggered false when ~Ascii line is reached
    header_end = False
    header_cnt = 0

    #Variables for header information
    DepthStart = ""
    DepthStep = ""
    DepthStop = ""
    NullValue = ""
    WellID = ""
    UWI = ""    
    WellX = ""
    WellY = ""
    WellKB = ""
    WellID = ""
    
    #regex pattern matches to extract well header data from LAS file
    regexStartD = "^STRT\\s{0,5}\\.\\w{1,2}\\s+(\\d+\\.?\\d{0,5})\\s+:"
    regexStepD = "^STEP\\s{0,5}\\.\\w{1,2}\\s+(\\d+\\.?\\d{0,5})\\s+?:"
    regexStopD = "^STOP\\s{0,5}\\.\\w{1,2}\\s+(\\d+\\.?\\d{0,5})\\s+?:"
    regexNullV = "^NULL\\s{0,5}\\.\\s+(-?\\d+\\.?\\d{0,5})\\s+?:"
    regexUWI = "^UWI\\s{0,5}\\.\\s+(.{0,30})\\s+?:"
    regexXwell = "^XWELL\\s{0,5}\\.\\w{0,2}\\s+(\\d+\\.?\\d{0,5}).*?:"
    regexYwell = "^YWELL\\s\\.\\w{0,2}\\s+(\\d+\\.?\\d{0,5}).*?:"
    regexKB = "^EDF\\s{0,5}\\.\\s+(\\d+\\.\\d{0,5}).*:"
    regexWellID = "^WELL\\s{0,5}\\.\\s+(.{0,30})\\s+:"
    regexCurveID = "^(.*?)\\s+(.*?)\\s+\\:\\s+\\d{0,3}?\\s{0,10}?(\\w+)"
    #regexCurveID = "^(\w+)\s+\\.(\w{0,10}\/?\w{0,7}?)\s+\:\s+\d{0,3}?\s{0,10}?(\w+)"
    #regexCurveID = "^(\w+)\\s{0,60}?\\.([A-Za-z\/0-9\_]{0,12}\\.?[A-Za-z\/0-9\_]{0,12}?)\\s+\:\\s+\d{0,3}?\\s{0,10}?(\w+)"
    regexAscii = "^~Ascii"
    
    #lists to host curve names + curve units, used a 2 headers in final dataframe columns
    CurveIDList = []
    CurveUnitsList = [] 
    
    CurveCnt = 0

    #text reader set to read data specfically between markers
    #pattern matches before the line ~Curve will not be added tp the log list    
    write_logs = False
    
    #read las file
    try:
        LasInput = open(las_path, "r")
        #print (LasInput.read())
        for line in LasInput:

            if re.search("^\\S", line):
                #if first character not a space
                #print(line)
                header_cnt += 1

                if re.search("^~Curve",line):
                    #print("Curve Found")
                    write_logs = True
                
                if re.search(regexStartD, line):
                    match = re.search(regexStartD, line)
                    #print("Well ID = %s" % match.group(1))
                    DepthStart = match.group(1)

                if re.search(regexStepD, line):
                    match = re.search(regexStepD, line)
                    #print("Well ID = %s" % match.group(1))
                    DepthStep = match.group(1)

                if re.search(regexStopD, line):
                    match = re.search(regexStopD, line)
                    #print("Well ID = %s" % match.group(1))
                    DepthStop = match.group(1)

                if re.search(regexNullV, line):
                    match = re.search(regexNullV, line)
                    #print("Well ID = %s" % match.group(1))
                    NullValue = match.group(1)

                if re.search(regexUWI, line):
                    match = re.search(regexUWI, line)
                    #print("Well ID = %s" % match.group(1))
                    UWI = match.group(1)

                if re.search(regexWellID, line):
                    match = re.search(regexWellID, line)
                    #print("Well ID = %s" % match.group(1))
                    WellID = match.group(1)
                
                if re.search(regexXwell, line):
                    #print(line)
                    match = re.search(regexXwell, line)
                    #print("KB = %s" % match.group(1))
                    WellX = match.group(1)

                if re.search(regexYwell, line):
                    match = re.search(regexYwell, line)
                    #print("KB = %s" % match.group(1))
                    WellY = match.group(1)

                if re.search(regexKB, line):
                    match = re.search(regexKB, line)
                    #print("KB = %s" % match.group(1))
                    WellKB = match.group(1)

                if re.search(regexAscii, line):
                    match = re.search(regexAscii,line)
                    header_end = True

                if re.search(regexCurveID, line):
                    #print("Log Found", write_logs)
                    if write_logs == True:
                        #print("TRUE MARKER")
                        match = re.search(regexCurveID, line)
                        CurveIDList.insert(CurveCnt, match.group(1))
                        #replace _ character with unitless
                        curve_unit_temp = match.group(2)
                        curve_unit = curve_unit_temp.replace("_","Unitless")
                        CurveUnitsList.insert(CurveCnt, curve_unit)
                        #print("%" + match.group(1) + "%" + "    " + "%" + match.group(2) + "%")
                        #print(match.group(2),"end")
                        CurveCnt += 1
                        
    except Error as e:
        print(e)
    finally:
        LasInput.close()

    #header info will not be present in every data export, if not found add deault string info.
    if DepthStart == "":
        DepthStart = "Not found..."    
    if WellID == "":
        WellID = "Not found..."    
    if WellX == "":
        WellX = "Not found..."
    if WellY == "":
        WellY = "Not found..." 
    if WellKB == "":
        WellKB = "Not found..."         

    #Print summary of information found 
    if print_info == True:
        print("Start Log Depth = %s" % DepthStart)
        print("Log Step = %s" % DepthStep)
        print("End Log Depth = %s" % DepthStop)
        print("Null Values = %s" % NullValue) 
        print("UWI = %s" % UWI) 
        print("Well ID = %s" % WellID)
        print("Well X = %s" % WellX)
        print("Well Y = %s" % WellY)
        print("Well KB = %s" % WellKB)

        print("\nNumber Of Curves Found = %s" %CurveCnt)
        print(CurveIDList)
        print("\n")
        #print(CurveUnitsList)
        #print(len(CurveIDList))
        #print(len(CurveUnitsList))
            #create dataframe, split on whitespace, skip header, columns to be added next   
    #df = pd.read_csv(las_path,header=None,delim_whitespace=True ,skiprows= (totalcnt - nonheadcnt + 1))
    df = pd.read_csv(las_path,header=None,sep='\\s+' ,skiprows= header_cnt)

    #add main column header = name of curve
    df.columns = CurveIDList
    #add second column header = curve untis
    df.columns = pd.MultiIndex.from_arrays([df.columns, CurveUnitsList], names=['Curve','Units'])
    #print(df.head(80))
    
    df[('WELLID','name')] = WellID
    df[('UWI','name')] = UWI
    
    return df
    