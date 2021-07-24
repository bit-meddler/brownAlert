# factions - the players and AI
# entities - Base class, and superclasses of all units

from coord import Coord


class Faction( object ):

    """
    A Faction at war in the battlefield.  This could be a Human or computer Player.
    
    Attributes:
        money (int): Resources to buy buildings and units.
        name (string): Name
        power (int): Power to run buildings
        squads (TBD): Groups of units, allows coordination, and inter-unit comms
        tech_level (int): what's the max level we can build.
    """
    
    def __init__( self, name ):
        self.name = name

        # Faction capabilities
        self.tech_level = 0

        # "In America, first you get the Mushrooms, then you get the Power, then you get the Women."
        self.money = 0
        self.power = 0

        # Combat
        self.squads = None

    def strat_XXX( self ):
        """
        Factions will have software defined strategies for:
            Building (Base/Power/Factories/Defeneces)
            Production (Units/Resources)
            Attacks (Issue FRAGOS to units)
            Defence (Issue FRAGOS to units)
            Maintainence (Buildings, repairing units)
            Inteligence Gathering

        Strategies will issue 'FRAGOS' to Units (or buildings), the units will use their own
        tactics to try and execute the orders.  Coordination could be achived using squads.

        Attack Strategies could include Probe/Faint as well as a tank rush.

        """
        pass

    def prosecute( self ):
        """
        Prosecute war against the OpFor.
        For 'AI' players this is a State machine to chose:
            Enimey
            Battle Phase
            Next Phase

        Then execute strategies to move to the next phase.
        """
        pass


"""
Make a Special case for the "Gaia" faction that 'owns' the dodads.
"""


class Entity( Coord ):

    """
    An entity on the battlefield.  Anything other than terrain.
    
    Might have an animation managment system for the sprite TBD
    
    Attributes:
        alegiance (faction): Faction commanding this entity
        altitude (int): Hight above ground level, suppose could be below sea level for submarines
        armour (TBD): Type of armour (needs to be a matrix of Wepon vs Armour )
        armour_integrity (int): %age of armour remaining
        grudge_list (TBD): list of Factions and or units that have done this entity damage.
        heat (int): Heat signature of the unit
        hit_points (int): Life
        id (int): UID
        is_active (bool): should the entity be processd
        is_destructable (bool): Can this be destroyed?
        is_movable (bool): can this be moved (eg. not a tree)
        sight_range (int): How far into fog can this unit see
        size (list): Physical size on the game map
        sprite (TBD): Image to draw for the entity
        weapon (TBD): Describe Weapon, damage, type, rof, cool-down

    """
    
    def __init__( self ):
        super( Entity, self ).__init__( self )

        # Managment
        self.id = -1
        self.is_active = False
        self.is_destructable = False
        self.alegiance = None

        # Drawing
        self.sprite = None

        # Movement
        self.is_movable = False
        self.altitude = 0
        self.size = [ 0, 0 ]
        self.heat = 0
        self.sight_range = 0

        # Combat
        self.hit_points = 0
        self.armour_integrity = 0
        self.armour = None
        self.weapon = None
        self.grudge_list = None

    def canMoveOn( self, tile ):
        """
        ## Implementer Overide ##

        Tests that this entity can move in the given tile, most important for land units that might
        be blocked by impassable terrain, dodads, or buildings.
        
        Args:
            tile (tile): Target tile
        
        Returns:
            bool: yes or no
        """
        return self.is_movable

    def takeDamage( self, belligerent ):
        """
        Take damage from the belligerent.weapon against self.armour
        add belligerent and thier faction to the grudge list

        Args:
            belligerent (Entity): Person dealing me damage
        """
        pass

    def automate( self ):
        """
        Virtual - process the AI or automatic processes for the entity
        """
        pass


class Commandable( Entity ):
    """
    A Unit that a faction could issue commands to
    
    Attributes:
        command_queue (TBD): List of commands to execute
    """
    
    def __init__( self ):
        super( Commandable, self ).__init__( self )

        # commandable attrs
        self.command_queue = None

    def frago( self, command ):
        """
        A Frago is formatted:
            Urgency
            Situation
            Mission
            Tasks
            Coordination
        Need to simplify a bit for use here.
        
        Args:
            command (list-like): Encapsulation of the Frago
        """
        pass

    def tact_XXX( self ):
        """
        Every war-like unit will have some tactics it can execute:
            Attack/Defend
            Guard
            Patrol
            Escort?
            Reconnoitre?
            Infiltraite?

        These may not be implemented (eg. Powerplant has no weapons), or have
        a special implmentation (AA-Guns, Pill Box)
        """
        pass


class Structure( Commanable ):
    """
    A building, this could be a dumb Powerplant/Farm, a Factory, or Defensive.

    I quite like the Starcraft metaphor that the factory has the buttons to build units,
    rather than the C&C sidebar where all the options get lost off the end.
    """

    def __init__( self ):
        super( Structure, self ).__init__( self )


class Moveable( Commanable ):
    """
    Something that can move about.

    Attributes:
        propulsion (TBD): Might affect movement over different terrains, and heat profile
        speed (int): Unit's speed
    """
    
    def __init__( self ):
        super( Moveable, self ).__init__( self )

        # Movement
        self.speed = 0
        self.propulsion = None

    def motionPlan( self ):
        """
            Plan this unit's motion.
                Air and Sea units should be fairly easy.
                Land units may have their way blocked by:
                    terrain
                    debris
                    dodads
                    buildings
                    defensive structures
                Land units may be impeaded by:
                    mud
                    fords
                    uphill gradients
                    colliding with structures
                Land units might be ordered to an unreachable position
                Units might experiance 'Contact' with the OpFor
        """
        pass


class Infantry( Moveable ):
    """
    Dudes - as in "I'm in your base killing your dudes."
    """
    pass


class Mechanized( Moveable ):
    """
    You shall have Jeeps, Trucks, and Tanks.  You're welcome.
    """
    pass


class Aircraft( Moveable ):
    """
    Get to dah Choppah!
    """
    pass


class Vessel( Moveable ):
    """
    Atomic wessills
    """
    pass