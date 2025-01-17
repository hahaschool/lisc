"""Custom errors for LISC."""

###################################################################################################
###################################################################################################

class LISCError(Exception):
    """Base class for errors in the LISC module."""

class InconsistentDataError(LISCError):
    """Custom error for when data is inconsistent."""
