# mapping - classes to describe the map and the tiles


# Terrain types
TRN_WATER   = 0
TRN_LAND    = 1
TRN_IMPASS  = 2 # River, clifs
TRN_LIMINAL = 3 # Shoreline

# Occupancy flags
# Special case: A commandable could be standing on a building (Aircraft on Runway, Tank on Bay)
OCY_NONE        = 0      # Fat nothing
OCY_DESTRUCT    = 1      # blocker that can be destroyied (sanbags, tree)
OCY_IMMOVEABLE  = 1 << 1 # Ruins
OCY_BUILDING    = 1 << 2 # Ownable Building
OCY_COMMANDABLE = 1 << 3 # Units

MASK_SPAWN_OK   = OCY_DESTRUCT | OCY_COMMANDABLE # Shrooms can spawn under destructables, or units
MASK_SPAWN_NO   = OCY_IMMOVEABLE | OCY_BUILDING  # Ground based blockers won't allow spawning

class Map( object ):

    """
    
    Attributes:
        COMPASS_POINTS (tuple): Conveniance list of Cardinal and ordinal compass points
        NEIGHBORS (dict): lut of compass direction to coordinate offset to access 8-Neigbors

        dim_x (int): Map Dimention X
        dim_y (int): Map Dimention Y
        grid (list of lists): the grid of map tiles
        ravel_max (int): max tile ID
        mission (Mission): mission specification
        occupied_tiles (set): Set of tiles with occupancy
        viewer_tiles (set): Set of tiles viewed? TBD
    """
    
    NEIGHBORS = {
        "N"  : ( 0,-1),
        "NE" : ( 1,-1),
        "E"  : ( 1, 0),
        "SE" : ( 1, 1),
        "S"  : ( 0, 1),
        "SW" : (-1, 1),
        "W"  : (-1, 0),
        "NW" : (-1,-1),
    }

    COMPASS_POINTS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")

    def __init__( self, mission ):
        # Hold reference to the Mission setup
        self.mission = mission

        # Map data - Row Mjr
        self.grid  = [[]]
        self.dim_x = 0
        self.dim_y = 0
        self.ravel_max = 0

        # Fast Lookup with Maps?
        self.occupied_tiles = set()
        self.viewer_tiles = set()

    def setMap( self, grid, dim_x, dim_y ):
        """
        Attach the supplied grid of tiles

        Args:
            grid (list): Nested array of tiles - the battlefield map
            dim_x (int): Map Dimention in X
            dim_y (int): Map Dimentino in Y - row major index of grid
        """
        self.grid = grid
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.ravel_max = dim_y * dim_x

    def accessRavel( self, idx ):
        """
        Access a tile by it's "ravel" index eg as if the matrix was flat
        Args:
            idx (int): index of tile
        
        Returns:
            tile: requested tile if valid, None if not
        """
        if( (idx < 0) or (idx > self.ravel_max) ):
            return None
        y, x = divmod( idx, self.dim_y )
        return self.accessXY( x, y )

    def accessXY( self, x, y ):
        """
        Convenience to offer protected access to the grid of tiles, save the
        brain-ache when thinking in X,Y, but accessing blar[Y,X]
        Args:
            x (int): X coord
            y (int): Y coord
        
        Returns:
            tile: requested tile if valid, None if not
        """
        if( (x > self.dim_x) or (x < 0) or
            (y > self.dim_y) or (y < 0) ):
            return None
        return self.grid[ y ][ x ]

    def randomDirection( self ):
        return self.mission.rand.choice( self.COMPASS_POINTS )

    # Map Automation routines ########################################################

    def growShrooms( self ):
        """
        Manage Shroom regrowth and spawning.
        """
        for row in self.grid:
            for tile in row:

                if( tile.shroomCanGrow() ):
                    tile.shrooms += self.mission.shroom_grow_amount

                if( tile.shroomCanSpread() ):
                    pos = self.NEIGHBORS[ self.randomDirection() ]

                    if( self.mission.rand.randint(0,100) > 95 ):
                        # big sneaze
                        new = ( pos[0] * 2, pos[1] * 2 )
                        target = tile.accessOffset( new )
                        
                    else:
                        target = tile.accessOffset( pos )

                    if( (target is not None) and target.shroomCanSpawn() ):
                        target.shrooms += self.mission.shroom_grow_amount

    def heatDecay( self ):
        """
        Manage heat decay
        """
        for row in self.grid:
            for tile in row:
                if( tile.heat > 0 ):
                    tile.heat -= self.mission.heat_decay
                # TODO: Accumulate Heat from units on the tile

                    
class Tile( object ):

    """
    
    Attributes:
        DATA_ATTERS (TYPE): lut of JSON dict keys to the attr they need to fill

        decal (TBD): Passive enviroment art
        decay (TBD): An art overlay that decays with time (blood, damage, skid marks)
        dodad (TBD): Environment art that impeads or prevents movement
        field (Map): refference to the mission 'map'
        heat (int): Heat buildup on the tile.  Just as appearance and occupancy are shown on radar, an IR satelite can see heat
        is_uncovered (TBD): bitfield (?) of visability for each faction
        mission (Mission): Mission Paramiters
        move_limit (int): Slowdown factor applied to land movement on this tile
        occupancy_flags (int): Indicate who is in the tile
        pos (List): [x,y] position of the tile
        ravel_id (int): index into an unraveled 2D Array, also the UID of the Tile, may be useful for hashing
        shrooms (int): The amount of valuable mushrooms growing on the tile
        terrain (int): Terain Type
    """
    
    DATA_ATTERS = {
        "SHROOM_LIST"  : "shrooms",
        "SPEED_LIST"   : "move_limit",
        "TERRAIN_LIST" : "terrain",
    }

    def __init__( self, field, pos, terrain=TRN_LAND ):
        self.field = field # Map
        self.mission = field.mission # Mission settings
        self.pos = pos

        self.ravel_id = ( self.pos[0] + (self.pos[1] * self.field.dim_y) )

        # Mapping
        self.is_uncovered = None # Needs to be a flag for each faction that has seen this tile

        ### Things that can be placed on the Map tile ###
        # Navigation, Placement
        self.terrain = terrain
        self.dodad = None # DoDads have a physical presences and interfear with placement and nav

        # Drawing
        self.decal = None # enviroment art that doesn't impead movement
        self.decay = None # bloodstains, impact craters

        # Navigation
        self.move_limit = 0 # if passable, does the ground type (terrain+dodad) penalise movement?

        # Occupancy
        # ??? DTRT
        self.occupancy_flags = OCY_NONE

        # Heat
        self.heat = 0

        # Shrroms
        self.shrooms = 0

    def accessOffset( self, offset ):
        """
        Get the neighboring tile using the supplied offset.  If an invalid coord is made
        Returns None

        Args:
            offset (tuple(x,y)): Coordinate offset
        
        Returns:
            tile: The neighboring tile if valid, None if not
        """
        x, y = self.pos
        dx, dy = offset
        return self.field.accessXY( x+dx, y+dy )

    # Shrooms Logic ###########################################################

    def shroomCanGrow( self ):
        """
        Test if the Terrain will let more shrooms grow

        Returns:
            bool: Can Shrooms grow
        """
        return bool( self.shrooms > self.mission.shroom_grow_limit )

    def shroomCanSpread( self ):
        """
        Test if there is enough muchrooms to start spreading

        Returns:
            bool: spreadability
        """
        return bool( self.shrooms > self.mission.shroom_spread_limit )

    def shroomCanSpawn( self ):
        """
        Test to see if shrooms can spawn here.  They can only spawn on land, and there
        must be no blocker on the tile.
        
        Returns:
            bool: spawn ability
        """
        return bool( (not (self.occupancy_flags & MASK_SPAWN_NO)) and (self.terrain == TRN_LAND) )

    # Getter / setter for the shrooms
    @property
    def shrooms( self ):
        """
        Getter for the 'shroom count

        Returns:
            int: Quantity of valuable shrooms on this tile
        """
        return self.__shrooms

    @shrooms.setter
    def shrooms( self, x ):
        """
        Setter for the number of mushrooms.  Clamps in valid ranges
        
        Args:
            x (int): New 'shroom count
        """
        if( x <= 0 ):
            self.__shrooms = 0

        elif( x > self.mission.shroom_cap ):
            self.__shrooms = self.mission.shroom_cap

        else:
            self.__shrooms = x

    # Heat Logic ##############################################################

    @property
    def heat( self ):
        """
        Getter for map tile heat

        Returns:
            int: heat
        """
        return self.__heat

    @heat.setter
    def heat( self, x ):
        """
        Setter for the tile heat. Clamps within mission settings
        
        Args:
            x (int): New heat factor
        """
        if( x <= 0 ):
            self.__heat = 0

        elif( x > self.mission.heat_cap ):
            self.__heat = self.mission.heat_cap

        else:
            self.__heat = x

    def getHeat( self ):
        """
        This is a combination of Tile heat + Heat of units on the tile.
        If Units stay on the tile for a while it heats up.
        If a big unit traverses it, it will pick up a little heat.
        Once it is empty it cools down.
        """
        pass

    # Building Logic ##########################################################

    def canBuildHere( self, native=TRN_LAND ):
        """
        Test if it's possible to place a building in this tile.  You must only build on
        'native' Terrain for the building, so docks on water, everything else on land.
        Also the tile must not be occupied.

        Args:
            native (Terrain ID): The building's native enviroment. (Default land)
        
        Returns:
            bool: If Buildable
        """
        return bool( (self.occupancy_flags == OCY_NONE) and (self.terrain == native) )