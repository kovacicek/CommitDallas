"""
Created on 28.05.2016.

@author: Milan Kovacic
@e-mail: kovacicek@hotmail.com
@e-mail: milankovacic1988@gmail.com
@skype: kovacicek0508988
"""

from os import path, listdir, mkdir
from os.path import join, exists
from pandas import read_csv, DataFrame, concat
from commit_utils import Utils


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
                print("File path: " + fp)
                # Pandas.read_csv method returns DataFrame object
                # try:
                if "campus" in fn or 'cfy' == fn[0:3]:
                    if [ft for ft in
                            ('ea1', 'ebi', 'ee1', 'ee2', 'eus') if ft in fn]:
                        df = read_csv(fp,
                                      delimiter=",",
                                      header=0,
                                      low_memory=False)
                elif ('district' in fn or 'dfy' == fn[0:3] or
                      'state' in fn or 'sfy' == fn[0:3]):
                    df = read_csv(fp,
                                  delimiter=",",
                                  header=0,
                                  low_memory=False)
                    if 'state' in fn or 'sfy' == fn[0:3]:
                        print('\t State file modification')
                        df.insert(0, 'DISTRICT', "1")
                else:
                    print("\t Skipping file: %s" % fp)
                    continue

                df = self.convert_data(df)

                self.write_data(df, filename)
                # except:
                #     print("Error while reading %s" % filename)
    # end ReadData

    @staticmethod
    def convert_data(data, language='English'):
        columns = ('CAMPUS', 'YEAR', 'REGION', 'DISTRICT', 'DNAME',	'CNAME',
                   'Subject', 'Grade', 'Language', 'Category')

        converted = DataFrame(index=columns)
        print(converted)

        demo_parts = dict()
        for col in data.columns[6:]:
            # first 6 columns are equal to all parts
            part = data.ix[:, columns[:6]]

            # split column name to extract subject, demo and category
            col_split = col.split('_')

            subject = col_split[0]
            demo = col_split[1]
            category = '_'.join(col_split[2:])

            # add subject, category, grade and language to part
            part['Subject'] = subject
            part['Category'] = category
            part['Grade'] = data.GRADE if 'GRADE' in data.columns else 'EOC'
            part['Language'] = language

            # add demo column to part
            part[demo] = data.ix[:, col]
            # print(part)

            # if part with the same demo exists in demo_parts then append this
            # part on it, otherwise add this part to demo_parts
            if demo_parts.get(demo) is None:
                demo_parts[demo] = part
            else:
                demo_parts[demo] = demo_parts[demo].append(part, ignore_index=True)

        # TODO:
        # all demo_part has 6 additional Categories
        # docs_n, abs_n, oth_n, docs_r, abs_r, oth_r
        # remove them or add them to other demo_parts

        # TODO:
        # merge all demo_parts

        print(demo_parts)

        return converted

    def write_data(self,
                   data_frame,
                   output_name):
        """
        Demonstrated how to write files in .csv and .xlsx format
        DataFrame object has methods to_csv and to_excel
        """
        if not exists(self.output_dir):
            mkdir(self.output_dir)
        # remove '- parsed wide' from file name
        output_name = "%s - Parsed Wide.csv" % output_name
        print("\t Writing %s" % output_name)
        data_frame.to_csv(join(self.output_dir, output_name),
                          sep=",",
                          index=True)
    # end WriteData


def main():
    # staar_original = join('..', "1_staar_original")
    # staar_wide = join('..', "2_staar_wide")
    staar_original = join('..', "1_tmp")
    staar_wide = join('..', "2_tmp")

    for item_dir in listdir(staar_original):
        input_dir = join(staar_original, item_dir)
        output_dir = join(staar_wide, item_dir)
        StaarWidenAll(input_dir, output_dir)
    print("Finished")

if __name__ == "__main__":
    main()
