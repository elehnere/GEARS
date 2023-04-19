with open("team92_map.csv", "w") as mazeMap:
    mazeMap.write("Team : 92\n")
    mazeMap.write("Map: 1\n")
    mazeMap.write("Unit Length: 40\n")
    mazeMap.write("Unit: cm\n")
    mazeMap.write("Origin: (3, 0)\n")
    mazeMap.write("Notes: This is a map for the PoC \n")
    
    
    mapArray = [["0", "0", "0", "0", "0", "0"], 
                ["0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0"],
                ["0", "0", "0", "0", "0", "0"]]
    current_pos = [0, 3]
    print(mapArray[current_pos[0]][current_pos[1]])
    mapArray[current_pos[0]][current_pos[1]] = "5"
    check = 0
    while check == 0:
        axis = int(input("What direction (y/x) did you go? "))
        if axis == 2:
            mapArray[current_pos[0]][current_pos[1]] = "4"
            check = 1
        else:
            sign = int(input("What direction (+/-) did you go? "))
            current_pos[axis] += sign
            mapArray[current_pos[0]][current_pos[1]] = "1"
        for line in mapArray:
            print(line)
            print(" ")
    for line in mapArray:
        for element in line:
            mazeMap.write(element)
            mazeMap.write(", ")
        mazeMap.write("\n")
        
    