# Info

Given:
- mesh file (at the moment only .ply)
- rotation and translation values of the mesh wrt the camera frame
- camera parameters (intrinsics, width, height)

The script computes the mask of the mesh object at the provided pose. 

TODO:
- add support for stl files (commonly present in robot descriptions in ROS)

# How to run

create conda virtual environment with ```conda create --name render python=3.8```.

activate environment with ```conda activate render``

install matplotlib with ```conda install maptlotlib```.

then ```pip install -r requirements.txt```


## Example:
### mesh file
<img src="output/w1.png" width="50%" height="50%">   

### mask generated (for given rotation and translation values):
<img src="output/mask.png" width="50%" height="50%">   



