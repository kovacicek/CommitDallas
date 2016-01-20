'''
Created on 19.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import listdir, remove
from os.path import join, splitext, exists
from pandas import read_csv
from utils import *

# Columns that will be extracted from the files
Columns = {'campus': ["PSTEXPA",
                      "PSTTOSA",
                      "PST00SA",
                      "PST00FP",
                      "PST01FP"],
           'district': ["PSTURNR",
                        "PSTEXPA",
                        "PSTTOSA",
                        "PST00SA",
                        "PST00FP",
                        "PST01FP"]
           }

class StaffTeacher:
    script_name = "StaffTeacher"
    inputs = {"campus": (join("..", "Inputs", "1_aeis_campus"),
                         join("..", "Outputs", "%sCampus" % script_name)),
              "district": (join("..", "Inputs", "4_district_state"),
                           join("..", "Outputs", "%sDistrict" % script_name))
              }
    merged_files_dir = join("..", "MergedFiles")

    def __init__(self):
        self.clean_output()
        self.read_data()
        self.merge()
    # end __init__

    def clean_output(self):
        print("Clean Output")
        for key, value in self.inputs.items(): 
            if exists(value[1]):
                for item in listdir(value[1]):
                    remove(join(value[1], item))
                print("\t %s output dir cleaned: %s" % (key, value[1]))
    # end CleanOutput

    def read_data(self):
        print("\nRead Data")
        for ds, value in self.inputs.items():
            if not exists(value[0]):
                print("\t Data Directory Does Not Exist %s" % value[0])
                exit()
            else:

                # List directory containing the .csv files
                for filename in listdir(value[0]):
                    # Check the extension of the files,
                    # so only .csv files will be considered

                    if(splitext(filename)[1] == ".csv" 
                       and Utils.extract_type(filename) == "staff"):
                        # create path to the file
                        file_path = join(value[0], filename)

                        # extract year from file_name
                        year = Utils.extract_year(filename)
                        # adjust columns
                        adjusted_columns = Utils.adjust_columns(
                            columns=Columns, ds=ds, year=year)
                        self.adjusted = adjusted_columns

                        # Pandas.read_csv method returns DataFrame object
                        try:
                            data_frame = read_csv(file_path,
                                              usecols=adjusted_columns,
                                              delimiter=",",
                                              header=0,
                                              low_memory=False)
                            Utils.write_data(data_frame, filename, value[1])
                        except:
                            print("Error while reading %s" % filename)
                            print("Columns: %s\n" % adjusted_columns)
    # end ReadData

    def merge(self):
        print("Start merging")
        # create merge directory
        if not exists(self.merged_files_dir):
            mkdir(self.merged_files_dir)

        # Read Inputs
        for key, value in self.inputs.items():
            print("\t Merging %s" % key)
            data_frames = list()
            for item in listdir(value[1]):
                if splitext(item)[1] == ".csv":
                    f = join(value[1], item)
                    data_frames.append(read_csv(f,
                                                delimiter=",",
                                                header=0,
                                                low_memory=False))
            # Merge data
            if data_frames:
                data = data_frames[0]
                for item in data_frames[1:]:
                    data = data.append(item)
    
                # Write to output
                merged_file = join("..",
                                   "MergedFiles",
                                   "%s_%s.csv" % (self.script_name, key))
                data.to_csv(merged_file, sep=",", index = False)
                print("\t %s files merged into: %s" % (key, merged_file))
            else:
                print('\t Error while merging %s data' % key)
    # end Merge


def main():
    StaffTeacher()
    print("Finished")

if __name__ == "__main__":
    main()
