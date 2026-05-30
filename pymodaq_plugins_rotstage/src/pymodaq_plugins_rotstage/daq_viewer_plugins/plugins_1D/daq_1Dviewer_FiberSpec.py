import numpy as np

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport, Axis
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

from pymodaq_plugins_rotstage.hardware.fiberspec import QminiSpectrometer



class DAQ_1DViewer_FiberSpec(DAQ_Viewer_base):
    """ Instrument plugin class for a 1D viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    params = comon_parameters+[{'title': 'Exposure time [s]:', 'name': 'exposure_time',
         'type': 'float', 'min': 0.001, 'value': 0.1, 'max': 10,
         'tip': 'Exposure time in seconds'}
        ]

    def ini_attributes(self):
        self.controller: QminiSpectrometer = None
        self.x_axis = None

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        if param.name() == "exposure_time":
            print(f"Changing exposure time to {param.value()}s")
            self.controller.set_exposure(param.value())

    def ini_detector(self, controller=None):
        """Detector communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator/detector by controller
            (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """

        if self.is_master:
            self.controller = QminiSpectrometer() 
            initialized = self.controller.connect()  
        else:
            self.controller = controller
            initialized = True

        data_x_axis = self.controller.get_wavelengths() 
        self.x_axis = Axis(data=data_x_axis, label='wavelength', units='nm', index=0)
        
        dfp = DataFromPlugins(name='QminiSpectrometer',
                                data=[np.zeros(len(data_x_axis))],
                                dim='Data1D', axes=[self.x_axis],
                                labels=['Intensity'])
        self.dte_signal_temp.emit(DataToExport(name='QminiSpectrometer', data=[dfp]))

        info = "QminiSpectrometer initialized" if initialized else "QminiSpectrometer initialization failed"
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        if self.is_master:
            self.controller.close() 

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """

        ##synchrone version (blocking function)
        data_tot = self.controller.get_spectrum()
        dfp = DataFromPlugins(name='QminiSpectrometer', data=data_tot, dim='Data1D', labels=['Intensity'], axes=[self.x_axis])
        self.dte_signal.emit(DataToExport('spectrum', data=[dfp]))

    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport('myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data1D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.controller.stop_exposure()  
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))
        return ''


if __name__ == '__main__':
    main(__file__)
