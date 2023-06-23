fname = "CCR6SE_test3.gcode"

with open(f'{fname}', 'r') as f:
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
        
print(base_max_layer)
