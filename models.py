"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """
    # How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        # Initialize string variable for hazardous message referenced in __str__ method.

        # Coerce designation to str type
        self.designation = str(info.get('pdes', None))
        if self.designation == '':
            self.designation = None

        # Coerce name to str type
        self.name = str(info.get('name', None))
        if self.name == '':
            self.name = None

        # Coerce diameter to float type
        diam = info.get('diameter', float('nan'))
        if diam == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(diam)

        # Coerce hazardous attribute to boolean type
        self.hazardous = info.get('pha', 'None') == 'Y'

        # Define hazardous message part
        self.hazardous_str = info.get('pha', 'None')

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        # Use self.designation and self.name to build a fullname for this object.
        fullname_str = self.designation

        if (fullname_str is not None) and (self.name is not None):
            fullname_str += ' (' + self.name + ')'
        elif fullname_str is None:
            fullname_str = 'None'

        return fullname_str

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.

        # Define hazardous message part
        if self.hazardous_str == 'None':
            hazard_str = "[is/is not]"
        elif self.hazardous:
            hazard_str = "is"
        else:
            hazard_str = "is not"

        # Define diameter message part
        if math.isnan(self.diameter):
            diameter_str = "undefined"
        else:
            diameter_str = f"{self.diameter:.3f}"

        return f"NEO {self.fullname} has a diameter of {diameter_str} km and {hazard_str} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """
        Return serialized Near Earth Object (NEO) as a dictionary

        example: Return {'designation': '433', 'name': 'Eros', 'diameter_km': 16.84, 'potentially_hazardous': False}
        """
        neo_dict = {'designation': self.designation,
                    'name': self.fullname,
                    'diameter_km': self.diameter,
                    'potentially_hazardous': self.hazardous}
        return neo_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    # How can you, and should you, change the arguments to this constructor?
    # If you make changes, be sure to update the comments in this file.
    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.

        # Coerce self._designation to str type
        self._designation = str(info.get('des', None))
        if self._designation == '':
            self._designation = None

        # Check for null or blank cd (calendar date)
        cd = str(info.get('cd', None))
        if cd == '':
            cd = None

        # Call cd_to_datetime function to format the calendar date
        if cd is not None:
            self.time = cd_to_datetime(cd)
        else:
            self.time = None

        # Nominal approach distance in astronomical units (au) to Earth at closest point
        self.distance = info.get('dist', float('nan'))
        if self.distance == '':
            self.distance = float('nan')
        else:
            self.distance = float(self.distance)

        # Velocity in kilometers (km) per second relative Earth at closest point
        self.velocity = info.get('v_rel', float('nan'))
        if self.velocity == '':
            self.velocity = float('nan')
        else:
            self.velocity = float(self.velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        if self.time is not None:
            formatted_datetime_str = datetime_to_str(self.time)
        else:
            formatted_datetime_str = 'Undefined'

        return formatted_datetime_str

    @property
    def full_name(self):
        # Use self.designation and self.name to build a fullname for this object.
        if self.neo is None:
            if self._designation is None:
                return 'None'
            else:
                return self._designation
        else:
            return self.neo.fullname

    def __str__(self):
        """Return `str(self)`."""
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"At {self.time_str}, '{self.full_name}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        """
        Return serialized CloseApproach object as dictionary

        example: Return {'datetime_utc': '2025-11-30 02:18', 'distance_au': 0.397647483265833, 'velocity_km_s': 3.72885069167641}
        """
        approach_dict = {'datetime_utc': self.time_str,
                         'distance_au': self.distance,
                         'velocity_km_s': self.velocity}
        return approach_dict
