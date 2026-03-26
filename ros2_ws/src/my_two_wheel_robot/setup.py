from setuptools import setup
import os
from glob import glob

package_name = 'my_two_wheel_robot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*launch.py'))),
        (os.path.join('share', package_name, 'urdf'),
            glob(os.path.join('urdf', '*.*'))),
        (os.path.join('share', package_name, 'meshes'),
            glob(os.path.join('meshes', '*.*'))),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pi',
    maintainer_email='pi@todo.todo',
    description='Robot description and launch files for my_two_wheel_robot',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
)
