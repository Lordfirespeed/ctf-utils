# The contents of this file are significantly based upon 
# https://github.com/tqdm/tqdm/blob/0ed5d7f18fa3153834cbac0aa57e8092b217cc16/tqdm/utils.py
# Copyright 2015-2024 (c) Casper da Costa-Luis
# The referenced materials are licensed to Lordfirespeed under the terms of the MPL-2.0 license.

"""
General helpers required for `utils.reprint.printer`.
"""
import re

from wcwidth import wcswidth


RE_ANSI = re.compile(r"\x1b\[[;\d]*[A-Za-z]")


def disp_len(data):
    """
    Returns the real on-screen length of a string which may contain
    ANSI control codes and wide chars.
    """
    return wcswidth(RE_ANSI.sub('', data))


__all__ = ("disp_len",)
