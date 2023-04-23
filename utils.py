from PIL.TiffImagePlugin import IFDRational
from fractions import Fraction
import base64

def convert_to_serializable(data):
    if isinstance(data, IFDRational):
        # Convert IFDRational to a tuple (numerator, denominator)
        return (data.numerator, data.denominator)
    elif isinstance(data, bytes):
        # Convert binary data to a base64-encoded string
        return base64.b64encode(data).decode('utf-8')
    elif isinstance(data, dict):
        # Recursively process dictionary values
        return {k: convert_to_serializable(v) for k, v in data.items()}
    elif isinstance(data, list):
        # Recursively process list elements
        return [convert_to_serializable(v) for v in data]
    else:
        # Return other data types as-is
        return data