import numpy as np
import re


def square(data):
    return [i ** 2 for i in data]


def fit_poly_equation(timelist, observed):
    polynomial = 2
    if len(timelist) <= 2:
        polynomial = 1
    coefs = np.polyfit(timelist, observed, polynomial)
    return coefs


def get_expected_values(self, well, x, borders) -> []:
    # Fits a 2nd degree polynomial to the original line
    # For estimating the 'y' of a given 'x'
    # x can be a list or a single element
    polynomialcoefs = fit_poly_equation(self.time[borders[0]:borders[1]],
                                        well.get_rfus()[borders[0]:borders[1]])
    if isinstance(x, float):
        x = [x]
    x2 = square(x)
    i = 0
    if len(polynomialcoefs) > 2:
        ax2 = [polynomialcoefs[i] * x for x in x2]
        i += 1
    else:
        ax2 = [0 for x in range(len(x))]
    bx = [polynomialcoefs[i] * x for x in x]
    prediction = [(a + b + polynomialcoefs[i+1]) for (a, b) in zip(ax2, bx)]
    return prediction


def get_linear_approx(x1, x2, y1, y2):
    slope = (y2 - y1) / (x2 - x1)
    yintercept = y2 - slope * x2
    return [slope, yintercept]


def get_percent_difference(self, inflections):
    relativeDifference = [abs(a[1] - b[1]) / ((a[1] + b[1]) / 2)
                          for a, b in zip(inflections, self.control.get_inflections())
                          if a[0] == b[0]]
    return [element * 100 for element in relativeDifference]


def get_derivatives(well) -> []:
    # Returns the first and second derivatives in a dictionary
    derivative = {1: smooth(np.gradient(well.get_rfus()))}
    derivative[2] = np.gradient(derivative[1])
    return derivative


def smooth(a):
    # a: NumPy 1-D array containing the data to be smoothed
    # WSZ: smoothing window size needs, which must be odd number,
    # as in the original MATLAB implementation
    windowsize = 5
    out0 = np.convolve(a, np.ones(windowsize, dtype=int), 'valid') / windowsize
    r = np.arange(1, windowsize - 1, 2)
    start = np.cumsum(a[:windowsize - 1])[::2] / r
    stop = (np.cumsum(a[:-windowsize:-1])[::2] / r)[::-1]
    return np.concatenate((start, out0, stop))

def reg_conc(item, dataset=None):
    if dataset is not None and dataset.get_metadata()['gpcr']:
        return re.match(r'(\d+(|\s|[a-z]+\/)+([a-z]+[A-Z]))', item)
    else:
        return re.match(r'(\d+(|\s|[a-z]+\/)+([a-z]+[A-Z]))', item)
