import unittest

import minesim.biome_generators as biogen

import numpy as np

import vtk
import os
data_dir = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'data'+os.sep

def convertToNumber (s):
    return int.from_bytes(s.encode(), 'little')

def convertToColor(s):
    i = convertToNumber (s)
    return ((i/(255**2))%1.0, (i/255)%(1.0), i%1.0)

#todo: create 3d testing library for point clouds
class MockModel(object):
    def __init__(self):
        self.dots = []
        pass

    def add_block(self, position, type, immediate = False):
        self.dots.append((*position, convertToColor(type)))

    def batch_blocks(self, array_in, type):
        self.dots = array_in


    def show_cloud(self):
        points = vtk.vtkPoints()

        vertices = vtk.vtkCellArray()

        for d in self.dots:
            p = points.InsertNextPoint((d[0], d[1], d[2]))
            vertices.InsertNextCell(1)
            vertices.InsertCellPoint(p)

        cloud = vtk.vtkPolyData()

        cloud.SetPoints(points)
        cloud.SetVerts(vertices)

        # Visualize
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(cloud)
        else:
            mapper.SetInputData(cloud)

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetPointSize(2)

        renderer = vtk.vtkRenderer()
        renderWindow = vtk.vtkRenderWindow()
        renderWindow.AddRenderer(renderer)
        renderWindowInteractor = vtk.vtkRenderWindowInteractor()
        renderWindowInteractor.SetRenderWindow(renderWindow)

        renderer.AddActor(actor)

        renderWindow.Render()
        renderWindowInteractor.Start()



class TestBiomeGenerators(unittest.TestCase):
    # todo: change this to a non-interactive test, like glsl_compute tests
    # todo: add interactive tests that require y/n == y to pass
    def testFullBiomeGen(self):
        plains = biogen.plains_gen( 50, 50, 10, 3, 5, turbulence=0.1).astype(np.bool_)
        min_h = 0
        max_h = 3
        h = max_h-min_h
        dissipation = 0.5
        # us, but not them boolean operators to remove boolean arrays from other boolean arrays
        # if I run into long strings of operators like these, consider moving back to glsl.
        cave_caves = biogen.cloud_layer_gen(50, 50, h, 0.2, 0.0, 0) & ~biogen.cloud_layer_gen(50, 50, h, 1, 0.0, 0)
        cave_caves = biogen.cloud_layer_gen(50, 50, h, 0.05, 0.0, dissipation) & ~cave_caves
        plains[0:50, 0:50, min_h:max_h] = plains[0:50, 0:50, min_h:max_h] & ~cave_caves
        visible_plains = biogen.restrict_visible(plains, plains, show_bounds=True)
        visible_locations = biogen.get_locations(visible_plains).astype(np.uint16)  # even as 48 bits, should still be less
        with open(data_dir + self.testFullBiomeGen.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(),np.packbits(visible_locations).tobytes())

    def testVisibleGen(self):
        plains = biogen.cloud_layer_gen(10, 10, 5, 0.2, 0.0, 0)
        visible_plains = biogen.restrict_visible(plains, plains, show_bounds=True)
        visible_locations = biogen.get_locations(visible_plains).astype(np.uint16)
        with open(data_dir + self.testVisibleGen.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(visible_locations).tobytes())

    def testPlainsGen(self):
        plains = biogen.plains_gen( 10, 10, 10, 3, 5, turbulence=0.1).astype(np.bool_)
        with open(data_dir + self.testPlainsGen.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(plains).tobytes())

    def testStoneContainer(self):
        stone = biogen.get_locations(biogen.stone_container_gen( 10, 10, 10))
        with open(data_dir + self.testStoneContainer.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(stone).tobytes())

    def testCloudLayerGen(self):
        clouds = biogen.get_locations(biogen.cloud_layer_gen(10, 10, 10, 0.2, 0.0, .5))
        with open(data_dir + self.testCloudLayerGen.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(clouds).tobytes())

    def testFoamGen(self):
        foam = biogen.get_locations(biogen.cloud_layer_gen(10, 10, 10, 0.2, 0.0, 0))
        with open(data_dir + self.testFoamGen.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(foam).tobytes())

    def testCaveDig(self):
        caves = biogen.get_locations(biogen.inverse_cloud_layer_gen(10, 10, 10, 0.2, 0.5, .5))
        with open(data_dir + self.testCaveDig.__name__ + ".binary", 'rb') as test_file:
            self.assertEqual(test_file.read(), np.packbits(caves).tobytes())