import os
import numpy as np
import random
import open3d 
import csv
import math
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
            camera_position.append(line[:6])
   # camera_position = camera_position[1:]
    return camera_position


def Visuell_PointCloud(sampled, label, SavePCDFile = False, FileName = None):
    #get only the koordinate from sampled
    sampled = np.asarray(sampled)
    PointCloud_koordinate = sampled[:, 2:5]
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


def add_noise(patch_motor):
    ######### add uniform noise ############
    for point in patch_motor:
        noise_x = random.uniform(-0.001, 0.001)
        noise_y = random.uniform(-0.001, 0.001)
        noise_z = random.uniform(-0.005, 0.005)
        point[2] += noise_x
        point[3] += noise_y
        point[4] += noise_z
    
    ############ add downsample ############
   # patch_motor = Operator.PointCloud_Downsample(np.array(patch_motor), int(0.6 * len(patch_motor)))

    return patch_motor

def down_sampled(patch_motor, pointsToKeep):
    # no_elements_to_delete = pointsToRemove
    # no_elements_to_keep = len(patch_motor) - no_elements_to_delete
    b = random.sample(patch_motor, int(pointsToKeep))  # the `if i in b` on the next line would benefit from b being a set for large lists
    
    return b

def change_intoPointNet(wholescene):

    cor = wholescene[:, 2:5]
    color = wholescene[:, 9:12]
    lable = np.array([wholescene[:, 8]])
    new = np.concatenate((cor, color, lable.T), axis = 1)

    return new




 
def main():
    noise = True
    random_cly = True
    file_path = "D:\Masterarbeit_dataset\withNoiseNoCover\PCD\TypeB1" 
    root, Motor_type = os.path.split(file_path)
    List_WholeScene = os.listdir(file_path)

    if 'RandomInfor.csv' in List_WholeScene :
        List_WholeScene.remove('RandomInfor.csv')
    print("The number of Motor %s is: %d" % (Motor_type, len(List_WholeScene)))

    csv_path = "D:\Masterarbeit_dataset\withNoiseNoCover\PCD\\" + Motor_type + '\\RandomInfor.csv'
    camera_position = read_CameraPosition(csv_path)
    
    if not random_cly:
        Corners = [(-0.65, -0.8, 1.23), (0.75, -0.8, 1.23), (0.75, 0.05, 1.23), (-0.65, 0.05, 1.23), (-0.65, -0.8, 0.1), (0.75, -0.8, 0.1), (0.75, 0.05, 0.1), (-0.65, 0.05, 0.1)]
    else:
        cly_bottom = random.uniform(0.1, 0.41)
        Corners = [(-0.65, -0.8, 1.23), (0.75, -0.8, 1.23), (0.75, 0.05, 1.23), (-0.65, 0.05, 1.23), (-0.65, -0.8, cly_bottom), (0.75, -0.8, cly_bottom), (0.75, 0.05, cly_bottom), (-0.65, 0.05, cly_bottom)]

    for dir in List_WholeScene:
        k = dir.split('_')
        numpy_path = file_path + '\\' + dir + '\\' + 'wholeScene\\' + 'scan_' + Motor_type + '_' + k[1] + '.npy'
        whole_scene = np.load(numpy_path)

        camera_position_now = camera_position[int(k[1])]
        cor_inCam = []
        for corner in Corners:
            cor_inCam_point = get_Corordinate_inCam(camera_position_now[0], camera_position_now[1], camera_position_now[2], camera_position_now[3], camera_position_now[4], camera_position_now[5], corner)
            cor_inCam.append(cor_inCam_point)
        panel_1 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[2])
        panel_2 = get_panel(cor_inCam[5], cor_inCam[6], cor_inCam[4])
        panel_3 = get_panel(cor_inCam[0], cor_inCam[3], cor_inCam[4])
        panel_4 = get_panel(cor_inCam[1], cor_inCam[2], cor_inCam[5])
        panel_5 = get_panel(cor_inCam[0], cor_inCam[1], cor_inCam[4])
        panel_6 = get_panel(cor_inCam[2], cor_inCam[3], cor_inCam[6])
        panel_list = {'panel_up':panel_1, 'panel_bot':panel_2, 'panel_front':panel_3, 'panel_behind':panel_4, 'panel_right':panel_5, 'panel_left':panel_6}

        patch_motor = []
        patch_labels = []
        for point in whole_scene:
            if not noise:
                point_cor = (point[2], point[3], point[4])
            else:
                point_cor = (point[5], point[6], point[7])
            if set_Boundingbox(panel_list, point_cor):
                patch_motor.append(point)
                patch_labels.append(point[8])
        patch_motor = add_noise(patch_motor)
       # patch_motor = down_sampled(patch_motor, pointsToKeep = 0.4 * len(patch_motor))

       # break
        patch_motor = change_intoPointNet(np.array(patch_motor))  # resort the file information N*13 -> N*7
        np.save(root + '\\Training_set_0825_noise\\' + 'Training_' + Motor_type + '_noise' + k[1], patch_motor)
        print("Cutting process of motor type: %s -------------> number: %s is finished" %(Motor_type, k[1]))
        
   #  print(len(patch_motor))
   # Visuell_PointCloud(patch_motor, patch_labels)
    










if __name__ == '__main__' :
    main()