import vtk
import numpy as np
from vtk.util.numpy_support import *
from pathlib import Path


class VTK_data:
    def __init__(self,base_dir='tmp'):
        self.base_dir = Path(base_dir)
        self.geometries   = []
        self.results = []

    def load_data(self):
        print('loading data')
        vtm_path_list = self.base_dir.glob('**/*.vtm')
        for vtm_path in vtm_path_list:
         #print(path)
            path_parts = vtm_path.parts
            if 'geometry' in vtm_path.as_posix():
                self.geometries.append(vtk_geom_to_np( vtm_path.as_posix() ))
            if 'bstep2d_iT0100000' in vtm_path.as_posix():
                self.results.append(vtk_results_to_np( vtm_path.as_posix() )) 


def vtk_results_to_np(results_vtm):

	# read file for steady state flow
	reader = vtk.vtkXMLMultiBlockDataReader()
	reader.SetFileName(Path(results_vtm).absolute().as_posix())
	reader.Update()
	data = reader.GetOutput()
	data_iterator = data.NewIterator()
	img_data = data_iterator.GetCurrentDataObject() 

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

	return steady_flow_array

def vtk_geom_to_np(geom_vtm):
	reader = vtk.vtkXMLMultiBlockDataReader()
	reader.SetFileName(Path(geom_vtm).absolute().as_posix())
	reader.Update()
	data = reader.GetOutput()
	data_iterator = data.NewIterator()
	img_data = data_iterator.GetCurrentDataObject() 
	point_data = img_data.GetPointData()
	array_data = point_data.GetArray(0)
	np_array = vtk_to_numpy(array_data)
	img_shape = img_data.GetExtent()#.GetWholeExtent()
	np_shape = [img_shape[3] - img_shape[2] + 1, img_shape[1] - img_shape[0] + 1, 1]
	geometry_array = np_array.reshape(np_shape)

	return geometry_array

# vtm = VTK_data()
# vtm.load_data()
# print(vtm.results)