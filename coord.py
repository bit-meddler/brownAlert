# coord
#
# In-Game coordinates.  The map is made of Tiles with various properties
# there is also a fractional 'sub-coordinate' system, say to move dudes around inside a tile
# 

from collections import OrderedDict
import math
import random


class Coord( object ):

    HEADING = OrderedDict(
      ( ("N"  ,   0.),
        ("NE" ,  45.),
        ("E"  ,  90.),
        ("SE" , 135.),
        ("S"  , 180.),
        ("SW" , 225.),
        ("W"  , 270.),
        ("NW" , 315.),
      )
    )

    PI      = math.pi
    TWO_PI  = math.pi * 2.
    HALF_PI = math.pi / 2.


    __init__( self, x=0., y=0. ):
        self.x = x
        self.y = y

    def distanceSq( self, other ):
        """
        Args:
            other (coord): The other coordinate
        
        Returns:
            float: squared distance to the other coordinate
        """
        dx = self.x - other.x
        dy = self.y - other.y
        return (dx*dx + dy*dy)

    def distanceTo( self, other ):
        """
        Args:
            other (coord): The other coordinate

        Returns:
            float: distance to other coordinate
        """
        return math.sqrt( self.distanceSq( other ) )

    def asCellPos( self ):
        """
        Return x,y as ints so they can index an array
        
        Returns:
            tuple: x and y as ints
        """
        return ( int(self.x), int(self.y), )

    def vector( self, heading, distance ):
        """
        Move this coord _distance_ along _heading_
        
        Args:
            orientation (float): Angle in degrees - North = 0, clockwise incremental rotation
            distance (float): distance in coord units (cell.sub-cell)
        """
        self.x += math.sin( math.radians(heading) ) * distance
        self.y += math.cos( math.radians(heading) ) * distance

    def suggestRando( self, distance ):
        """
        Suggest a Random location _distance_ away from this coord's current position.
        
        Args:
            distance (float): distance away
        
        Returns:
            Coord: New coordinate randomly away from self's position
        """
        new_pos = Coord( self.x, self.y )
        new_pos.vector( random.uniform( 0.0, 360.0 ), distance )
        return new_pos

    @classmethod
    def quantizeHeading( angle ):
        """
        Lock the supplied angle to one of the compass headings we know about
        
        Args:
            angle (float): an angle, can be > 360
        
        Returns:
            float: nearest compass point from HEADING
        """
        test = (angle % 360) - 22.5
        for direction in self.HEADING.values():
            if( test < direction ):
                return direction
        return HEADING["N"]

    def headingTo( self, position ):
        """
        Get the angle from this coord to the position
        
        Args:
            position (coord): Place we want to inspect
        
        Returns:
            float: amgle to the position
        """
        ang = math.atan2( position.x - self.x, self.y - position.y )
        if( ang < 0. ):
            ang += self.TWO_PI
            
        return math.degrees( ang )

    def headingToQnt( self, position ):
        """
        Get the Quantized Heading to some position
        
        Args:
            position (Coord): opsition we're heading to
        
        Returns:
            float: compass point to bring us close
        """
        return self.quantizeHeading( self.headingTo( position ) )

        