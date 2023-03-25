#cython: profile=False
# Copyright 2004-2023 Tom Rothamel <pytom@bishoujo.us>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from __future__ import print_function

import math

def euler_slerp(complete, old, new):
    """
    Use quaternions to interpolate between two euler angles.
    """

    if old == new:
        return new

    #select the shorten root
    old_x, old_y, old_z = old
    old_x = old_x % 360
    old_y = old_y % 360
    old_z = old_z % 360
    new_x, new_y, new_z = new
    new_x = new_x % 360
    new_y = new_y % 360
    new_z = new_z % 360
    if new_x - old_x > 180:
        new_x = new_x - 360
    if new_y - old_y > 180:
        new_y = new_y - 360
    if new_z - old_z > 180:
        new_z = new_z - 360


    #z-y-x Euler angles to quaternion conversion
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    old_x_div_2 = math.radians(old_x) * 0.5
    old_y_div_2 = math.radians(old_y) * 0.5
    old_z_div_2 = math.radians(old_z) * 0.5
    cx = math.cos(old_x_div_2)
    sx = math.sin(old_x_div_2)
    cy = math.cos(old_y_div_2)
    sy = math.sin(old_y_div_2)
    cz = math.cos(old_z_div_2)
    sz = math.sin(old_z_div_2)

    old_q_x = sx * cy * cz - cx * sy * sz
    old_q_y = cx * sy * cz + sx * cy * sz
    old_q_z = cx * cy * sz - sx * sy * cz
    old_q_w = cx * cy * cz + sx * sy * sz

    new_x_div_2 = math.radians(new_x) * 0.5
    new_y_div_2 = math.radians(new_y) * 0.5
    new_z_div_2 = math.radians(new_z) * 0.5
    cx = math.cos(new_x_div_2)
    sx = math.sin(new_x_div_2)
    cy = math.cos(new_y_div_2)
    sy = math.sin(new_y_div_2)
    cz = math.cos(new_z_div_2)
    sz = math.sin(new_z_div_2)

    new_q_x = sx * cy * cz - cx * sy * sz
    new_q_y = cx * sy * cz + sx * cy * sz
    new_q_z = cx * cy * sz - sx * sy * cz
    new_q_w = cx * cy * cz + sx * sy * sz


    #calculate new quaternion between old and new.
    old_q_mul_new_q = (old_q_x * new_q_x + old_q_y * new_q_y + old_q_z * new_q_z + old_q_w * new_q_w)
    dot = old_q_mul_new_q
    if dot > 1.0:
        dot = 1.0
    elif dot < -1.0:
        dot = -1.0
    theta = abs(math.acos(dot))

    st = math.sin(theta)

    sut = math.sin(theta * complete)
    sout = math.sin(theta * (1 - complete))

    coeff1 = sout / st
    coeff2 = sut / st

    q_x = coeff1 * old_q_x + coeff2 * new_q_x
    q_y = coeff1 * old_q_y + coeff2 * new_q_y
    q_z = coeff1 * old_q_z + coeff2 * new_q_z
    q_w = coeff1 * old_q_w + coeff2 * new_q_w


    #Quaternion to z-y-x Euler angles conversion
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    sinx_cosp = 2 * (q_w * q_x + q_y * q_z)
    cosx_cosp = 1 - 2 * (q_x * q_x + q_y * q_y)
    siny = 2 * (q_w * q_y - q_z * q_x)
    sinz_cosp1 = 2 * (q_x * q_y - q_w * q_z)
    cosz_cosp1 = 1 - 2 * (q_x * q_x + q_z * q_z)
    sinz_cosp2 = 2 * (q_w * q_z + q_x * q_y)
    cosz_cosp2 = 1 - 2 * (q_y * q_y + q_z * q_z)

    if siny >= 1:
        x = 0
        y = math.pi/2
        z = math.atan2(sinz_cosp1, cosz_cosp1)
    elif siny <= -1:
        x = 0
        y = -math.pi/2
        z = math.atan2(sinz_cosp1, cosz_cosp1)
    else:
        x = math.atan2(sinx_cosp, cosx_cosp)
        if siny > 1.0:
            siny = 1.0
        elif siny < -1.0:
            siny = -1.0
        y = math.asin(siny)
        z = math.atan2(sinz_cosp2, cosz_cosp2)
    x = math.degrees(x) % 360
    y = math.degrees(y) % 360
    z = math.degrees(z) % 360

    return (x, y, z)
