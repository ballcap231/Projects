import pysrt
import glob
from os import path
from pathlib import Path
import srt_to_txt
from natsort import natsorted
"""
dir_ folder should contain all srt files - assumed to be numerically ordered by file name


"""

dir_ r'srt_files'

for f in natsorted(glob.glob(path.join(dir_, '*.srt')), reverse =True):
    srt_to_txt.main(['',path.basename(f), 'utf-8'])
    print('finished writing: ' +  Path(f).stem)
    # with open(f, 'r') as srt_f:
    #     data = srt_f.read()
    #     with open( Path(f).stem + '.txt', 'w') as to_file:
    #         to_file.write(data)
    #         print('finished writing: ' + Path(f.stem))

