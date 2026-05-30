import clr
import time
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os

HERE = Path(__file__).resolve().parent
DLL_PATH = HERE / "RgbDriverKit.dll"
print(DLL_PATH)
clr.AddReference(str(DLL_PATH))

# Import namespaces from DLL
import RgbDriverKit


class QminiSpectrometer:
    def __init__(self):
        self.spectrometer = None
        self.wavelengths = None

    def connect(self):
        """
        Search and connect to first available spectrometer
        """

        devices = RgbDriverKit.RgbSpectrometer.SearchDevices()

        if devices.Length == 0:
            devices = RgbDriverKit.Qseries.SearchDevices()

        if devices.Length == 0:
            devices = RgbDriverKit.Qstick.SearchDevices()

        if devices.Length == 0:
            print("No spectrometer found")
            return False

        self.spectrometer = devices[0]

        print("Initializing spectrometer...")
        self.spectrometer.Open()

        print("Connected")
        print("Device:", self.spectrometer.DetailedDeviceName)
        print("Model:", self.spectrometer.ModelName)
        print("Serial:", self.spectrometer.SerialNo)
        print("Pixels:", self.spectrometer.PixelCount)
        return True
    
    def get_wavelengths(self):
        return np.array(list(self.spectrometer.GetWavelengths()), dtype=np.float64)

    def set_exposure(self, exposure_seconds):
        self.spectrometer.ExposureTime = float(exposure_seconds)

    def get_spectrum(self):
        """
        Acquire one spectrum
        """

        print(f"Taking spectrum ({self.spectrometer.ExposureTime}s)")

        self.spectrometer.StartExposure()

        while (
            self.spectrometer.Status ==
            RgbDriverKit.SpectrometerStatus.TakingSpectrum
            or
            self.spectrometer.Status ==
            RgbDriverKit.SpectrometerStatus.WaitingForTrigger
        ):
            print(".", end="", flush=True)
            time.sleep(0.05)

        print()

        intensities = np.array(
            list(self.spectrometer.GetSpectrum()),
            dtype=np.float32
        )

        return intensities
    
    def stop_exposure(self):
        return True
    
    def enable_sensitivity_calibration(self, enable=True):

        if hasattr(self.spectrometer, "UseSensitivityCalibration"):
            self.spectrometer.UseSensitivityCalibration = enable

    def close(self):

        if self.spectrometer is not None:
            self.spectrometer.Close()

            if not self.spectrometer.IsOpen:
                print("Spectrometer closed")


# =========================
# Example usage
# =========================

if __name__ == "__main__":

    spec = QminiSpectrometer()

    try:
        spec.connect()

        spec.enable_sensitivity_calibration(False)

        spec.set_exposure(0.1)

        wavelengths = spec.get_wavelengths()
        intensities = spec.get_spectrum()

        plt.plot(wavelengths, intensities)
        plt.xlabel("Wavelength (nm)")
        plt.ylabel("Intensity")
        plt.title("Spectrum")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    finally:
        spec.close()