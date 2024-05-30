#cython: profile=False
# Copyright 2004-2024 Tom Rothamel <pytom@bishoujo.us>
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

from libc.math cimport sin, cos, atan2, asin, acos

DEF pi = 3.14159265358979323846

cdef double radians(double degrees):
    return degrees * pi / 180.0


cdef double degrees(double radians):
    return radians * 180.0 / pi


def euler_slerp(double complete, old, new):
    """
    Use quaternions to interpolate between two euler angles.
    """

    cdef double coeff1
    cdef double coeff2
    cdef double cosx_cosp
    cdef double cosz_cosp1
    cdef double cosz_cosp2
    cdef double cx
    cdef double cy
    cdef double cz
    cdef double dot
    cdef double new_q_w
    cdef double new_q_x
    cdef double new_q_y
    cdef double new_q_z
    cdef double new_x
    cdef double new_x_div_2
    cdef double new_y
    cdef double new_y_div_2
    cdef double new_z
    cdef double new_z_div_2
    cdef double old_q_mul_new_q
    cdef double old_q_w
    cdef double old_q_x
    cdef double old_q_y
    cdef double old_q_z
    cdef double old_x
    cdef double old_x_div_2
    cdef double old_y
    cdef double old_y_div_2
    cdef double old_z
    cdef double old_z_div_2
    cdef double q_w
    cdef double q_x
    cdef double q_y
    cdef double q_z
    cdef double sinx_cosp
    cdef double siny
    cdef double sinz_cosp1
    cdef double sinz_cosp2
    cdef double sout
    cdef double st
    cdef double sut
    cdef double sx
    cdef double sy
    cdef double sz
    cdef double theta
    cdef double x
    cdef double y
    cdef double z

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
    old_x_div_2 = radians(old_x) * 0.5
    old_y_div_2 = radians(old_y) * 0.5
    old_z_div_2 = radians(old_z) * 0.5
    cx = cos(old_x_div_2)
    sx = sin(old_x_div_2)
    cy = cos(old_y_div_2)
    sy = sin(old_y_div_2)
    cz = cos(old_z_div_2)
    sz = sin(old_z_div_2)

    old_q_x = sx * cy * cz - cx * sy * sz
    old_q_y = cx * sy * cz + sx * cy * sz
    old_q_z = cx * cy * sz - sx * sy * cz
    old_q_w = cx * cy * cz + sx * sy * sz

    new_x_div_2 = radians(new_x) * 0.5
    new_y_div_2 = radians(new_y) * 0.5
    new_z_div_2 = radians(new_z) * 0.5
    cx = cos(new_x_div_2)
    sx = sin(new_x_div_2)
    cy = cos(new_y_div_2)
    sy = sin(new_y_div_2)
    cz = cos(new_z_div_2)
    sz = sin(new_z_div_2)

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
    theta = abs(acos(dot))

    st = sin(theta)

    if st == 0:
        return new

    sut = sin(theta * complete)
    sout = sin(theta * (1 - complete))

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
        y = pi/2
        z = atan2(sinz_cosp1, cosz_cosp1)
    elif siny <= -1:
        x = 0
        y = -pi/2
        z = atan2(sinz_cosp1, cosz_cosp1)
    else:
        x = atan2(sinx_cosp, cosx_cosp)
        if siny > 1.0:
            siny = 1.0
        elif siny < -1.0:
            siny = -1.0
        y = asin(siny)
        z = atan2(sinz_cosp2, cosz_cosp2)
    x = degrees(x) % 360
    y = degrees(y) % 360
    z = degrees(z) % 360

    return (x, y, z)
