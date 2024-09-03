# from deprecated import deprecated
# import matplotlib.pyplot as plt

import math
import matplotlib.pyplot as plt
from deprecated import deprecated
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError

class FractionProfile(object):

    def __init__(self, iD: str, sample_information: dict[str], sampleData: dict[str, float]):

        self.iD: str = iD  # string from regular expression that contains all key information and is unique
        self.information: dict[
            str] = sample_information  # dictionary which includes all parameters such as treatment, etc.
        self.sampleData: dict[
            str, float] = sampleData  # keys are the fractions and values float values with protein levels

    def calculate_distances(self: "FractionProfile", other: list["FractionProfile"], method: str = "euclidean") -> list[float]:
        
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
        manhattan distance, spearman and pearson distance, levenstein distance. # ToDo check whether this contains all measurements
        """

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

        list1: list[float]  = list(self.sampleData.values())
        list2: list[float]  = list(other.sampleData.values())

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
        list1: list[float] = sorted(list(self.sampleData.values()))
        list2: list[float] = sorted(list(other.sampleData.values()))

        if len(list1) != len(list2):
            raise UnequalFractionsError

        d_squared:  list[float] = [(val1 - val2) ** 2 for val1, val2 in zip(list1, list2)]
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

    
    @staticmethod
    def generate_FractionProfiles(raw_data: list[dict]) -> list["FractionProfile"]:

        """
        Function to create FractionProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of FractionProfiles:
        """
        
        # raise an error if user passes an empty list
        if raw_data == None: 
            raise EmptyProfileListError
        
        array_fraction_profiles: list[dict] = [None for _ in range(len(raw_data))]

        for index, data_point in enumerate(raw_data):
            array_fraction_profiles[index] = FractionProfile(*data_point)
            
        return array_fraction_profiles