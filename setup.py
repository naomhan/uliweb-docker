import uliweb
from uliweb.utils.setup import setup
import apps

__doc__ = """doc"""

setup(name='project',
    version=apps.__version__,
    description="Description of your project",
    package_dir = {'project':'apps'},
    packages = ['project'],
    include_package_data=True,
    zip_safe=False,
)
