import os
import bpy
import numpy as np
import random

'''
Value-distribution:
    Type A_Type 1 :
                    Bottom Length = 4.00 - 8.00  step = 0.03
                    Sub Bottom Length = 0.6 - 2  setp = 0.03

                    Lower Gear Dia = 3.5 - 4.5  step = 0.03
                    Lower Gear Position = 3.6 - 4.2
                    Upper Gear Dia = 5 - 6.5

                    Bolts Type = 'mf_Bit_Slot', 'mf_Bit_Torx', 'mf_Bit_Corss',
                    Bolt Orientation = 'mf_all_same', 'mf_all_random'

                    Position of Bolt 1 on lower gear = 190 - 230    step = 5
                    Position of Bolts on lower gear = 320 - 350    step = 5
                    Random of Position around lower gear = True/False

                    Number of Bolts = 1, 2, 3

                    Position of bolt 1 on larger gear = 0 - 105    step = 1
                    Position of bolt 2 on larger gear = 106 - 210    step = 1

The rule I used now:
                    Each changed parameter in changed value + the other parameter in default values  ->  3 groups with different type of bolts
'''

def create_Motor_Obj(Extension_Type_A, Bolt_type_mode, changed_parameter, Upper_Bolt_Nummber, save_dir) :         # Motor_type = ['Type_A', 'Type_B']  Type_A_Extension = ['Type_1', 'Type_2']
    try :
        if bpy.data.objects['Cube'] :       # Delete the Cube object and Lamp object from Blender's intialization
            bpy.data.objects.remove(bpy.data.objects['Cube'])
        if bpy.data.objects['Light'] :
            bpy.data.objects.remove(bpy.data.objects['Light'])
    except KeyError :
        pass

    try :
        if bpy.data.objects['Motor']:
            bpy.data.objects.remove(bpy.data.objects['Motor'])
    except KeyError:
        pass
    
    Bolts_Type = ['mf_Bit_Slot', 'mf_Bit_Torx', 'mf_Bit_Corss']
    if Extension_Type_A == 'mf_Extension_Type_1' :
        if Bolt_type_mode == 'Torx' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_Extension_Type_1', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Torx', save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
        elif Bolt_type_mode == 'Random' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_Extension_Type_1', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type=random.choice(Bolts_Type), save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])

    elif Extension_Type_A == 'mf_Extension_Type_2' :
        if Bolt_type_mode == 'Torx' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_Extension_Type_2', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Torx', save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
        elif Bolt_type_mode == 'Random' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_Extension_Type_2', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type=random.choice(Bolts_Type), save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])

    elif Extension_Type_A == 'mf_Extension_Type_None' :
        if Bolt_type_mode == 'Torx' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_None', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Torx', save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
        elif Bolt_type_mode == 'Random' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=True,  mf_Upper_Gear_Bolt_Random=True, temp_save=True, mf_Top_Type='mf_Top_Type_A',
                    mf_Extension_Type_A='mf_None', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'],
                    mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Upper_Gear_Dia=changed_parameter['changed_UGD'], mf_Upper_Bolt_Nummber=Upper_Bolt_Nummber, 
                    mf_Bolt_Orientation='mf_all_random', mf_Bit_Type=random.choice(Bolts_Type), save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])


        # bpy.ops.mesh.add_motor(change=True, mf_Flip=False, mf_Color_Render=True, mf_Lower_Gear_Bolt_Random=False, 
        #     mf_Gear_Bolt_Random_B=False, mf_Upper_Gear_Bolt_Random=False, temp_save=False, mf_Top_Type='mf_Top_Type_A',
        #     mf_Extension_Type_A='mf_Extension_Type_1', mf_Extension_Type_B='mf_Extension_Type_1', mf_Gear_Orientation_1='r0', 
        #     mf_Gear_Orientation_2='r270', mf_Bottom_Length=8, mf_Sub_Bottom_Length=1.97, mf_Lower_Gear_Dia=4.47, 
        #     mf_Lower_Gear_Position=4.17, mf_Lower_Gear_Bolt_Position_1=225, mf_Lower_Gear_Bolt_Position_2=350, mf_Gear_Bolt_Nummber_B='2', 
        #     mf_Gear_Bolt_Position_B_1=215, mf_Gear_Bolt_Position_B_2=90, mf_Gear_Bolt_Position_B_3=180, mf_Type_B_Height_1=7, 
        #     mf_Type_B_Height_2=3.5, mf_Gear_Bolt_Right_B=2.5, mf_Upper_Gear_Dia=6.47, mf_Upper_Bolt_Nummber='2', 
        #     mf_Upper_Gear_Bolt_Position_1=209, mf_Upper_Gear_Bolt_Position_2=210, mf_Upper_Gear_Bolt_Position_3=200, 
        #     mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Cross', save_path="None")

    

def main() :

    Upper_Bolt_Nummber = ['1', '2', '3']
    save_dir_TypeA1 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA1"
    save_dir_TypeA2 = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeA2"
    save_dir_TypeANone = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeANone"


    ################################################
    ####  Number of Bolt on the upper gear : 1  ####
    ################################################
    
    number_motor = 25
    for _ in range(number_motor):
        changed_parameter = {}
        changed_parameter['changed_BL'] = float(np.random.uniform(4.0, 8.0, 1))          # Bottom_Length
        changed_parameter['changed_SBL'] = float(np.random.uniform(0.6, 2.0, 1))         # Sub_Bottom_Length
        changed_parameter['changed_LGD'] = float(np.random.uniform(3.5, 4.5, 1))         # Lower_Gear_Diameter
        changed_parameter['changed_LGP'] = float(np.random.uniform(3.6, 4.2, 1))         # Lower_Gear_Position
        changed_parameter['changed_UGD'] = float(np.random.uniform(5, 6.5, 1))           # Upper_Gear_Diameter
        ###########################################  
        #   Create Type A Extension 1 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_1', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[0], save_dir = save_dir_TypeA1)

        ###########################################  
        #   Create Type A Extension 2 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_2', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[0], save_dir = save_dir_TypeA2)

        ###########################################  
        #   Create Type A Extension None Motor    #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_None', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[0], save_dir = save_dir_TypeANone)


    ################################################
    ####  Number of Bolt on the upper gear : 2  ####
    ################################################
    
    number_motor = 50
    for _ in range(number_motor):
        changed_parameter = {}
        changed_parameter['changed_BL'] = float(np.random.uniform(4.0, 8.0, 1))          # Bottom_Length
        changed_parameter['changed_SBL'] = float(np.random.uniform(0.6, 2.0, 1))         # Sub_Bottom_Length
        changed_parameter['changed_LGD'] = float(np.random.uniform(3.5, 4.5, 1))         # Lower_Gear_Diameter
        changed_parameter['changed_LGP'] = float(np.random.uniform(3.6, 4.2, 1))         # Lower_Gear_Position
        changed_parameter['changed_UGD'] = float(np.random.uniform(5, 6.5, 1))           # Upper_Gear_Diameter
        ###########################################  
        #   Create Type A Extension 1 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_1', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[1], save_dir = save_dir_TypeA1)

        ###########################################  
        #   Create Type A Extension 2 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_2', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[1], save_dir = save_dir_TypeA2)

        ###########################################  
        #   Create Type A Extension None Motor    #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_None', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[1], save_dir = save_dir_TypeANone)


    ################################################
    ####  Number of Bolt on the upper gear : 3  ####
    ################################################
    
    number_motor = 25
    for _ in range(number_motor):
        changed_parameter = {}
        changed_parameter['changed_BL'] = float(np.random.uniform(4.0, 8.0, 1))          # Bottom_Length
        changed_parameter['changed_SBL'] = float(np.random.uniform(0.6, 2.0, 1))         # Sub_Bottom_Length
        changed_parameter['changed_LGD'] = float(np.random.uniform(3.5, 4.5, 1))         # Lower_Gear_Diameter
        changed_parameter['changed_LGP'] = float(np.random.uniform(3.6, 4.2, 1))         # Lower_Gear_Position
        changed_parameter['changed_UGD'] = float(np.random.uniform(5, 6.5, 1))           # Upper_Gear_Diameter
        ###########################################  
        #   Create Type A Extension 1 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_1', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[2], save_dir = save_dir_TypeA1)

        ###########################################  
        #   Create Type A Extension 2 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_2', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[2], save_dir = save_dir_TypeA2)

        ###########################################  
        #   Create Type A Extension None Motor    #
        ###########################################
        create_Motor_Obj(Extension_Type_A = 'mf_Extension_Type_None', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Upper_Bolt_Nummber=Upper_Bolt_Nummber[2], save_dir = save_dir_TypeANone)
    





if __name__ == '__main__':
    main()