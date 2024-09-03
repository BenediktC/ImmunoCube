from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError

class SumProfile(FractionProfile):

    def __init__(self, iD: str, sample_information: dict[str], sampleData: dict[str, float]): 
        super().__init__(iD, sample_information, sampleData)
        
        summation = sum(self.sampleData.values())
        
        if summation == 0:
            raise ZeroSumError

        self.sampleData: dict[str, float] = {
            key: value / summation for key, value in self.sampleData.items()
        }


    @staticmethod
    def generate_SumProfiles(profiles: list[FractionProfile]) -> list["SumProfile"]:

        """
        Function to create SumProfiles for n number of FractionProfiles
        :param profile array of FractionProfiles:
        :return array of SumProfiles:
        """
        
        if profiles == None: 
            raise EmptyProfileListError
            
        array_sum_profiles: list[SumProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_sum_profiles[index] = SumProfile(profile.iD, profile.information, profile.sampleData)

        return array_sum_profiles