# Team94 FIRST Robotics FRC Robot Code
[FIRST Robotics FRC](http://www.usfirst.org/) is a high 
school robotics program.  This repository contains the code used in the 
Southfield High School Team 94 (TechnoJays) robot.

## Important Notes
**Python**: This codebase uses Python3.

**External Libraries**:
* [pyfrc](https://github.com/robotpy/pyfrc)

## Getting Started
1. Follow the [pyfrc instruction](http://pyfrc.readthedocs.org/en/latest/)
to install and get started with pyfrc.
2. Copy/install all .py files in the src/robot folder to the robot.


## Running Tests
1. Make sure, you have ```tox``` installed::

   ```$ pip3 install -U tox```
   
2. Run all tests across all locally available python versions::

   ```$ tox```
   
   ```tox``` is running ```python src/robot.py coverage test``` from
   [RobotPy Unit Testing](https://robotpy.readthedocs.io/en/stable/guide/testing.html)