from .FractionProfile import FractionProfile
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError
from typing import Self, List, Dict, Set
from deprecated import deprecated
import matplotlib.pyplot as plt


class StatProfile(FractionProfile):
    
    def __init__(self, profiles: List[FractionProfile], main: str = "median", iD: str = None, information: Dict[str,str] = None,  fractions: List[str]=None):
        
        if not profiles:
            raise EmptyProfileListError
            
        self.numberProfiles: int = len(profiles)
        self.profiles: List[FractionProfile] = profiles
        self.profileSampleData: List[List[float]] = [
            list(profile.sampleData.values()) for profile in self.profiles] # I don't think I use this later in the code.

        if fractions == None: 
            # if no fractions are specified the first profile in the list provides the default fractions
            self.fractions: List[str] = list(self.profiles[0].sampleData.keys())
        else:
            self.fractions: List[str] = fractions
                
        # uses dictionaries instead of np.arrays
        self.mean: Dict[str, float] = self._get_mean()
        self.median: Dict[str, float] = self._get_median()
        self.std: Dict[str, float] = self._get_std()
        
        # in order to use the normal functionalities of the FractionProfile base class (e.g. plotting, conversion to SumProfile, etc.) 
        # one of the metrices of mean, median or std has to be assigned to the sampleData dictionary
        if main == "median":
                 self.sampleData = self.median
        elif main == "mean":
                 self.sampleData = self.mean
        elif main == "std":
                 self.sampleData = self.std
        else:
                 raise ProfileError("Accepted arguments are median, mean & std")
                
        self.iD = iD
        self.information = information

        
        # Notes pseudocode andreas, delete soon   
#     something: List[FractionProfile] = [FractionProfile(sdkfljs), StatProfile(2347234e982)]
       
#     a = FractionProfile(sdkjfls)
#     b = FractionProfile(sdkjflx)
#     c = FractionProfile(sdkjflsz)
#     something: List[FractionProfile] = [FractionProfile, StatProfile]
        
        
#     something2: List[FractionProfile] = []
#     for item in something:
#         something2.append(item.objectify_w_profiles([a, b, c])
    
    @classmethod
    def objectify_w_profile(cls, profile: 'Profile', deep_copy: bool = False) -> Self: 
        raise ProfileError("It does not make sense to create a StatProfile out of a single Profile.")
        
    @classmethod
    def objectify_w_profiles(cls, profiles: List['Profile'], deep_copy: bool = False, main:str = "median", iD: str= None, information: Dict[str,str] = None,  fractions: List[str] = None) -> Self: 
            
            # ToDo deepcopy
            
            if not profiles: 
                raise EmptyProfileListError
                
            return cls(profiles, main, information, iD, fractions)
    
    # change the representation of the sample data to another metrix
    def change_main(self, main):
        
        if main == "median":
                 self.sampleData = self.median
        elif main == "mean":
                 self.sampleData = self.mean
        elif main == "std":
                 self.sampleData = self.std
        else:
                 raise ProfileError("Accepted arguments are median, mean & std")
        
    def _get_mean(self):

        self.mean: Dict[str, float] = {}

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

        self.median: Dict[str, float] = {}

        for fraction in self.fractions:
            self.median_list: List[float] = []

            try:
                for profile in self.profiles:
                    self.median_list.append(profile.sampleData[fraction])

                self.median_list = sorted(self.median_list)
                self.median[fraction] = self.find_median(self.median_list)

            except UnequalFractionsError as e:
                print(f"UnequalFractionsError: {e}")

        return self.median

    def _get_std(self):

        self.std: Dict[str, float] = {}
        self.variance: Dict[str, float] = {}
            
        for fraction in self.fractions:

            self.std[fraction]: float = 0
            self.variance[fraction]: float = 0

            try:
                for profile in self.profiles:
                    self.variance[fraction] += (profile.sampleData[fraction] - self.mean[fraction]) ** 2

                self.variance[fraction] /= self.numberProfiles
                
                self.std[fraction] = self.variance[fraction]**0.5 # math.sqrt(self.variance[fraction])

            except UnequalFractionsError as e:
                print(f"UnequalFractionsError: {e}")

        return self.std
    
    @deprecated
    def plotter(self, errorbars=True):
        # Create the plot
        plt.figure(figsize=(10, 6))  # Set the figure size

        x_values = list(self.sampleData.keys())
        y_values = list(self.sampleData.values())
        std_errors = list(self.std.values()) 
        
        if errorbars and std_errors is not None:
            # Plot the data points with error bars
            plt.errorbar(x_values, y_values, yerr=std_errors, fmt='-o', 
                         markersize=10, markerfacecolor='blue', markeredgecolor='black', 
                         linewidth=2, capsize=5, color='blue', ecolor='grey')
        else:
            # Plot the data points without error bars
            plt.plot(x_values, y_values, '-o', 
                     markersize=10, markerfacecolor='blue', markeredgecolor='black', 
                     linewidth=2, color='blue')

        # Customizing the plot
        plt.title("Sample: {}".format(self.iD))  # Title
        plt.xlabel('Fractions')  # X-axis label
        plt.ylabel('Protein Concentration')  # Y-axis label

        # Display the plot
        plt.show()

