from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError

class StatProfile(FractionProfile):
    
    def __init__(self, profiles: list[FractionProfile], iD = None, information = None, main: str = "median",  fractions: list[str]=None):
        
        if profiles is None:
            raise EmptyProfileListError
            
        self.numberProfiles: int = len(profiles)
        self.profiles: list[FractionProfile] = profiles
        self.profileSampleData: list[list[float]] = [
            list(profile.sampleData.values()) for profile in self.profiles] # I don't think I use this later in the code.

        if fractions == None: 
            # if no fractions are specified the first profile in the list provides the default fractions
            self.fractions: list[str] = self.profiles[0].sampleData.keys()
        else:
            self.fractions: list[str] = fractions
                
        # uses dictionaries instead of np.arrays
        self.mean: dict[str, float] = self._get_mean()
        self.median: dict[str, float] = self._get_median()
        self.std: dict[str, float] = self._get_std()

        if main == "median":
                 self.sampleData = self.median
        elif main == "mean":
                 self.sampleData = self.mean
        elif main == "std":
                 self.sampleData = self.std
        else:
                 raise ProfileError
                
        self.iD = iD
        self.information = information
        
    def change_main(main):
        
        if main == "median":
                 self.sampleData = self.median
        elif main == "mean":
                 self.sampleData = self.mean
        elif main == "std":
                 self.sampleData = self.std
        else:
                 raise ProfileError
        
    def _get_mean(self):

        self.mean: dict[str, float] = {}

        for fraction in self.fractions:
            self.mean[fraction]: float = 0

            try:
                for profile in self.profiles:
                    self.mean[fraction] += profile.sampleData[fraction]

                self.mean[fraction] /= self.numberProfiles

            except UnequalFractionsError as e:
                print(f"UnequalFractionsError: {e}")

        return self.mean

    @staticmethod
    def find_median(sorted_list):
        n = len(sorted_list)
        mid = n // 2
        # For odd n, return the middle element
        if n % 2 == 1:
            return sorted_list[mid]
        # For even n, return the average of the middle elements
        else:
            return (sorted_list[mid - 1] + sorted_list[mid]) / 2.0

    def _get_median(self):

        self.median: dict[str, float] = {}

        for fraction in self.fractions:
            self.median_list: list[float] = []

            try:
                for profile in self.profiles:
                    self.median_list.append(profile.sampleData[fraction])

                self.median_list = sorted(self.median_list)
                self.median[fraction] = self.find_median(self.median_list)

            except UnequalFractionsError as e:
                print(f"UnequalFractionsError: {e}")

        return self.median

    def _get_std(self):

        self.std: dict[str, float] = {}

        for fraction in self.fractions:

            self.std[fraction]: float = 0

            try:
                for profile in self.profiles:
                    self.std[fraction] += (profile.sampleData[fraction] - self.mean[fraction]) ** 2

                self.std[fraction] /= self.numberProfiles

            except UnequalFractionsError as e:
                print(f"UnequalFractionsError: {e}")

        return self.std
    
    

