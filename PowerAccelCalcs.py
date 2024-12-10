import numpy as np
import math
from cmath import sqrt
from tkinter import Frame
import pandas as pd
import fnmatch
import os

# internal functions

def is_right(a, x):
    if a > 0:
        x = x*-1
        return x
    else:
        return x

def is_left(a, x):
    if a < 0:
        x = x*-1
        return x
    else:
        return x

def unit_vector(v):
    return v / np.linalg.norm(v)

def magnitude(v):
    return math.sqrt(sum(pow(element, 2) for element in v))

# trans_global(v, x, y, z): transforms a vector (v) into the same vector in a passively rotated coordinate system
# v = vector to paasively rotate, must be defined as a 1x3 column (vertical) matrix
# x = angle of rotation about the x axis to transform local coordinates into global coordinates (in degrees)
# y = angle of rotation about the y axis to transform local coordinates into global coordinates (in degrees)
# z = angle of rotation about the z axis to transform local coordinates into global coordinates (in degrees)

def trans_global(v, x, y, z):

    # apply three rotations to vector x y z accels, one for each of the global angel transformations

    # Below is no longer needed after making this its own function
    # x = # accel in X
    # y = # accel in y
    # z = # accel in Z

    # Note that the vector passed to this function still needs to be a column matrix as below
    # v = np.array([[x],
    #               [y],
    #               [z]])

    # apply first passive rotation about X

    xr = math.radians(x) # degrees of rotation about x axis converted to radians (from global angles)

    xa = abs(xr)

    # build rotation matrix for x

    mrx = np.array([[1, 0, 0],
                    [0, math.cos(xa), is_right(xr, math.sin(abs(xr)))],
                    [0, is_left(xr, math.sin(abs(xr))), math.cos(xa)]])

    # perform rotation

    v = np.matmul(mrx, v)

    # apply next passive rotation about Y

    yr = math.radians(y) # degrees of rotation about y axis converted to radians (from global angles)

    ya = abs(yr)

    # build rotation matrix for y

    mry = np.array([[math.cos(ya), 0, is_left(yr, math.sin(abs(yr)))],
                    [0, 1, 0],
                    [is_right(yr, math.sin(abs(yr))), 0, math.cos(ya)]])

    # perform rotation

    v = np.matmul(mry, v)

    # apply last passive rotation about Z

    zr = math.radians(z) # degrees of rotation about z axis converted to radians (from global angles)

    za = abs(zr)

    # build rotation matrix for z

    mrz = np.array([[math.cos(za), is_right(zr, math.sin(abs(zr))), 0],
                    [is_left(zr, math.sin(abs(zr))), math.cos(za), 0],
                    [0, 0, 1]])

    # perform rotation

    v = np.matmul(mrz, v)

    return v

def trans_global_alt(v, x, y, z):

    # apply three rotations to vector x y z accels, one for each of the global angel transformations

    # Below is no longer needed after making this its own function
    # x = # accel in X
    # y = # accel in y
    # z = # accel in Z

    # Note that the vector passed to this function still needs to be a column matrix as below
    # v = np.array([[x],
    #               [y],
    #               [z]])

    # apply first passive rotation about Y

    yr = math.radians(y) # degrees of rotation about y axis converted to radians (from global angles)

    ya = abs(yr)

    # build rotation matrix for y

    mry = np.array([[math.cos(ya), 0, is_left(yr, math.sin(abs(yr)))],
                    [0, 1, 0],
                    [is_right(yr, math.sin(abs(yr))), 0, math.cos(ya)]])

    # perform rotation

    v = np.matmul(mry, v)

    # apply next passive rotation about Z

    zr = math.radians(z) # degrees of rotation about z axis converted to radians (from global angles)

    za = abs(zr)

    # build rotation matrix for z

    mrz = np.array([[math.cos(za), is_right(zr, math.sin(abs(zr))), 0],
                    [is_left(zr, math.sin(abs(zr))), math.cos(za), 0],
                    [0, 0, 1]])

    # perform rotation

    v = np.matmul(mrz, v)

    # apply last passive rotation about X

    xr = math.radians(x) # degrees of rotation about x axis converted to radians (from global angles)

    xa = abs(xr)
    
    # build rotation matrix for x

    mrx = np.array([[1, 0, 0],
                    [0, math.cos(xa), is_right(xr, math.sin(abs(xr)))],
                    [0, is_left(xr, math.sin(abs(xr))), math.cos(xa)]])

    # perform rotation

    v = np.matmul(mrx, v)

    return v

# minus_g(v): subtracts the correct acceleration due to gravity from a global vector and returns the transformed vector
# v = global acceleration vector to transform by removing acceleration due to gravity

def minus_g(v):

    # get acceleration due to gravity at the given sampling rate

    g = np.array([[0],
                  [0],
                  [9.80665]])

    v = v - g
    
    return v

# angle_between(v, d): finds the angle between two vectors v and d
# v: first vector to find the angle between, will flatten vector, so you can use a column vector
# d: second vector to find the angle between, will flatten vector, so you can use a column vector

def angle_between(v, d):

    # flatten arrays to make this work

    v = v.flatten(order='C')
    d = d.flatten(order='C')
    
    # transform each vector to unit vectors and find the angle between them

    v_u = unit_vector(v)
    d_u = unit_vector(d)
    return np.arccos(np.clip(np.dot(v_u, d_u), -1.0, 1.0))

# outcome_mag(v, a): computes the scalar projection of vector v to find its component magnitude in the direction of a second vector, where a is the angle between the vectors
# v = original vector to perform scalar projection on
# a = angle between v and vector you would like to know magnitude in the direction of

def outcome_mag(v, a):

    m = magnitude(v)

    return m*math.cos(a)

# Process for calculating outcome variables

    # 1) Identify sample range for the first 50% and the full throw (50% range of samples will be used later and full throw will be used for average power and velocity calcs)
    # 2) Find the midpoint (m) of the first 50% of samples
    # 3) Find the directional vector (dv) for the throw by running trans_global and minus_g on the vector at m, we will transform in the direction of this vector in subsequent steps - maybe average a few samples before and after to control for wobble, could even average the direction vectors for the full 50%
    # 4) Compute the global vector (v) for each sample by applying trans_global and minus_g to the local vector, store vectors in data frame
    # 5) For each global vector (v) in the df, find the angle between v and dv (a) with angle_between, set angle a into df
    # 6) Find the magnitude of global vector (v) in the direction of dv by applying ||v||*cos(a) via the outcome_mag function
    # 7) Now you have all your accelerations in the direction of movement and it is just basic algebra going forward to get velocity for each acceleration
    # 8) Then simply a*(mass of the ball)*v will yield instant power for each sample

# Jordan IMU validation

# ebonfowl: import csv
os.chdir(os.path.dirname(os.path.abspath(__file__)))
mydata = pd.read_csv("Tendo validation throw 3.csv")

# ebonfowl: add ID column
mydata["ID"] = mydata.index + 1

i = 0
n = mydata['ID'].max()

while i < n:

    ax = mydata.at[i, "ax_m/s/s"]
    ay = mydata.at[i, "ay_m/s/s"]
    az = mydata.at[i, "az_m/s/s"]

    # I have mixed these up to account for which axis is actually being rotated about based on the IMU app description
    x = mydata.at[i, "z_deg"]
    y = mydata.at[i, "x_deg"]
    z = mydata.at[i, "y_deg"]

    v = np.array([[ax],
                  [ay],
                  [az]])
    
    b = trans_global(v, x, y, z)

    #b = minus_g(b)

    if i == 0:
        print(b)

    gax = b[0,0]
    mydata.at[i, "glb_ax"] = gax

    gay = b[1,0]
    mydata.at[i, "glb_ay"] = gay

    gaz = b[2,0]
    mydata.at[i, "glb_az"] = gaz

    # ebonfowl: get resultant for all global vectors and toss in frame

    gres = magnitude(b)
    mydata.at[i, "glb_res"] = gres

    i += 1

print(mydata)

mydata.to_csv('glb_vector.csv')

# q = minus_g(b)

# print(q)

# print(magnitude(b))

# print(magnitude(q))
