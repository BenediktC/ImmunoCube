import math
import matplotlib.pyplot as plt
from deprecated import deprecated
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError
from abc import ABC, abstractmethod
from typing import Self, List, Dict, Set

class FractionProfile(object):
    
    def __init__(self, iD: str, sample_information: Dict[str, str], sampleData: Dict[str, float]):

        self.iD: str = iD  # string from regular expression that contains all key information and is unique
        self.information: Dict[
            str, str] = sample_information  # dictionary which includes all parameters such as treatment, etc.
        self.sampleData: Dict[
            str, float] = sampleData  # keys are the fractions and values float values with protein levels
    
    @classmethod
    def objectify_w_profile(cls, profile: 'Profile', deep_copy: bool = False) -> Self: 
        # ToDo if deep_copy: copy.deepcopy(original) 
        
        if not profile: 
             raise EmptyProfileError
                
        return cls(profile.iD, profile.information, profile.sampleData)
    
    @classmethod
    def objectify_w_profiles(cls, profiles: List['Profile'], deep_copy: bool = False) -> List[Self]: 
        # To Do deepcopy
        return [cls(profile.iD, profile.information, profile.sampleData) for profile in profiles]
        
    @classmethod
    def objectify_w_csv(cls, path)-> Self: 
        # pipeline ToDo
        return cls(iD, information, sampleData)
    
    def calculate_distances(self: "FractionProfile", other: List["FractionProfile"], method: str = "euclidean") -> List[float]:
        
        """
        Calculates all distances between a profile and a list of profiles. By default it computes the euclidean distance. Other measures are:
        manhattan distance, spearman and pearson distance, levenstein distance. 
        """
         
        distances = []
        
        for otherProfile in other:

            distances.append(self.calculate_distance(otherProfile, method))

        return distances


    def calculate_distance(self: "FractionProfile", other: "FractionProfile", method: str = "euclidean") -> float:

        """
        Calculates the distance between two profiles. By default it computes the euclidean distance. Other measures are:
        manhattan distance, spearman and pearson distance, levenstein distance. 
        """
        
        if not other:
            raise EmptyProfileListError
            
        method = method.lower()

        match method:
            case "euclidean":
                return self._calculate_euclidean_distance(other)
            case "manhattan":
                return self._calculate_manhattan_distance(other)
            case "spearman":
                return self._calculate_spearman(other)
            case "pearson":
                return self._calculate_pearson(other)
            case _:
                raise ProfileInvalidDistanceError

    def _calculate_euclidean_distance(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        try:
            
            for key in self.sampleData.keys():

                measure_a: float = self.sampleData.get(key)
                measure_b: float = other.sampleData.get(key)

                distance_measure += (measure_a - measure_b) ** 2
            
            distance_measure = math.sqrt(distance_measure)
            
        except UnequalFractionsError as e:
            print(f"UnequalFractionsError: {e}")

        if distance_measure < 0:
            raise ProfileNegativeDistanceError
            
        return distance_measure

    def _calculate_manhattan_distance(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        try:
            
            for key in self.sampleData.keys():
       
                measure_a: float = self.sampleData.get(key)
                measure_b: float = other.sampleData.get(key)
                    
                distance_measure += abs(measure_a - measure_b)
                    
        except UnequalFractionsError as e:
            print(f"UnequalFractionsError: {e}")
            
        if distance_measure < 0:
            raise ProfileNegativeDistanceError
            
        return distance_measure

    def _calculate_pearson(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        list1: List[float]  = list(self.sampleData.values())
        list2: List[float]  = list(other.sampleData.values())

        avg1: float  = sum(list1) / len(list1)
        avg2: float  = sum(list2) / len(list2)

        if len(list1) != len(list2):
            raise UnequalFractionsError

        numerator: float = sum(
            [(list1[i] - avg1) * (list2[i] - avg2) for i in range(len(list1))])
        denominator: float = math.sqrt(
            sum([(item - avg1) ** 2 for item in list1]) * sum([(item - avg2) ** 2 for item in list2]))

        if denominator == 0:
            raise ZeroDivisionError
            
        distance_measure: float = numerator / denominator
        
        if distance_measure < 0:
            raise ProfileNegativeDistanceError
            
        return distance_measure

    def _calculate_spearman(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0
        list1: List[float] = sorted(list(self.sampleData.values()))
        list2: List[float] = sorted(list(other.sampleData.values()))

        if len(list1) != len(list2):
            raise UnequalFractionsError

        d_squared:  List[float] = [(val1 - val2) ** 2 for val1, val2 in zip(list1, list2)]
        n: int = len(list1)

        distance_measure: float = (6 * sum(d_squared)) / (n * (n ** 2 - 1))
        
        if distance_measure < 0:
            raise ProfileNegativeDistanceError
            
        return distance_measure

    @deprecated
    def plotter(self):

        # Create the plot
        plt.figure(figsize=(10, 6))  # Set the figure size
        plt.plot(self.sampleData.keys(), self.sampleData.values(), '-o', markersize=10, markerfacecolor='blue',
                 markeredgecolor='black', linewidth=2)  # Plot lines and circles

        # Customizing the plot
        plt.title("Sample: {}".format(self.iD))  # Title
        plt.xlabel('Fractions')  # X-axis label
        plt.ylabel('Protein Concentration')  # Y-axis label

        # Display the plot
        plt.show()

    # function replaced with objectify_w_profile   
    @deprecated
    @staticmethod
    def generate_Profiles(raw_data: List[Dict]) -> List["FractionProfile"]:

        """
        Function to create FractionProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of FractionProfiles:
        """
        
        # raise an error if user passes an empty list
        if not raw_data: 
            raise EmptyProfileListError
        
        array_fraction_profiles: List[Dict] = [None for _ in range(len(raw_data))]

        for index, data_point in enumerate(raw_data):
            array_fraction_profiles[index] = FractionProfile(*data_point)
            
        return array_fraction_profiles