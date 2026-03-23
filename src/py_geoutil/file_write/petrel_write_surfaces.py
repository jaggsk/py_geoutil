import numpy as np

def write_irap_ascii(filename=None, Z=None, x0=None, y0=None, nx=None,ny=None,dx=None, dy=None,angle=None, null_value=9999900.000000):
    
    """
    Write a 2D array of data to an IRAP ASCII raster file format.

    Parameters
    ----------
    filename : str
        Path to the output file to write the ASCII grid.
    Z : 2D numpy array MUST BE IN MESHGRID FORMAT
        Grid of values to export. NaNs will be replaced by `null_value`.
    x0, y0 : float
        Coordinates of the lower-left corner of the grid.
    nx, ny : int
        Number of columns (nx) and rows (ny) in the grid.
    dx, dy : float
        Grid spacing in the x and y directions.
    angle : float
        Rotation angle of the yaxis grid, from 0 = 90deg E,in degrees.
    null_value : float, optional, default=9999900.0
        Value used to replace NaNs in the grid.

    Notes
    -----
    - The grid is flattened in column-major (Fortran-style) order when written.
    - Output follows the IRAP ASCII grid format with a specific header.
    - Each line of the data section contains up to 6 values formatted to 6 decimal places.

    Example
    -------
    write_irap_ascii("filepath/output.asc", Z=my_array, x0=0, y0=0, nx=100, ny=100, dx=1, dy=1, angle=0)
    """
    
    Zout = np.where(np.isnan(Z), null_value, Z)

    x_min = x0
    x_max = x0 + ((nx - 1)* dx)
    y_min = y0
    y_max = y0 + ((ny - 1)* dy)

    with open(filename, "w") as f:
        # Header
        f.write(f"-996 {ny} {dx:.6f} {dy:.6f}\n")
        f.write(f"{x_min:.6f} {x_max:.6f} {y_min:.6f} {y_max:.6f}\n")
        f.write(f"{nx} {angle:.6f} {x0:.6f} {y0:.6f}\n")
        f.write(f"0 0 0 0 0 0 0\n")
        
        # flatten row-wise (row-major order)
        flat = Zout.flatten(order='F')

        #flat.reshape(-1,1)
        # Number of values per line
        n_per_line = 6

        # Compute number of full rows
        n_full_rows = len(flat) // n_per_line

        # Reshape full rows
        rows = flat[:n_full_rows * n_per_line].reshape(-1, n_per_line)

        # Remaining values
        remainder = flat[n_full_rows * n_per_line:]

        for row in rows:
            f.write(" ".join(f"{v:.6f}" for v in row) + "\n")
        if remainder.size > 0:
            f.write(" ".join(f"{v:.6f}" for v in remainder) + "\n")
