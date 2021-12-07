'''读取CT图像'''

import pydicom
import numpy as np
import matplotlib.pyplot as plt


for i in range(85):
    file_path=f'4560/{i*5-193}.CT.DCM'
    ds=pydicom.dcmread(file_path,force=True)
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    if i == 0:
        data=np.array(ds.pixel_array)
        data = data.reshape(1,data.shape[0], data.shape[0])
    else:
        array=np.array(ds.pixel_array)
        data = np.insert(data,i,array,0)

print(np.max(data))
print(np.min(data))
plt.imshow(data[1,:,:],cmap='bone')
plt.show()