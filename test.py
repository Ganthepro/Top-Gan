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
    script = ["M83",f"G1 F300 Z8.4","G1 F9000 X190 Y190","G1 F300 Z15","M104 S180","M300","M0","G4 S180","M109 S200",f"G1 F300 Z7.4",f"G1 F9000 X55.247 Y39.597",f"G1 F300 Z7.4",f"G1 F1500",f"M82","G92 E2296.52556"]
    texts.insert(texts.index(f";LAYER:{base_max_layer + 2}\n"),)
        
print(base_max_layer)
