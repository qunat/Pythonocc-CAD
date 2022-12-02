# pythonocc-CAD
The pythonocc CAD open source framework is adapted from the SimpleGui in pythonocc. It incorporates the beautiful ribbon style, which also uses the open source library QupyRibbon in Github.

This framework can basically meet the needs of graduation design of college students and enterprise level lightweight CAD software development. Because it is based on the python language, the running efficiency cannot be compared with that of the c++version. But there is no bad language in the world. Only the less excellent programmers can write software with good performance as long as they continue to optimize the algorithm.



![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/pythonocc-CAD-1.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/pythonocc-CAD-2.png)
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/pythonocc-CAD-3.png)

# pythonocc
![alt tag](http://cad-upyun.test.upcdn.net/pythonocc-CAD/setup_pic.png)
# first create an environment
```
conda create --name=pyoccenv python=3.7
source activate pyoccenv
conda install -c conda-forge pythonocc-core=7.4
```

#Run it 
```
git clone https://github.com/qunat/Pythonocc-CAD.git
conda activate your environment
cd pythonocc-CAD
python BaseGui.py
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
