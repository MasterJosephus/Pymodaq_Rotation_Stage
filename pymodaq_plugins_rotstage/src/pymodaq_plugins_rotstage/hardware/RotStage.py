from thorlabs_elliptec import ELLx, ELLError, ELLStatus, list_devices

# print all devices and note the vid and pid of the device you want to connect to
# print(list_devices())

class RotStage:
    def __init__(self):
        pass
    
    def open_communication(self):
        # connect to device
        self.stage = ELLx(vid=0x0403, pid=0x6015)
        print(f"{self.stage.model_number} on {self.stage.port_name}, serial number {self.stage.serial_number}, status {self.stage.status.description}")
        print("opened communication with UV rotational stage.")
        return True
        
    def get_position(self):
        return self.stage.get_position()

    def close_communication(self):
        self.stage.close()   
        print("closed communication with UV rotational stage.")
        
    def move_home(self):
        # Move device to the home position
        self.stage.home()
        self.stage.wait() 
        print(f"moved home to{self.stage.get_position()}{self.stage.units}")
        
    def move_to_absolute_position(self, position):
        # Move device to the home position
        # self.move_home()
        # Movements are in real units appropriate for the device (degrees, mm).
        self.stage.move_absolute(position)     
        self.stage.wait()   
        print(f"{self.stage.get_position()}{self.stage.units}")
        
    def move_to_relative_position(self, position):
        # Movements are in real units appropriate for the device (degrees, mm).
        # if rel position larger than 360, subtract 360 until it is less than 360
        while self.stage.get_position() + position > 360:
            position = self.stage.get_position() + position - 360
        self.stage.move_relative(position)      
        self.stage.wait()
        print(f"{self.stage.get_position()}{self.stage.units}")
        
    def stop_moving(self):
        pass
        

# Example usage
if "__main__" == __name__:  
    stage = RotStage()
    stage.open_communication()
    stage.move_to_absolute_position(65)
    stage.stop_moving()