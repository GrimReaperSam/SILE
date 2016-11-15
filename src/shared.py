import numpy as np

# HISTOGRAMS DEFAULT SIZES
DEFAULT_1D_HISTOGRAM_NBINS = 16
DEFAULT_2D_HISTOGRAM_NBINS = 9
DEFAULT_3D_HISTOGRAM_NBINS = 15

# REFERENCE SAMPLE SIZE FOR CHARACTERISTICS COMPARISON
REFERENCE_SAMPLE_SIZE = 500

# Z-VALUES THRESHOLD UNDER WHICH A CHARACTERISTIC IS IGNORED
Z_VALUE_THRESHOLD = 15
# DELTA THRESHOLD UNDER WHICH A CHARACTERISTIC IS IGNORED
DELTA_THRESHOLD = 0.1

# COMMONLY USED VALUES FOR PLOTS
rgb_hue = np.array([[0.7624, 0.3070, 0.4123],
                    [0.7405, 0.3379, 0.2920],
                    [0.6793, 0.3876, 0.1875],
                    [0.5875, 0.4386, 0.1081],
                    [0.4727, 0.4815, 0.0911],
                    [0.3354, 0.5133, 0.1593],
                    [0.1352, 0.5341, 0.2672],
                    [0, 0.5452, 0.3934],
                    [0, 0.5477, 0.5255],
                    [0, 0.5415, 0.6477],
                    [0, 0.5253, 0.7425],
                    [0, 0.4970, 0.7949],
                    [0.3483, 0.4560, 0.7964],
                    [0.5355, 0.4044, 0.7473],
                    [0.6626, 0.3509, 0.6564],
                    [0.7377, 0.3120, 0.5389]])

rgb_chroma = np.array([[0.4663, 0.4664, 0.4663],
                       [0.5021, 0.4544, 0.4672],
                       [0.5362, 0.4416, 0.4681],
                       [0.5689, 0.4278, 0.4690],
                       [0.6004, 0.4129, 0.4700],
                       [0.6309, 0.3967, 0.4710],
                       [0.6606, 0.3791, 0.4720],
                       [0.6896, 0.3598, 0.4730],
                       [0.7180, 0.3383, 0.4741],
                       [0.7458, 0.3143, 0.4752],
                       [0.7733, 0.2870, 0.4764],
                       [0.8003, 0.2552, 0.4775],
                       [0.8270, 0.2166, 0.4788],
                       [0.8534, 0.1666, 0.4800],
                       [0.8795, 0.0881, 0.4813],
                       [0.9054, 0, 0.4826]])
