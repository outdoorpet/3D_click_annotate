import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import numpy as np


def visualize3DData(X, annotes):
    """Visualize data in 3d plot with popover next to mouse click (middle button) position.
    
    Modified from DonCristobal's Answer on StackOverflow:
    http://stackoverflow.com/questions/10374930/matplotlib-annotating-a-3d-scatter-plot

    Args:
        X (np.array) - array of points, of shape (numPoints, 3)
        annotes - list of length (numPoints) of user defined annotes
    Returns:
        None
    """
    fig = plt.figure(figsize=(16, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(X[:, 0], X[:, 1], X[:, 2], depthshade=False, picker=True)

    def distance(point, event):
        """Return distance between mouse position and given data point

        Args:
            point (np.array): np.array of shape (3,), with x,y,z in data coords
            event (MouseEvent): mouse event (which contains mouse position in .x and .xdata)
        Returns:
            distance (np.float64): distance (in screen coords) between mouse pos and data point
        """
        assert point.shape == (3,), "distance: point.shape is wrong: %s, must be (3,)" % point.shape

        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(point[0], point[1], point[2], plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = ax.transData.transform((x2, y2))

        return np.sqrt((x3 - event.x) ** 2 + (y3 - event.y) ** 2)

    def calcClosestDatapoint(X, event):
        """"Calculate which data point is closest to the mouse position.

        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            event (MouseEvent) - mouse event (containing mouse position)
        Returns:
            smallestIndex (int) - the index (into the array of points X) of the element closest to the mouse position
        """
        distances = [distance(X[i, 0:3], event) for i in range(X.shape[0])]
        return np.argmin(distances)

    def annotatePlot(X, index, annotes, button):
        """Create popover label in 3d chart

        Args:
            X (np.array) - array of points, of shape (numPoints, 3)
            index (int) - index (into points array X) of item which should be printed
        Returns:
            None
        """
        # If we have previously displayed another label, remove it first
        if hasattr(annotatePlot, 'label'):
            annotatePlot.label.remove()

        if button == 2:
            # Get data point from array of points X, at position index
            x2, y2, _ = proj3d.proj_transform(X[index, 0], X[index, 1], X[index, 2], ax.get_proj())

            annote = annotes[index]

            annotatePlot.label = plt.annotate(annote,
                                              xy=(x2, y2), xytext=(-20, 20), textcoords='offset points', ha='right',
                                              va='bottom',
                                              bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                                              arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        # if we press another button (i.e. to pan the axis we need to create a dummy (blank) annotate
        # this is because the annotePlot still has an attribute (it has previously been called
        elif button != 2:
            annotatePlot.label = plt.annotate('', xy=(0, 0), xytext=(0, 0))

        fig.canvas.draw()

    def onMouseClick(event):
        """Event that is triggered when mouse is clicked. Shows text
        annotation over data point closest to mouse click."""
        closestIndex = calcClosestDatapoint(X, event)
        annotatePlot(X, closestIndex, annotes, event.button)

    fig.canvas.mpl_connect('button_press_event', onMouseClick)  # on mouse click
    plt.show()
