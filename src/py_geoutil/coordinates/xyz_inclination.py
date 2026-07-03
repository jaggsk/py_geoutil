import math 

def inclination_xyz(xyz_tuple1=None,xyz_tuple2=None):
    '''
    Calculate angle of inclination between 2 xyz tuples

    xyz_tuple1 (float): x y z coords for first input point
    xyz_tuple2 (float): x y z coords for second input point

    Raises: None

    Example: df_tops["Angle_Incl"] =  df_tops.apply(lambda x: inclination_xyz(xyz_tuple1=(x["Top_X"], x["Top_Y"],x["Top_Z"]),xyz_tuple2=(x["Base_X"], x["Base_Y"],x["Base_Z"])), axis=1) 
    '''
    dx = xyz_tuple2[0] - xyz_tuple1[0]
    dy = xyz_tuple2[1] - xyz_tuple1[1]
    dz = xyz_tuple2[2] - xyz_tuple1[2]

    # Horizontal distance (projection onto XY plane)
    horizontal_dist = math.sqrt(dx**2 + dy**2)

    # Inclination angle from horizontal plane
    angle_rad = math.atan2(dz, horizontal_dist)
    angle_deg = math.degrees(angle_rad)

    return angle_deg