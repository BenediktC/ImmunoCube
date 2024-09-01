from .FractionProfile import FractionProfile, FractionProfileError
import math
class ReferenceProfile(FractionProfile):


    def __init__(self, iD: str, sample_information: dict[str], sample_data: dict[str, float],
                 reference_profile: FractionProfile, logarithm=math.log):
        
        super().__init__(iD, sample_information, sample_data) # korrigierte sampleData direkt hier reinhauen statt unten comprehension.

        # check whether same keys exist.
        assert sorted(list(reference_profile.sampleData.keys())) == sorted(list(self.sampleData.keys())), "KeyError"

        if any(reference_profile.sampleData.values()==0): 
            raise FractionProfileError("meaningful message")
        
        self.sampleData: dict[str, float] = {
            key: logarithm(self.sampleData[key] / reference_profile.sampleData[key]) for key in
            reference_profile.sampleData.keys()
        }
        
        # ToDo Division by zero catch


    @staticmethod
    def generate_ReferenceProfiles(profiles: list[FractionProfile], ref_profile: "ReferenceProfile", logarithm=math.log) -> list["ReferenceProfile"]:

        """
        Function to create ReferenceProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of ReferenceProfiles:
        """

        array_reference_profile: list[ReferenceProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_reference_profile[index] = ReferenceProfile(profile.iD, profile.information, profile.sampleData, ref_profile, logarithm)
            
        return array_reference_profile