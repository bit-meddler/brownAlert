# Equipment
#
# Projectile, Weapon, and Armour models

import coord


class Weapon( object ):
    """
    Weapons are a "Projectile factory" and manage their rof, cooldown, and chargeup.
    
    Attributes:
        owner (Entity): The Entity with this weapon.
    """
    STATE_WAITING = 0
    STATE_CHARGEUP = 1
    STATE_FIRING = 2
    STATE_COOLING = 3


    def __init__( self, owner, name ):
        self.owner = owner
        self.name = name

        ### Firing ###
        # Shots to fire
        self.rof = 0 # Burst rpm?
        self.range = 0 # in map tiles

        # Times between shots/bursts in GAME TICKS (assumed 15tps)
        self.warmup = 0 # delay before ready to fire
        self.cooldown = 0 # delay before ready to fire again
        self.count = 0 # countdown before next state change

        # which counter is active?
        self.state = Weapon.STATE_WAITING
        self.target = None

        # Projectile Factory
        self.fires = None

    def fireOn( self, target ):
        if( self.state == Weapon.STATE_WAITING ):
            # ready to start firing procedure
            self.target = target
            
            if( self.warmup == 0 ):
                self.state = Weapon.STATE_FIRING
                self.count = self.rof

            else:
                self.state = Weapon.STATE_CHARGEUP
                self.count = self.warmup

            if( self.state == Weapon.STATE_FIRING ):
                # Try and do a zero warmup shot in this tick
                self.count -= 1
                self.doFire()

        else:
            # Ignore until we're next ready to fire
            pass

    def tick( self, clock ):
        if( self.state == Weapon.STATE_WAITING ):
            return

        count -= 1
        if( count < 1 ):
            # Cycle state
            if( self.state == Weapon.STATE_CHARGEUP ):
                # ready to fire
                self.state = Weapon.STATE_FIRING
                self.count = self.rof
                self.doFire()

            elif( self.state == Weapon.STATE_FIRING ):
                # end of burst
                self.state = Weapon.STATE_COOLING
                self.count = self.cooldown
                self.target = None

            elif( self.state == Weapon.STATE_COOLING ):
                # waiting
                self.state = Weapon.STATE_WAITING

    def doFire( self ):
        # make a projectile and shoot it at self.target
        pass


class Projectile( object ):
    """
    Projectiles will be "minted" when fired, and manage drawing, hits, and damage dealing.
    """

    def __init__( self ):
        self.damage = 0
        self.velocity = 0
        self.homing = 0 # > 0 is the speed at which it can course-correct towards target

    def tick( self, clock ):
        pass


class Armour( object ):
    """
    Keep track of damage and armour effectivness.

    Diferent armour types will modify the amount of damage done by a Projectile.
    """

    def __init__( self ):
        pass

    def tick( self, clock ):
        pass

        
if( __name__ == "__main__" ):
    # Try out setting up some equipment

    # Projectiles
    proj = {
        "9mm"    : {},
        "5.56mm" : {},
        "7.62mm" : {},
        "40mm"   : {},
    }

    weapons = {
        "pistol" : {
            "fires"    : "9mm",
            "rof"      : 1,
            "warmup"   : 0,
            "cooldown" : 5,
        },
        "carbine" : {
            "fires" : "5.56mm",
            "rof"      : 3,
            "warmup"   : 0,
            "cooldown" : 15,
        },
        "gpmg" : {
            "fires" : "7.62mm",
            "rof"      : 5,
            "warmup"   : 0,
            "cooldown" : 20,
        },
        "usg" : {
            "fires" : "40mm",
            "rof"      : 1,
            "warmup"   : 10,
            "cooldown" : 15,
        },

    }