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


# Columns that will be extracted from the files
def cols_generator():
    pivot = 'Category'
    values = ('all', 'atry', 'econ', 'ecoy', 'etha', 'ethb', 'ethh', 'ethi',
              'ethp', 'ethv', 'ethw', 'eth2', 'lepc', 'sexf', 'sexm', 'sexv')
    base_cols_district = ["YEAR", "REGION", "DISTRICT", "DNAME", "Subject",
                          "Grade", "Language"]
    base_cols_campus = ["CAMPUS", "YEAR", "REGION", "DISTRICT", "DNAME",
                        "CNAME", "Subject", "Grade", "Language"]
    for value in values:
        cols_district = base_cols_district + [pivot, value]
        cols_campus = base_cols_campus + [pivot, value]
        yield (cols_campus, cols_district, pivot, value)
        

class StaarPivotAll:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        for cols in cols_generator():
            self.Process(*cols)
    # end __init__

    def Process(self, cols_campus, cols_district, pivot_col, value_col):
        print("Processing started\nPivot column: %s\nValue column: %s" 
              % (pivot_col, value_col))
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):
            fn = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                try:
                    if "campus" in fn:
                        df = read_csv(file_path,
                                      usecols=cols_campus,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df_pivot = df.set_index(
                            cols_campus[:-1]).unstack(pivot_col)
                    elif 'district-state' in fn:
                        df = read_csv(file_path,
                                      usecols=cols_district,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df_pivot = df.set_index(
                            cols_district[:-1]).unstack(pivot_col)
                    else:
                        print("\t Skipping file: %s" % file_path)
                        
                    self.WriteData(df_pivot, filename, value_col)
                except OSError:
                   print("Error while reading %s" % filename)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name,
                  value):
        """
        Write data_frame
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        output_name = output_name.replace("merged", "pivoted_%s" % value)
        print("\n\tWriting %s" % output_name)
        # fix the column names after multiindexing
        data_frame.reset_index(col_level=1, inplace=True)
        data_frame.columns = data_frame.columns.get_level_values(1)

        # add demo column
        print("\tAdding demo column in: %s" % output_name)
        if "campus" in output_name:
            data_frame.insert(9, 'demo', value)
        elif 'district-state' in output_name:
            data_frame.insert(7, 'demo', value)
        else:
            print("\tDemo column not added in: %s" % output_name)
        
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
    
