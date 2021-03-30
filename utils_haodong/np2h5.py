import numpy as np
import h5py

scan = np.loadtxt("Motor_test2_separate.numpy")
#Filter all points with a distance along the z coordinate small than 0
filtered = scan[scan[:,7] < 0]

#Create the h5 file from np file
with h5py.File('Motor_test.h5', 'w') as hf :
        hf.create_dataset("label", data = filtered[:, 8])
        hf.create_dataset("data", data = np.delete(filtered, 8, 1))

hr = h5py.File('Motor_test.h5', 'r')
print(hr.keys())