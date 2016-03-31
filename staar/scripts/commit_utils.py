from os.path import splitext, join, exists, splitext
from os import mkdir, listdir, remove

ds_map = {'district': 'D', 
          'campus': 'C'}

class Utils:
    @staticmethod
    def adjust_columns(columns=None, ds=None, year=None):
        adjusted_columns = list()
        # add district/campus and year to columns
        if ds == 'district':
            adjusted_columns.append('DISTRICT')
        elif ds == 'campus':
            adjusted_columns.append('CAMPUS')
        else:
            print("Can't determine district or campus: ds = %" % ds)
        adjusted_columns.append('YEAR')

        if columns is not None:
            # check to see if columns are the same or different for C and D
            # files, determined by type of the columns arg
            if type(columns) == list:
                # when extracted columns from C and D files are the same
                _columns = columns
            elif type(columns) == dict:
                # when extracted columns from C and D files are different
                _columns = columns[ds]
    
            # iterate through columns that need to be extracted from file
            for column in _columns:
                if ds is not None:
                    column = ds_map[ds] + column
                if year is not None:
                    column = column.replace('*YY*', year)
                adjusted_columns.append(column)

        return adjusted_columns
    # end AdjustColumns

    @staticmethod
    def extract_year(filename):
        name_of_file = splitext(filename)[0]
        name_parts = name_of_file.split("_")
        try:
            int(name_parts[0])
            year = name_parts[0][2:]
        except:
            year = None
        return year
    # end extract_year

    @staticmethod
    def extract_type(filename):
        name_of_file = splitext(filename)[0]
        name_parts = name_of_file.split("_")
        return name_parts[2]
    # end extract_type

    @staticmethod
    def write_data(data_frame,
                   output_name,
                   output_dir):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(output_dir):
            mkdir(output_dir)
        print("\t Writing file %s" % join(output_dir, output_name))
        data_frame.to_csv(join(output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData
    
    @staticmethod
    def find_proper_state_file_1(district_filename, data_dir_state):
        """
        For files with names: YYYY_district/state/campus_type.csv
        It returns state file that corresponds to district filename.
        If corresponding file is not found, return value is None
        """
        for state_item in listdir(data_dir_state):
            # Check only .csv files
            if splitext(state_item)[1] == ".csv":
                state_file_path = join(data_dir_state, state_item)
                # get full name of the state file
                state_filename = splitext(state_item)[0]
                tmp = state_filename.replace("state", "district")
                if district_filename == tmp:
                    return state_file_path
        else:
            print("There is no corresponding file for %s" % district_filename)
            return None
    # end FindProperStateFile
    
    @staticmethod
    def find_proper_state_file_2(district_filename, data_dir_state):
        """
        For files with names: d/s/ctype.csv
        It returns state file that corresponds to district filename.
        If corresponding file is not found, return value is None
        """
        for state_item in listdir(data_dir_state):
            # Check only .csv files
            if splitext(state_item)[1] == ".csv":
                state_file_path = join(data_dir_state, state_item)
                # get full name of the state file
                state_filename = splitext(state_item)[0]
                tmp = 'd%s' % state_filename[1:]
                if district_filename == tmp:
                    return state_file_path
        else:
            print("There is no corresponding file for %s" % district_filename)
            return None
    # end FindProperStateFile

    def clean_output(data_dir_output):
        print("Clean Output")
        if exists(data_dir_output):
            for item in listdir(data_dir_output):
                remove(join(data_dir_output, item))
            print("\tOutput directory %s cleaned" % data_dir_output)
        else:
            print("\tOutput directory does not exist: %s" % (data_dir_output))
    # end CleanOutput
