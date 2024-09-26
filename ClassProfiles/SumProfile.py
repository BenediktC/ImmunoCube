from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError
from typing import Self, List, Dict, Set
from deprecated import deprecated
import matplotlib.pyplot as plt

class SumProfile(FractionProfile):

    def __init__(self, iD: str, sample_information: Dict[str, str], sampleData: Dict[str, float]): 
        super().__init__(iD, sample_information, sampleData)
        
        # calculates the total intensity of all samples
        summation = sum(self.sampleData.values())
        
        # prevent division by zero error
        if summation == 0:
            raise ZeroSumError
           
        # dict comprehension to calculate relative values
        self.sampleData: Dict[str, float] = {
            key: value / summation for key, value in self.sampleData.items()
        }


    # function replaced with objectify_w_profile   
    @deprecated
    @staticmethod
    def generate_Profiles(profiles: List[FractionProfile]) -> List["SumProfile"]:

        """
        Function to create SumProfiles for n number of FractionProfiles
        :param profile array of FractionProfiles:
        :return array of SumProfiles:
        """
        
        if not profiles: 
            raise EmptyProfileListError
            
        array_sum_profiles: List[SumProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_sum_profiles[index] = SumProfile(profile.iD, profile.information, profile.sampleData)

        return array_sum_profiles