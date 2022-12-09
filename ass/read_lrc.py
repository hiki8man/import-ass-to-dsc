#指令列表

def read(ass_file):
    with open(ass_file, 'r' ,encoding='UTF-8') as lyric_file:
        lyric_list = lyric_file.readlines()
        id = 0
        lyric_data = []
        for lyric_o_data in lyric_list:
            if lyric_o_data.find("Dialogue:") == 0:
                list=[]
                n = -1
                #使用逗号分隔 ass文件 不同数据部分
                for i in range(9):
                    n = lyric_o_data[(n+1):].find(",") + n + 1
                    #print(n)
                    list.append(n)
                #print(list)
                #构建数据结构
                lyric_data.append({ "real_id":id+1,
                                    "start":0,
                                    "end":0,
                                    "R":255,
                                    "G":255,
                                    "B":255,
                                    "A":255,
                                    "lyric":""
                                 })
                lyric_data[id]["start"] = convert_time(lyric_o_data[list[0]+1:list[1]])
                lyric_data[id]["end"] = convert_time(lyric_o_data[list[1]+1:list[2]])
                if lyric_o_data[list[8] + 1:].find("{\c&H") != -1:
                    color_R_start = list[8] + lyric_o_data[list[8] + 1:].find("{\\c&H") + 6
                    color_R_end = color_R_start + 2
                    color_G_end = color_R_end + 2
                    color_B_end = color_G_end + 2
                    lyric_data[id]["R"] = int(lyric_o_data[color_R_start:color_R_end],16)
                    lyric_data[id]["G"] = int(lyric_o_data[color_R_end:color_G_end],16)
                    lyric_data[id]["B"] = int(lyric_o_data[color_G_end:color_B_end],16)
                    if lyric_o_data[color_B_end:].find("\\1a&H") != -1:
                        alpha_start = lyric_o_data[color_B_end:].find("\\1a&H") + color_B_end + 5
                        alpha_end = alpha_start + 2
                        lyric_data[id]["A"] = 255 - int(lyric_o_data[alpha_start:alpha_end],16)
                lyric_start = list[8] + lyric_o_data[list[8] + 1:].find("}") + 2
                lyric_data[id]["lyric"] = lyric_o_data[lyric_start:-1]
                #检测当前歌词是否与上一句歌词重复
                #第一句歌词时跳过
                if id == 0:
                    lyric_data[id]["id"] = 1
                #根据情况设置ID值，摆烂直接浅复制值，反正小工具要啥效率
                elif lyric_data[id]["lyric"] == lyric_data[id-1]["lyric"]:
                    lyric_data[id]["id"] = lyric_data[id-1]["id"]
                else:
                    lyric_data[id]["id"] = lyric_data[id-1]["id"] + 1
                id += 1
    return lyric_data

def convert_time(time):
    time_h = int(time[0:1]) * 60 *60 * 100 * 10
    time_m = int(time[2:4]) * 60 * 100 * 10
    time_s = int(time[5:7]) * 100 * 10
    time_ms = int(time[8:10]) * 10
    time = int(time_h + time_m + time_s + time_ms) * 100
    return time