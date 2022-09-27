#指令列表
import op_list

list = op_list.list
common_list = {}
for common in list:
   common_list.update({common:list[common]})
   
#写入思路1（使用字符）
#byte_val = bytes(chr(1),encoding="latin1")
#dsc_ft = b'\x21\x09\x05\x14'
#test=b'\x00'
#bitout = open('test.dsc', 'wb')
#bitout.write(dsc_ft+byte_val+test*7)
#bitout.close

#写入思路2（使用字节数组写入）
#byte_val = bytes(bytearray([1,2,3,16]))
#dsc_ft = b'\x21\x09\x05\x14'
#test=b'\x00'
#bitout = open('test.dsc', 'wb')
#print(byte_val)
#bitout.write(dsc_ft+byte_val+test*7)
#bitout.close

ft_format = b'\x21\x09\x05\x14'
note_format = b'\x06\x00\x00\x00'
note_circle_hold = note_format + b'\x05\x00\x00\x00'
note_cross_hold  = note_format + b'\x06\x00\x00\x00'
note_square_hold = note_format + b'\x07\x00\x00\x00'
note_triangle_hold = note_format + b'\x04\x00\x00\x00'

import pprint
import os
pprint.pprint(common_list)
#读入数据
def fix_hold_note_show(dsc_data_list):
    num = 0
    fix_dsc_data_list = dsc_data_list.copy()
    for time_data in dsc_data_list:
        list_temp1_hold = [0,0,0,0]
        list_temp2_hold = []
        list_temp = []
        for i in range(len(time_data["data"])):
            check_hold_note = time_data["data"][i][0:8]
            if check_hold_note == note_circle_hold:
                list_temp1_hold[0] = time_data["data"][i]
            elif check_hold_note == note_cross_hold:
                list_temp1_hold[1] = time_data["data"][i]
            elif check_hold_note == note_square_hold:
                list_temp1_hold[2] = time_data["data"][i]
            elif check_hold_note == note_triangle_hold:
                list_temp1_hold[3] = time_data["data"][i]
            else:
                list_temp.append(time_data["data"][i])
        for i in list_temp1_hold:
            if i != 0:
                list_temp2_hold.append(i)
        list_temp.extend(list_temp2_hold)
        if len(list_temp2_hold) != 0:
            fix_dsc_data_list[num]["data"] = list_temp.copy()
        #pprint.pprint(fix_dsc_data_list)
        #print("------------------------------------")
        num += 1
        #pprint.pprint(time_data)
    #print("------------------------------------")
    #pprint.pprint(fix_dsc_data_list)
    return fix_dsc_data_list

def write(dsc_data_list, dsc_file_name):
    fix_dsc_name = "fix_"+os.path.basename(dsc_file_name)
    fix_dsc_path = os.path.dirname(dsc_file_name)
    fix_dsc = os.path.join(fix_dsc_path,fix_dsc_name)
    with open(fix_dsc, 'wb') as fix_dsc:
        fix_dsc.write(ft_format)
        print(len(dsc_data_list))
        for data in dsc_data_list:
            print(data["time"])
            print("------------------------------------")
            fix_dsc.write(data["time"])
            for another_data in data["data"]:
                print(another_data)
                fix_dsc.write(another_data)
            print("------------------------------------")
                
def read(dsc_file_name):
    with open(dsc_file_name, 'rb') as read_file_dsc:
        read_dsc = read_file_dsc.read()
        dsc_data = []
        for data in read_dsc:
            dsc_data.append(data)
        dsc_format = bytearray(dsc_data[0:4])
        if dsc_format != ft_format:
            print("not ft dsc")
            sys.exit(0)
        else:
            dsc_data_list=[]
            dsc_id = 4
            data_id = -1
        while dsc_id < len(dsc_data):
            opcode_id = dsc_data[dsc_id]
            if opcode_id == 1:
                data_id += 1
                dsc_data_time = bytearray(dsc_data[dsc_id:dsc_id+8])
                dsc_data_list.append({
                                      "time":dsc_data_time,
                                      "data":[]
                                    })
            else:
                another_end_id = dsc_id + (common_list[opcode_id]["len"] + 1) * 4
                dsc_data_another = bytearray(dsc_data[dsc_id:another_end_id])
                dsc_data_list[data_id]["data"].append(dsc_data_another)
            dsc_id += (common_list[opcode_id]["len"] + 1) * 4
            #print(dsc_id)
        pprint.pprint(dsc_data_list)
        #print("------------------------------------")
        #fix_dsc_data_list = fix_hold_note_show(dsc_data_list)
        #pprint.pprint(fix_dsc_data_list)
        #write_to_dsc(fix_dsc_data_list ,dsc_file_name)
