import numpy as np
import random

def Get_ObjectID(x) :    #get all kinds of ObjectID from numpy file

    dic = []
    for i in range(x.shape[0]):
        if x[i][8] not in dic:
            dic.append(x[i][8])

    return dic


def PointCloud_Downsample(x, pointsToRemove) :   #downsample the pointcloud    #pointsToRemove = Number of points need to be deleted

    LastPointIndex = x.shape[0] -1

    for _ in range(pointsToRemove):
        ds = np.random.uniform(0, LastPointIndex, 1)
        index = int(ds)
        x[[index, LastPointIndex]] = x[[LastPointIndex,index]]
        x = np.delete(x, LastPointIndex, 0)
        LastPointIndex -= 1
    
    return x

def ChangeLabel(x):
    if x.shape[1] == 13 :
        for i in range(x.shape[0]):
            if x[i][8] == 808464432.0 :
                x[i][8] = int(0)
            elif x[i][8] == 825307441.0 :
                x[i][8] = int(1)
            elif x[i][8] == 842150450.0 :
                x[i][8] = int(2)
            elif x[i][8] == 875836468.0 :
                x[i][8] = int(4)
            elif x[i][8] == 892679477.0 :
                x[i][8] = int(5)
            elif x[i][8] == 909522486.0 :
                x[i][8] = int(6)
    else: 
        print("The cor of numpy is not right")
            
    return x



def Resort_IDX(x):     #reset the IDX Value in the filtered numpy
    
    for i in range(x.shape[0]) :
        x[i][-1] = i

    return x


def Print_ValueOfPoint(x, NumOfPoint) :

    try:
        if x.shape[1] == 16 :
            print("Points one: timestamp {0[0]} / yaw {0[1]} / pitch {0[2]} / distance {0[3]} / distance_noise {0[4]} / Koordinate {0[5]},{0[6]},{0[7]} / Noise: {0[8]}, {0[9]}, {0[10]} / Object_id: {0[11]} / Color : {0[12]}, {0[13]}, {0[14]} / IDX: {0[15]}".format(
             x[NumOfPoint]))
        elif x.shape[1] == 13 :
            print("Points one: / distance {0[0]} / distance_noise {0[1]} / Koordinate {0[2]},{0[3]},{0[4]} / Noise: {0[5]}, {0[6]}, {0[7]} / Object_id: {0[8]} / Color : {0[9]}, {0[10]}, {0[11]} / IDX: {0[12]}".format(
                x[NumOfPoint]))
    except Exception as err :
        print(err)


def CutNumpy(x):     #drop the timestamp, yaw, pitch off and the point of (0,0,0)

    try :
        if x.shape[1] == 16 :
            x = x[:, 3:]
    except Exception as err :
        print(err)

    #Filter all points with a distance along the z coordinate small than 0
    y = x[x[:, 7] < 0]

    return y


# scan = np.loadtxt("F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD\TypeB\Motor_0001\whole\\scan_TypeA_1_000100000.numpy")

# print (scan.shape)
# print ("Points {0} / Values per point {1}".format(
#         scan.shape[0],
#         scan.shape[1]))

# np.save("Color_test", scan)

# filtered = CutNumpy(scan)
# filtered = ChangeLabel(filtered)


# print ("Points after filtered and cutted {0} / Values per point {1}".format(
#     filtered.shape[0],
#     filtered.shape[1]))

# filtered = Resort_IDX(filtered)
# Print_ValueOfPoint(filtered, 70000)

# object_id_1 = Get_ObjectID(filtered)
# print(object_id_1)

# sampled = PointCloud_Downsample(filtered, 20000)
