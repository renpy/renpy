# This file contains the spline motion code contributed by Aenakume, at
# http://lemmasoft.renai.us/forums/viewtopic.php?f=8&t=3977

init -1500 python:
    class _SplineInterpolator(object):

        ANCHORS = {
            'top'    : 0.0,
            'center' : 0.5,
            'bottom' : 1.0,
            'left'   : 0.0,
            'right'  : 1.0,
            }

        def __init__(self, points, anchors=(0.5, 0.5)):

            assert len(points) >= 2, "Need at least a start and end point."

            def setup_coordinate_(c):
                if len(c) == 2:
                    c += anchors
                return [ self.ANCHORS.get(i, i) for i in c ]

            self.points = []

            for p in points:
                length = len(p)

                if isinstance(p[-1], float):
                    length = len(p) - 1
                    point = [ p[-1] ]
                else:
                    length = len(p)
                    point = [ -1 ]

                self.points.append(point + [ setup_coordinate_(p[i]) for i in range(length) ])

            # Make sure start and end times are set, if not already set
            if self.points[0][0] == -1:
                self.points[0][0] = 0.0
            if self.points[-1][0] == -1:
                self.points[-1][0] = 1.0

            # Now we gotta calculate the step times that need calculating
            for start in range(1, len(self.points) - 1):
                if self.points[start][0] != -1:
                    continue

                end = start + 1

                while end < (len(self.points) - 1) and self.points[end][0] == -1:
                    end += 1

                step = (self.points[end][0] - self.points[start - 1][0]) / float(end - start + 1)

                for i in range(start, end):
                    self.points[i][0] = self.points[i - 1][0] + step

            # And finally, sort the list of points by increasing time
            self.points.sort(key=lambda a : a[0])

            self.initialized = None

        def init_values(self, sizes):
            def to_abs_(value, size):
                if isinstance(value, float):
                    return value * size
                else:
                    return value

            def coord_(c):

                if len(c) == 2:
                    c = c + (0, 0)

                return ( to_abs_(c[0], sizes[0]) - to_abs_(c[2], sizes[2]),
                         to_abs_(c[1], sizes[1]) - to_abs_(c[3], sizes[3]) )

            for p in self.points:
                for i in range(1, len(p)):
                    p[i] = coord_(p[i])

            self.initialized = sizes

        def __call__(self, t, sizes):
            # Initialize if necessary
            if not self.initialized == sizes:
                self.init_values(sizes)

            # Now we must determine which segment we are in
            for segment in range(len(self.points)):
                if self.points[segment][0] > t:
                    break

            # If this is the zeroth segment, just start at the start point
            if segment == 0:
                result = self.points[0][1]
            # If this is past the last segment, just leave it at the end point
            elif segment == len(self.points) - 1 and t > self.points[-1][0]:
                result = self.points[-1][1]
            else:
                # Scale t
                t = (t - self.points[segment - 1][0]) / (self.points[segment][0] - self.points[segment - 1][0])

            # Get start and end points
            start = self.points[segment - 1][1]
            end   = self.points[segment][1]

            # Now what kind of interpolation is it?
            if len(self.points[segment]) == 2:   # Straight line
                t_p = 1.0 - t

                result = [ t_p * start[i] + t * end[i] for i in (0,1) ]

            elif len(self.points[segment]) == 3: # Quadratic Bezier
                t_pp = (1.0 - t)**2
                t_p = 2 * t * (1.0 - t)
                t2 = t**2

                result = [ t_pp * start[i] + t_p * self.points[segment][2][i] + t2 * end[i] for i in (0,1) ]

            elif len(self.points[segment]) == 4: # Cubic Bezier
                t_ppp = (1.0 - t)**3
                t_pp = 3 * t * (1.0 - t)**2
                t_p = 3 * t**2 * (1.0 - t)
                t3 = t**3

                result = [ t_ppp * start[i] + t_pp * self.points[segment][2][i] + t_p * self.points[segment][3][i] + t3 * end[i] for i in (0,1) ]

            return ( absolute(result[0]), absolute(result[1]), 0, 0 )

    def SplineMotion(points, time, child=None, anchors=(0.5, 0.5), repeat=False, bounce=False, anim_timebase=False, style='default', time_warp=None, **properties):
        return Motion(_SplineInterpolator(points, anchors), time, child, repeat=repeat, bounce=bounce, anim_timebase=anim_timebase, style=style, time_warp=time_warp, add_sizes=True, **properties)
