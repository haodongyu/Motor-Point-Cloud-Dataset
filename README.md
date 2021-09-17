# README  
These python programs are used for generating and preprocessing the 3D point cloud from Bosch motors. They can automatically export CAD model of motors in [Blender 2.9](https://www.blender.org/download/releases/2-90/) with the help of [Motor Factory](https://github.com/cold-soda-jay/blenderMotorFactory).
Afer that, they can be used for generating and labeling 3D point cloud data with the help of [Blensor](https://www.blensor.org/). The camera's positon in this process will randomly keep moving in the top of a sphere. The diagram of this filed is showing in the figure_1. We also generalize the RGB-images, normal-images, depth-images and semantic maps from the motor's CAD model with the help of [BlenderProc](https://github.com/DLR-RM/BlenderProc). The results of them is showing in figure_2.   

## Preparing  
- If the Blender 2.79 with [Blensor](https://www.blensor.org/) addon is already be installed:  
Copy the folder **utils_haodong** into path : Blensor-1.0.18-Blender-2.79-Winx64\2.79\scripts\addons  
- Download the [BlenderProc](https://github.com/DLR-RM/BlenderProc). Then please check the config file in [/BlenderProc/examples/semantic_segmentation](https://github.com/DLR-RM/BlenderProc/blob/main/examples/semantic_segmentation/config.yaml). We have changed **position of camera and configuration of BlenderLoader** in this folder to suit the position and size of our CAD models. The configuration of our task is be uploaded in this project. Besides that, a new empty binary file `camera_position_zivid` is also needed in this folder, which can dynamically store the random positons of the zivid-vision's camera.    
```
Camera_position :
0 0 3.9  0 0 -1.57 
```  
```
BlenderLoder :  
{
      "module": "loader.BlendLoader",
      "config": {
        "path": "<args:1>",
        "datablocks": ["objects", "lights"],
        "obj_types": ["mesh", "light"]
      }
 },
```  
The other configuration, such as path to the configuration file, scene file and output directory, will be fitted at one of our main program [export_WholeRGBandSegMap.py](./export_WholeRGBandSegMap.py) at **line 204 - line206**. 

## Get Started  
### Generating Motor's CAD models  
Run the [Blender 2.9](https://www.blender.org/download/releases/2-90/). Open a text editor in the working space and load the file [create_TypeA_Obj_new.py](./create_TypeA_Obj_new.py).  
The path for saving the CAD models need be defined in the main function.
- **save_dir_TypeA1** -> The path of TypeA1's output directory  
- **save_dir_TypeA2** -> The path of TypeA2's output directory  
- **save_dir_TypeANone** -> The path of TypeANone's output directory  
- **number_motor** -> The number of motors that need to be exported  

```
def main() :

    save_dir_TypeA1 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    save_dir_TypeA2 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA2"
    save_dir_TypeANone = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeANone"
    
    number_motor = 5
```

### Generating PCD File and Numpy File of whole Scene(Plane, Clampingsystem, motor)  
Run the Blender 2.79 with [Blensor](https://www.blensor.org/) addon. Open a text editor in the working space and load the file [export_WholePCDandNumpy.py](./export_WholePCDandNumpy.py).  
Then the following pathes and parameters in the main function need to be defined:  
- **file_path** -> The path of motor's CAD file  
- **Clamping_dir** -> The path of clampingsystem   
- **save_path** -> The path of output directory (Each motor from `file_path` will get a corresponding folder in this directory.)  
- **scan_mode** -> Working mode of the program. It has two parameters: **'single' and 'all_folders'**  
  - **'single'** means only load one Motor with the clampingsystem. The choice of single motor can be defined by the parameter **dirs**. In this mode, the program will not             export PCD and Numpy file. It can be finished manually in the Blensor's Propeties. So this mode is suitable for testing process  
  - **'all_folders'** will load all the motors from the `file_path` with the clampingsystem and export the PCD and Numpy file.  
The random position of camera will be stored in a csv file `RandomInfor.csv`.

```
def main():
    scan_mode = 'single'                             # ['single', 'all_folders']
    file_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA2"
 
    Clamping_dir = "F:\KIT\Masterarbeit\Dateset\clampingSystem\ClampingSystem.obj"
    save_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD" + '\\' + Motor_type
``` 
```
elif scan_mode == 'single' :
        dirs = 'MOtor_0001'
```  
### Generating PCD File and Numpy File of only Motor with Background   
Run the Blender 2.79 with [Blensor](https://www.blensor.org/) addon. Open a text editor in the working space and load the file [export_MotorPCDandNumpy.py](./export_MotorPCDandNumpy.py). This programm will read the camera's position frim `RandomInfor.csv`, then scan only the coresponding motor with a plane(background).  
It working similarly as [export_WholePCDandNumpy.py](./export_WholePCDandNumpy.py).The pathes and parameter's configuration can be copyed from [export_WholePCDandNumpy.py](./export_WholePCDandNumpy.py).

### Generating RGB image and Segmentation Map of whole Scene(Plane, Clampingsystem, motor)   
If the [BlenderProc](https://github.com/DLR-RM/BlenderProc) is already be configurated, the Blender2.91 will also be installed with following the directory from the config file in [/BlenderProc/examples/semantic_segmentation](https://github.com/DLR-RM/BlenderProc/blob/main/examples/semantic_segmentation/config.yaml).  
Run the Blender2.91 and open a text editor like in Blender 2.90/2.79. Then load the file [export_WholeRGBandSegMap.py](./export_WholeRGBandSegMap.py).  
The following pathes in the **export_png** function need to be defined:  
- **BlenderProc_path** -> The path of `run.py` of BlenderProc  
- **config_path** -> The path of configuration file, in the form of `xxxx.yaml`
- **camera_position_seg** -> The path of camera's configuration file  
- **SaveAsImage_path** -> The path of `SaveAsImage.py` from BlenderProc.   

Remember to keep the space after the string.  
Then the following pathes and parameters in the **main function** need to be defined:  
- **file_path** -> The path of motor's CAD file  
- **Clamping_dir** -> The path of clampingsystem  
- **save_path** -> The path of RGB image and Segmentation output directory. It can be defined as same as in the [export_WholePCDandNumpy.py](./export_WholePCDandNumpy.py).  
```
def main():
    scan_mode = 'all_folders'                             # ['single', 'all_folders']
    file_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    filters = ["Motor.obj"]                                # No_needed obj file
    Clamping_dir = "F:\KIT\Masterarbeit\Dateset\clampingSystem\ClampingSystem.obj"
    root, Motor_type = os.path.split(file_path)
    save_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD" + '\\' + Motor_type
```
### Generating RGB image and Segmentation Map of only Motor with Background   
Run the Blender2.91 and open a text editor like in Blender 2.90/2.79. Then load the file [export_MotorRGBandSegMap.py](./export_MotorRGBandSegMap.py). The pathes and parameter's configuration can be copyed from [export_WholeRGBandSegMap.py](./export_WholeRGBandSegMap.py).  

## Get the synthetic data for training  
### Export PCD and Numpy file for whole scene
If the motor data in the form of .mtl and .obj is already finished. Then run the [export_NoiseWholePCDandNumpy.py](./export_NoiseWholePCDandNumpy.py). Then the noised data which special for the training of Neural Network will be exported. The noise is following this random field:  

| Variables| explain| random field|
| :-: | :-: |:-|
| random_cover_position| the positon of a surfuce over the motor | x~(-0.2, 0.6), y~(-0.6, -0.15) |  
| random_Clamping_position| the positionof the two parts of the Clamping system | Base_part: x~(-0.1, 0.3), y~(-0.2, 0.2) <br> Slind_part: x~(-0.655, 0.345) <br> Cyinder: x~(-0.15, 0.05) |  
| sigma | sigma parameter of Gaussian Noise | (0.01, 0.02) |  
| random_cut_bottom | the lower limit when cutting the cuboid | (0, 1/3) |  


### Cut the numpy file from whole scene into cuboid 
If you want to get the **training data**:
```
python cut_WholePCDandNumpy.py
```
else if you want to cut the **test data** from Zivid:
```
python cut_labeledZivid.py
python cut_Zivid.py                # depends on the zivid PCD is labeled or not
```
Then these numpy files can be used in [SOTA-Networks-for-Master-Thesis-Semantic-segmentation-on-Bosch-Motors](https://github.com/haodongyu/SOTA-Networks-for-Master-Thesis-Semantic-segmentation-on-Bosch-Motors).  
Remember to check the numpy file in the form of :  
```
x, y, z, r, g, b, label
```
