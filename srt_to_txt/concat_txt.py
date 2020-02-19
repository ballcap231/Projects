from natsort import natsorted
import glob
from pathlib import Path
from os import path

"""


"""

dir_ = r'txt_files'

filenames = natsorted(glob.glob(path.join(dir_, '*.txt')))

with open(path.join(dir_, 'full_text.txt'), 'w') as outfile:
    for fname in filenames:
        with open(fname) as infile:
            outfile.write(infile.read())
            outfile.write('\n' + Path(fname).stem + '\n')
            print('finished writing: ' +  Path(fname).stem)
            