import numpy as np

arr256 = np.loadtxt("step256.txt", dtype=int)

arr512 = np.loadtxt("step512.txt", dtype=int)

arr1024 = np.loadtxt("step1024.txt", dtype=int)

arr2048 = np.loadtxt("step2048.txt", dtype=int)

maxValuesList = np.loadtxt("maxValuesList.txt", dtype=int)

print("256 steps\n", arr256)
print("\n512 steps\n", arr512)
print("\n1024 steps\n", arr1024)
print("\n2048 steps\n", arr2048)
print("\nmaximum values in each game\n", maxValuesList)
