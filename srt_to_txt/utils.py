import glob
from os import path
import os
from natsort import natsorted
from collections import defaultdict

srt_dir = r'srt_files'

srt_files_ls = natsorted(glob.glob(path.join(srt_dir, '*.srt')))



def remove_non_english_audio(srt_files: list):
    eng_regx = 'lang_en'
    for file_name in srt_files:
        basename = path.basename(file_name)

        if eng_regx not in basename:
            os.remove(file_name)



def reveal_duplicates(srt_files: list):
    def_dict = defaultdict(int)
    for file_name in srt_files:
        file_num = path.basename(file_name).split(' ')[0]
        def_dict[file_num] += 1
        # break
    # print(def_dict)
    dupl_ls = []
    for k,v in def_dict.items():
        if v > 1:
            dupl_ls.append(k)
    print(dupl_ls)
    
    




if __name__ == "__main__":
    remove_non_english_audio(srt_files_ls)
    reveal_duplicates(srt_files_ls)

