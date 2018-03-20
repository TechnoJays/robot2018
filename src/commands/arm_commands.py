from wpilib.command import Command

LIFT_RANGE = 100

OPEN_RANGE = 100

STALL_PERIOD = 0.5


class OpenArms(Command):

    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_open_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arm_laterally(0)

    def execute(self):
        self._robot.arm.move_arm_laterally(1.0)

    def isFinished(self):
        STALL_PERIOD = 0.5
        is_finished = self._robot.arm.get_open_period() > STALL_PERIOD or self._robot.arm.get_open_count() >= OPEN_RANGE
        if is_finished:
            self._robot.arm.set_open(True)
        return is_finished


class CloseArms(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_open_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arm_laterally(0)

    def execute(self):
        self._robot.arm.move_arm_laterally(-1.0)

    def isFinished(self):
        is_finished = self._robot.arm.get_open_period() > STALL_PERIOD or self._robot.arm.get_open_count() >= OPEN_RANGE
        if is_finished:
            self._robot.arm.set_open(False)
        return is_finished


class RaiseArms(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_vertical_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arms_vertically(0)

    def execute(self):
        self._robot.arm.move_arms_vertically(-1.0)

    def isFinished(self):
        is_finished = self._robot.arm.get_vertical_period() > STALL_PERIOD or self._robot.arm.get_vertical_count() >= LIFT_RANGE
        if is_finished:
            self._robot.arm.set_lowered(False)
        return is_finished


class LowerArms(Command):
    def __init__(self, robot, name=None, timeout=None):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_vertical_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arms_vertically(0)

    def execute(self):
        self._robot.arm.move_arms_vertically(1.0)

    def isFinished(self):
        is_finished = self._robot.arm.get_vertical_period() > STALL_PERIOD or self._robot.arm.get_vertical_count() >= LIFT_RANGE
        if is_finished:
            self._robot.arm.set_lowered(True)
        return is_finished
