from wpilib.command.command import Command


class ToggleBoundsChecking(Command):

    def __init__(self, oi, name=None, timeout=5):
        super().__init__(name, timeout)
        self._oi = oi

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._oi.toggle_bounds_checking_enabled()

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return True

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()
