from wpilib.command import Command

from oi import UserController, JoystickAxis


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
        vert_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.DPADY) * -0.7
        self.robot.arm.move_arms_vertically(vert_speed)
        hor_speed = self.robot.oi.get_axis(UserController.SCORING, JoystickAxis.DPADX) * 0.7
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