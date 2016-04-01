'''
Created on 07.11.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import path, listdir, mkdir, remove
from os.path import join, splitext, exists, basename
from pandas import ExcelWriter, read_csv, concat


class StaarMergeAll:
    script_name = "StaarMergeAll"
    data_frames = list()

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        
        self.ReadData()
        self.Merge()
    # end __init__

    def ReadData(self):
        print("\nRead Data")
        self.data_frames = list()
        # List directory containing the .csv files
        for filename in listdir(self.input_dir):
            # Check file extensions,
            # only .csv files will be considered
            if(path.splitext(filename)[1] == ".csv"):
                file_path = path.join(self.input_dir, filename)

                # Pandas.read_csv method returns DataFrame object
                try:
                    data_frame = read_csv(file_path,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                    self.data_frames.append(data_frame)
                    print("\tFile appended: %s" % filename)
                except:
                    print("\tError while reading: %s" % filename)
    # end ReadData

    def Merge(self):
        print("Merging started")
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        data = concat(self.data_frames)

        # Change filename
        if 'filtered' in basename(self.input_dir):
            fn = basename(self.input_dir.replace('filtered', 'merged'))
        else:
            fn = '%s_merged' % basename(self.input_dir)

        # Write to output
        merged_file = join(
            self.output_dir,
            "%s.csv" %(fn))
        data.to_csv(merged_file, sep=",", index = False)
        print("\t%s files merged into: %s" % (self.input_dir, merged_file))
    # end Merge

def main():
    staar_filter = join('..', "3_staar_filtered")
    staar_merged = join('..', "4_staar_merged")

    # clean output directory
    from commit_utils import Utils
    Utils.clean_output(staar_merged)

    for item_dir in listdir(staar_filter):
        input_dir = join(staar_filter, item_dir)
        # output_dir = join(staar_merged, item_dir)
        output_dir = staar_merged
        StaarMergeAll(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
