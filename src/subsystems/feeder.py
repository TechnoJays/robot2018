import configparser
from configparser import ConfigParser
from wpilib import IterativeRobot
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon


class Feeder(Subsystem):
    _left_motor_section: str = "FeederMotorLeft"
    _right_motor_section: str = "FeederMotorRight"
    _general_section: str = "FeederGeneral"
    _switch_section: str = "FeederSwitch"

    _enabled_key: str = "ENABLED"
    _channel_key: str = "CHANNEL"
    _inverted_key: str = "INVERTED"
    _pickup_speed_scale_key: str = "PICKUP_SPEED"
    _shoot_speed_scale_key: str = "SHOOT_SPEED"

    _left_motor_channel: int = None
    _right_motor_channel: int = None
    _switch_channel: int = None

    _left_motor_inverted: bool = None
    _right_motor_inverted: bool = None

    _robot: IterativeRobot = None
    _config: ConfigParser = None
    _left_motor: Talon = None
    _right_motor: Talon = None
    _switch: DigitalInput = None

    _pickup_speed_scale: float = 0.0
    _shoot_speed_scale: float = 0.0

    def __init__(self, robot: IterativeRobot, name=None, configfile: str='/home/lvuser/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self.init_components()
        super().__init__(name=name)

    # TODO: add default command

    def has_cube(self) -> bool:
        if self._switch:
            return not self._switch.get()
        else:
            return False

    def spin_feeder(self, speed: float, left_should_spin: bool, right_should_spin: bool):
        if speed != 0.0:
            if speed > 0.0:
                speed = speed * self._shoot_speed_scale
            if speed < 0.0:
                speed = speed * self._pickup_speed_scale
            if self._left_motor and left_should_spin:
                self._left_motor.set(speed)
            if self._right_motor and right_should_spin:
                self._right_motor.set(speed)

    def init_components(self):
        self._pickup_speed_scale = self._config.getfloat(self._general_section, self._pickup_speed_scale_key)
        self._shoot_speed_scale = self._config.getfloat(self._general_section, self._shoot_speed_scale_key)

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
