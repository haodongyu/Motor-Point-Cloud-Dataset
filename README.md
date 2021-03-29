# README  
These python program are produced for processing the 3D points cloud from Bosch motors. They can automatically exported CAD model of motors in Blender 2.9 with the help of Motor Factory().
Afer that they can produce 3D points cloud data and label them with the corresponding numbers with the help of Blensor().  

## Preparing  
If the Blensor is aready be downloaded:  
Put the folder ' utils_haodong ' into path : '' Blensor-1.0.18-Blender-2.79-Winx64\2.79\scripts\addons ''  

## Get Started  
### Creating Motor's CAD models  
Run the Blender 2.9. Open a text editor in the working space and load the file ' create_TypeA_Obj_new.py '.  
The path for saving the CAD models can be defined at **line 105 - line 108**.  
```
def main() :

    Upper_Bolt_Nummber = ['1', '2', '3']
    save_dir_TypeA1 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    save_dir_TypeA2 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA2"
    save_dir_TypeANone = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeANone"
```

### Creating PCD File and Numpy File  
Run the Blender 2.79 with Blensor addon. Open a text editor in the working space and load the file ' create_PCDAndNumpy.py '.  
The path of motor's CAD file and Campingsystem should be given at **line 255 and line 257**.  
```
def main():
    scan_mode = 'single'                             # ['single', 'all_folders']
    file_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA2"
 
    Clamping_dir = "F:\KIT\Masterarbeit\Dateset\clampingSystem\ClampingSystem.obj"
```
The path of saving PCD and Numpy can be defined at line 259.  
```
save_path = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\PCD" + '\\' + Motor_type
```
The ' scan_mode ' has two parameters: **'single' and 'all_folders'**. 'single' means only load one Motor with the clampingsystem. 'all_folders' will load all the motor models from the line 255.  
The choice of single motor can be defined at **line 366** : parameter **dirs**.
```
elif scan_mode == 'single' :
        dirs = 'MOtor_0001'
```
