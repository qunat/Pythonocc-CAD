# BrepCAD
The BrepCAD open source framework is adapted from the SimpleGui in pythonocc. It incorporates the beautiful ribbon style, which also uses the open source library QupyRibbon in Github.

This framework can basically meet the needs of graduation design of college students and enterprise level lightweight CAD software development. Because it is based on the python language, the running efficiency cannot be compared with that of the c++version. But there is no bad language in the world. Only the less excellent programmers can write software with good performance as long as they continue to optimize the algorithm.


![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/BrepCAD-1.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/BrepCAD-2.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/BrepCAD-3.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/BrepCAD-4.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/BrepCAD-5.png)


pythonocc-core
--------------

About
-----

pythonocc is a python package whose purpose is to provide 3D modeling
features. It is intended to CAD/PDM/PLM and BIM related development.

version : [pythonocc-core 7.4.0 (february 2020)](https://github.com/tpaviot/pythonocc-core/releases/tag/7.4.0)

Features
--------
pythonocc provides the following features:

*   a full access from Python to almost all af the thousand OpenCascade C++ classes. Classes and methods/functions share the same names, and, as possible as it can be, the same signature

*   3D visualization from the most famous Python Gui (pyQt, PySide1 and 2, wxPython)

*   3D visualization in a web browser using WebGl and/or x3dom renderers

*   3D visualization and work within a jupyter notebook

*   Various utility Python classes/methods for DataExchange, Topology operations, intertia computations etc.



# first create an environment
```
conda create --name=pyoccenv python=3.7
source activate pyoccenv
conda install -c conda-forge pythonocc-core=7.4
```

# Run it 
```
git clone https://github.com/qunat/Pythonocc-CAD.git
conda activate your environment
cd pythonocc-CAD
python BaseGui.py
also clcik the BrepCAD.exe

```
# update it 
```
git pull
this can get the latest version
```

```

```


# QupyRibbon
![alt tag](http://i.imgur.com/ry2SudV.png)

This is a ribbon implementation in Python 3 using PyQt5.

To use this you need to get the dependencies:
```
sudo apt install python3
sudo apt install python3-pyqt5
```

The project is made in Pycharm community eddition.
For example clone the project:
```
git clone https://github.com/pracedru/QupyRibbon
```
and run:
```
python3 main.py 
```
