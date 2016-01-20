from os.path import splitext, join, exists
from os import mkdir

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
    def add_column(data_frame, col_name, value):
        pass