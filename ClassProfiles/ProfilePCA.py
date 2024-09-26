from .FractionProfile import FractionProfile
from .StatProfile import StatProfile
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError, ComponentErrorPCA
from typing import Self, List, Dict, Set
import math
from deprecated import deprecated
import matplotlib.pyplot as plt


class ProfilePCA(FractionProfile):

    def __init__(self, profiles: List['Profile'], transpose: bool = False, no_components: int = 6, fractions: List[str] = None, PCA_iD: str = None, PCA_information: Dict[str,str] = None):
        
        """
        Initializes a ProfilePCA object, performing dimensionality reduction on a list of profiles.

        Args:
            profiles (List[Profile]): List of profile objects to perform PCA on.
            transpose (bool): Whether to transpose the data matrix before applying PCA. Default is False.
            This is fairly important. When set to False each PC will replace the fractions and return a matrix
            with the dimensions of (no_profiles, no_components), where the fractions are replaced with PC1, PC2, ..PCn. 
            When set to True a matrix with the dimensions (no_fractions, no_components) is created, replacing the profiles
            with the principle components.
            
            no_components (int): Number of principal components to retain. Default is 6.
            fractions (List[str]): List of fractions. If None, the fractions are taken from the first profile.
            PCA_iD (str): Optional ID for the PCA object.
            PCA_information (Dict[str, str]): Optional information dictionary for the PCA object.

        Raises:
            ComponentErrorPCA: If the number of components exceeds the number of fractions or samples.
        """
        
        # storing the profiles 
        self.profiles = profiles
        self.no_profiles = len(profiles)
        self.no_components = no_components  
        self.transpose = transpose 
        
        if fractions == None: 
            # if no fractions are specified the first profile in the list provides the default fractions
            self.fractions: List[str] = list(self.profiles[0].sampleData.keys())
        else:
            self.fractions: List[str] = fractions
                
        # check whether number principle components not bigger than number of fractions or number of samples
        if no_components > len(self.fractions):
            raise ComponentErrorPCA(f"Number of components ({no_components}) exceeds the number of fractions ({len(self.fractions)}).")
        if no_components > len(self.profiles):
            raise ComponentErrorPCA(f"Number of components ({no_components}) exceeds the number of samples ({len(self.profiles)}).")
        
        # perform PCA
        self.data_pca: 'np.array' = self._calculate_pca(self.no_components, profiles)
        
        # get PC labels 
        self.PCs: List[str] = [f"PC{i}" for i in range(1, self.no_components + 1)]
        # Assign the protein concentrations to the corresponding PCs
        self.sampleData: Dict[str, List[float]] = {PC: component for PC, component in zip(self.PCs, self.components)}
        
        # optionally, the PCA object can be assigned an ID and an information dictionary, please do not confuse this
        # with the iDs and information dictionaries of the individual profiles stored in self.profiles
        self.iD: str = PCA_iD
        self.information: Dict[str, str] = PCA_information
        
        
    def _calculate_pca(self, no_components: int, profiles) -> 'np.array':
        
        """
        Performs PCA on the provided profiles.

        Args:
            no_components (int): Number of principal components to retain.
            profiles (List[Profile]): List of profile objects to be processed.

        Returns:
            np.array: Transformed data after PCA.
        """
    
        # perform PCA
        pca = PCA(no_components)
        self.scaler = StandardScaler()
        
        data_samples: List[List[float]] = [list(profile.sampleData.values()) for profile in profiles]
        scaled_data = self.scaler.fit_transform(data_samples)    
        
        if self.transpose:
            data_pca = pca.fit_transform(scaled_data.T)
        else:
            data_pca = pca.fit_transform(scaled_data)
        
        # accessing PCA attributes
        self.explained_variance = pca.explained_variance_
        self.explained_variance_ratio = pca.explained_variance_ratio_
        self.singular_values = pca.singular_values_
        self.mean = pca.mean_
        self.components = pca.components_
        self.noise_variance = pca.noise_variance_
                
        return data_pca

    @classmethod
    def objectify_w_profile(cls, profile: 'Profile', deep_copy: bool = False) -> Self: 
        raise ProfileError("It does not make sense to create a PCA out of a single Profile.")
        
    @classmethod
    def objectify_w_profiles(cls, profiles: List['Profile'], deep_copy: bool = False, no_components: int = 5, iD: str= None, information: Dict[str,str] = None,  fractions: List[str] = None) -> Self: 
            
            # ToDo deepcopy
            if not profiles: 
                raise EmptyProfileListError
                
            return cls(profiles, no_components, information, iD, fractions)
    
    @classmethod
    def retrieve_PCA_profiles_to_objectify_downstream(cls, profile: 'Profile', deep_copy: bool = False) -> List['PseudoProfile']: 
        
        """
        Retrieves PCA-transformed profiles (as 'PseudoProfiles') to be used in downstream processes. 
        Depending on whether the PCA was transposed or not, this method exports the profiles in a consistent format.

        Args:
            profile (Profile): A profile object to use in the process (this argument may be for compatibility or downstream use).
            deep_copy (bool): If True, the profiles will be deep-copied. Default is False.

        Returns:
            List[PseudoProfile]: A list of pseudo profiles (either fraction-based or profile-based) containing profile information
            and intensity values across fractions or principal components (PCs), depending on whether the data is transposed or not.

        """
        
        PCA_profile_list: List['PseudoProfile'] = []

        if self.transpose:
            
            # For transposed data, each fraction corresponds to a row, and PCs are the columns (intensities)
            for idx, row in enumerate(self.data_pca.T):  # Transposing data to treat fractions as rows
                profile_sampleData: Dict[str, float] = {pc: intensity for pc, intensity in zip(self.PCs, row)}
                # Append the fractions and their information (like profiles) based on the transposed data
                PCA_profile_list.append([self.fractions[idx], {"info": "Fraction-based"}, profile_sampleData])
            
        else:
            for idx, row in enumerate(self.data_pca):
                
                profile_sampleData: Dict[str, float] = {fraction: intensity for fraction, intensity in zip(self.fractions, row)}
                PCA_profile_list.append([self.profiles[idx].iD, self.profiles[idx].information, profile_sampleData])
        
        return PCA_profile_list
    
    @deprecated
    def plotter(self, max_samples_to_plot=None):
        
        # Plotting each row of the data as a separate line
        plt.figure(figsize=(10, 6))  # Set the figure size
        
        if self.transpose:

            for idx, row in enumerate(self.data_pca.T[:max_samples_to_plot]):
                plt.plot(self.fractions, row, label=self.PCs[idx], marker='o')

            # Customize the plot
            plt.title('PCs Across Fractions')
            plt.xlabel('Fractions')  # X-axis label: Fractions
            plt.ylabel('Intensity')  # Y-axis label: Intensity
            plt.legend(title='PC Profiles')  # Legend with PC labels
            plt.grid(True)  # Optional: Add a grid for clarity

            # Show the plot
            plt.tight_layout()
            plt.show()
            
        else: 
        
            # Loop through the rows and plot each one
            for idx, row in enumerate(self.data_pca[:max_samples_to_plot]):
                plt.plot(self.PCs, row, label=self.profiles[idx].iD, marker='o')

            # Customize the plot
            plt.title('Profiles Across PCs')
            plt.xlabel('PC Fractions')
            plt.ylabel('Intensity')
            plt.legend(title='Sample IDs', loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0)
            plt.grid(True)  # Optional: Add a grid for clarity

            # Show the plot
            plt.tight_layout()
            plt.show()