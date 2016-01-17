'''
Created on 03.11.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists, basename
from pandas import ExcelWriter, read_csv, concat
from astropy.extern.bundled.six import next


class StaarDSMerge:
    script_name = "StaarDSMerge"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        # self.CleanOutput()
        self.ReadData()
        self.Merge()
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
            # Check the extension of the files,
            # so only .csv files will be considered
            name_of_file = path.splitext(filename)[0]
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)
                print("Filepath: %s", file_path)
                # Pandas.read_csv method returns DataFrame object
                try:
                    data_frame = read_csv(file_path,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                    #if "state" in filename:
                    #    data_frame.drop('DISTRICT', 1, inplace=True)
                    #    data_frame.insert(0, 'DISTRICT', 1)
                    self.data_frames.append(data_frame)
                    print("File with name %s appended" % filename)
                    # self.WriteData(data_frame, filename)
                except:
                    print("Error while reading %s" % filename)
    # end ReadData

    def Merge(self):
        print("Start merging")
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        data =  concat(self.data_frames)

        # Write to output
        merged_file = join(self.output_dir,
                           "%s_merged.csv" % (basename(self.input_dir)))
        data.to_csv(merged_file, sep=",", index = False)
        print("\t %s files merged into: %s" % (self.input_dir, merged_file))
    # end Merge

def main():
    staar_filter = "3_staar_filtered"
    staar_merged = "4_staar_merged"

    for item_dir in listdir(staar_filter):
        input_dir = join(staar_filter, item_dir)
        # output_dir = join(staar_merged, item_dir)
        output_dir = staar_merged
        StaarDSMerge(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
