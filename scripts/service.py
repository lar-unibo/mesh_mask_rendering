#!/usr/bin/env python  

import rospy
import math
import tf
import geometry_msgs.msg
from robot_shape_removal.srv import removeShape, removeShapeResponse
import numpy as np
import os 
import rospkg

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


class ServiceClass():

    def __init__(self):

        rospack = rospkg.RosPack()
        rospack.list()
        self.dir_path = rospack.get_path('robot_shape_removal')

        self.mesh_dir = os.path.join(self.dir_path, "meshes")


        self.listener = tf.TransformListener()

        self.topic_service = "remove_shape"
        s = rospy.Service(self.topic_service, removeShape, self.service_callback)
        print("service [{}] created".format(self.topic_service))


    def getTransform(self, frame1, frame2):
        try:
            (trans,rot) = self.listener.lookupTransform(frame1, frame2, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            print("no TF available!")
            pass
        
        R = tf.transformations.quaternion_matrix([rot[0], rot[1], rot[2], rot[3]])
        R = R[:3,:3]
        t = np.array([trans[0], trans[1], trans[2]]).reshape(3,1)
        return R, t

    def service_callback(self, req):
        
        # input values
        obj_id = 0
        R, t = self.getTransform("gripper_camera", "panda_link0")
        model_name = "pippo.ply"
        model_path = os.path.join(self.mesh_dir, model_name)

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



if __name__ == '__main__':
    rospy.init_node('robot_shape_removal_service')
    r = ServiceClass()
    while not rospy.is_shutdown():
        rospy.spin()

