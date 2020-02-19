About
======
<!-- TOC -->

- [Preview](#preview)
    - [User input](#user-input)
    - [Full scale (Zoom x1)](#full-scale-zoom-x1)
    - [Smallest scale (Zoom x2000)](#smallest-scale-zoom-x2000)
    - [Full overview](#full-overview)
- [Running the code](#running-the-code)
    - [Python setup](#python-setup)
    - [Input data](#input-data)

<!-- /TOC -->

This is a graphical tool for browsing output data of an electical drives simulation (e.g. form Matlab Simulink) in the space vector domain and in the rotor flux linkage reference frame.

Usually this data is graphed along several time axis in different scales or in a static locus around the x-y plane. This allows to view the complete development of all the scalar vector components at once, but leaves the spatial interpretation completely to the viewer.

This tool allows viewing the vecotr value development graphically one sample at a time. By browsing through the simulation, the value development is animated under full control of the viewer.

A full description of the tool can be found in:
 [M. Stunda, "Graphical Tool for Browsing Motor Control Simulation Data in the Space Vector Domain," _2019 IEEE 7th IEEE Workshop on Advances in Information, Electronic and Electrical Engineering (AIEEE)_, Liepaja, Latvia, 2019, pp. 1-5.][link.ieee]

This is a continuation of [__a previous project__][link.type1] that ran on simplified motor model equations. 

## Preview
 
### User input
The user only has conrol over the timepoint within the simulation. This is manipulated by four differently scaled sliders. By using diferent sliders, different processes can be observed best. 

### Full scale (Zoom x1)
The top slider, which moves the timepoint the fastest, is best for viewing slow processes, such as the magnetization of the machine. This is resembled by the i_mr vector, as it grows towards the target.
![GUI magnetization slowest][gif.slow]

### Smallest scale (Zoom x2000)
The botom slider, which can be used to move the timepoint by a single sample, is best for viewing the fastest processes, such as switching of the gates and changing of the electrical torque, which has the highest bandwidth.
The "zoom coefficient" required to browse by single sample is of course dependent on the length and resolution of the simulation.
![GUI gates fastest][gif.fast]

### Full overview
Here is a recording of operating all the sliders.
The middle sliders are best for observing the current space vector following it's target and the voltage space vector required to do so.
![GUI overview][gif.overview]


## Running the code
The graphical interface is built using _Python 3.7_ and the _TkInter_ library.

### Python setup
For a quick and easy isolated _Python 3.x_ setup the [_Miniconda_][link.conda] installer (not full _Anaconda_) and the [_Spyder_][link.spyder] IDE can be recommended. 
After installing miniconda _Spyder_ can be installed through the [_Anaconda Prompt_][link.prompt] by running: 
```
conda install spyder
```

If not yet installed, the following Python packages will be required: 
* _xlrd_ and _pandas_ for reading the spreadsheet
* _math_ for calculating the rotating Hexagon 
* _tk_ for building the GUI.

### Input data
To produce the space vector values, simulation data must be exported from Matlab Simulink in spreadsheet (_.xlsx_) format using "_To Workspace_". The column indentifiers and simulation length must be modified within the code to match the spreadsheet contents. A sample spreadsheet is added to run the code instantly. Loading it might take a while.


[link.ieee]: https://ieeexplore.ieee.org/document/8976934
[link.type1]:https://github.com/mstunda/motor-visual-type1-math
[gif.slow]: images/GUI_magnetization_slowest.gif
[gif.fast]: images/GUI_gates_fastest.gif
[gif.overview]: images/GUI_overview.gif
[link.conda]: https://docs.conda.io/en/latest/miniconda.html
[link.spyder]: https://www.spyder-ide.org/
[link.prompt]: https://docs.conda.io/projects/conda/en/4.6.0/_downloads/52a95608c49671267e40c689e0bc00ca/conda-cheatsheet.pdf