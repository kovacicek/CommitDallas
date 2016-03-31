'''
Created on 26.10.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import read_csv
from pandas.core.frame import DataFrame

# Columns related to pivoting
col_name = 'demo'
value = 'sexm'


class AddColumn:
    script_name = "AddColumn"

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

                df = read_csv(file_path,
                              delimiter=",",
                              header=0,
                              low_memory=False)

                self.WriteData(df, filename)
    # end ReadData

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        print("\t Writing %s" % output_name)
        # fix the column names after multiindexing

        if 'district-state' in output_name:
            data_frame.insert(7, col_name, value)

        data_frame.to_csv(join(self.output_dir,
                              output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_pivot = join('..', '5_staar_pivoted')
    tmp = join('..', 'tmp')

    AddColumn(staar_pivot, tmp)
    print("Finished")

if __name__ == "__main__":
    main()
    
