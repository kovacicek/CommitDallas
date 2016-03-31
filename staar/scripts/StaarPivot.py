'''
Created on 26.10.2015.

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
index_col = "CAMPUS"
pivot_col = "Category"
value_col = "sexm"

# Columns that will be extracted from the files
Columns = [index_col,
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


class StaarPivot:
    script_name = "StaarPivot"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.Process()
    # end __init__

    def Process(self):
        print("\nRead Data")
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):
            name_of_file = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                print("File path: " + file_path)

                try:
                    df = read_csv(file_path,
                                  usecols=Columns,
                                  delimiter=",",
                                  header=0,
                                  low_memory=False)

                    df_pivot = df.set_index(Columns[:-1]).unstack(pivot_col)

                    self.WriteData(df_pivot, filename)
                except OSError:
                   print("Error while reading %s" % filename)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        output_name = output_name.replace("merged", "pivoted_%s" % value_col)
        print("\t Writing %s" % output_name)
        # fix the column names after multiindexing
        data_frame.reset_index(col_level=1, inplace=True)
        data_frame.columns = data_frame.columns.get_level_values(1)

        data_frame.to_csv(join(self.output_dir,
                              output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_merge = "4_staar_merged"
    staar_pivot = "5_staar_pivoted"

#     for item_dir in listdir(staar_merge):
#         input_dir = join(staar_merge, item_dir)
#         output_dir = join(staar_pivot, item_dir)
#         input_dir = staar_merge
#         output_dir = staar_pivot
#         StaarPivot(input_dir, output_dir)
#         StaarPivot(input_dir, output_dir)
    StaarPivot(staar_merge, staar_pivot)
    print("Finished")

if __name__ == "__main__":
    main()
    
