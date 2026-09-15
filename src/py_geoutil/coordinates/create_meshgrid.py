import numpy as np
from numbers import Integral, Real
from ..utils.validation import validate_type,validate_required,validate_positive

def create_indexed_meshgrid(x0=None,y0=None,nx=None,ny=None,dx=None,dy=None, angle_rot = 0.0):

    '''
       
    Routine to create X & Y coordinate meshgrids from origin points, number of points in each direction and rotation angle

    Arguments:
    filename (float): full file location of selected tops file
    return_meshgrid (bool): return either meshgrid or pandas dataframe
    
    Returns:
    X & Y - coordinate neshgrids with correct dimensions and rotated coordinates

    Raises:
    ValidationError if any required inputs are empty
    ValidationError if any of the inputs are not in the coorect format
    ValidationError coords and number of points are not positive

    Example:
    X, Y = create_indexed_meshgrid(x0=1000,y0=1000,nx=20,ny=20,dx=12.5,dy=12.5, angle_rot=41.2)

    PRECONDITIONS: input grid dimensions are correct.
    KJAGGS Sep 2026
    
    '''

    #Validate Inputs
    validate_required(x0=x0,y0=y0,nx=nx,ny=ny,dx=dx,dy=dy, angle_rot = angle_rot)

    # Types
    validate_type(x0, Real, "n_col")
    validate_type(y0, Real, "n_row")
    validate_type(nx, Integral, "Number of X Points")
    validate_type(ny, Integral, "Number of Y Points")
    validate_type(dx, Real, "dx")
    validate_type(dy, Real, "dy")
    validate_type(angle_rot, Real, "Angle of Rotation")

    # Values
    validate_positive(x0, "X Origin")
    validate_positive(y0, "Y Origin")
    validate_positive(nx, "Number Of Columns")
    validate_positive(ny, "Number of Rows")


    x = x0 + np.arange(nx) * dx
    y = y0 + np.arange(ny) * dy

    X, Y = np.meshgrid(x, y, indexing="ij")

    # Convert angle to radians
    theta = np.radians(angle_rot)

    # Coordinates relative to origin
    X_rel = X - x0
    Y_rel = Y - y0

    # Rotate
    X_rot = x0 + X_rel * np.cos(theta) - Y_rel * np.sin(theta)
    Y_rot = y0 + X_rel * np.sin(theta) + Y_rel * np.cos(theta)

    return X_rot,Y_rot