# -*- coding: utf-8 -*-
"""
This file takes as input an array of (PUF x row values x column values) data and writes a text file summarising the number of passes of the 
appropriate tests for a pre-chosen p-value. The array must be saved in the same folder as an np array. For more detailed results, the file
"Randomness_Tests" has a method to obtain the p-values directly.
"""
import numpy as np
from Paper_submission_code.Inter_Array_FHD import *
from Paper_submission_code.Randomness_Tests import *
from Paper_submission_code.Data_Formatting import *
from Paper_submission_code.chi_sq_testing_paper import *

key_lengths = [2 ** i for i in range(5, 11)]
fhds = [0 for _ in key_lengths]

for i, kl in enumerate(key_lengths):
    #%%User Input Choices
    #data input file, results output file, 
    type = "3D"
    data_file_name = f"inputs/keys_{type}_{kl}.txt"
    results_file_name = f"output_{type}_{kl}.txt"
    #block size choices b1 and b2; relatively safe to leave these as 4.
    b1 = 4
    b2 = 4

    #%%hardcode chosen p-value parameters
    p_value = 0.01

    #%%Put the data you want here
    data = np.loadtxt(data_file_name, dtype=str)
    data = np.array([Data_formatting.string_to_array(b) for b in data])
    # file = open(data_file_name, "rb")
    # data = np.load(file, allow_pickle = True)

    #extract some helpful parameters
    number_of_devices = len(data)

    #%%
    #stage 2: run the tests, output results. Occasionally prints a progress update, as the functions can be slow on large datasets and are not optimized.
    FHD_scores = FHD.FHD_values_serializer(data)
    #%%Collate pass-fail scores
    FHD_pass_fails = (FHD_scores > p_value).sum()
    fhds[i] = FHD_pass_fails
    print("Progress Update: FHD test computed")
    #stage 3: compile the results in an output .txt

    results_file = open(results_file_name, "a")

    results_file.write("There were %s devices in the dataset \n" % number_of_devices)
    results_file.write("The p-value for tests was %s" % p_value)
    results_file.write("\n")
    #start adding things one by one. Start with Uniqueness; FHD
    results_file.write(f"FHD Test: {FHD_pass_fails} devices out of {number_of_devices} passed \n")
    results_file.write("\n")
    results_file.write("The p-values are written as arrays by Main for more information e.g. for running tests for uniformity")
    results_file.close()

    print("Results saved to", results_file_name)


from matplotlib import pyplot as plt

plt.plot(key_lengths, fhds)
plt.xlabel("Key length (bits)")
plt.ylabel("FHD Performance")
plt.show()