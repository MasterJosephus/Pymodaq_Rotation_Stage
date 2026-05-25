# Pymodaq Rotation Stage Test

We made a venv (python 3.11) with miniforge (mamba). To activate the venv use:

`mamba activate pymodaq_rot_env`

in the miniforge shell. All scripts can be found on `Desktop/Other Programs/pymodaq_test`. 

For our rotation stage there is no plugin. Hence we need to write our own plugin. For this we can clone 
the pymodaq_template_repo:

`git clone https://github.com/PyMoDAQ/pymodaq_plugins_template.git`

to control the rotation stage we will use the `thorlabs-elliptec` package:

`pip install thorlabs-elliptec`