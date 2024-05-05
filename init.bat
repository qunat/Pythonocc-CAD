@echo off
cd /d %~dp0
set path=%~dp0
set parameter0=Win64\python3.7
set parameter1=\Library\mingw-w64\bin
set parameter2=\Library\usr\bin
set parameter3=\Library\bin
set parameter4=\Scripts
set parameter5=\bin
set parameter6=\Lib\site-packages\PyQt5\Qt5\plugins\platforms

set path0=%path%%parameter0%
set path1=%path0%%parameter1%
set path2=%path0%%parameter2%
set path3=%path0%%parameter3%
set path4=%path0%%parameter4%
set path5=%path0%%parameter5%
set path6=%path0%%parameter6%

set PATH=%PATH%;%path0%
set PATH=%PATH%;%path1%
set PATH=%PATH%;%path2%
set PATH=%PATH%;%path3%
set PATH=%PATH%;%path4%
set PATH=%PATH%;%path5%
set QT_QPA_PLATFORM_PLUGIN_PATH=%path6%

echo %PATH%

REM Check if opengl32.dll is present, if yes remove it.
SET BREPCAD_GUI_ROOT_DIR=%path%\Win64\Gui\

REM START python.exe %path%\brepcad %*
python Brepcad.py





