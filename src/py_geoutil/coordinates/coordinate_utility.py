import numpy as np
from numbers import Integral, Real
from ..utils.validation import validate_type, validate_positive, validate_required

def pythagoras_calc(Xone=None,Xtwo=None,Yone=None, Ytwo=None):
    '''
    Calculates distance between 2 xy coordinate pairs

    Xone (Float): x coordinate of first pair 
    Yone (Float): y coordinate of first pair 
    Xtwo (Float): x coordinate of second pair 
    Ytwo (Float): y coordinate of second pair 
    Raises: None
    
    K Jaggs June 2026
    '''
    return (((Xone-Xtwo)**2) + ((Yone-Ytwo)**2))**0.5

def corner_points_from_origin(n_col=None,n_row=None,dx=None,dy=None,angle=None,x0=None,y0=None):
    """
    Create the four corner points and Shapely polygon
    for a rotated IRAP Classic grid.

    Parameters
    ----------
    n_col : int Number of columns.
    n_row : int Number of rows.
    dx : float Grid spacing in column direction.
    dy : float Grid spacing in row direction.
    angle : float Grid rotation in degrees. rotation angle is measured counter-clockwise from the positive X axis (East) to the grid I/column direction.
    x0, y0 : float Grid origin.

    Returns
    -------
    corners : np.ndarray Four corner coordinates, shape (4, 2).
   

    Raises:
    -------
    ValidationError if any required inputs are empty
    ValidationError if any of the inputs are not in the coorect format
    ValidationError coords and number of points are not positive

    PRECONDITIONS: supplied grid geometry is correct
    KJAGGS Sep 2026
    """

    validate_required(n_col=n_col,n_row=n_row,dx=dx,dy=dy,angle=angle,x0=x0,y0=y0)

    # Types
    validate_type(n_col, Integral, "n_col")
    validate_type(n_row, Integral, "n_row")
    validate_type(dx, Real, "dx")
    validate_type(dy, Real, "dy")
    validate_type(angle, Real, "angle")
    validate_type(x0, Real, "x0")
    validate_type(y0, Real, "y0")

    # Values
    validate_positive(n_col, "n_col")
    validate_positive(n_row, "n_row")
    validate_positive(dx, "dx")
    validate_positive(dy, "dy")
    validate_positive(x0, "Grid X Origin")
    validate_positive(y0, "Grid Y Origin")

    theta = np.radians(angle)

    # Direction of columns
    col_vector = np.array([np.cos(theta),np.sin(theta)])

    # Direction of rows, perpendicular to columns
    row_vector = np.array([-np.sin(theta),np.cos(theta)])

    # Physical dimensions of grid
    width = (n_col - 1) * dx
    height = (n_row - 1) * dy

    origin = np.array([x0, y0])

    # Four corners
    p00 = origin
    p10 = origin + width * col_vector
    p11 = p10 + height * row_vector
    p01 = origin + height * row_vector

    corners = np.array([p00,p10,p11,p01])

    return corners