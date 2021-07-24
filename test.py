# Test the game

from mission import Mission
import mapping as maps


from pprint import pprint
from time import sleep

TRN_TPY = {
    maps.TRN_WATER   : "w",
    maps.TRN_LAND    : "l",
    maps.TRN_IMPASS  : "x",
    maps.TRN_LIMINAL : "s",
    
}

def dump_shrooms( field ):
    data = ""
    for row in field.grid:
        for tile in row:
            data += "{}{: >2} ".format( TRN_TPY[tile.terrain], tile.shrooms )
        data += "\n"
    data += "\n"

    print( data )
    
my_mission = Mission( "test_map.json" )

for i in range( 20 ):
    dump_shrooms( my_mission.field )
    my_mission.field.growShrooms()
    sleep( 0.5 )
