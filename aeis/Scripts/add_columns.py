from utils import *
from os.path import join
from pandas import read_csv

files_columns_map = (
    [join('..', 'Inputs', '1_aeis_campus'), '2015_campus_staff.csv', 'YEAR', '2015'],
    [join('..', 'Inputs', '2_aeis_district'), '2015_district_staff.csv', 'YEAR', '2015'],
    [join('..', 'Inputs', '3_aeis_state'), '2015_state_staff.csv', 'YEAR', '2015'],
    [join('..', 'Inputs', '3_aeis_state'), '2015_state_staff.csv', 'DISTRICT', 'state']
    )

def main():
    # add YEAR to 2015_campus_staff.csv
    for item in files_columns_map:
        # create local variables from list values
        file_dir = item[0]
        file_name = item[1]
        col = item[2]
        value = item[3]
        file_path = join(file_dir, file_name)

        print('Reading file %s' % file_path)
        # read data frame
        data_frame = read_csv(file_path,
                              delimiter=",",
                              header=0,
                              low_memory=False)
        # add column
        data_frame[col] = str(value)
        # write data frame
        Utils.write_data(data_frame, file_name, file_dir)

if __name__ == '__main__':
    main()
