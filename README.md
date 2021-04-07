# README  
These python programs are used for generating and preprocessing the 3D point cloud from Bosch motors. They can automatically export CAD model of motors in [Blender 2.9](https://www.blender.org/download/releases/2-90/) with the help of [Motor Factory](https://github.com/cold-soda-jay/blenderMotorFactory).
Afer that, they can be used for generating and labeling 3D point cloud data with the help of [Blensor](https://www.blensor.org/). We also generalize the RGB-images and semantic maps from the motor's CAD model with the help of [BlenderProc](https://github.com/DLR-RM/BlenderProc).   

## Preparing  
- If the Blender 2.79 with [Blensor](https://www.blensor.org/) addon is already be installed:  
Copy the folder **utils_haodong** into path : Blensor-1.0.18-Blender-2.79-Winx64\2.79\scripts\addons  
- Download the [BlenderProc](https://github.com/DLR-RM/BlenderProc). Then please check the config file in [/BlenderProc/examples/semantic_segmentation](https://github.com/DLR-RM/BlenderProc/blob/main/examples/semantic_segmentation/config.yaml). We have changed **position of camera and configuration of lights** in this folder to suit the position and size of our CAD models.  
```
Camera position :
0.03 -3.8 1.7  1.57 0 0 
```  
```
Light configuration:
{
      "module": "lighting.LightLoader",
      "config": {
        "lights": [
          {
            "type": "POINT",
            "location": [0.9, -7, 0.4],
            "rotation": [3.142, 1.57, 1.57],
            "energy": 800
          }
        ]
      }
    },
```  
The other configuration, such as path to the configuration file, scene file and output directory, will be fitted at one of our main program [export_RGBandSegMap.py](./export_RGBandSegMAP.py) at **line 204 - line206**. 

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

### Generating PCD File and Numpy File  
Run the Blender 2.79 with [Blensor](https://www.blensor.org/) addon. Open a text editor in the working space and load the file [export_PcdAndNumpy.py](./export_PcdAndNumpy.py).  
Then the following pathes and parameters in the main function need to be defined:  
- **file_path** -> The path of motor's CAD file  
- **Clamping_dir** -> The path of clampingsystem   
- **save_path** -> The path of output directory (Each motor from `file_path` will get a corresponding folder in this directory.)  
- **scan_mode** -> Working mode of the program. It has two parameters: **'single' and 'all_folders'**  
  - **'single'** means only load one Motor with the clampingsystem. The choice of single motor can be defined by the parameter **dirs**. In this mode, the program will not             export PCD and Numpy file. It can be finished manually in the Blensor's Propeties. So this mode is suitable for testing process  
  - **'all_folders'** will load all the motors from the `file_path` with the clampingsystem and export the PCD and Numpy file.  

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
### Generating RGB image and Segmentation Map  
If the [BlenderProc](https://github.com/DLR-RM/BlenderProc) is already be configurated, the Blender2.91 will also be installed with following the directory from the config file in [/BlenderProc/examples/semantic_segmentation](https://github.com/DLR-RM/BlenderProc/blob/main/examples/semantic_segmentation/config.yaml).  
Run the Blender2.91 and open a text editor like in Blender 2.90/2.79. Then load the file [export_RGBandSegMap.py](./export_RGBandSegMap.py).  
The following pathes in the **export_png** function need to be defined:  
- **BlenderProc_path** -> The path of `run.py` of BlenderProc  
- **config_path** -> The path of configuration file, in the form of `xxxx.yaml`
- **camera_position_seg** -> The path of camera's configuration file  
- **SaveAsImage_path** -> The path of `SaveAsImage.py` from BlenderProc.   

Remember to keep the space after the string.  
Then the following pathes and parameters in the main function need to be defined:  
- **file_path** -> The path of motor's CAD file  
- **Clamping_dir** -> The path of clampingsystem  
- **save_path** -> The path of RGB image and Segmentation output directory. It can be defined as same as in the [export_PcdAndNumpy.py](./export_PcdAndNumpy.py).  
```
def main():
    scan_mode = 'all_folders'                             # ['single', 'all_folders']
    file_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    filters = ["Motor.obj"]                                # No_needed obj file
    Clamping_dir = "F:\KIT\Masterarbeit\Dateset\clampingSystem\ClampingSystem.obj"
    root, Motor_type = os.path.split(file_path)
    save_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD" + '\\' + Motor_type
```
