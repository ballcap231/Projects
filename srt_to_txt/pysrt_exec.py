import pysrt
import glob
from os import path
from pathlib import Path
import srt_to_txt
from natsort import natsorted
from concat_txt import concat_txt


"""
dir_ folder should contain all srt files - assumed to be numerically ordered by file name
"""
srt_dir = r'srt_files'
srt_files_ls = natsorted(glob.glob(path.join(srt_dir, '*.srt')), reverse =False)



for f in srt_files_ls:
    print(f)
    # srt_to_txt.main(['',path.basename(f), 'utf-8'])
    srt_to_txt.main(['',f, 'utf-8'])
    print('finished writing: ' +  Path(f).stem)

print('Concatenating txt files')
concat_txt(srt_dir)


if __name__ == "__main__":
    pass