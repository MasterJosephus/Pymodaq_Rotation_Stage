# Pymodaq Rotation Stage Test

We made a venv (python 3.11) with miniforge (mamba). To activate the venv use:

`mamba activate pymodaq_rot_env`

in the miniforge shell. All scripts can be found on `Desktop/Other Programs/pymodaq_test`. 

## Thorlabs Rotation Stage

For our rotation stage there is no plugin. Hence we need to write our own plugin. For this we can clone 
the pymodaq_template_repo:

`git clone https://github.com/PyMoDAQ/pymodaq_plugins_template.git`

To control the rotation stage we will use the `thorlabs-elliptec` package:

`pip install thorlabs-elliptec`

The interfacing of the thorlabs stage was very straight-forward and the code to interface it is located at `scr/hardware/RotStage.py` and its implementation in
pymodaq is at `daq_move_plugins/daq_move_RotStage.py`.

## Qmini RGBLasersystems Fiber Spectrometer

To interface the qmini rgblasersystems USB mini spectrometer we had to download the SDK here: "https://docs.broadcom.com/docs/12398530" 
We then copied the provided `RgbDriverKit.dll` to the `hardware` directory within the pymodaq plugin. In addition the dowload of the `Waves` software form the provider is required to operate the spectrometer. This software can be dowloaded free of charge from the proveder webiste following the link: "https://docs.broadcom.com/docs/12398529".

The SDK exposes the spectrometer API through a .NET assembly (`RgbDriverKit.dll`). A .NET assembly is a compiled software library containing reusable classes and methods that can be called from any .NET-compatible language such as C#, MATLAB, or Python.

To access the DLL methods from Python, we translated the vendor-provided MATLAB example into Python using the `pythonnet` library.

`pip install pythonnet`

`pythonnet` provides interoperability between Python and the Microsoft .NET runtime, allowing Python code to directly load .NET assemblies and call their classes and methods.