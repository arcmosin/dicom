'''看一看原始图片方位'''
import pydicom
import numpy as np
import matplotlib.pyplot as plt

file_path=f'4560/97.CT.DCM'
ds = pydicom.read_file(file_path, force=True)

ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
data=np.array(ds.pixel_array)

plt.imshow(data,cmap='bone')
plt.show()