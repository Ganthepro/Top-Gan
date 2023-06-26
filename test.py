fname = "CCR6SE_test3.gcode"

with open(f'{fname}', 'r+') as f:
    texts = f.readlines()
    flag_mash = False
    flag_type = False
    base_line = ""
    base_max_layer = 0 
    for t in texts:
        if base_line != "":
            if base_line in t:
                base_max_layer += 1
        else:
            if "MESH" in t:
                flag_mash = True
            if "TYPE" in t and t != ";TYPE:SKIRT\n":
                flag_type = True
            if flag_mash and flag_type and "X" in t and "Y" in t:
                for i in t.removesuffix("\n"):
                    if i != "X":
                        t = t.removeprefix(i)
                    if i == "E":
                        t = t.replace(t[t.index(i):-1],"")
                        break
                # print(t.removesuffix("\n"))
                base_line = t.removesuffix("\n")
    # หาต่ำแหน่ง x,y,z,e ล่าสุด
    flag_value = {"G1" : False,"z" : False,"e" : False}
    value = {"G1" : "","z" : "","e" : ""}
    for i in range(texts.index(f";LAYER:{base_max_layer + 2}\n") - 1,0,-1):
        if "X" in texts[i].removesuffix("\n") and "Y" in texts[i].removesuffix("\n") and not flag_value["G1"]: 
            flag_value["G1"] = True
            print(texts[i])
            try:
                value["G1"] = texts[i].removeprefix(texts[i][0:texts[i].index("F")])
            except:
                value["G1"] = texts[i].removeprefix(texts[i][0:texts[i].index("X")])
        if "Z" in texts[i].removesuffix("\n") and not flag_value["z"]:
            flag_value["z"] = True
            value["z"] = texts[i][texts[i].index("Z"):-1]
        if "E" in texts[i].removesuffix("\n") and ("G1" in texts[i].removesuffix("\n") or "G0" in texts[i].removesuffix("\n")) and not flag_value["e"]:
            flag_value["e"] = True
            value["e"] = texts[i][texts[i].index("E"):-1]
        for v in flag_value.values():
            if v == False:
                flag = False
                break
            else:
                flag = True
        if flag:
            break
    # print(value.items())
    x = value["z"][value["z"].index("Z") + 1:-1] + value["z"][-1]
    print(float(x) + 1)
    script = ["M83\n",f"G1 F300 Z{float(x) + 1}\n","G1 F9000 X190 Y190\n"
              ,"G1 F300 Z15\n","M104 S180\n","M300\n","M0\n","G4 S180\n","M109 S200\n",f"G1 F300 {value['z']}\n"
              ,f"G1 {value['G1']}",f"G1 F300 {value['z']}\n","G1 F1500\n","M82\n",f"G92 {value['e']}\n"]
    for i in script:
        texts.insert(texts.index(f";LAYER:{base_max_layer + 2}\n"),i)
        
with open("example.gcode", "w") as file:
    for line in texts:
        file.write(line)
