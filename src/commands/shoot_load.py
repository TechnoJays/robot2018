from wpilib.command.command import Command
import time

class ShootLoad(Command):

    _time_stamp = 0

    def __init__(self, robot, feedouttime: float, speed: float=0.0,, name=None, timeout=5):
        super().__init__(name, timeout)
        self._robot = robot
        self._feed_time = feedouttime
        self._feeder_speed: float = speed
        self.requires(robot.feeder)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._time_stamp = time.time()
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.feeder.feed_cube(self._feeder_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return time.time() > self._time_stamp + self._feed_time

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.feeder.feed_cube(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()