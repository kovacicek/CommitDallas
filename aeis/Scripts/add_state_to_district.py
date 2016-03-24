'''
Created on 17.09.2015.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
'''

from os import listdir, mkdir, remove, getcwd
from os.path import join, splitext, exists
from pandas import ExcelWriter, read_csv, concat
from commit_utils import Utils


class AddStateRow:
    base = join('..', 'Inputs', 'data_csv')
#     data_dir_district = join("..", "Inputs", "2_aeis_district")
#     data_dir_state = join("..", "Inputs", "3_aeis_state")
#     data_dir_output = join("..", "Inputs", "4_district_state")
    data_dir_district =  join(base, 'AEIS 2011-12', 'district')
    data_dir_state = join(base, 'AEIS 2011-12', 'state')
    data_dir_output = join(base, 'AEIS 2011-12', 'district_with_state')

    def __init__(self):
        Utils.clean_output(AddStateRow.data_dir_output)
        self.Process()
    # end __init__

    def Process(self):
        print ("Processing started")
        print(self.data_dir_district)
        if not exists(self.data_dir_district):
            print ("\t Data Directory District Does Not Exist")
            exit()

        elif not exists(self.data_dir_state):
            print ("\t Data Directory State Does Not Exist")
            exit()

        else:
            data_frames = list()
            # List directory containing the .csv files
            for district_item in listdir(self.data_dir_district):
                # Check only .csv files
                if (splitext(district_item)[1] == ".csv"
                        and "_district_reference" not in district_item
                        and "_district_finance" not in district_item):
                    district_file_path = join(self.data_dir_district,
                                              district_item)
                    district_filename = splitext(district_item)[0]

                    # Find proper state file
                    state_file_path = Utils.find_proper_state_file_2(
                        district_filename, self.data_dir_state)

                    if state_file_path is not None:
                        data_frame_output = self.ConcatenateFiles(
                                                        district_file_path,
                                                        state_file_path)
                        self.WriteData(data_frame_output, district_item)
    # end Process

    def ConcatenateFiles(self,
                         district_file_path,
                         state_file_path):
        # read district .csv file
        data_frame_district = read_csv(district_file_path,
                                       delimiter=",",
                                       header=0)
        # read state .csv file
        data_frame_state = read_csv(state_file_path,
                                    delimiter=",",
                                    header=0)

        # rename columns in the state data frame
        columns = dict()
        for col in data_frame_state.columns:
            if col not in ("DISTRICT", "YEAR"):
                columns[col] = "D" + col[1:]
        data_frame_state.rename(columns=columns, inplace=True)

        # concatenate district and state data frames
        # add state at the end
        data_frame_output = concat((data_frame_district, data_frame_state),
                                   ignore_index=True)
        
        # DISTRICT should be the first column
        columns = data_frame_output.columns.tolist()
        columns.remove('DISTRICT')
        columns = ['DISTRICT'] + columns
        data_frame_output = data_frame_output[columns]
        
        # write '1 in DISTRICT column of state row
        data_frame_output['DISTRICT'].iloc[-1] = "'1"

        return data_frame_output
    # end ConcatenateFiles

    def WriteData(self,
                  data_frame,
                  output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.data_dir_output):
            mkdir(self.data_dir_output)
        print ("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.data_dir_output, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    AddStateRow()
    print("Finished")

if __name__ == "__main__":
    main()
