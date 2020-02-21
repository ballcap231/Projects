from natsort import natsorted
import glob
from pathlib import Path
from os import path
import sys
"""


"""

def concat_txt(dir_):
    filenames = natsorted(glob.glob(path.join(dir_, '*.txt')))

    with open(path.join(dir_, 'full_text.txt'), 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                outfile.write(infile.read())
                outfile.write('\n' + Path(fname).stem + '\n')
                outfile.write('#############################################################' +'\n')
                print('finished writing: ' +  Path(fname).stem)

if __name__ == "__main__":
    dir_ = sys.argv[1]
    if not dir_:
        dir_ = './'
        print('Concatenating text files from current directory')
    concat_txt(dir_)
    print('Finished concatenating txt files')

                