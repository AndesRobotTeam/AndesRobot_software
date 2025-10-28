from setuptools import setup
import os
from glob import glob

package_name = 'hfi_b9_imu'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # ✅ Instalar los launch files
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='fots',
    maintainer_email='fots@todo.todo',
    description='Nodo ROS 2 para leer y visualizar el IMU HFI-B9 con RViz',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hfi_b9_imu_node = hfi_b9_imu.hfi_b9_imu_node:main',
        ],
    },
)
