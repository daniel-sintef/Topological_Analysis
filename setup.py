from setuptools import setup, find_packages
import os
import platform
import subprocess
import sys
import tarfile
import urllib.request
from setuptools.command.install import install

class CustomInstallCommand(install):
    """Custom install command to download and install Zeo++."""
    
    def run(self):
        # First, run the standard install command
        install.run(self)
        
        # Then install Zeo++ if on Linux
        if platform.system() != "Linux":
            print("WARNING: Zeo++ can only be installed on Linux systems.")
            print("You will need to install Zeo++ manually from http://www.zeoplusplus.org/")
            return
        
        try:
            self.install_zeopp()
            print("Zeo++ installation complete.")
        except Exception as e:
            print(f"ERROR installing Zeo++: {e}")
            print("Please install Zeo++ manually from http://www.zeoplusplus.org/")
    
    def install_zeopp(self):
        """Download and install Zeo++"""
        # Create directory for installation
        install_dir = os.path.expanduser('~/.local/bin')
        os.makedirs(install_dir, exist_ok=True)
        
        # Download Zeo++
        zeopp_url = "http://www.zeoplusplus.org/zeo++-0.3.tar.gz"
        zeopp_tar = os.path.join(install_dir, "zeo++-0.3.tar.gz")
        
        print(f"Downloading Zeo++ from {zeopp_url}")
        urllib.request.urlretrieve(zeopp_url, zeopp_tar)
        
        # Extract the tar file
        print("Extracting Zeo++...")
        zeopp_dir = os.path.join(install_dir, "zeo++-0.3")
        if os.path.exists(zeopp_dir):
            import shutil
            shutil.rmtree(zeopp_dir)
            
        with tarfile.open(zeopp_tar, "r:gz") as tar:
            tar.extractall(path=install_dir)
        
        # Compile Voro++
        print("Compiling Voro++ library...")
        voro_dir = os.path.join(zeopp_dir, "voro++", "src")
        current_dir = os.getcwd()
        os.chdir(voro_dir)
        subprocess.check_call(["make"])
        
        # Compile Zeo++
        print("Compiling Zeo++...")
        os.chdir(zeopp_dir)
        subprocess.check_call(["make"])
        
        # Create symlink to the network executable
        print("Creating symlink to the Zeo++ executable...")
        network_exe = os.path.join(zeopp_dir, "network")
        network_link = os.path.join(install_dir, "network")
        
        if os.path.exists(network_link):
            os.remove(network_link)
        
        os.symlink(network_exe, network_link)
        os.chmod(network_exe, 0o755)  # Make executable
        
        # Return to original directory
        os.chdir(current_dir)
        
        # Check if install_dir is in PATH
        if install_dir not in os.environ.get("PATH", "").split(os.pathsep):
            print(f"\nWARNING: {install_dir} is not in your PATH.")
            print(f"Please add it to your PATH to use Zeo++ by adding this to your shell profile:")
            print(f"export PATH=\"{install_dir}:$PATH\"")

setup(
    name="topology",
    version="0.4.0",
    author="Xingfeng He, Yunsheng Liu",
    author_email="yliu1240@umd.edu",
    description="Analyze material structures with Voronoi analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/materialsvirtuallab/Topological_Analysis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pymatgen>=2022.0.0",
        "numpy>=1.19.0",
        "monty>=2021.0.0",
        "pandas>=1.2.0",
        "ruamel.yaml>=0.17.0",
        "prettytable>=2.0.0",
    ],
    package_data={
        "Topological_Analysis": ["files/*.yaml"],
    },
    scripts=[
        "scripts/analyze_voronoi_nodes.py",
    ],
    cmdclass={
        "install": CustomInstallCommand,
    },
)
