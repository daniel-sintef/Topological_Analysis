"""
Compatibility layer between zeo and pyzeo.
This module creates fake zeo modules that redirect to pyzeo.extension.
"""

import sys
import types

def setup_compatibility():
    try:
        import pyzeo.extension
        
        # Create fake zeo modules
        zeo_module = types.ModuleType('zeo')
        sys.modules['zeo'] = zeo_module
        
        # Create the cluster submodule
        cluster_module = types.ModuleType('zeo.cluster')
        sys.modules['zeo.cluster'] = cluster_module
        cluster_module.prune_voronoi_network_close_node = pyzeo.extension.prune_voronoi_network_close_node
        
        # Create the netstorage submodule
        netstorage_module = types.ModuleType('zeo.netstorage')
        sys.modules['zeo.netstorage'] = netstorage_module
        netstorage_module.AtomNetwork = pyzeo.extension.AtomNetwork
        
        # Set up the fake zeo module to have these submodules
        zeo_module.cluster = cluster_module
        zeo_module.netstorage = netstorage_module
        
        print("Successfully set up compatibility between zeo and pyzeo")
        return True
    except ImportError:
        print("Could not import pyzeo, zeo compatibility will not be available")
        return False

# Setup compatibility when this module is imported
setup_compatibility()
