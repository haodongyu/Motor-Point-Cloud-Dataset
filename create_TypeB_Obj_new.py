import os
import bpy
import numpy as np
import random

'''
Value-distribution:
    Type B :
                    Bottom Length = 4.00 - 8.00  step = 0.03
                    Sub Bottom Length = 0.6 - 2  setp = 0.03

                    Lower Gear Dia = 3.5 - 4.5  step = 0.03
                    Lower Gear Position = 3.6 - 4.2
                    Height of Extension left = 6.3 - 7.5
                    Height of Extension right = 3 - 6

                    Bolts Type = 'mf_Bit_Slot', 'mf_Bit_Torx', 'mf_Bit_Corss',
                    Bolt Orientation = 'mf_all_same', 'mf_all_random'

                    Position of Bolt at right = 1.7 - 4    step = 0.03

                    Position of bolt 1 on larger gear = 210 - 225    step = 1
                    Position of bolt 2 on larger gear = 70 - 110    step = 1

The rule I used now:
                    Each changed parameter in changed value + the other parameter in default values  ->  3 groups with different type of bolts
'''

def create_Motor_Obj(Extension_Type_B, Bolt_type_mode, changed_parameter, Gear_Bolt_Nummber_B, save_dir) :         # Motor_type = ['Type_A', 'Type_B']  Type_A_Extension = ['Type_1', 'Type_2']
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
    if Extension_Type_B == 'Extension_Type_1' :
        if Bolt_type_mode == 'Torx' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Gear_Bolt_Random_B=True, temp_save=True, mf_Top_Type='mf_Top_Type_B',
                mf_Extension_Type_B='mf_Extension_Type_1', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'], 
                mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Gear_Bolt_Nummber_B='2', mf_Type_B_Height_1=changed_parameter['changed_HEL'], 
                mf_Type_B_Height_2=changed_parameter['changed_HER'], mf_Gear_Bolt_Right_B=changed_parameter['changed_GBR'],
                mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Torx', save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
        elif Bolt_type_mode == 'random' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Gear_Bolt_Random_B=True, temp_save=True, mf_Top_Type='mf_Top_Type_B',
                mf_Extension_Type_B='mf_Extension_Type_1', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'], 
                mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Gear_Bolt_Nummber_B='2', mf_Type_B_Height_1=changed_parameter['changed_HEL'], 
                mf_Type_B_Height_2=changed_parameter['changed_HER'], mf_Gear_Bolt_Right_B=changed_parameter['changed_GBR'],
                mf_Bolt_Orientation='mf_all_random', mf_Bit_Type=random.choice(Bolts_Type), save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
    
    elif Extension_Type_B == 'Extension_Type_None' :
        if Bolt_type_mode == 'Torx' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Gear_Bolt_Random_B=True, temp_save=True, mf_Top_Type='mf_Top_Type_B',
                mf_Extension_Type_B='mf_None', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'], 
                mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Gear_Bolt_Nummber_B=Gear_Bolt_Nummber_B, mf_Type_B_Height_1=changed_parameter['changed_HEL'], 
                mf_Type_B_Height_2=changed_parameter['changed_HER'], mf_Gear_Bolt_Right_B=changed_parameter['changed_GBR'],
                mf_Bolt_Orientation='mf_all_random', mf_Bit_Type='mf_Bit_Torx', save_path=save_dir)
            bpy.data.objects.remove(bpy.data.objects['Motor'])
        elif Bolt_type_mode == 'Random' :
            bpy.ops.mesh.add_motor(change=True, mf_Color_Render=True, mf_Gear_Bolt_Random_B=True, temp_save=True, mf_Top_Type='mf_Top_Type_B',
                mf_Extension_Type_B='mf_None', mf_Bottom_Length=changed_parameter['changed_BL'], mf_Sub_Bottom_Length=changed_parameter['changed_SBL'], mf_Lower_Gear_Dia=changed_parameter['changed_LGD'], 
                mf_Lower_Gear_Position=changed_parameter['changed_LGP'], mf_Gear_Bolt_Nummber_B=Gear_Bolt_Nummber_B, mf_Type_B_Height_1=changed_parameter['changed_HEL'], 
                mf_Type_B_Height_2=changed_parameter['changed_HER'], mf_Gear_Bolt_Right_B=changed_parameter['changed_GBR'],
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

    Upper_Bolt_Nummber = ['2', '3']
    ###########################################  
    #           Create Type B Motor           #
    ###########################################
    save_dir_TypeB = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeB"
    save_dir_TypeBNone = "F:\KIT\Masterarbeit\Dateset\Test\TestforScript\TypeBNone"

    number_motor = 10



    ################################################
    ####  Number of Bolt on the upper gear : 2  ####
    ################################################
    
    for _ in range(number_motor):
        changed_parameter = {}
        changed_parameter['changed_BL'] = float(np.random.uniform(4.0, 8.0, 1))          # Bottom_Length
        changed_parameter['changed_SBL'] = float(np.random.uniform(0.6, 2.0, 1))         # Sub_Bottom_Length
        changed_parameter['changed_LGD'] = float(np.random.uniform(3.5, 4.5, 1))         # Lower_Gear_Diameter
        changed_parameter['changed_LGP'] = float(np.random.uniform(3.6, 4.2, 1))         # Lower_Gear_Position
        changed_parameter['changed_GBR'] = float(np.random.uniform(1.7, 4.0, 1))         # Gear_Bolt_Right_B
        changed_parameter['changed_HEL'] = float(np.random.uniform(6.3, 7.5, 1))         # Height of Extension left
        changed_parameter['changed_HER'] = float(np.random.uniform(3.0, 6.0, 1))         # Height of Extension right
        ###########################################  
        #   Create Type B Extension 1 Motor       #
        ###########################################
        create_Motor_Obj(Extension_Type_B = 'Extension_Type_1', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Gear_Bolt_Nummber_B= Upper_Bolt_Nummber[0] , save_dir = save_dir_TypeB)      # Bolt_type_mode = ['Random', 'Torx']

        ###########################################  
        #   Create Type B Extension None Motor    #
        ###########################################
        create_Motor_Obj(Extension_Type_B = 'Extension_Type_None', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Gear_Bolt_Nummber_B= Upper_Bolt_Nummber[0], save_dir = save_dir_TypeBNone)

    ###########################################################
    ####  Number of Bolt on the upper gear : 3 (Type_None) ####
    ###########################################################

    for _ in range(number_motor):
        changed_parameter = {}
        changed_parameter['changed_BL'] = float(np.random.uniform(4.0, 8.0, 1))          # Bottom_Length
        changed_parameter['changed_SBL'] = float(np.random.uniform(0.6, 2.0, 1))         # Sub_Bottom_Length
        changed_parameter['changed_LGD'] = float(np.random.uniform(3.5, 4.5, 1))         # Lower_Gear_Diameter
        changed_parameter['changed_LGP'] = float(np.random.uniform(3.6, 4.2, 1))         # Lower_Gear_Position
        changed_parameter['changed_GBR'] = float(np.random.uniform(1.7, 4.0, 1))         # Gear_Bolt_Right_B
        changed_parameter['changed_HEL'] = float(np.random.uniform(6.3, 7.5, 1))         # Height of Extension left
        changed_parameter['changed_HER'] = float(np.random.uniform(3.0, 6.0, 1))         # Height of Extension right

        ###########################################  
        #   Create Type B Extension None Motor    #
        ###########################################
        create_Motor_Obj(Extension_Type_B = 'Extension_Type_None', Bolt_type_mode = 'Torx', changed_parameter = changed_parameter, Gear_Bolt_Nummber_B = Upper_Bolt_Nummber[1], save_dir = save_dir_TypeBNone)



if __name__ == '__main__':
    main()