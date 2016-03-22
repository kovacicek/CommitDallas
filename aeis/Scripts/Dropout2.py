'''
Created on 29.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat, merge
from pandas.core.frame import DataFrame

# Columns that will be extracted from the files
Columns = ["B0912DR*R",
           "A0912DR*R",
           "30912DR*R",
           "R0912DR*R",
           "E0912DR*R",
           "F0912DR*R",
           "H0912DR*R",
           "L0912DR*R",
           "M0912DR*R",
           "I0912DR*R",
           "40912DR*R",
           "S0912DR*R",
           "20912DR*R",
           "W0912DR*R"
           ]

DS = {'district': 'D',
      'campus': 'C'}


class Dropout2:
    script_name = "Dropout2"
    # inputs = {ds : (input_dir, output_dir)}
    inputs = {"campus": (join("..", "Inputs", "AEIS_Campus"),
                         "%sCampus" % script_name),
              "district": (join("..", "Inputs", "DistrictState"),
                           "%sDistrict" % script_name)
             }
    columns_dict = dict()

    def __init__(self):
        self.CleanOutput()
        self.ReadData()
        self.Merge()
    # end __init__

    def Merge(self):
        print("Start merging")

        # Read Inputs
        for key, value in self.inputs.items():
            data_frames = list()

            # read generated files and append those data frames to the list
            for item in listdir(value[1]):
                if path.splitext(item)[1] == ".csv":
                    f = path.join(value[1], item)
                    data_frames.append(read_csv(f,
                                                delimiter=",",
                                                header=0,
                                                low_memory=False))

            # Merge data frames into one data frame
            data = data_frames[0]
            for item in data_frames[1:]:
                data = data.append(item)

            # Write to output
            merged_file = join("..",
                               "MergedFiles",
                               "%s_%s.csv" % (self.script_name, key))
            print("Merged file: " + merged_file)

            # get output columns from self.columns_dict dictionary
            cols = self.GetOutputCols(ds=key) 
            
            # write merged data frame to csv file
            data.to_csv(merged_file, sep=",", index = False, columns=cols)
            print("\t %s files merged into: %s" % (key, merged_file))
    # end Merge

    def GetOutputCols(self, ds):
        """
        From self.columns_dict dictionary extract columns that will be written
        to the output file. This is being done because of writing order
        """
        a = list()
        a.append("DISTRICT" if ds == 'district' else "CAMPUS")
        a.append("YEAR")
        b= [x for x in set(self.columns_dict.values()) if
                (x[0].lower() == ds[0].lower())]
        return a + b
    # end GetOutputCols

    def AdjustColumn(self, ds, year=None):
        adjusted_columns = list()
        # add district/campus and year to columns
        if ds == 'district':
            adjusted_columns.append('DISTRICT')
            # self.columns_dict['DISTRICT'] = 'DISTRICT'
        elif ds == 'campus':
            adjusted_columns.append('CAMPUS')
            # self.columns_dict['CAMPUS'] = 'CAMPUS'
        else:
            print("Can't determine district or campus: ds = %" % ds)
        adjusted_columns.append('YEAR')
        self.columns_dict['YEAR'] = 'YEAR'
        # sometimes in files stands year
        adjusted_columns.append('year')
        self.columns_dict['year'] = 'YEAR'

        for column in Columns:
            if ds is not None:
                column = DS[ds] + column
                key = column
            if year is not None:
                column = column.replace('*', year)
            adjusted_columns.append(column)
            self.columns_dict[column] = key
        return adjusted_columns
    # end AdjustColumns

    def CleanOutput(self):
        print("Clean Output")
        for key, value in self.inputs.items(): 
            if exists(value[1]):
                for item in listdir(value[1]):
                    remove(join(value[1], item))
                print("\t %s output dir cleaned: %s" % (key, value[1]))
    # end CleanOutput

    def ReadData(self):
        print("\nRead Data")
        for ds, value in self.inputs.items():
            if not path.exists(value[0]):
                print("\t Data Directory Does Not Exist %s" % value[0])
                exit()
            else:
                # List directory containing the .csv files
                for item in listdir(value[0]):
                    # Check the extension of the files,
                    # so only .csv files will be considered
                    name_of_file = path.splitext(item)[0]
                    name_parts = name_of_file.split("_")
                    name_year = str(int(name_parts[0]) - 1)[2:4]

                    if(path.splitext(item)[1] == ".csv" 
                       and name_parts[2] == "noner"):
                        file_path = path.join(value[0], item)
                        adjusted_columns = self.AdjustColumn(ds=ds,
                                                             year=name_year)
                        self.adjusted = adjusted_columns
                        
                        data_frames = list()
                        for col in adjusted_columns:
                            try:
                                data_f = read_csv(file_path,
                                                  usecols=[col],
                                                  delimiter=",",
                                                  header=0,
                                                  low_memory=False)
                                data_frames.append(data_f)
                            except:
                                # year column in files can be YEAR or year
                                if col.lower() != 'year':
                                    print("No such column %s" % col)
                        data_frame = data_frames[0]
                        for right_frame in data_frames[1:]:
                            data_frame = merge(data_frame,
                                               right_frame,
                                               left_index=True,
                                               right_index=True,
                                               sort=False)
                        data_frame.rename(columns=self.columns_dict,
                                          inplace=True)
                        self.WriteData(data_frame, item, value[1])
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name,
                  output_dir):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(output_dir):
            mkdir(output_dir)
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    Dropout2()
    print("Finished")

if __name__ == "__main__":
    main()
