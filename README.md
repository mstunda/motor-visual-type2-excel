# About
The interface is built using Python 3.7 and the TkInter library.
To produce the space vector values simulation data must be exported from Matlab Simulink in spreadsheet format.
A full description of the tool can be found in:

M. Stunda, "Graphical Tool for Browsing Motor Control Simulation Data in the Space Vector Domain," _2019 IEEE 7th IEEE Workshop on Advances in Information, Electronic and Electrical Engineering (AIEEE)_, Liepaja, Latvia, 2019, pp. 1-5.
https://ieeexplore.ieee.org/document/8976934

### User input
The user only has conrol over the timepoint within the simulation. This is manipulated by four differently scaled sliders. By using diferent sliders, different processes can be observed best. 

### Full scale (Zoom x1)
The top slider, which moves the timepoint the fastest, is best for viewing slow processes, such as the magnetization of the machine. This is resembled by the i_mr vector, as it grows towards the target.
![GUI magnetization slowest][1]

### Smallest scale (Zoom x2000)
The botom slider, which can be used to move the timepoint by a single sample, is best for viewing the fastest processes, such as switching of the gates and changing of the electrical torque, which has the highest bandwidth.
The "zoom coefficient" required to browse by single sample is of course dependent on the length and resolution of the simulation.
![GUI gates fastest][2]

### Full overview
Here is a recording of operating all the sliders.
The middle sliders are best for observing the current space vector following it's target and the voltage space vector required to do so.
![GUI overview][3]

[1]: images/GUI_magnetization_slowest.gif
[2]: images/GUI_gates_fastest.gif
[3]: images/GUI_overview.gif