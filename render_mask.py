import os
import numpy as np
from scipy.spatial.transform import Rotation
import cv2 

'''
lib is a striped-down version of the functionalities 
present in https://github.com/thodan/bop_toolkit
'''
from lib import inout
from lib import misc
from lib import renderer

class CameraParams():

    '''
    camera_matrix = np.array([[929.885,0,665.668],[0,929.833,365.149],[0,0,1]])
    camera_dist = np.array([0, 0, 0, 0, 0], np.float)  
    width = 1280
    height = 720  
    '''
    camera_matrix = np.array([[528.8181, 0.0, 347.5102],[0, 528.5537, 258.8532],[0,0,1]])
    camera_dist = np.array([0.003729, -0.111591, -0.000104, 0.002567, 0.210856], np.float)  
    width = 640
    height = 480  



# Input values
obj_id = 0
model_path = "data/panda/link0.ply"
img_debug = "data/panda/frame0000.jpg"

# tf gripper_camera panda_link0
R = Rotation.from_quat([0.674, -0.521, -0.300, -0.430]).as_matrix()
t = np.array([0.021, -0.060, 0.429]).reshape(3,1)

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

### debugging
img = cv2.imread(img_debug, cv2.IMREAD_COLOR)
mask_c = cv2.cvtColor(255 * mask.astype(np.uint8), cv2.COLOR_GRAY2BGR)
added_image = cv2.addWeighted(img,0.4,mask_c,0.2,0)

cv2.imshow("debug", added_image)
cv2.waitKey(0)


