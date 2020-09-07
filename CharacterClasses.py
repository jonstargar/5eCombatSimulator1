from DamageConstructs import DamageDie
from ItemConstructs import Weapon, RangedWeapon


class BaseCreature:

  def __init__(self, team, name, hp, ac, proficiency, strength, dexterity, constitution, intelligence, wisdom, charisma):
    # give the base stats
    self.name = name
    self.hp = hp
    self.ac = ac
    self.proficiency = proficiency
    self.strength = strength
    self.dexterity = dexterity
    self.constitution = constitution
    self.intelligence = intelligence
    self.wisdom = wisdom
    self.charisma = charisma

    # give it its team
    self.team = team

    # build an array of weapons to add to
    self.weapons = []

    # armour slot
    self.armour = None

  def __str__(self):
    return 'Name: {}, HP: {}, AC: {}, Proficiency Bonus: {}, '\
           'Strength {}, Dexterity {}, Con: {},'\
           'Int: {}, Wis: {}, Charisma {}. Weapons: {}'.format(self.name,
                                                               self.hp,
                                                               self.ac,
                                                               self.proficiency,
                                                               self.strength,
                                                               self.dexterity,
                                                               self.constitution,
                                                               self.intelligence,
                                                               self.wisdom,
                                                               self.charisma,
                                                               self.weapons)

  def __repr__(self):
    return 'Team: {}, Name: {}, HP: {}, AC: {}'.format(self.team,
                                                       self.name,
                                                       self.hp,
                                                       self.ac)

  def give_melee_weapon(self, name, damage_die, damage_type, finesse, magic_bonus):
    weapon = Weapon(name, damage_die, damage_type, finesse, magic_bonus)
    self.weapons.append(weapon)

  def give_ranged_weapon(self, name, damage_die, damage_type, range, magic_bonus):
    ranged_weapon = RangedWeapon(name, damage_die, damage_type, range, True, magic_bonus)
    self.weapons.append(ranged_weapon)

  def give_light_armor(self, armor):
    self.ac = armor.ac + self.dex
    print(self.ac)

  def give_heavy_armor(self, armor):
    self.ac = armor.ac

  def get_bonus(self, stat_score):
    if stat_score <= 0:
      return 0
    else:
      return int(stat_score / 2) - 5
