import os
import numpy as np

'''
lib is a striped-down version of the functionalities 
present in https://github.com/thodan/bop_toolkit
'''
from lib import inout
from lib import misc
from lib import renderer

class CameraParams():
    camera_matrix = np.array([[929.885,0,665.668],[0,929.833,365.149],[0,0,1]])
    camera_dist = np.array([0, 0, 0, 0, 0], np.float)  
    width = 1280
    height = 720  

# Input values
obj_id = 0
model_path = "data/W1.ply"
R = np.eye(3)
t = np.array([0, 0, 0.5]).reshape(3,1)

# Initialize a renderer.
misc.log('Initializing renderer...')
ren = renderer.create_renderer(CameraParams.width, CameraParams.height, renderer_type="python", mode='depth')

# Add object model.
ren.add_object(obj_id, model_path)

K = CameraParams.camera_matrix
fx, fy, cx, cy = K[0, 0], K[1, 1], K[0, 2], K[1, 2]

# Render the depth image.
depth_gt = ren.render_object(obj_id, R, t, fx, fy, cx, cy)['depth']

# Convert depth image to distance image.
dist_gt = misc.depth_im_to_dist_im(depth_gt, K)

# Mask of the full object silhouette.
mask = dist_gt > 0

# Save the calculated masks.
inout.save_im("output/mask.png", 255 * mask.astype(np.uint8))
