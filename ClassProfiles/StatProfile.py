from .FractionProfile import FractionProfile, FractionProfileError

class StatProfile(FractionProfile):
    
    def __init__(self, profiles: list[FractionProfile], fractions: set[str]):

        # maybe a list of profiles is the easiest to implement and handle
        self.numberProfiles: int = len(profiles)
        self.profiles: list[FractionProfile] = profiles
        self.profileSampleData: list[list[float]] = [
            list(profile.sampleData.values()) for profile in self.profiles]
        # self.total_n_numbers = sum of all n_number from profiles

        # set of strings
        self.fractions: set[str] = fractions

        # uses dictionaries instead of np.arrays
        self.mean: dict[str, float] = self._get_mean()
        self.median: dict[str, float] = self._get_median()
        self.std: dict[str, float] = self._get_std()
    
    def _get_mean(self):

        self.mean: dict[str, float] = {}

        for fraction in self.fractions:
            self.mean[fraction]: float = 0

            try:
                for profile in self.profiles:
                    self.mean[fraction] += profile.sampleData[fraction]

                self.mean[fraction] /= self.numberProfiles

            except KeyError:
                print("fraction does not exist across all samples")

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

            except KeyError:
                print("fraction does not exist across all samples")

        return self.median

    def _get_std(self):

        self.std: dict[str, float] = {}

        for fraction in self.fractions:

            self.std[fraction]: float = 0

            try:
                for profile in self.profiles:
                    self.std[fraction] += (profile.sampleData[fraction] - self.mean[fraction]) ** 2

                self.std[fraction] /= self.numberProfiles

            except KeyError:
                print("fraction does not exist across all samples")

        return self.std