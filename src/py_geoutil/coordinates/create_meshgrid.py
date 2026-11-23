import numpy as np
import pandas as pd
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

def meshgrid_extract(df, Z, x0, y0, dx, dy, angle_rot):
    """
    Bilinearly interpolate a rotated structured grid at XY points.

    Parameters
    ----------
    df : pandas.DataFrame
        Must contain columns "X", "Y", and "Z".

    Z : np.ndarray
        Structured grid with shape (nx, ny).

    x0, y0 : float
        XY coordinates of grid node [0, 0].

    dx, dy : float
        Grid spacing in the unrotated grid coordinate system.

    angle_rot : float
        Grid rotation angle in degrees, positive counter-clockwise.

    Returns
    -------
    pandas.DataFrame
        Copy of df with:
            Z_mesh  : bilinearly interpolated Z
            Delta   : df["Z"] - Z_mesh
            I_mesh  : fractional I coordinate
            J_mesh  : fractional J coordinate
    """

    # --------------------------------------------------
    # Grid dimensions
    # --------------------------------------------------

    nx, ny = Z.shape

    # --------------------------------------------------
    # Rotation
    # --------------------------------------------------

    theta = np.radians(angle_rot)

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # --------------------------------------------------
    # Input coordinates
    # --------------------------------------------------

    x = df["X"].to_numpy(dtype=float)
    y = df["Y"].to_numpy(dtype=float)

    # --------------------------------------------------
    # Translate to grid origin
    # --------------------------------------------------

    xr = x - x0
    yr = y - y0

    # --------------------------------------------------
    # Reverse grid rotation
    # --------------------------------------------------

    x_unrot = (
        xr * cos_theta
        + yr * sin_theta
    )

    y_unrot = (
        -xr * sin_theta
        + yr * cos_theta
    )

    # --------------------------------------------------
    # Fractional grid indices
    # --------------------------------------------------

    I_float = x_unrot / dx
    J_float = y_unrot / dy

    # --------------------------------------------------
    # Cell indices
    # --------------------------------------------------

    I0 = np.floor(I_float).astype(int)
    J0 = np.floor(J_float).astype(int)

    I1 = I0 + 1
    J1 = J0 + 1

    # --------------------------------------------------
    # Points for which a complete cell exists
    # --------------------------------------------------

    valid = (
        (I0 >= 0) &
        (I1 < nx) &
        (J0 >= 0) &
        (J1 < ny)
    )

    # --------------------------------------------------
    # Initialise
    # --------------------------------------------------

    z_interp = np.full(len(df), np.nan)

    # --------------------------------------------------
    # Fraction within cell
    # --------------------------------------------------

    fi = I_float - I0
    fj = J_float - J0

    # --------------------------------------------------
    # Bilinear interpolation
    # --------------------------------------------------

    if np.any(valid):

        i0 = I0[valid]
        i1 = I1[valid]

        j0 = J0[valid]
        j1 = J1[valid]

        fiv = fi[valid]
        fjv = fj[valid]

        z00 = Z[i0, j0]
        z10 = Z[i1, j0]
        z01 = Z[i0, j1]
        z11 = Z[i1, j1]

        z_interp[valid] = (
            z00 * (1.0 - fiv) * (1.0 - fjv)
            + z10 * fiv       * (1.0 - fjv)
            + z01 * (1.0 - fiv) * fjv
            + z11 * fiv       * fjv
        )

    # --------------------------------------------------
    # Output
    # --------------------------------------------------

    result = df.copy()

    result["Z_mesh"] = z_interp
    #result["Delta"] = result["Z"] - result["Z_mesh"]

    result["I_mesh"] = I_float
    result["J_mesh"] = J_float

    return result["Z_mesh"]