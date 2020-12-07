groups = []
with open("input6", "r") as f:
    thisgroup = set()
    for line in f:
        if line.strip() == "":
            groups.append(thisgroup)
            thisgroup = set()
        [thisgroup.add(c) for c in line.strip()]
    groups.append(thisgroup)
    
        
    
