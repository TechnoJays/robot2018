from configparser import ConfigParser
from enum import Enum

from wpilib.command import CommandGroup

from commands.drive_encoder_counts import DriveEncoderCounts
from commands.drive_time import DriveTime
from commands.turn_degrees import TurnDegrees
from commands.turn_time import TurnTime
from robot import MyRobot


class Goal(Enum):
    switch = 1, "DriveLineToSwitch", "PlaceSwitch"
    scale = 2, "DriveLineToScale" "PlaceScale"

    def __new__(cls, value, drive_section, place_section):
        obj = object.__new__(cls)
        obj._value = value
        obj.drive_config_section = drive_section
        obj.place_config_section = place_section
        return obj


class CrossLine(CommandGroup):

    _SECTION = "CrossLine"
    _SPEED = "DRIVE_SPEED"
    _TIME = "DRIVE_TIME"
    _DISTANCE_THRESHOLD = "DRIVE_ENCODER_THRESHOLD"
    _DISTANCE = "DRIVE_ENCODER"

    _robot: MyRobot = None

    _drive_speed: float = None
    _drive_distance: int = None
    _drive_threshold: int = None
    _drive_time: float = None

    def __init__(self, robot: MyRobot, config_path: str="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config)

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._SPEED)
        self._drive_distance = parser.getint(self._SECTION, self._DISTANCE)
        self._drive_threshold = parser.getint(self._SECTION, self._DISTANCE_THRESHOLD)
        self._drive_time = parser.getfloat(self._SECTION, self._TIME)

    def initialize(self):
        if use_encoder(self._robot):
            command = DriveEncoderCounts(self._robot,
                                         self._drive_distance,
                                         self._drive_speed,
                                         self._drive_threshold)
        else:
            command = DriveTime(self._robot,
                                self._drive_time,
                                self._drive_speed)
        self.addSequential(command)


class PlaceCube(CommandGroup):

    _SPEED_KEY = "DRIVE_SPEED"
    _TIME_FORWARD_KEY = "DRIVE_TIME_FORWARD"
    _DISTANCE_FORWARD_KEY = "DRIVE_ENCODER"
    _DRIVE_THRESHOLD_KEY = "DRIVE_ENCODER_THRESHOLD"
    _LIFT_HEIGHT_KEY = "LIFT_HEIGHT"
    _LIFT_SPEED_KEY = "LIFT_SPEED"
    _LIFT_THRESHOLD_KEY = "LIFT_THRESHOLD"
    _LIFT_TIME_KEY = "LIFT_TIME"

    _robot: MyRobot = None

    _drive_speed: float = None
    _drive_distance: int = None
    _drive_time: float = None
    _drive_threshold: int = None

    _lift_speed: float = None
    _lift_height: int = None
    _lift_time: float = None
    _lift_threshold: int = None

    def __init__(self,
                 robot: MyRobot,
                 goal: Goal,
                 config_path: str="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config, goal)

    def initialize(self):  # do some stuff here when james merges stuff
        pass

    def _load_config(self, parser: ConfigParser, goal: Goal):
        self._drive_speed = parser.getfloat(goal.place_config_section, self._SPEED_KEY)
        self._drive_distance = parser.getint(goal.place_config_section, self._DISTANCE_FORWARD_KEY)
        self._drive_threshold = parser.getint(goal.place_config_section, self._DRIVE_THRESHOLD_KEY)
        self._drive_time = parser.getfloat(goal.place_config_section, self._TIME_FORWARD_KEY)

        self._lift_speed = parser.getfloat(goal.place_config_section, self._LIFT_SPEED_KEY)
        self._lift_height = parser.getint(goal.place_config_section, self._LIFT_HEIGHT_KEY)
        self._lift_threshold = parser.getint(goal.place_config_section, self._LIFT_THRESHOLD_KEY)
        self._lift_time = parser.getfloat(goal.place_config_section, self._LIFT_TIME_KEY)


class DriveLineToGoal(CommandGroup):

    _SPEED = "DRIVE_SPEED"
    _TURN_SPEED = "TURN_SPEED"
    _TIME_FORWARD = "DRIVE_TIME_FORWARD"
    _TIME_LATERAL = "DRIVE_TIME_LATERAL"
    _DISTANCE_FORWARD = "DRIVE_ENCODER_FORWARD"
    _DISTANCE_LATERAL = "DRIVE_ENCODER_LATERAL"
    _DISTANCE_THRESHOLD = "DRIVE_ENCODER_THRESHOLD"
    _TURN_TIME = "TURN_TIME"
    _TURN_DEGREES = "TURN_DEGREES"

    _robot: MyRobot = None

    _drive_speed: float = None
    _turn_speed: float = None

    _encoder_threshold: int = None
    _distance_forward: int = None
    _distance_lateral: int = None

    _time_forward: int = None
    _time_lateral: int = None

    _turn_degrees: float = None
    _turn_time: float = None

    def __init__(self,
                 robot: MyRobot,
                 goal: Goal,
                 config_path: str="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        config = ConfigParser()
        config.read(config_path)
        self._load_config(config, goal)

    def initialize(self):
        if use_encoder(self._robot):
            forward_command = DriveEncoderCounts(self._robot,
                                                 self._distance_forward,
                                                 self._drive_speed,
                                                 self._encoder_threshold)
        else:
            forward_command = DriveTime(self._robot,
                                        self._time_forward,
                                        self._drive_speed)

        self.addSequential(forward_command)

        if use_gyro(self._robot):
            turn_command = TurnDegrees(self._robot,
                                       self._turn_degrees,
                                       self._turn_speed,
                                       self._encoder_threshold)
        else:
            turn_command = TurnTime(self._robot,
                                    self._turn_time,
                                    self._turn_speed)

        self.addSequential(turn_command)

        if use_encoder(self._robot):
            lateral_command = DriveEncoderCounts(self._robot,
                                                 self._distance_lateral,
                                                 self._drive_speed,
                                                 self._encoder_threshold)
        else:
            lateral_command = DriveTime(self._robot,
                                        self._time_lateral,
                                        self._drive_speed)

        self.addSequential(lateral_command)

    def _load_config(self, config_parser: ConfigParser, goal: Goal):
        self._drive_speed = config_parser.getfloat(goal.drive_config_section, self._SPEED)
        self._turn_speed = config_parser.getfloat(goal.drive_config_section, self._TURN_SPEED)

        self._encoder_threshold = config_parser.getint(goal.drive_config_section, self._DISTANCE_THRESHOLD)
        self._distance_forward = config_parser.getint(goal.drive_config_section, self._DISTANCE_FORWARD)
        self._distance_lateral = config_parser.getint(goal.drive_config_section, self._DISTANCE_LATERAL)

        self._time_forward = config_parser.getfloat(goal.drive_config_section, self._TIME_FORWARD)
        self._time_lateral = config_parser.getfloat(goal.drive_config_section, self._TIME_LATERAL)

        self._turn_degrees = config_parser.getfloat(goal.drive_config_section, self._TURN_DEGREES)
        self._turn_time = config_parser.getfloat(goal.drive_config_section, self._TURN_TIME)


def use_encoder(robot: MyRobot) -> bool:
    return robot.drivetrain.is_encoder_enabled()


def use_gyro(robot: MyRobot) -> bool:
    return robot.drivetrain.is_gyro_enabled()
