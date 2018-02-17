import configparser
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon


class FeederArms(Subsystem):
    _left_motor_section = "FeederArmLeftMotor"
    _right_motor_section = "FeederArmRightMotor"
    _general_section = "FeederArmGeneral"
    _upper_switch_section = "FeederArmUpperSwitch"
    _lower_switch_section = "FeederArmLowerSwitch"

    _enabled_key = "ENABLED"
    _channel_key = "CHANNEL"
    _inverted_key = "INVERTED"
    _move_speed_scale_key = "MOVE_SPEED"

    _left_motor_channel = None
    _right_motor_channel = None
    _upper_switch_channel = None
    _lower_switch_channel = None

    _left_motor_inverted = False
    _right_motor_inverted = False

    _robot = None
    _config = None
    _left_motor = None
    _right_motor = None
    _upper_switch = None
    _lower_switch = None

    _move_speed_scale = 0.0

    def __init__(self, robot, name=None, configfile='/home/lvuser/configs/subsystems.ini'):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self.init_components()
        super().__init__(name=name)

    # TODO: add default command

    def upright_position(self):
        if self._upper_switch:
            return not self._upper_switch.get()
        else:
            return False

    def lowered_position(self):
        if self._lower_switch:
            return not self._lower_switch.get()
        else:
            return False

    def move_feeder_arm(self, speed):
        speed = speed * self._move_speed_scale
        if self._left_motor and self._right_motor:
            self._left_motor.set(speed)
            self._right_motor.set(speed)

    def init_components(self):
        self._move_speed_scale = self._config.getfloat(self._general_section, self._move_speed_scale_key)

        if self._config.getboolean(FeederArms._general_section, FeederArms._enabled_key):
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

        if self._config.getboolean(FeederArms._upper_switch_section, FeederArms._enabled_key):
            self._upper_switch_channel = self._config.getint(self._upper_switch_section, self._channel_key)

        if self._upper_switch_channel:
            self._upper_switch = DigitalInput(self._upper_switch_channel)

        if self._config.getboolean(FeederArms._lower_switch_section, FeederArms._enabled_key):
            self._lower_switch_channel = self._config.getint(self._lower_switch_section, self._channel_key)

        if self._lower_switch_channel:
            self._lower_switch = DigitalInput(self._lower_switch_channel)
