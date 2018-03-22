from configparser import ConfigParser

from wpilib.counter import Counter

from commands.arm_commands import MoveArmLol
from wpilib.command.subsystem import Subsystem
from wpilib.digitalinput import DigitalInput
from wpilib.talon import Talon
from wpilib.smartdashboard import SmartDashboard


class Arm(Subsystem):
    _vertical_motor_section: str = "ArmVerticalMotor"
    _lateral_motor_section: str = "ArmLateralMotor"
    _general_section: str = "ArmGeneral"
    _lowered_counter_section: str = "ArmLoweredCounter"
    _open_counter_section: str = "ArmOpenCounter"

    _enabled_key: str = "ENABLED"
    _channel_key: str = "CHANNEL"
    _inverted_key: str = "INVERTED"
    _move_speed_scale_key: str = "ARM_MOVE_SPEED"

    _vertical_motor_channel: int = None
    _lateral_motor_channel: int = None
    _lowered_counter_channel: int = None
    _open_counter_channel: int = None

    _vertical_motor_inverted: bool = False
    _lateral_motor_inverted: bool = False

    _robot = None
    _config: ConfigParser = None
    _vertical_motor: Talon = None
    _lateral_motor: Talon = None
    _open_counter: Counter = None
    _vertical_counter: Counter = None

    _is_lowered: bool = False
    _is_open: bool = True

    _move_speed_scale: float = 1.0

    def __init__(self, robot, name=None, configfile: str='/home/lvuser/py/configs/subsystems.ini'):
        super().__init__(name=name)
        self._robot = robot
        self._config = ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard()

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveArmLol(self._robot))

    def reset_vertical_count(self):
        self._vertical_counter.reset()

    def get_vertical_count(self):
        SmartDashboard.putNumber("Vertical Count", self._vertical_counter.get())
        return self._vertical_counter.get()

    def get_vertical_period(self):
        return self._vertical_counter.getPeriod()

    def reset_open_count(self):
        self._open_counter.reset()

    def get_open_count(self):
        SmartDashboard.putNumber("Open Count", self._vertical_counter.get())
        return self._open_counter.get()

    def get_open_period(self):
        return self._vertical_counter.getPeriod()

    def is_lowered(self) -> bool:
        return self._is_lowered

    def is_open(self) -> bool:
        return self._is_open

    def set_open(self, is_open):
        self._is_open = is_open
        self._update_smartdashboard()

    def set_lowered(self, is_lowered):
        self._is_lowered = is_lowered
        self._update_smartdashboard()

    def move_arm_laterally(self, speed: float) -> None:
        if not self._lateral_motor:
            return
        if speed < 0.0 and self._is_open:
            return
        elif speed > 0.0 and not self._is_open:
            return
        self._lateral_motor.set(speed * self._move_speed_scale)
        self._update_smartdashboard()

    def move_arms_vertically(self, speed: float) -> None:
        if not self._vertical_motor:
            return
        if speed > 0.0 and not self._is_lowered:
            return
        elif speed < 0.0 and self._is_lowered:
            return
        self._vertical_motor.set(speed * self._move_speed_scale)
        self._update_smartdashboard()

    def _update_smartdashboard(self):
        SmartDashboard.putBoolean("Arm is lowered", self._is_lowered)
        SmartDashboard.putBoolean("Arm is open", self._is_open)

    def _init_components(self) -> None:
        if self._config.getfloat(self._general_section, self._move_speed_scale_key) is not None:
            self._move_speed_scale = self._config.getfloat(self._general_section, self._move_speed_scale_key)

        if self._config.getboolean(Arm._lateral_motor_section, Arm._enabled_key):
            self._lateral_motor_channel = self._config.getint(self._lateral_motor_section, self._channel_key)
            self._lateral_motor_inverted = self._config.getboolean(self._lateral_motor_section, self._inverted_key)

        if self._config.getboolean(Arm._vertical_motor_section, Arm._enabled_key):
            self._vertical_motor_channel = self._config.getint(self._vertical_motor_section, self._channel_key)
            self._vertical_motor_inverted = self._config.getboolean(self._vertical_motor_section, self._inverted_key)

        if self._vertical_motor_channel:
            self._vertical_motor = Talon(self._vertical_motor_channel)
            if self._vertical_motor:
                self._vertical_motor.setInverted(self._vertical_motor_inverted)

        if self._lateral_motor_channel:
            self._lateral_motor = Talon(self._lateral_motor_channel)
            if self._lateral_motor:
                self._lateral_motor.setInverted(self._lateral_motor_inverted)

        if self._config.getboolean(Arm._lowered_counter_section, Arm._enabled_key):
            self._lowered_counter_channel = self._config.getint(self._lowered_counter_section, self._channel_key)
            print("Lowered Counter Channel: " + str(self._lowered_counter_channel))
            dio = DigitalInput(self._lowered_counter_channel)
            print("Lowered DigitalInput: " + str(dio))
            if self._lowered_counter_channel:
                self._vertical_counter = Counter(dio)
                print("Lowered Counter: " + str(self._vertical_counter))

        if self._config.getboolean(Arm._open_counter_section, Arm._enabled_key):
            self._open_counter_channel = self._config.getint(self._open_counter_section, self._channel_key)
            print("Open Counter Channel: " + str(self._open_counter_channel))
            dio = DigitalInput(self._open_counter_channel)
            print("Open DigitalInput: " + str(dio))
            if self._open_counter_channel:
                self._open_counter = Counter(dio)
                print("Open Counter: " + str(self._open_counter))
