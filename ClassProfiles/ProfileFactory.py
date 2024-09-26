from .FractionProfile import FractionProfile
from .StatProfile import StatProfile
from .SumProfile import SumProfile
from .ReferenceProfile import ReferenceProfile
from .ProfilePCA import ProfilePCA
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError, ComponentErrorPCA
from typing import Self, List, Dict, Set

class ProfileFactory(object):
    
    '''
    Sketch of ProfileFactory, ToDo
    '''
    
    SumProfile = SumProfile
    FractionProfile = FractionProfile
    ReferenceProfile = ReferenceProfile
    StatProfile = StatProfile
    
    # def csv pipeline
    def create_fraction_profiles_with_csv(file: str, profile) -> FractionProfile:
        # ToDo later
        pass