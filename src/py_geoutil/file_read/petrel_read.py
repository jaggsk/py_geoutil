import re
import pandas as pd
import numpy as np
from sqlite3 import Error
from ..coordinates.create_meshgrid import create_indexed_meshgrid
from ..utils.validation import validate_file_path,validate_equal,validate_pattern, validate_boolean

def petrel_irap_classic_grid_read(filename, return_meshgrid=False):

    '''    
    Routine to read Petrel Format Irap Classic Grid To Meshgrid or Pandas Dataframe

    Arguments:
    filename (float): full file location of selected tops file
    return_meshgrid (bool): return either meshgrid or pandas dataframe
    
    Returns:
    Pandas Dataframe containing X,Y,I,J,Z data columns from export
    Or
    Numpy Meshgrid containing X,Y,I,J,Z data columns from export
    Recommend to use np.meshgrid for faster provessing and plotting speed.

    Raises:
    FileNotFoundError if not a valid user supplied filepath
    ValidationError if return_meshgrid is not a boolean operator
    ValidationError if any of the first 3 header lines fail the regualr expression match
    ValidationError if calculated grid dimensions do not match length of input file

    Example:
    X,Y,I,J,Z  = read_petrel_irap_classic_grid(infile,return_meshgrid=True)

    PRECONDITIONS: exported file is a valid Petrel Irap classic grid format.
    KJAGGS Sep 2026
    
    '''

    field_names = []
    grid_definition = {}

    validate_file_path(filename)
    validate_boolean(return_meshgrid, value="Meshgrid/df output selector")

    with open(filename, "r") as f:

        #read header and populate grid_definition dictionary
        header_4_lines = [line.rstrip("\n") for _, line in zip(range(4), f)]

        line1_pattern = r"^\s*(-?\d+)\s+(\d+)\s+([+-]?\d*\.?\d+)\s+([+-]?\d*\.?\d+)\s*$"
        line2_pattern = r"^\s*(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*$"
        line3_pattern = r"^\s*(\d+)\s+(-?\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s*$"

        line1_match = validate_pattern(
            header_4_lines[0],
            line1_pattern,
            "Regular Expression failed IRAP header line 1"
        )
        line1_match = re.match(line1_pattern,header_4_lines[0])
        grid_definition["IRAP Code"] = float(line1_match.group(1))
        grid_definition["No Columns"] = int(line1_match.group(2))
        grid_definition["Grid X Spacing"] = float(line1_match.group(3))
        grid_definition["Grid Y Spacing"] = float(line1_match.group(4))


        line2_match = validate_pattern(
            header_4_lines[1],
            line2_pattern,
            "Regular Expression failed IRAP header line 2"
        )
        line2_match = re.match(line2_pattern,header_4_lines[1])
        grid_definition["Grid X Min"] = float(line2_match.group(1))
        grid_definition["Grid X Max"] = float(line2_match.group(2))
        grid_definition["Grid Y Min"] = float(line2_match.group(3))
        grid_definition["Grid Y Max"] = float(line2_match.group(4))

        line3_match = validate_pattern(
            header_4_lines[2],
            line3_pattern,
            "Regular Expression failed IRAP header line 3"
        )
        line3_match = re.match(line3_pattern,header_4_lines[2])
        grid_definition["No Rows"] = int(line3_match.group(1))
        grid_definition["Rotation Angle"] = float(line3_match.group(2))
        grid_definition["Grid X Origin"] = float(line3_match.group(3))
        grid_definition["Grid Y Origin"] = float(line3_match.group(4))

        #read rest of file
        lines = f.readlines()[:]   # line 4 -> EOF

        z = np.array(
            [float(x) for line in lines for x in line.split()],
            dtype=float
        )

        # IRAP Classic null value
        z[z == 9999900.0] = np.nan


        Z = z.reshape(grid_definition["No Rows"],grid_definition["No Columns"], order="F")

        #validate output grid size
        no_z_values = z.shape[0]
        no_grid_bins = grid_definition["No Rows"]*grid_definition["No Columns"]
        validate_equal(no_z_values, no_grid_bins,name="IRAP Grid Array. No rows x No columns and file length ")

        #create meshgrid
        X, Y = create_indexed_meshgrid(x0=grid_definition["Grid X Origin"],y0=grid_definition["Grid Y Origin"],nx=grid_definition["No Rows"],ny=grid_definition["No Columns"],dx=grid_definition["Grid X Spacing"],dy=grid_definition["Grid Y Spacing"], angle_rot=grid_definition["Rotation Angle"])
        # I and J indices
        J, I = np.indices(X.shape)

        if return_meshgrid:

            return X,Y,J,I,Z
        else:
            # Flatten into dataframe
            df = pd.DataFrame({
                "X": X.ravel(),
                "Y": Y.ravel(),
                "Z": Z.ravel(),
                "I": I.ravel(),
                "J": J.ravel()
                })
        
            return df

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