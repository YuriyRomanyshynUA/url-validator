import setuptools


setuptools.setup(
    name="url-validator-pkg-yuriy-romanyshyn",
    version="0.0.1",
    author="Yuriy Romanyshyn",
    author_email="yuriy.romanyshyn.lv.ua@gmail.com",
    description="url validator",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.0'
)
