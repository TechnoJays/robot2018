from configparser import ConfigParser

from wpilib.command import CommandGroup

from commands.drive_encoder_counts import DriveEncoderCounts
from commands.drive_time import DriveTime
from robot import MyRobot


class CrossLine(CommandGroup):

    _CROSS_SECTION = "CrossLine"
    _CROSS_SPEED = "CROSS_LINE_SPEED"
    _CROSS_TIME = "CROSS_LINE_TIME"
    _CROSS_DISTANCE = "CROSS_LINE_ENCODER"
    _CROSS_DISTANCE_THRESHOLD = "CROSS_LINE_ENCODER_THRESHOLD"

    _robot: MyRobot = None
    _config: ConfigParser = None

    def __init__(self, robot: MyRobot, config_path: str="/home/lvuser/py/configs/autonomous.ini"):
        super().__init__()
        self._robot = robot
        self._config = ConfigParser()
        self._config.read(config_path)

    def initialize(self):
        use_encoder = self._robot.drivetrain.is_encoder_enabled()
        drive_speed = self._config.getfloat(CrossLine._CROSS_SECTION,
                                            CrossLine._CROSS_SPEED)
        if use_encoder:
            encoder_distance = self._config.getint(CrossLine._CROSS_SECTION,
                                                   CrossLine._CROSS_DISTANCE)
            encoder_threshold = self._config.getint(CrossLine._CROSS_SECTION,
                                                    CrossLine._CROSS_DISTANCE_THRESHOLD)
            command = DriveEncoderCounts(self._robot,
                                         encoder_distance,
                                         drive_speed,
                                         encoder_threshold)
        else:
            drive_time = self._config.getfloat(CrossLine._CROSS_SECTION,
                                               CrossLine._CROSS_TIME)
            command = DriveTime(self._robot,
                                drive_time,
                                drive_speed)
        self.addSequential(command)
