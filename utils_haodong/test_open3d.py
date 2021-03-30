import open3d as o3d 
import numpy as np 

def Visuell_PointCloud(sampled, SavePCDFile = False, FileName = None):
    #get only the koordinate from sampled
    PointCloud_koordinate = sampled[:, 5:8]


    #visuell the point cloud
    point_cloud = open3d.geometry.PointCloud()
    point_cloud.points = open3d.utility.Vector3dVector(PointCloud_koordinate)
    open3d.visualization.draw_geometries([point_cloud])

    if SavePCDFile is True:
    # #save the pcd file
        o3d.io.write_point_cloud(FileName +'.pcd', point_cloud)

scan = np.load("Color_test.npy")

point_cloud = o3d.geometry.PointCloud()
point_cloud = o3d.utility.DoubleVector(scan)
o3d.io.write_point_cloud(FileName +'.pcd', point_cloud)
