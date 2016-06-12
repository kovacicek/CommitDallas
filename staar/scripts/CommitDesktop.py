"""
Created on 28.05.2016.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
"""

from os import path, listdir, mkdir
from os.path import join, exists, isdir
from pandas import read_csv
from commit_utils import Utils
from pandas.parser import CParserError


class StaarWidenAll:
    script_name = "StaarFilterAll"

    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

        Utils.clean_output(self.output_dir)

        self.read_data()
    # end __init__

    def read_data(self):
        print("\nRead Data")
        # List input directory containing the .csv files
        for filename in listdir(self.input_dir):
            fn = path.splitext(filename)[0]
            if path.splitext(filename)[1] == ".csv":
                fp = path.join(self.input_dir, filename)
                print("\nFile path: " + fp)
                try:
                    # determine what columns are going to be used based on fn
                    if "campus" in fn or 'cfy' == fn[0:3]:
                        columns = ['CAMPUS', 'YEAR', 'REGION', 'DISTRICT',
                                   'DNAME', 'CNAME']
                    elif 'district' in fn or 'dfy' == fn[0:3]:
                        columns = ['DISTRICT', 'YEAR', 'REGION', 'DNAME']
                    elif 'state' in fn or 'sfy' == fn[0:3]:
                        columns = ['YEAR']
                    else:
                        print("\t Skipping file: %s" % fp)
                        continue

                    # read file into pandas data frame
                    df = read_csv(fp,
                                  delimiter=",",
                                  header=0,
                                  low_memory=False)

                    # determine what language to use based on filename
                    spanish = ('s3', 's4', 's5')
                    language = ('Spanish' if [ft for ft in spanish if ft in fn]
                                else 'English')

                    # widen data
                    df = StaarWidenAll.convert_data(df, columns,
                                                    language=language)

                    # sort data
                    df = StaarWidenAll.sort_data(df, columns)

                    # write data
                    self.write_data(df, filename)
                except CParserError:
                    print("Error while reading %s, check content" % filename)
                    continue
    # end ReadData

    @staticmethod
    def convert_data(data, columns, language='English'):
        from collections import OrderedDict
        demo_parts = OrderedDict()

        # check if GRADE column exists
        if 'GRADE' in data.columns:
            grade = int(data.loc[0, 'GRADE'])
            data.drop('GRADE', axis=1, inplace=True)
        else:
            grade = 'EOC'

        print('\t Creating parts')
        for col in data.columns[6:]:
            # first n columns are same for all parts
            part = data.ix[:, columns]

            # split column name to extract subject, demo and category
            col_split = col.split('_')

            subject = col_split[0]
            demo = col_split[1]
            category = '_'.join(col_split[2:])

            # add subject, category, grade and language to part
            part['Subject'] = subject
            part['Grade'] = grade
            part['Language'] = language
            part['Category'] = category

            # add demo column to part
            part[demo] = data[col]

            # if part with the same demo exists in demo_parts then append this
            # part on it, otherwise add this part to demo_parts
            if demo_parts.get(demo) is None:
                demo_parts[demo] = part
            else:
                demo_parts[demo] = demo_parts[demo].append(part,
                                                           ignore_index=True)

        print('\t Merging parts into one')
        converted = None
        for demo, frame in demo_parts.items():
            converted = (frame
                         if converted is None
                         else converted.merge(frame, how='outer'))
        return converted

    @staticmethod
    def sort_data(data, columns):
        sort_columns = [columns[0], 'Subject', 'Category']
        data = data.sort(sort_columns)
        return data

    def write_data(self,
                   data_frame,
                   output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        output_name = "%s - Parsed Wide.csv" % output_name
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.output_dir, output_name),
                          sep=",",
                          index=False)
    # end WriteData


def main():
    staar_original = join('..', "1_staar_original")
    staar_wide = join('..', "2_staar_wide")
    # staar_original = join('..', "1_tmp")
    # staar_wide = join('..', "2_tmp")

    dirs = [dir_name for dir_name in listdir(staar_original) if
            isdir(join(staar_original, dir_name))]
    print(dirs)
    for item_dir in dirs:
        input_dir = join(staar_original, item_dir)
        output_dir = join(staar_wide, item_dir)
        StaarWidenAll(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
