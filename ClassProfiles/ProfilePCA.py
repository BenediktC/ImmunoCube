from .FractionProfile import FractionProfile
from .StatProfile import StatProfile
from sklearn.decomposition import PCA


class ProfilePCA(object):

    def __init__(self, no_components: int, profiles: list[FractionProfile]):
        self.data_pca = self._calculate_pca(no_components, profiles)

    def _calculate_pca(self, no_components: int, profiles):
        # check whether number principle components not bigger than number of samples
        assert no_components <= len(
            profiles), "More dimension than samples. The StatProfile contains {} profiles currently.".format(
            self.numberProfiles)

        # perform PCA
        pca = PCA(no_components)
        data_samples = [list(profile.sampleData.values()) for profile in profiles]
        print(data_samples)
        data_pca = pca.fit_transform(data_samples)

        # accessing PCA attributes
        self.explained_variance = pca.explained_variance_
        self.explained_variance_ratio = pca.explained_variance_ratio_
        self.singular_values = pca.singular_values_
        self.components = pca.components_
        self.mean = pca.mean_
        self.n_components = pca.n_components_
        self.noise_variance = pca.noise_variance_

        return data_pca

    def get_pc(self,
               no_pcs: int) -> "numpy.ndarray":  # I don't use numpy directly but this is how PCA is implemented in Python
        return self.n_components[:no_pcs]