from enum import Enum

class DesignStatusTag(Enum):
    DEV = 0
    PROD = 1

    def describle(self):
        if self == DesignStatusTag.DEV:
            return "IP/Chip in development"
        elif self == DesignStatusTag.PROD:
            return "IP/Chip in production"