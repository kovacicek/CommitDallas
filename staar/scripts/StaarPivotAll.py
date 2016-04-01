'''
Created on 07.11.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat, merge, pivot, pivot_table
from pandas.core.frame import DataFrame

# Columns related to pivoting
pivot_col = "Category"
value_col = "econ"

# Columns that will be extracted from the files
ColumnsCampus = ["CAMPUS",
                 "YEAR",
                 "REGION",
                 "DISTRICT",
                 "DNAME",
                 "CNAME",
                 "Subject",
                 "Grade",
                 "Language",
                 pivot_col,
                 value_col
                 ]

ColumnsDS = ["YEAR",
             "REGION",
             "DISTRICT",
             "DNAME",
             "Subject",
             "Grade",
             "Language",
             pivot_col,
             value_col
             ]


class StaarPivotAll:
    script_name = "StaarPivotAll"

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.Process()
    # end __init__

    def Process(self):
        print("Processing started")
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):
            fn = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                try:
                    if "campus" in fn:
                        df = read_csv(file_path,
                                      usecols=ColumnsCampus,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df_pivot = df.set_index(
                            ColumnsCampus[:-1]).unstack(pivot_col)
                    elif 'district-state' in fn:
                        df = read_csv(file_path,
                                      usecols=ColumnsDS,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df_pivot = df.set_index(
                            ColumnsDS[:-1]).unstack(pivot_col)
                    else:
                        print("\t Skipping file: %s" % file_path)
                        
                    self.WriteData(df_pivot, filename)
                except OSError:
                   print("Error while reading %s" % filename)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Write data_frame
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        output_name = output_name.replace("merged", "pivoted_%s" % value_col)
        print("\t Writing %s" % output_name)
        # fix the column names after multiindexing
        data_frame.reset_index(col_level=1, inplace=True)
        data_frame.columns = data_frame.columns.get_level_values(1)

        # add demo column
        if "campus" in output_name:
            data_frame.insert(9, 'demo', value_col)
        elif 'district-state' in output_name:
            data_frame.insert(7, 'demo', value_col)
        else:
            print("\t Demo column not added in: %s" % output_name)
        
        data_frame.to_csv(join(self.output_dir,
                              output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_merge = join('..', "4_staar_merged")
    staar_pivot = join('..', "5_staar_pivoted")

    StaarPivotAll(staar_merge, staar_pivot)
    print("Finished")

if __name__ == "__main__":
    main()
    
