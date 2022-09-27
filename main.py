import pprint
import os,sys
from ass import ass_to_dsc, read_ass
import dsc
import chart.option

def run(dsc_file_path ,ass_file ,merge_dsc_file_path):
    os.chdir(sys.path[0])
    #check output folder
    exe_path = os.getcwd()
    output_path = os.path.join(exe_path,"temp")
    if os.path.isdir(output_path) == False:
        os.mkdir(output_path)
    print(output_path)

    print("Read dsc data......")
    dsc_data_list = dsc.read(dsc_file_path)
    print(len(dsc_data_list))
    print("Done!")

    print("Read ass data......")
    ass_data = read_ass.read(ass_file)
    print("Done!")
    print("Convert ass to dsc......")
    ass_dsc_file_name ,lyric_file_name = ass_to_dsc.main(ass_data ,ass_file)
    print("Done!")

    ass_dsc_data_list = dsc.read(ass_dsc_file_name)
    print("Delete old lyric......")
    no_lyric_dsc_data_list = chart.option.delete_lyric(dsc_data_list)
    print(len(no_lyric_dsc_data_list))
    print("Done!")

    print("Merge dsc data......")
    merge_dsc_data_list = chart.option.merge_dsc_data(no_lyric_dsc_data_list,ass_dsc_data_list)
    #pprint.pprint(merge_dsc_data_list)
    print("Done!")

    print("Save merge dsc......")
    output_path_name = dsc.write(merge_dsc_data_list, merge_dsc_file_path)
    print("Done!")
    print("Output:\n" + merge_dsc_file_path)
    return lyric_file_name ,ass_dsc_file_name
