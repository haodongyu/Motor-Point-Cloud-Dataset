# coding: utf-8
import numpy as np
import cv2, PIL
from cv2 import aruco
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import pandas as pd



def read_transform(file_name):
    """Read transformation matrix from a YAML file.

    Args:
        file_name: Path to the YAML file.
    """
    file_storage = cv2.FileStorage(file_name, cv2.FILE_STORAGE_READ)
    cam_to_base_transform = file_storage.getNode("PoseState").mat()
    file_storage.release()
        
    return cam_to_base_transform

def base_to_camera(cam_to_base_transform, xyz, calc_angle=False):
    '''
    now do the base to camera transform
    '''
        # squeeze the first two dimensions
    xyz_transformed2 = xyz.reshape(-1, 3)  # [N=X*Y, 3]

        # homogeneous transformation
    if calc_angle:
        xyz_transformed2 = np.hstack((xyz_transformed2, np.zeros((xyz_transformed2.shape[0], 1))))  # [N, 4]
    else:
        xyz_transformed2 = np.hstack((xyz_transformed2, np.ones((xyz_transformed2.shape[0], 1))))  # [N, 4]

    cam_to_base_transform = np.matrix(cam_to_base_transform)
    base_to_cam_transform = cam_to_base_transform.I
    xyz_transformed2 = np.matmul(base_to_cam_transform, xyz_transformed2.T).T  # [N, 4]

    return xyz_transformed2[:, :-1].reshape(xyz.shape)  # [X, Y, 3]



def camera_to_base(cam_to_base_transform, xyz, calc_angle=False):
    '''
    '''
        # squeeze the first two dimensions
    xyz_transformed2 = xyz.reshape(-1, 3)  # [N=X*Y, 3]

        # homogeneous transformation
    if calc_angle:
        xyz_transformed2 = np.hstack((xyz_transformed2, np.zeros((xyz_transformed2.shape[0], 1))))  # [N, 4]
    else:
        xyz_transformed2 = np.hstack((xyz_transformed2, np.ones((xyz_transformed2.shape[0], 1))))  # [N, 4]


    xyz_transformed2 = np.matmul(cam_to_base_transform, xyz_transformed2.T).T  # [N, 4]

    return xyz_transformed2[:, :-1].reshape(xyz.shape)  # [X, Y, 3]

# cam_to_base_transform = read_transform('F:\KIT\Masterarbeit\Dateset\Testset_Pointclouds\\3d\\2021-04-14_16-22-18_right_robot_small\\transformation.yaml')
# xyz = np.array([-92.916695, 107.071205, 504.738525])
# xyz = transform(cam_to_base_transform, xyz)
# print(xyz)