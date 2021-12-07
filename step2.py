'''此脚本实现的功能：1.提取勾画信息为矩阵，2.提取CT图像为矩阵，3.将CT图像矩阵中勾画区域设置成高亮。4.将矩阵薄层为mat文件 '''
import pydicom
import numpy as np
import scipy.io as scio

'''随便打开一个CT文件，为了获取矩阵左上角点 在x,y,z坐标系中对应的值，以及每个像素点的尺寸'''
file_path=f'4560/97.CT.DCM'
ds = pydicom.read_file(file_path, force=True)
x0,y0,z0=ds.ImagePositionPatient#获取矩阵左上角点 在x,y,z坐标系中对应的值
dx,dy=ds.PixelSpacing#每个像素点的尺寸

'''打开勾画文件'''
file_path2=f'004560_StrctrSets.dcm'
ds2=pydicom.dcmread(file_path2,force=True)
ctrs = ds2.ROIContourSequence#ctrs存储了勾画坐标

'''创造一个0矩阵，用于存储勾画信息'''
matrix=np.zeros((85,512,512),int)

def get_CTPosition(z):
    ''' 此函数用于，输出z轴的坐标，返回matrix的层数'''
    IPP=[]
    for i in range(85):
        IPP.append(i*5-193)
    return IPP.index(z)

for i in range(33):
    '''此循环是将勾画信息填充到matrix里面'''
    data0=ctrs[0].ContourSequence[i].ContourData
    d = len(data0)
    data_list = np.array([float(c) for c in data0])
    data_list = data_list.reshape(int(d / 3), 3)
    x = data_list[:, 0]#获取每一层的所有x坐标
    y = data_list[:, 1]#获取每一层的所有y坐标
    z = data_list[:, 2]#获取每一层的所有z坐标,但其实每一层只有一个z值，所以z中的元素都是相同的
    _x=(x-x0)/dx#将x坐标转换为matrix的对应点
    _x=np.array(_x).astype(int)
    _y = (y - y0) / dy#将y坐标转换为matrix的对应点
    _y = np.array(_y).astype(int)
    for j in range(len(_x)):
        matrix[get_CTPosition(z[0]),_y[j],_x[j]]=1

for i in range(85):
    '''此循环是将所有CT图像信息提取到data这个矩阵里面'''
    file_path=f'4560/{i*5-193}.CT.DCM'
    ds=pydicom.dcmread(file_path,force=True)
    ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
    if i == 0:
        data=np.array(ds.pixel_array)
        data = data.reshape(1,data.shape[0], data.shape[0])
    else:
        array=np.array(ds.pixel_array)
        data = np.insert(data,i,array,0)

'''将勾画区域设置成高亮'''
for i in range(85):
    for j in range(512):
        for k in range(512):
            if matrix[i,j,k]==1:
                data[i,j,k]=4095

scio.savemat('Gouhua.mat', {'gouhua': matrix})
scio.savemat('CT.mat', {'CT': data})
