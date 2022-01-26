# function for making dp possible

from multiprocessing import Pool

import numpy as np
from sklearn.preprocessing import MinMaxScaler

import config
from data import Original
from utils import read_csv_file, check_folder, mkdir_folder, write_pkl_file

class DiffPrivacy:
    def __init__(self,
                original,
                output_folder):

        self.original = original
        self.original_data = original.data
        self.levels = original.levels
        self.filter_category = original.filter_category

        self.output_folder = output_folder

    def get_differential_privacy_value(self, value, epsilon):

        # na 값이 포함되어 있으면 무시한다.
        if np.isnan(value) : return np.nan

        def pdf(x):
            b = 2 / (epsilon)
            c = 1 - 0.5 * (np.exp(-(value+1)/b) + np.exp(-(1 - value)/b))
            return 1 / (b * c * 2) * np.exp(-np.absolute(x - value)/b)

        elements = np.linspace(-1, 1, 10**4)
        probabilities = pdf(elements)
        probabilities /= np.sum(probabilities)

        return np.random.choice(elements, size = 1, p = probabilities).item()

    def get_discretized_value(self, value, level):

        if level == 1:
            return -1

        # precalculate all values by arr Y
        beta = (value + 1) * (level - 1) / 2
        k = np.floor(beta)
        z1 = 2 * (k + 1) / (level - 1) - 1
        z2 = 2 * k / (level - 1) - 1
        p = (level - 1) * (value + 1) / 2 - k

        # Binom function to get {0, 1} by p
        binom = lambda p_i : np.random.binomial(size = 1, n = 1, p = p_i)

        # make Z vector by choosing z1, z2 using condition vector
        Z = np.where(binom(p), z1, z2)

        return Z

    def normalize(self, data):
        """
        min max normalize
        """
        self.scaler = MinMaxScaler(feature_range=(-1,1))
        self.scaler.fit(data)
        return self.scaler.transform(data)

    def unnormalize(self, data):
        """
        unnormalized by inverse_transform
        """
        return self.scaler.inverse_transform(data)

    def save_data_to_pickle(self, data, epsilon):
        """
        save numpy ot pickle
        """
        # create folder
        if not check_folder(self.output_folder):
            mkdir_folder(self.output_folder)

        # save to pickle
        write_pkl_file(data, self.output_folder, f"{epsilon}.pkl")

    def dp(self, epsilon):
        # normalize
        data = self.normalize(self.original_data)

        # DP
        get_differential_privacy_value = np.vectorize(self.get_differential_privacy_value)
        data = get_differential_privacy_value(data, epsilon/data.shape[1])

        # DISC
        # get_discretized_value = np.vectorize(self.get_discretized_value)
        # data[:, self.filter_category] = get_discretized_value(data[:, self.filter_category], self.levels[self.filter_category])

        # unnormalize
        data = self.unnormalize(data)

        # save
        # self.save_data_to_pickle(data, epsilon)
        return data



