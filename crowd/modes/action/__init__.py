import crowd.modes
import crowd.resource
import crowd.input
import crowd.web

import collections

from crowd.modes.action.challenges.cave import CaveChallenge
from crowd.modes.action.challenges.race import RaceChallenge
from crowd.modes.action.challenges.jump import JumpChallenge
from crowd.modes.action.challenges.gather import GatherChallenge
from crowd.modes.action.challenges.rainbow import RainbowChallenge
from crowd.modes.action.challenges.shooter import ShooterChallenge

from crowd.modes.action.base import ActionMode

AVAILABLE_CHALLENGES = [RainbowChallenge, ShooterChallenge, CaveChallenge, RaceChallenge, JumpChallenge, GatherChallenge]

