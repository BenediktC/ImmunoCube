# from deprecated import deprecated
# import matplotlib.pyplot as plt
# Maybe just delete the whole function to get ride of these packages above
import math
from .DistanceError import DistanceError

class FractionProfileError(Exception):
    pass


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
                raise DistanceError # ToDo DistanceError("method XY not implemented, others methods available are:")
                # above output for end user

    def _calculate_euclidean_distance(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        for key in self.sampleData.keys():
            measure_a = self.sampleData.get(key)
            measure_b = other.sampleData.get(key)

            distance_measure += (measure_a - measure_b) ** 2

        distance_measure = math.sqrt(distance_measure)

        return distance_measure

    def _calculate_manhattan_distance(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        for key in self.sampleData.keys():
            measure_a = self.sampleData.get(key)
            measure_b = other.sampleData.get(key)

            distance_measure += abs(measure_a - measure_b)

        return distance_measure

    def _calculate_pearson(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0

        list1 = list(self.sampleData.values())
        list2 = list(other.sampleData.values())

        avg1 = sum(list1) / len(list1)
        avg2 = sum(list2) / len(list2)

        assert len(list1) == len(list2), "unequal number of fractions"

        numerator = sum(
            [(list1[i] - avg1) * (list2[i] - avg2) for i in range(len(list1))])
        denominator = math.sqrt(
            sum([(item - avg1) ** 2 for item in list1]) * sum([(item - avg2) ** 2 for item in list2]))

        assert denominator != 0, "Division by zero"
        distance_measure = numerator / denominator

        return distance_measure

    def _calculate_spearman(self: "FractionProfile", other: "FractionProfile") -> float:

        distance_measure: float = 0
        list1 = sorted(list(self.sampleData.values()))
        list2 = sorted(list(other.sampleData.values()))

        assert len(list1) == len(list2), "unequal number of fractions"

        d_squared = [(val1 - val2) ** 2 for val1, val2 in zip(list1, list2)]
        n = len(list1)

        distance_measure = (6 * sum(d_squared)) / (n * (n ** 2 - 1))

        return distance_measure

    # @deprecated
    # def plotter(self):
    #
    #     # Create the plot
    #     plt.figure(figsize=(10, 6))  # Set the figure size
    #     plt.plot(self.sampleData.keys(), self.sampleData.values(), '-o', markersize=10, markerfacecolor='blue',
    #              markeredgecolor='black', linewidth=2)  # Plot lines and circles
    #
    #     # Customizing the plot
    #     plt.title("Sample: {}".format(self.iD))  # Title
    #     plt.xlabel('Fractions')  # X-axis label
    #     plt.ylabel('Protein Concentration')  # Y-axis label
    #
    #     # Display the plot
    #     plt.show()

    @staticmethod
    def generate_FractionProfiles(profiles: list["FractionProfile"], ref_profile: "FractionProfile", logarithm=math.log) -> list["FractionProfile"]:

        """
        Function to create FractionProfiles for n number of FractionProfiles
        :param profiles array of FractionProfiles:
        :return array of FractionProfiles:
        """

        array_reference_profile: list[FractionProfile] = [None for _ in range(len(profiles))]

        for index, profile in enumerate(profiles):
            array_reference_profile[index] = FractionProfile(profile.iD, profile.information, profile.sampleData, ref_profile, logarithm)
            
        return array_reference_profile