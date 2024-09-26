from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError
import math
from typing import Self, List, Dict, Set
from deprecated import deprecated
import matplotlib.pyplot as plt

class ReferenceProfile(FractionProfile):


    def __init__(self, iD: str, sample_information: Dict[str, str], sample_data: Dict[str, float],
                 reference_profile: FractionProfile, logarithm=math.log):
        
        super().__init__(iD, sample_information, sample_data)
        
        # Checks whether same fractions were passed in
        if sorted(list(reference_profile.sampleData.keys())) != sorted(list(self.sampleData.keys())):
            raise UnequalFractionsError
        
        # prevent division by zero error
        if any(value == 0 for value in reference_profile.sampleData.values()): 
            raise FractionZeroDivisionError(reference_profile.sampleData)
        
        # dict comprehension to calculate the intensity relative to the reference profile
        self.sampleData: Dict[str, float] = {
            key: logarithm(self.sampleData[key] / reference_profile.sampleData[key]) for key in
            reference_profile.sampleData.keys()
        }
        
    @classmethod
    def objectify_w_profile(cls, profile: 'Profile', reference_profile, logarithm=math.log, deep_copy: bool = False) -> Self: 
        # ToDo if deep_copy: copy.deepcopy(original) 
        return cls(profile.iD, profile.information, profile.sampleData, reference_profile, logarithm)
    
    @classmethod
    def objectify_w_profiles(cls, profiles: List['Profile'], logarithm=math.log, deep_copy: bool = False) -> List[Self]:
           
            if not profiles: 
                raise EmptyProfileListError
            # ToDo deepcopy   
            return [cls(profile.iD, profile.information, profile.sampleData, reference_profile, logarithm) for profile in profiles]
    
    # function replaced with objectify_w_profile   
    @deprecated    
    @staticmethod
    def generate_Profiles(profiles: List[FractionProfile], ref_profile: "ReferenceProfile", logarithm=math.log) -> List["ReferenceProfile"]:

        """
        Function to create ReferenceProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of ReferenceProfiles:
        """
        
        if not profiles: 
            raise EmptyProfileListError
            
        array_reference_profile: List[ReferenceProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_reference_profile[index] = ReferenceProfile(profile.iD, profile.information, profile.sampleData, ref_profile, logarithm)
            
        return array_reference_profile