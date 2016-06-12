'''
Created on 02.11.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat, merge
from pandas.core.frame import DataFrame
#from bokeh.sampledata.stocks import filename

values = ["d",
          "rs",
          "satis_ph1_nm",
          "satis_ph2_nm",
          "satis_rec_nm"]


class StaarDSFilter:
    script_name = "StaarDSFilter"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.CleanOutput()
        self.ReadData()
    # end __init__

    def CleanOutput(self):
        """
        Cleans output dir if exists
        """
        print("Clean Output")
        if exists(self.output_dir):
            for item in listdir(self.output_dir):
                remove(join(self.output_dir, item))
            print("\t output dir cleaned: %s" % (self.output_dir))
        else:
            print("\t output dir does not exist: %s" % (self.output_dir))
    # end CleanOutput

    def ReadData(self):
        print("\nRead Data")
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):

            name_of_file = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                # Pandas.read_csv method returns DataFrame object
                try:
                    df = read_csv(file_path,
                                  delimiter=",",
                                  header=0,
                                  low_memory=False)
                    df = df[df['Category'].isin(values)]
                    if "state" in name_of_file:
                        df.insert(0, 'DISTRICT', "1")
                    self.WriteData(df, filename)
                except:
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
        output_name = "%s_filtered.csv" % output_name.split(" - ")[0]
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_wide = "2_staar_wide"
    staar_filtered = "3_staar_filtered"

    for item_dir in listdir(staar_wide):
        input_dir = join(staar_wide, item_dir)
        output_dir = join(staar_filtered, item_dir)   
        StaarDSFilter(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
    