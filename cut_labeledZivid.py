import os
import numpy as np
import random
import open3d 
import csv
import math
import transformation
import matplotlib.pyplot as plt
from utils_haodong import Operator

def get_Corordinate_inCam(cam_pos_x, cam_pos_y, cam_pos_z, alpha, beta, theta, cor):

    # alpha = 0.581*math.pi/180.0
    # beta = 9.43*math.pi/180.0
    # theta = -90.0*math.pi/180.0
    # cor = np.array([1, 1.5, 2]).T
    # cam_pos = np.array([-0.05, -0.8, 6]).T
    alpha = float(alpha)
    beta = float(beta)
    theta = float(theta)
    cor = np.array(cor).T
    cam_pos = np.array([float(cam_pos_x), float(cam_pos_y), float(cam_pos_z)]).T
    cor = cor - cam_pos

    c_mw = np.array([[math.cos(beta)*math.cos(theta), math.cos(beta)*math.sin(theta), -math.sin(beta)],
            [-math.cos(alpha)*math.sin(theta)+math.sin(alpha)*math.sin(beta)*math.cos(theta), math.cos(alpha)*math.cos(theta)+math.sin(alpha)*math.sin(beta)*math.sin(theta), math.sin(alpha)*math.cos(beta)],
            [math.sin(alpha)*math.sin(theta)+math.cos(alpha)*math.sin(beta)*math.cos(theta), -math.sin(alpha)*math.cos(theta)+math.cos(alpha)*math.sin(beta)*math.sin(theta), math.cos(alpha)*math.cos(beta)] ])

    cor_new = c_mw.dot(cor)

    return tuple(cor_new)


def get_panel(point_1, point_2, point_3):

    x1 = point_1[0]
    y1 = point_1[1]
    z1 = point_1[2]

    x2 = point_2[0]
    y2 = point_2[1]
    z2 = point_2[2] 

    x3 = point_3[0]
    y3 = point_3[1]
    z3 = point_3[2]
    
    a = (y2-y1)*(z3-z1) - (y3-y1)*(z2-z1)
    b = (z2-z1)*(x3-x1) - (z3-z1)*(x2-x1)
    c = (x2-x1)*(y3-y1) - (x3-x1)*(y2-y1)
    d = 0 - (a*x1 + b*y1 + c*z1)

    return (a, b, c, d)


def read_CameraPosition(csv_path):

    camera_position = []
    with open(csv_path,"r+") as f:
        csv_read = csv.reader(f)
        for line in csv_read:
            camera_position.append(line)
   # camera_position = camera_position[1:]
    return camera_position

def Read_PCD(pcd_path):

    pts = []
    f = open(pcd_path, 'r')
    data = f.readlines()
 
    f.close()
	# print line
    line = data[7]
    i = line.split(' ')
    for line in data[10:] :
        line = line.strip('\n')
        xyzrgb = line.split(' ')
        x, y, z = [eval(i) for i in xyzrgb[:3]]
        if x != 0 and y!=0 and z!=0 :
            label = xyzrgb[4]
            rgb = xyzrgb[3]
            rgb = eval(rgb)
           # rgb = bin(eval(rgb))[2:]
            r = (rgb>>16) & 0x0000ff
            g = (rgb>>8)&0x0000ff
            b = (rgb)&0x0000ff
            
            pts.append([x, y, z, r, g, b, label])
    
   # assert len(pts) == pts_num
    pts_num = len(pts)
    res = np.zeros((pts_num, len(pts[0])), dtype=np.float)
    for i in range(pts_num):
        res[i] = pts[i]
	# x = np.zeros([np.array(t) for t in pts])
    return res




# def get_pcd_label(pcd_path):

#     f = open(pcd_path, 'r')
#     data = f.readlines()
#     f.close()
#     point_and_label = []

#    # get the number of points
#     for line in data[10:]:
#         line = line.strip('\n')
#         line_infor = line.split(' ')
#         label = eval(line_infor[4])
#         x,y,z = [eval(i) for i in line_infor[:3]]
#         if x != 0 and y!=0 and z!=0:
#             point_and_label.append([x,y,z, label])
    
#     return point_and_label

def binarySearch (arr, l, r, x): 
  
    if r >= l: 
        mid = int(l + (r - l)/2)
        if float(arr[mid]) == x: 
            return mid 
        elif float(arr[mid]) > x: 
            return binarySearch(arr, l, mid-1, x) 
        else: 
            return binarySearch(arr, mid+1, r, x) 
    else: 
        return -1

def cut_motorPatch(Corners, cam_to_robot_transform, whole_scene):
    cor_inCam = []
    for corner in Corners:
        cor_inCam_point = transformation.base_to_camera(cam_to_robot_transform, np.array(corner))
        cor_inCam.append(np.squeeze(np.array(cor_inCam_point)))

    panel_1 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[2])
    panel_2 = get_panel(cor_inCam[5], cor_inCam[6], cor_inCam[4])
    panel_3 = get_panel(cor_inCam[0], cor_inCam[3], cor_inCam[4])
    panel_4 = get_panel(cor_inCam[1], cor_inCam[2], cor_inCam[5])
    panel_5 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[4])
    panel_6 = get_panel(cor_inCam[2], cor_inCam[3], cor_inCam[6])
    panel_list = {'panel_up':panel_1, 'panel_bot':panel_2, 'panel_front':panel_3, 'panel_behind':panel_4, 'panel_right':panel_5, 'panel_left':panel_6}

    patch_motor = []
    for point in whole_scene:
        point_cor = (point[0], point[1], point[2])
        if set_Boundingbox(panel_list, point_cor):
            patch_motor.append(point)
    return patch_motor


def transform_patch(patch_motor, cam_to_robot_transform, Cam_inBlensor_position):
    new_cor = []
    for point in patch_motor:
        # zivid to Robot
        cor_inRobot_point = transformation.camera_to_base(cam_to_robot_transform, point[0:3])    
        # Robot to Blensor real world
        cor_inReal = cor_inRobot_point
        cor_inReal[0:2] = -cor_inReal[0:2]
        # Blensor real world to Blensor camera
        cor_in_BlensorCam = get_Corordinate_inCam(Cam_inBlensor_position[0], Cam_inBlensor_position[1], Cam_inBlensor_position[2], Cam_inBlensor_position[3],
            Cam_inBlensor_position[4], Cam_inBlensor_position[5], cor_inReal)

        point_in_Blensor = np.squeeze(cor_in_BlensorCam)
        point_in_Blensor = np.hstack((point_in_Blensor, point[3:]))
        new_cor.append(np.squeeze(point_in_Blensor))
    
    return np.squeeze(np.asarray(new_cor))

def Visuell_PointCloud(sampled, label, SavePCDFile = False, FileName = None):
    '''
    :param data: n*3 matrix
    :param label: n*1 matrix (needed)
    :return: visual
    '''
    #get only the koordinate from sampled
    sampled = np.array(sampled)
    PointCloud_koordinate = sampled[:, 0:3]
    labels = np.asarray(label)
    print(labels.shape)
    max_label = labels.max()

    colors = plt.get_cmap("tab20")(labels / (max_label if max_label>0 else 1))

    #visuell the point cloud
    point_cloud = open3d.geometry.PointCloud()
    point_cloud.points = open3d.utility.Vector3dVector(PointCloud_koordinate)
    point_cloud.colors = open3d.utility.Vector3dVector(colors[:, :3])
    open3d.visualization.draw_geometries([point_cloud])

    if SavePCDFile is True:
    # #save the pcd file
        open3d.io.write_point_cloud(FileName +'.pcd', point_cloud)


def set_Boundingbox(panel_list, point_cor):

    if panel_list['panel_up'][0]*point_cor[0] + panel_list['panel_up'][1]*point_cor[1] + panel_list['panel_up'][2]*point_cor[2] + panel_list['panel_up'][3] <= 0 :   # panel 1
        if panel_list['panel_bot'][0]*point_cor[0] + panel_list['panel_bot'][1]*point_cor[1] + panel_list['panel_bot'][2]*point_cor[2] + panel_list['panel_bot'][3] >= 0 : # panel 2
            if panel_list['panel_front'][0]*point_cor[0] + panel_list['panel_front'][1]*point_cor[1] + panel_list['panel_front'][2]*point_cor[2] + panel_list['panel_front'][3] <= 0 : # panel 3
                if panel_list['panel_behind'][0]*point_cor[0] + panel_list['panel_behind'][1]*point_cor[1] + panel_list['panel_behind'][2]*point_cor[2] + panel_list['panel_behind'][3] >= 0 : # panel 4
                    if panel_list['panel_right'][0]*point_cor[0] + panel_list['panel_right'][1]*point_cor[1] + panel_list['panel_right'][2]*point_cor[2] + panel_list['panel_right'][3] >= 0 : #panel 5
                        if panel_list['panel_left'][0]*point_cor[0] + panel_list['panel_left'][1]*point_cor[1] + panel_list['panel_left'][2]*point_cor[2] + panel_list['panel_left'][3] >= 0 : # panel 6

                            return True
    return False



# best [(0,1200,900), (-941.7,1000,900), (-941.7,0,900), (0,200,900), (0,1200,50), (-941.7,1-00,50), (-941.7,0,50), (0,200,50)]

 
def main():
    Corners = [(35,880,300), (35,1150,300), (-150,1150,300), (-150,880,300), (35,880,50), (35,1150,50), (-150,1150,50), (-150,880,50)]  # [(0,1000,900), (-941.7,1000,900), (-941.7,0,900), (0,0,900), (0,1000,5), (-941.7,1-00,5), (-941.7,0,5), (0,0,5)]
    # [(0,1000,900), (-941.7,1000,900), (-941.7,0,900), (0,0,900), (0,1000,5), (-941.7,1-00,5), (-941.7,0,5), (0,0,5)]  #  [(-880,200,260), (-1180,200,260), (-1180,-200,260), (-880,-200,260), (-880,200,50), (-1180,200,50), (-1180,-200,50), (-880,-200,50)]  # [(0,1000,900), (-941.7,1000,900), (-941.7,0,900), (0,0,900), (0,1000,5), (-941.7,1-00,5), (-941.7,0,5), (0,0,5)]
    file_path = 'F:\KIT\Masterarbeit\Dateset\Testset_Pointclouds_labeled\zivid_20210907'     # "F:\KIT\Masterarbeit\Dateset\Testset_Pointclouds"

    List_zivid = os.listdir(file_path)

    Cam_inBlensor_position = (-0.136411824,	-0.589879807, 4.067452035, 0.033196298,	0.144020323, -1.57 )
    transforMatrix_path = 'F:\KIT\Masterarbeit\Dateset\Testset_Pointclouds\Zivid_Dataset_20210907\\transformation_matrix\\transformation.yaml'
    List_WholeScene = []
    for index in List_zivid:
        if os.path.splitext(index)[1] == '.pcd':
            List_WholeScene.append(index)

    cam_to_robot_transform = transformation.read_transform(transforMatrix_path)
    
    k = 1
    for scene in List_WholeScene:
        pcd_path = file_path + '\\' + scene
        whole_scene = Read_PCD(pcd_path)   # base self
       # whole_scene = whole_scene[11:, :]
       # print(labels[0])

        patch_motor = cut_motorPatch(Corners, cam_to_robot_transform, whole_scene)
        new_cor = transform_patch(patch_motor, cam_to_robot_transform, Cam_inBlensor_position)
        labels = new_cor[:, -1]

        break
        np_name = scene.split(".")[0]
        np.save(file_path + '\\Finetune_set\\' + 'Training_' + np_name, new_cor)
        print("Cutting process of zivid: %s -------------> number: %s is finished" %(scene,k))
        k += 1
        
   # print(len(patch_motor))
    Visuell_PointCloud(new_cor, labels)
    print('All finished')
    






if __name__ == '__main__' :
    main()