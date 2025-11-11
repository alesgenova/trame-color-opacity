import numpy as np
import vtkmodules.util.numpy_support as np_s
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa - this is required
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper


class VolumeView:
    def __init__(self):
        # Set up the VTK volume
        ren = vtkRenderer()
        ren_win = vtkRenderWindow()
        ren_win.AddRenderer(ren)
        ren_win.OffScreenRenderingOn()

        # White background
        ren.SetBackground(1, 1, 1)

        iren = vtkRenderWindowInteractor()
        iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
        iren.SetRenderWindow(ren_win)

        axes = vtkAxesActor()
        orientation_marker = vtkOrientationMarkerWidget()
        orientation_marker.SetOrientationMarker(axes)
        orientation_marker.SetInteractor(iren)

        # The property describes how the data will look.
        volume_property = vtkVolumeProperty()
        # volume_property.IndependentComponentsOff()
        volume_property.SetInterpolationTypeToLinear()
        volume_property.SetAmbient(0.5)
        volume_property.SetSpecular(0.9)
        volume_property.SetSpecularPower(10)

        # Fix the scalar opacity to be a no-op
        pwf = volume_property.GetScalarOpacity()
        pwf.RemoveAllPoints()
        pwf.AddPoint(0, 0)
        pwf.AddPoint(255, 1)

        volume_data = vtkImageData()

        volume_mapper = vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputData(volume_data)
        volume_mapper.UseJitteringOn()

        volume = vtkVolume()
        volume.SetMapper(volume_mapper)
        volume.SetProperty(volume_property)

        ren.AddVolume(volume)

        # Pitch the camera by 90 degrees to start
        ren.GetActiveCamera().Pitch(90)
        ren.GetActiveCamera().OrthogonalizeViewUp()

        # Store needed variables on self
        self.orientation_marker = orientation_marker
        self.renderer = ren
        self.render_window = ren_win
        self.volume_data = volume_data
        self.volume_property = volume_property

    def set_data(self, data):
        # We use C ordering throughout the application, but VTK uses
        # Fortran ordering. Reverse the shape to fix this.
        shape = data.shape
        set_array_to_image_data(data.ravel(), self.volume_data, shape)

        self.volume_data.Modified()
        self.render_window.Render()


def set_array_to_image_data(
    array: np.ndarray, image_data: vtkImageData, shape: tuple[int], clear=True
):
    vtk_array = np_s.numpy_to_vtk(array, deep=True)
    image_data.SetDimensions(shape)
    pd = image_data.GetPointData()

    if clear:
        while pd.GetNumberOfArrays() > 0:
            pd.RemoveArray(0)

    pd.SetScalars(vtk_array)
