import numpy as np
import pandas as pd

def create_grid_points(x_origin = None,y_origin = None, no_x_points = None, no_y_points = None,angle_rot = 0,x_int=1,y_int=1):
    '''
    Creates a pandas dataframe containing a rotated grid of x and y points
    Angle of rotation is clockwise from x-axis

    Parameters
    ----------
    x_origin : float, x coords origin of grid
    y_origin : float, y coords origin of grid
    no_x_points : int, number of columns in x direction
    no_y_points : int, number of rows in y direction
    angle_rot : float, angle of rotation in degrees clockwise from 90 degrees x axis
    x_int : float, unit increment of columns in x direction
    y_int : float, unit increments of row in y direction

    Raises
    ------
    None

    Examples
    --------
    df_rot = define_grid(x_origin=0,y_origin=0,no_x_points = 20, no_y_points = 20,x_int=10,y_int=10,angle_rot = 10)
    
    KJAGGS Feb 2026
    '''

    #angle converted to radians and * -1 to rotate clockwise from x axis
    theta = angle_rot *-1
    theta_rad = np.deg2rad(theta)

    #raw grid origin 0 inc 1
    x = np.arange(0, no_x_points)
    y = np.arange(0, no_y_points)

    X, Y = np.meshgrid(x, y)
    
    x_flat = X.ravel()
    y_flat = Y.ravel()
    
    x_flat = (x_flat * x_int) 
    y_flat = (y_flat * y_int)

    #rotation matrix
    R = np.array([
        [np.cos(theta_rad), -np.sin(theta_rad)],
        [np.sin(theta_rad),  np.cos(theta_rad)]
        ])
    
    #rotate and shift to origin
    #coords = np.vstack((x_flat - x_origin, y_flat - y_origin)).T 
    coords = np.vstack((x_flat, y_flat)).T 
    rot_coords = coords @ R.T

    X_rot = rot_coords[:, 0]# + x_origin
    Y_rot = rot_coords[:, 1]# + y_origin

    # ----------------------------
    # 4. Create output table
    # ----------------------------
    df = pd.DataFrame({
        #"X": x_flat + x_origin,
        #"Y": y_flat + y_origin,
        "X": X_rot + x_origin,
        "Y": Y_rot + y_origin
        })

    
    return df

def rotate_points(points, angle_deg, origin=(0, 0)):
    """
    points: Nx2 NumPy array of (x, y)
    angle_deg: rotation angle in degrees (positive = CCW)
    origin: tuple (ox, oy)
    Returns: Nx2 array of rotated points

    Example
    # Generate 1 million random points
    points = np.random.rand(1_000_000, 2) * 100  # in 0–100 range
    # Rotate 45° around (50, 50)
    rotated_points = rotate_points_fast(points, 45, origin=(50, 50))


    """
    # Convert to radians
    theta = np.radians(angle_deg)
    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)

    # Rotation matrix (2x2)
    R = np.array([[cos_theta, -sin_theta],
                  [sin_theta,  cos_theta]])

    # Translate points to origin and rotate
    rotated = (points - origin) @ R.T

    # Translate back
    return rotated + origin

def meshgrid_properties(grid_x = None,grid_y=None):

    '''
    Creates a dictionary summarising x and y meshgrid properties

    Parameters
    ----------
    grid_x : float, np.meshgrid of x coords
    grid_y : float, np.meshgrid of y coords

    Preconditions
    -------------
    Inputs must be x and y meshgrids - x and y grids must be same size
    
    Raises
    ------
    None

    Examples
    --------
    df_rot = define_grid(x_origin=0,y_origin=0,no_x_points = 20, no_y_points = 20,x_int=10,y_int=10,angle_rot = 10)
    
    KJAGGS Mar 2026
    '''

    meshgrid_dict = {}

    #Origin
    meshgrid_dict["x0"] = grid_x[0,0]
    meshgrid_dict["y0"] = grid_y[0,0]

    #Number of x columns and y rows
    meshgrid_dict["ny"] , meshgrid_dict["nx"] = grid_x.shape

    #X and Y direction vectors
    dx_vec = np.array([grid_x[0,1] - grid_x[0,0], grid_y[0,1] - grid_y[0,0]])
    dy_vec = np.array([grid_x[1,0] - grid_x[0,0], grid_y[1,0] - grid_y[0,0]])
    meshgrid_dict["dx_vector"] = dx_vec 
    meshgrid_dict["dy_vector"] = dy_vec 

    #calculate angle of rotation for y coords counter clockwise from 90 deg E
    theta = np.arctan2(dx_vec[1], dx_vec[0])  # radians
    meshgrid_dict["rotation"] =np.degrees(theta)-90

    #calculate increment between
    meshgrid_dict["x_inc"] = np.sqrt(np.square(grid_x[0,1] - grid_x[0,0]) +  np.square(grid_y[0,1] - grid_y[0,0]))
    meshgrid_dict["y_inc"] = np.sqrt(np.square(grid_x[1,0] - grid_x[0,0]) +  np.square(grid_y[1,0] - grid_y[0,0]))
    
    meshgrid_dict["min_x"] = grid_x.min()
    meshgrid_dict["max_x"] = grid_x.max()
    meshgrid_dict["min_y"] = grid_y.min()
    meshgrid_dict["max_y"] = grid_y.max()

    #print(dx_vec,dy_vec,rotation_deg,angle_deg)

    return meshgrid_dict