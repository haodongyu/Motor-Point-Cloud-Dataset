import os
import numpy as np
import open3d 
import csv
import math
import transformation
from utils_haodong import Operator


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



def Visuell_PointCloud(sampled, SavePCDFile = False, FileName = None):
    #get only the koordinate from sampled
    sampled = np.array(sampled)
    PointCloud_koordinate = sampled[:, 0:3]

    #visuell the point cloud
    point_cloud = open3d.geometry.PointCloud()
    point_cloud.points = open3d.utility.Vector3dVector(PointCloud_koordinate)
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





 
def main():
    Corners = [(-460.03,340,240), (-741.7,340,240), (-741.7,170,240), (-460,170,240), (-460,340,5), (-741.7,340,5), (-741.7,170,5), (-460,170,5)]
    file_path = "F:\KIT\Masterarbeit\Dateset\Testset_Pointclouds"

    root, Motor_type = os.path.split(file_path)
    List_zivid = os.listdir(file_path)


    transforMatrix_path = 'F:\KIT\Masterarbeit\Dateset\\3d\\rightRobot\\transformation.yaml'
    List_WholeScene = []
    for index in List_zivid:
        if os.path.splitext(index)[1] == '.pcd':
            List_WholeScene.append(index)

    cam_to_base_transform = transformation.read_transform(transforMatrix_path)
    

    for scene in List_WholeScene:
        k = 1
        pcd_path = file_path + '\\' + scene
        whole_scene = Operator.Read_PCD(pcd_path)   # base open3d
       # whole_scene = whole_scene[11:, :]
       # print(whole_scene.shape)
        

        cor_inCam = []
        for corner in Corners:
            cor_inCam_point = transformation.base_to_camera(cam_to_base_transform, np.array(corner))
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
                

        break
        # np_name = scene.split(".")[0]
        # np.save(root + '\\Testset_Pointclouds\\Test_set\\' + 'Test_' + np_name, patch_motor)
        # print("Cutting process of zivid: %s -------------> number: %s is finished" %(scene,k))
        # k += 1
        
    print(len(patch_motor))
    Visuell_PointCloud(patch_motor)
    








if __name__ == '__main__' :
    main()