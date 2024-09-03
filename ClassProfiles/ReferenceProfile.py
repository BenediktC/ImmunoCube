from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError
import math

class ReferenceProfile(FractionProfile):


    def __init__(self, iD: str, sample_information: dict[str], sample_data: dict[str, float],
                 reference_profile: FractionProfile, logarithm=math.log):
        
        super().__init__(iD, sample_information, sample_data)

        if sorted(list(reference_profile.sampleData.keys())) != sorted(list(self.sampleData.keys())):
            raise UnequalFractionsError

        if any(value == 0 for value in reference_profile.sampleData.values()): 
            raise FractionZeroDivisionError(reference_profile.sampleData)
        
        self.sampleData: dict[str, float] = {
            key: logarithm(self.sampleData[key] / reference_profile.sampleData[key]) for key in
            reference_profile.sampleData.keys()
        }
        

    @staticmethod
    def generate_ReferenceProfiles(profiles: list[FractionProfile], ref_profile: "ReferenceProfile", logarithm=math.log) -> list["ReferenceProfile"]:

        """
        Function to create ReferenceProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of ReferenceProfiles:
        """
        
        if profiles == None: 
            raise EmptyProfileListError
            
        array_reference_profile: list[ReferenceProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_reference_profile[index] = ReferenceProfile(profile.iD, profile.information, profile.sampleData, ref_profile, logarithm)
            
        return array_reference_profile