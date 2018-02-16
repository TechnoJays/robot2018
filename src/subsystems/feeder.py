import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon

class Feeder(Subsystem):
    _left_motor_section = "FeederMotorLeft"
    _right_motor_section = "FeederMotorRight"
    _general_section = "FeederGeneral"
    _switch_section = "FeederSwitch"

    _enabled_key = "ENABLED"
    _channel_key = "CHANNEL"
    _inverted_key = "INVERTED"
    _speed_scale_key = "MAX_SPEED"

    _left_motor_channel = None
    _right_motor_channel = None
    _switch_channel = None
    _left_motor_inverted = None
    _right_motor_inverted = None

    _robot = None
    _config = None
    _left_motor = None
    _right_motor = None
    _switch = None

    _has_cube = False
    _speed_scale = 0.0

    def __init__(self, robot, name = None, configfile = '/home/lvuser/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        super().__init__(name = name)

    # TODO: hasCube(), spinFeeder(), spinFeederLeft(), spinFeederRight()

    def _init_components(self):
        self._speed_scale = self._config.getfloat(self._general_section, self._speed_scale_key)

        if self._config.getboolean(Feeder._general_section, Feeder._enabled_key):
            self._left_motor_channel = self._config.getint(self._left_motor_section, self._channel_key)
            self._left_motor_inverted = self._config.getboolean(self._left_motor_section, self._inverted_key)
            self._right_motor_channel = self._config.getint(self._right_motor_section, self._channel_key)
            self._right_motor_inverted = self._config.getboolean(self._right_motor_section, self._inverted_key)

        if self._left_motor_channel:
            self._left_motor = Talon(self._left_motor_channel)
            if self._left_motor_inverted:
                self._left_motor.setInverted(self._left_motor_inverted)

        if self._right_motor_channel:
            self._right_motor = Talon(self._right_motor_channel)
            if self._right_motor_inverted:
                self._right_motor.setInverted(self._right_motor_inverted)

        if self._config.getboolean(Feeder._switch_section, Feeder._enabled_key):
            self._switch_channel = self._config.getint(self._switch_section, self._channel_key)

        if self._switch_channel:
            self._switch = DigitalInput(self._switch_channel)