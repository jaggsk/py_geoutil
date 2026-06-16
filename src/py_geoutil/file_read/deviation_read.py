import pandas as pd
import re

def read_ukooa_deviation(infile=None):

    header_pattern = r'^(H\d+)\s+(.+?):\s+(.*)$'
    header_dict= {}
    header_cnt = 0
    data_pattern = r"^D\s"
    data_list= []
    data_cnt = 0

    with open(infile, "r") as f:



        for line in f:
            header_match = re.match(header_pattern, line)

            data_match = re.match(data_pattern, line)

            if header_match:
                header_cnt+=1
                headerid_match, headertext_match, headerdata_match = header_match.groups()
                header_dict[headertext_match] = headerdata_match

            if data_match:
                data_list.append(line.split()[1:])
                data_cnt += 1
                #print(group2)
                #print(group3)

#            print(line.strip())
        #print(header_dict['Format Name and Version'])
        df = pd.DataFrame(data_list, columns=["MD","INC","AZI","Unknown","Unknown 2","TVD","Offset N", "Offset E","TVDSS","X","Y","LAT","LON"])
        #df = pd.DataFrame(data_rows, columns=["MD","INC","AZI"]).astype(float)

        return df
    