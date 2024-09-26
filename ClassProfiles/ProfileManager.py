from deprecated import deprecated
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Self, List, Dict, Set
from .ProfileErrors import ProfileError, ProfileNegativeDistanceError, ProfileInvalidDistanceError, FractionZeroDivisionError, UnequalFractionsError, ZeroSumError, EmptyProfileListError, ProfileNotFoundError, EmptyProfileError

class ProfileManager(object):
    
    def __init__(self) -> None:
        
        # idea: to avoid profiles sharing the same idea raise error -> if len(set([profile.iD for profile in profiles])) != len(profiles)
        # that line would detect duplicates

        pass
        
    @staticmethod    
    def retrieve_profile_by_iD(profile_list: List['Profile'], profile_iD: str) -> List['Profile']:
        
        '''
        takes a list of profiles as input and returns corresponding profile with matching ID.
        Note, every profile should have a different ID. If two profiles have the same ID it only returns the first profile.
        '''
        
        for profile in profile_list:
            if profile.iD == profile_iD: return profile
            
        raise ProfileNotFoundError
    
    @staticmethod    
    def retrieve_profile_by_iDs(profile_list: List['Profile'], profile_iDs: List[str]) -> List['Profile']:
        return [ProfileManager.retrieve_profile_by_iD(profile_list, profile_iD) for profile_iD in profile_iDs]
    
    @staticmethod
    def remove_profile_by_iD(profile_list: List['Profile'], profile_iD: str) -> List['Profile']:
        '''
        deletes profiles by their ID from the input list.
        '''
        copy_profile_list = profile_list.copy()
        
        for profile in copy_profile_list:
            if profile.iD == profile_iD:
                copy_profile_list.remove(profile)
                return copy_profile_list
            
        raise ProfileNotFoundError # optional, really necessary?
        
    @staticmethod
    def remove_profile_by_iDs(profile_list: List['Profile'], profile_iDs: List[str]) -> List['Profile']:
        '''
        takes a list of profiles as input and returns a sublist that does not contain the specified IDs.
        '''
        sub_set = set(profile_iDs)
        
        # optionallly raise error if not all profiles to delete were in data
        # Find the overlap (intersection) between the profile_list and the sub set
        overlap = len([profile for profile in profile_list if profile.iD in sub_set])

        # If there is no overlap, raise an error
        if overlap < len(sub_set):
            raise ValueError("No overlap between the large list and the small list")

        # Subtract the smaller list from the larger list
        ouput = [profile for profile in profile_list if profile.iD not in sub_set]

        return ouput

    
    @deprecated
    @staticmethod
    def plot_profiles(profile_list, title_name = None):
        '''
        takes a list of profiles and plots their intensity values for each fraction.
        '''
        plt.figure(figsize=(10, 6))  # Set the figure size

        for profile in profile_list:
            # Plot each profile's data on the same plot
            plt.plot(profile.sampleData.keys(), profile.sampleData.values(), '-o', 
                     markersize=8, markerfacecolor='blue', markeredgecolor='black', linewidth=2, label=profile.iD)

        # Customizing the plot
        if title_name:
            plt.title(title_name)
            
        plt.xlabel('Fractions')  # X-axis label
        plt.ylabel('Protein Concentration')  # Y-axis label
        plt.legend(title='Sample IDs', loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0)
        plt.grid(True)  # Optionally, add a grid for better readability

        # Display the plot
        plt.show()
    
    @staticmethod
    def get_distance_matrix(profiles_row_axis: List['Profile'], profiles_column_axis: List['Profile'], distance_method: str = "euclidean") -> np.ndarray:        
        
        '''
        Calculates a distance matrix for two lists of profiles. 
        User can specify the distance measurement, default euclidean.
        Returns a distance matrix, along with the column and row labels for downstream plotting/analysis.
        '''
        
        distance_matrix = np.zeros((len(profiles_row_axis), len(profiles_column_axis)))
        
        for i, row_profile in enumerate(profiles_row_axis):
            
            # Calculate the distance between profile_x and each profile in profiles_y_axis
            distances = row_profile.calculate_distances(profiles_column_axis, distance_method)

            # Fill the i-th row of the matrix with the calculated distances
            distance_matrix[i, :] = distances
            
        row_labels = [profile.iD for profile in profiles_row_axis]
        column_labels = [profile.iD for profile in profiles_column_axis]
        
        return distance_matrix, row_labels, column_labels 
    
    
    def retrieve_single_query(search_list: List["Profiles"], keyword: str, target_value: str) -> List['Profiles']:
        
        '''
        Helper function to search a list of profiles for a specific characteristic in their profile.information dictionary.
        Used in the function where several search queries are run for multiple characteristics.
        '''
        
        # init the output list
        return_list: List['Profile'] = []
                
        # iterate through all profiles that are left after each round
        for profile in search_list:
            if profile.information[keyword] == target_value:
                return_list.append(profile)
        
        return return_list
    
    def AND_operator_retrieve_by_profile_information(search_list: List['Profile'], search_query: Dict[str, str]):
        
        '''
        Performs a search query for multiple conditions for the AND operator. 
        The profiles must meet all requirements to be returned to the user.
        '''
        
        # iterating through all conditions
        for keyword, target_value in search_query.items():

            # checks whether query is a list of queries, e.g. "PG" (Proteine Group) = [Protein_A, Protein_B]
            if isinstance(target_value, list):
                for value in target_value:
                    
                    # return the profiles that met filter criteria
                    out_list = ProfileManager.retrieve_single_query(search_list, keyword, value)

                    # if no profile meets the condition, raise an error
                    if not out_list: raise ProfileNotFoundError

                    # update the search list to only include profiles that passed previous filter
                    search_list = out_list.copy()

            # if query is a single element, e.g. "PG" (Protein Group) = Protein_A
            else:

                # return the profiles that met filter criteria
                out_list = ProfileManager.retrieve_single_query(search_list, keyword, target_value)
                
                # update the search list to only include profiles that passed previous filter
                search_list = out_list.copy()

                # if no profile meets the condition, raise an error
                if not out_list: raise ProfileNotFoundError

                # update the search list to only include profiles that passed previous filter
                search_list = out_list.copy()

        # return profiles
        return out_list
    
    def OR_operator_retrieve_by_profile_information(search_list: List['Profiles'], search_query: Dict[str, str]) -> Set['Profiles']:
        
        '''
        Performs a search query for multiple conditions for the OR operator. 
        The profiles must meet only one criterion to be returned to the user.
        '''
        
        # Initialize an empty set to store profiles that match any condition.
        # A set is used to ensure uniqueness (no duplicate profiles).
        out_set: Set['Profile'] = set()

        # Iterate over the search query, where each key-value pair represents
        # a search criterion (keyword: target_value).
        for keyword, target_value in search_query.items():

            # If the target_value is a list, we need to check for any match
            # within that list. This allows multiple possible matches for a keyword.
            if isinstance(target_value, list):
                for value in target_value:

                    # Iterate over each profile in the search_list.
                    for profile in search_list:

                        # If the profile's information matches the current keyword and value,
                        # add it to the set. Using 'value' here instead of 'target_value'
                        # to check each value in the list.
                        if profile.information[keyword] == value:
                            out_set.add(profile)

            # If the target_value is not a list (i.e., it's a single value),
            # iterate through the search_list and check for matches.
            else:
                for profile in search_list:

                    # If the profile's information matches the current keyword and target_value,
                    # add it to the set.
                    if profile.information[keyword] == target_value:
                        out_set.add(profile)

        # If no profiles were added to the set, raise a ProfileNotFoundError.
        if not out_set:
            raise ProfileNotFoundError
        # Otherwise, return the set of profiles that matched any of the conditions.
        else:
            return out_set          
                
    @staticmethod                
    def retrieve_by_profile_information(profiles_list: List['Profile'], search_query: Dict[str, str], AND_Operator = True) -> List['Profile']:
        
        '''
        A search query is run on a list of profiles. The search query is a dictionary similar to the profile.information dictionary.
        The profile.information dictionaries of the list of profiles is searched for matches. The user can specify whether AND or OR 
        Operator should be used.
        '''
        try:
            
            # initialize search list
            search_list: List['Profile'] = profiles_list.copy()
            
            # if the profile must meet all query conditions
            if AND_Operator:
                return ProfileManager.AND_operator_retrieve_by_profile_information(search_list, search_query)
                
            # if the profiles only have to meet one requirement  
            else:
                return ProfileManager.OR_operator_retrieve_by_profile_information(search_list, search_query)
    
        except KeyError:
            print(f"Not a valid key. {keyword} was most likely not accounted for in the experiment")
    
    @deprecated
    @staticmethod
    def plot_heatmap(matrix, row_labels=None, column_labels=None) -> None:
        
        '''
        Function that takes a distance matrix as input and plots it as heatmap. 
        '''
        
        plt.figure(figsize=(8, 6))  # Set the figure size
        sns.heatmap(matrix, cmap='coolwarm', linewidths=0.5, 
                    xticklabels=column_labels, yticklabels=row_labels)

        # Add labels and title
        plt.title("Heatmap of Distance Matrix")
        plt.xlabel("Y Axis Profiles")
        plt.ylabel("X Axis Profiles")

        # Show the plot
        plt.show()
    
    @staticmethod
    def get_movement_matrix(matrix1, matrix2):
        return matrix2 - matrix1  
        
            
    @staticmethod
    def get_movement(matrix1, matrix2, row_labels, col_labels, target_of_interest, return_val="row"):
        
        '''
        Function that takes two distance matrices (e.g., treatment vs control distance matrix), substracts the two 
        in order to get the movement within the cells/compartments. Next, the row or column, depending on the value of 
        the return_val argument, of the target/protein of interest is selected and returned to the user along with the 
        labels for subsequent plotting.        
        '''
    
        movements = matrix2 - matrix1  

        if return_val == "row":

            index = row_labels.index(target_of_interest)
            movement_row = movements[index]
            matrix1_row = matrix1[index]
            matrix2_row = matrix2[index]

            return movement_row, matrix1_row, matrix2_row, col_labels, target_of_interest

        elif return_val == "col" or return_val == "column":

            index = col_labels.index(target_of_interest)
            movement_col = movements[:, index]
            matrix1_col = matrix1[:, index]
            matrix2_col = matrix2[:, index]

            return movement_col, matrix1_col, matrix2_col, row_labels, target_of_interest

        else:
            ValueError("accepted arguments are row, col or column")
    
    @deprecated
    @staticmethod
    def plot_movement(movement_row, row_treatment, row_untreated, y_labels, x_label):
        
        '''
        Plots the movement row of a target protein together with distance measurements for control and treatment.
        '''
        
        n_groups = len(y_labels)

        # Set the positions of the groups (reversed for horizontal plot)
        bar_positions = np.arange(n_groups)
        bar_height = 1 / n_groups

        # Create the plot
        fig, ax = plt.subplots(figsize=(6, 8))

        # Plot the categories (order reversed for horizontal plot)
        ax.barh(bar_positions, movement_row, bar_height, label="Movement", color='pink')
        ax.barh(bar_positions, row_untreated, bar_height, left=[max(move,0) for move in movement_row], label="DMSO", color='blue')
        ax.barh(bar_positions, row_treatment, bar_height, left=[max(move,0) for move in movement_row] + row_untreated, label="DIABZI", color='red')

        # Customize the plot
        ax.set_xlabel('Distance values')
        ax.set_title(f'Distances to {x_label} and movement upon treatment')
        ax.set_yticks(bar_positions)
        ax.set_yticklabels(y_labels)
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1), borderaxespad=0)
        
        # Calculate the maximum absolute value for setting x-axis limits
        max_val = max(
            abs(np.max(movement_row + row_treatment + row_untreated)), 
            abs(np.min(movement_row + row_treatment + row_untreated))
        )

        # Set x-axis limits to center the y-axis and accommodate negative values
        ax.set_xlim(-max_val, max_val)

        # Move the y-axis spine to the center (x=0)
        ax.spines['left'].set_position('center')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Show the plot
        plt.show()
    
    @deprecated # just for debugging, delete soon
    def print_profiles(self):
        print(self.profiles)