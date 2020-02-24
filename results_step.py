import vtk
import numpy as np
from vtk.util.numpy_support import *

steady_flow_file = 'tmp/vtkData/data/bstep2d_iT0119400.vtm'

# read file for steady state flow
reader = vtk.vtkXMLMultiBlockDataReader()
reader.SetFileName(steady_flow_file)
reader.Update()
data = reader.GetOutput()
data_iterator = data.NewIterator()
img_data = data_iterator.GetCurrentDataObject() 
print(img_data)

point_data = img_data.GetPointData()
velocity_array_data = point_data.GetArray(0)
pressure_array_data = point_data.GetArray(1)
velocity_np_array = vtk_to_numpy(velocity_array_data)
pressure_np_array = vtk_to_numpy(pressure_array_data)
img_shape = img_data.GetExtent()#.GetWholeExtent()
velocity_np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 2]
pressure_np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 1]
velocity_np_array = velocity_np_array.reshape(velocity_np_shape)
pressure_np_array = pressure_np_array.reshape(pressure_np_shape)
steady_flow_array = np.concatenate([velocity_np_array, pressure_np_array], axis=2)

print(steady_flow_array.shape)