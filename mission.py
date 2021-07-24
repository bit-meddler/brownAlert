# Mission
#
# Define the Mission specification (Allowed tech level, unit propities)
# Load and populate the battlefield

import json
from random import Random

from mapping import Map, Tile


class Mission( object ):

    """
    Defines the mission parameters.  limits on tech level, settings for heat decay and shroom growth.
    
    Attributes:
        field (list of lists): The battlefield as a 2D array of Tiles
        heat_cap (int): max heat a tile can absorbe.
        heat_decay (int): how much heat is lost per heat tick
        map_fq (string): fully qualified path to the mission JSON
        rand (Random): Random with a fixed seed, so some randomness is shared
        rand_seed (int): the shared seed
        shroom_cap (int): max shrooms that can exist on a tile
        shroom_grow_amount (int): how much the shrooms grow, if they can
        shroom_grow_limit (int): Shrooms can only grow above a theashold
        shroom_spread_limit (int): Shrooms can only spread above a theashold
    """
    
    def __init__( self, map_fq ):
        # The mission file
        self.map_fq = map_fq

        # The Batlefield
        self.field = None

        # Shrooms - my take on Tibiriam
        self.shroom_grow_amount  =   6
        self.shroom_grow_limit   =  20
        self.shroom_spread_limit =  76
        self.shroom_cap = 100

        # Heat - battlefield tiles get hot if exploded of tanks sited on them
        self.heat_cap = 128
        self.heat_decay = 8

        # Shared random seed
        self.rand_seed = 1

        # ???

        if( self.map_fq is not None ):
            self.loadMap()

    def loadMap( self, map_fq=None ):
        """
        load the mission JSON
        
        Args:
            map_fq (string): Overide the map that may have been passed on instansiation.
        """
        # override
        if( map_fq is not None ):
            self.map_fq = map_fq

        json_dict = {}
        with open( self.map_fq,"r" ) as fh:
            json_dict = json.load( fh )

        ### decode the dict ###

        # Load Mission settings
        for k, v in json_dict[ "MISSION_SETUP" ].items():
            setattr( self, k, v )

        # load the PRNG
        self.rand = Random( self.rand_seed )
        
        # Load the Map
        map_dict = json_dict[ "MAP_SETUP" ]
        self.field = Map( self )

        dim_x, dim_y = map_dict["DIMS"]

        grid = [ [Tile( self.field, (x,y), map_dict["BASE_TERRAIN"] ) for x in range(dim_x)] for y in range(dim_y) ]
        
        self.field.setMap( grid, dim_x, dim_x )

        # Work through the enviroment tile RLE lists
        for key, accessor in Tile.DATA_ATTERS.items():
            for (idx, val, num) in map_dict[ key ]:
                for i in range( num ):
                    tile = self.field.accessRavel( idx+i )
                    if( tile is not None ):
                        setattr( tile, accessor, val )