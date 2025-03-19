from setuptools import setup, find_packages
import os
import platform
import subprocess
import sys
import tarfile
import urllib.request
import shutil
import site
from setuptools.command.install import install

class CustomInstallCommand(install):
    """Custom install command to download and install Zeo++ and its Python wrapper."""
    
    def run(self):
        # Check if running in a virtualenv
        if not self.is_virtualenv():
            print("ERROR: Zeo++ installation must be performed within a virtualenv.")
            print("Please create and activate a virtualenv, then try again.")
            sys.exit(1)
            
        # First, run the standard install command
        install.run(self)
        
        # Check if Zeo++ is already installed
        if self.is_zeopp_installed():
            print("Zeo++ is already installed. Skipping installation.")
            return
        
        # Then install Zeo++ if on Linux
        if platform.system() != "Linux":
            print("WARNING: Zeo++ can only be installed on Linux systems.")
            print("You will need to install Zeo++ manually from http://www.zeoplusplus.org/")
            return
        
        try:
            self.install_zeopp()
            print("Zeo++ installation complete.")
        except Exception as e:
            print(f"ERROR during installation: {e}")
            print("Please install Zeo++ manually from http://www.zeoplusplus.org/")
    
    def is_virtualenv(self):
        """Check if running in a virtualenv."""
        # Check for virtualenv or venv
        return (
            hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        )
    
    def get_virtualenv_path(self):
        """Get the path to the current virtualenv."""
        return sys.prefix
    
    def is_zeopp_installed(self):
        """Check if Zeo++ is already installed."""
        try:
            # Check if the 'network' executable is in virtualenv's bin directory
            venv_bin = os.path.join(self.get_virtualenv_path(), 'bin')
            network_path = os.path.join(venv_bin, 'network')
            return os.path.exists(network_path) and os.access(network_path, os.X_OK)
        except:
            return False
    
    def install_zeopp(self):
        """Download and install Zeo++"""
        # Get virtualenv installation directory
        install_dir = os.path.join(self.get_virtualenv_path(), 'bin')
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
            shutil.rmtree(zeopp_dir)
            
        with tarfile.open(zeopp_tar, "r:gz") as tar:
            tar.extractall(path=install_dir)
        
        
        # Compile Voro++
        print("Compiling Voro++ library ...")
        voro_dir = os.path.join(zeopp_dir, "voro++", "src")
        current_dir = os.getcwd()
        os.chdir(voro_dir)
        subprocess.check_call(["make"])
        
        # No longer installing Voro++ with 'make install'
        # Instead, we'll set environment variables to point to the source location
        voro_src_dir = os.path.join(zeopp_dir, "voro++")
        
        # Compile Zeo++
        print("Compiling Zeo++ ...")
        os.chdir(zeopp_dir)
        
        # Set environment variable to help find Voro++ from its source location
        os.environ["VOROLINKDIR"] = f"-L{voro_src_dir}/src"
        os.environ["VOROINCLDIR"] = f"-I{voro_src_dir}/src"
        
        # Compile
        subprocess.check_call(["make"])
        
        # Move Zeo++ executables to bin directory
        print("Moving Zeo++ executables to bin directory...")
        for exe in ["network", "molecule_to_abstract", "framework_builder", "voro++/src/voro++"]:
            src = os.path.join(zeopp_dir, exe)
            dst = os.path.join(install_dir, os.path.basename(exe))
            print(f'moving: {src} to {dst}')
            
            if os.path.exists(dst):
                os.remove(dst)
            
            if os.path.exists(src):
                shutil.copy2(src, dst)  # copy2 preserves metadata including permissions
                os.chmod(dst, 0o755)  # Make executable
            else:
                print(f"Warning: Could not find {exe} executable in {zeopp_dir}")
        
        # Return to original directory
        os.chdir(current_dir)
        
        # Clean up: remove tar file and extracted directory
        print("Cleaning up temporary files...")
        if os.path.exists(zeopp_tar):
            os.remove(zeopp_tar)
            
        if os.path.exists(zeopp_dir):
            shutil.rmtree(zeopp_dir)
        
        # Since we're installing to the virtualenv's bin directory, which should 
        # already be in the PATH when the virtualenv is active, no need to warn about PATH
    
setup(
    name="topology",
    version="0.4.1",
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
        "pymatgen>=2025.3.10",
        "numpy>=1.19.0",
        "monty>=2021.0.0",
        "pandas>=1.2.0",
        "ruamel.yaml>=0.17.0",
        "pyzeo>=0.1",
        "prettytable>=2.0.0",
        "cython>=0.29.0",  # Added for the Python wrapper
    ],
    package_data={
        "topology": ["files/*.yaml"],
    },
    entry_points={
        'console_scripts': [
            'analyze_voronoi_nodes=topology.cli.analyze_voronoi_nodes:main',
        ],
    },
    cmdclass={
        "install": CustomInstallCommand,
    },
)
