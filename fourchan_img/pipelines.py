# -*- coding: utf-8 -*-
import os
import re

def sanitize_filename(filename):
    # Remove any characters that aren't alphanumeric, underscore, or dash
    return re.sub(r'(?u)[^-\w.]', '', str(filename))
