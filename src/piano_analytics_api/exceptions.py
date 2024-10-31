"""
© 2024 Omroep Gelderland
SPDX-License-Identifier: MIT
"""

from typing import Optional


class PianoAnalyticsException(Exception):
    """
    General exception for errors within the package.
    """

    pass


class APIException(PianoAnalyticsException):
    """
    API error reported by Piano Analytics.
    """

    def __init__(
        self, message: Optional[str], http_status: int, type: Optional[str] = None
    ) -> None:
        super().__init__(message, http_status, type)
        self.type = type


class NotImplementedException(PianoAnalyticsException):
    pass
