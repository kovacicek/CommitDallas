'''
Created on 07.11.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists, isdir
from pandas import ExcelWriter, read_csv, concat, merge
from pandas.core.frame import DataFrame

valuesCampus = ["d",
                "rs",
                "satis_ph1_nm",
                "satis_rec_nm"]

valuesDS = ["d",
            "rs",
            "satis_ph1_nm",
            "satis_ph2_nm",
            "satis_rec_nm"]


class StaarFilterAll:
    script_name = "StaarFilterAll"

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        from commit_utils import Utils
        Utils.clean_output(self.output_dir)

        self.ReadData()
    # end __init__

    def ReadData(self):
        print("\nRead Data")
        # List input directory containing the .csv files
        for filename in listdir(self.input_dir):
            fn = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                print("File path: " + file_path)
                # Pandas.read_csv method returns DataFrame object
                try:
                    if "campus" in fn or 'c' == fn[0]:
                        df = read_csv(file_path,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df = df[df['Category'].isin(valuesCampus)]
                    elif ('district' in fn or 'dfy' == fn[0] or
                          'state' in fn or 'sfy' == fn[0]):
                        df = read_csv(file_path,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                        df = df[df['Category'].isin(valuesDS)]
                        if 'state' in fn or 'sfy' == fn[0]:
                            print('\t State file modification')
                            df.insert(0, 'DISTRICT', "1")
                    else:
                        print("\t Skipping file: %s" % file_path)
                        continue
   
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
        # remove '- parsed wide' from file name
        output_name = "%s_filtered.csv" % output_name.split(" - ")[0]
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_wide = join('..', "2_staar_wide")
    staar_filtered = join('..', "3_staar_filtered")

    for item_dir in listdir(staar_wide):
        input_dir = join(staar_wide, item_dir)
        output_dir = join(staar_filtered, item_dir)   
        StaarFilterAll(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
    