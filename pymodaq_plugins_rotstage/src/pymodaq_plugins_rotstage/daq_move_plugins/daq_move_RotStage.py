
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)

from pymodaq_utils.utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq_gui.parameter import Parameter

from pymodaq_plugins_rotstage.hardware.RotStage import RotStage


class DAQ_Move_RotStage(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of controllers and actuators that should be compatible with this instrument plugin.
        * With which instrument and controller it has been tested.
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
    is_multiaxes = False  # TODO for your plugin set to True if this plugin is controlled for a multiaxis controller
    _axis_names: Union[List[str], Dict[str, int]] = ['']
    _controller_units: Union[str, List[str]] = '°' 
    _epsilon: Union[float, List[float]] = 0.01  
    data_actuator_type = DataActuatorType.DataActuator 
    params = [] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: RotStage = None
        pass

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = DataActuator(data=self.controller.get_position(),  # when writing your own plugin replace this line
                           units=self.axis_unit)
        return pos

    def close(self):
        if self.is_master:
            self.controller.close_communication()  

    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings

        Parameters
        ----------
        param: Parameter
            A given parameter (within detector_settings) whose value has been changed by the user
        """
        pass

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        if self.is_master:  # is needed when controller is master
            self.controller = RotStage() 
            initialized = self.controller.open_communication()  
        else:
            self.controller = controller
            initialized = True

        info = "Connected to UV rotational stage!"
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  #if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        self.controller.move_to_absolute_position(value.value(self.axis_unit))  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Moved Rot. Stage successfully!']))

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        self.controller.move_to_relative_position(value.value(self.axis_unit))  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Moved Rot. Stage successfully!']))

    def move_home(self):
        """Call the reference method of the controller"""

        self.controller.move_home()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Moved Rot. Stage to home position successfully!']))

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""

        self.controller.stop_moving()  # when writing your own plugin replace this line
        self.emit_status(ThreadCommand('Update_Status', ['Stop method not implemented yet!']))

if __name__ == '__main__':
    main(__file__)
