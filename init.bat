::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAjk
::fBw5plQjdCmDJNxKFcTj6pO6nYFa3+5q2j3wIGE6Nm18bHEtTfY3d4HU2bfDA8E31kznepg+6nZVn8RCBRhXHg==
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSzk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCmDJNxKFcTj6pO6nYFa3+5q2j3wIGE6Nm18bHEtTfY3d4HU2bfDA8E31mf2cIYO914UndMJbA==
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983

@echo off
cd /d %~dp0
set path=%~dp0
set parameter0=python3.7
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

python BaseGui.py





