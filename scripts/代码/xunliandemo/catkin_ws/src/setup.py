from distutils.core import setup
 
setup(
    version='0.0.0',
    scripts=['scripts/get_current_map_pose.py'],
    packages=['mobile_fetch'],
    package_dir={'': 'scripts'}
)