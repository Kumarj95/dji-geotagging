import numpy as np
def R_z(angle):
    '''
    Helper function to create a matrix for rotation around the Z axis
    
    Args:
        angle (float): angle in radians around which to rotate

    Returns:
        R_z (np.array): Rotation matrix about the Z axis with given angle
    '''
    return np.array([[np.cos(angle),-np.sin(angle),0],
                     [np.sin(angle), np.cos(angle),0],
                     [0,0,1                 ]])
def R_y(angle):
    '''
    Helper function to create a matrix for rotation around the Y axis
    
    Args:
        angle (float): angle in radians around which to rotate

    Returns:
        R_y (np.array): Rotation matrix about the Y axis with given angle
    '''

    return np.array([[np.cos(angle),0,np.sin(angle)],
                     [0, 1,0],
                     [-np.sin(angle),0,np.cos(angle)                 ]])

def R_x(angle):
    '''
    Helper function to create a matrix for rotation around the X axis
    
    Args:
        angle (float): angle in radians around which to rotate

    Returns:
        R_x (np.array): Rotation matrix about the X axis with given angle
    '''


    return np.array([[1,0,0],
                     [0, np.cos(angle),-np.sin(angle)],
                     [0,np.sin(angle),np.cos(angle)                 ]])

def dsm_height(dsm,x, y, Tinv, nrows, ncols):
    """Return height at world (x, y) using bilinear interpolation.
       Assumes `dsm`, `Tinv`, nrows, ncols are already in scope."""
    
    res= np.zeros((x.shape[0]))
    col, row = Tinv * (x, y)       # floating-point indices
    # if not (0 <= row < nrows-1 and 0 <= col < ncols-1):
    #     return np.nan              # outside raster
    res[~(((0 <= row )&  (row < nrows-1)) & ((0 <= col )&  (col < ncols-1)))]=np.nan
    row= row[~np.isnan(res)]
    col= col[~np.isnan(res)]

    r0, c0 = np.int32(row), np.int32(col)
    dr, dc = row - r0, col - c0

    # Four neighbouring pixels
    z00 = dsm[r0    , c0    ]
    z01 = dsm[r0    , c0 + 1]
    z10 = dsm[r0 + 1, c0    ]
    z11 = dsm[r0 + 1, c0 + 1]

    # Bilinear interpolation
    res[~np.isnan(res)] = (z00 * (1-dr) * (1-dc) +
            z01 * (1-dr) * dc     +
            z10 * dr     * (1-dc) +
            z11 * dr     * dc)
    return res
def to_dms_rational(deg):
    '''
    Helper function to convert value from degrees to degree minute seconds

    Args:
        deg (float): angle in degrees to convert

    Returns:
        dms (list): list in format () 
    '''
    d = int(abs(deg))
    m = int((abs(deg)-d)*60)
    s = (abs(deg)-d-m/60)*3600
    return [(d,1),(m,1),(int(s*100),100)]

