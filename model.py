import numpy as np
from scipy.stats import pearsonr, spearmanr, kendalltau

class CorrelationModel:
    def __init__(self):
        self.x_data = np.array([])
        self.y_data = np.array([])

    def set_data(self, x_data, y_data):
        """Установка данных"""
        self.x_data = np.array(x_data)
        self.y_data = np.array(y_data)

    def get_data(self):
        return self.x_data, self.y_data

    def calculate_correlations(self):
        if len(self.x_data) < 2 or len(self.y_data) < 2:
            raise ValueError("Недостаточно данных для рассчета (минимум 2 точки)")

        pearson_corr, pearson_p = pearsonr(self.x_data, self.y_data)
        spearman_corr, spearman_p = spearmanr(self.x_data, self.y_data)
        kendall_corr, kendall_p = kendalltau(self.x_data, self.y_data)


        return {
            "pearson": (pearson_corr, pearson_p),
            "spearman": (spearman_corr, spearman_p),
            "kendall": (kendall_corr, kendall_p),
        }       
    
    def calculate_regression_line(self):
        """Вычисление линии регересии"""
        coeffs = np.polyfit(self.x_data, self.y_data, 1)
        regression_line = np.poly1d(coeffs)
        x_range = np.linspace(min(self.x_data), max(self.x_data), 100)
        y_range = regression_line(x_range)
        return x_range, y_range
    