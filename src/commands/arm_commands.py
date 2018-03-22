from wpilib.command import Command

from oi import UserController, JoystickAxis


class OpenArms(Command):

    def __init__(self, robot, name=None, timeout=2):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_open_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arm_laterally(0)
        self._robot.arm.set_open(True)

    def execute(self):
        self._robot.arm.move_arm_laterally(-1.0)

    def isInterruptible(self):
        return True

    def isFinished(self):
        return self._robot.arm.get_open_count() >= 28


class CloseArms(Command):
    def __init__(self, robot, name=None, timeout=2):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_open_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arm_laterally(0)
        self._robot.arm.set_open(False)

    def execute(self):
        self._robot.arm.move_arm_laterally(1.0)

    def isInterruptible(self):
        return True

    def isFinished(self):
        return self._robot.arm.get_open_count() >= 25


class RaiseArms(Command):
    def __init__(self, robot, name=None, timeout=2):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_vertical_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arms_vertically(0)
        self._robot.arm.set_lowered(False)

    def isInterruptible(self):
        return True

    def execute(self):
        self._robot.arm.move_arms_vertically(1.0)

    def isFinished(self):
        is_finished = self._robot.arm.get_vertical_count() >= 130
        return is_finished


class LowerArms(Command):
    def __init__(self, robot, name=None, timeout=2):
        super().__init__(name, timeout)
        self._robot = robot
        self.requires(robot.arm)

    def initialize(self):
        self._robot.arm.reset_vertical_count()

    def interrupted(self):
        self.end()

    def end(self):
        self._robot.arm.move_arms_vertically(0)
        self._robot.arm.set_lowered(True)

    def execute(self):
        self._robot.arm.move_arms_vertically(-1.0)

    def isInterruptible(self):
        return True

    def isFinished(self):
        is_finished = self._robot.arm.get_vertical_count() >= 90
        return is_finished


class MoveArmLol(Command):

    def __init__(self, robot, name=None, timeout=5):
        super().__init__(name, timeout)
        self.robot = robot
        self.requires(robot.arm)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        vert_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.DPADY)
        self.robot.arm.move_arms_vertically(vert_speed)
        hor_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.DPADX)
        self.robot.arm.move_arm_laterally(hor_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self.robot.arm.move_arms_vertically(0.0)
        self.robot.arm.move_arm_laterally(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()