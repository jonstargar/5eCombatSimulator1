from DamageConstructs import DamageDie
from random import randint
import logging


class Weapon:

  def __init__(self, name, finesse, versatile, magic_bonus, damage_die, baseline_magic=False):
    self.name = name
    self.finesse = finesse
    self.versatile = versatile
    self.magic_bonus = magic_bonus
    self.tmp_damage_dice_list = []
    self.damage_dice_list = []
    for die in damage_die:
      self.tmp_damage_dice_list.append(die)
    for die in self.tmp_damage_dice_list:
      dice_size, damage_type = die
      self.damage_dice_list.append(DamageDie(dice_size, damage_type))
    self.magical = baseline_magic
    if magic_bonus > 0:
      self.magical = True

  def __str__(self):
    tmp_string = ''
    if self.magic_bonus > 0:
      tmp_string = tmp_string + '+ ' + str(self.magic_bonus) + ' magic'
    if self.versatile:
      tmp_string = tmp_string + ' versatile'
    if self.finesse:
      tmp_string = tmp_string + ' finesse'

    return '{} {} with {} damage'.format(self.name,
                                         tmp_string,
                                         self.damage_dice_list)

  def __repr__(self):
    tmp_string = ''
    if self.magic_bonus > 0:
      tmp_string = tmp_string + '+ ' + str(self.magic_bonus) + ' magic'
    if self.versatile:
      tmp_string = tmp_string + ' versatile'
    if self.finesse:
      tmp_string = tmp_string + ' finesse'

    return '{} {} with {} damage'.format(self.name,
                                         tmp_string,
                                         self.damage_dice_list)

  def get_appropriate_damage_die(self, two_handed=False):
    """."""
    damage_die = []
    if self.versatile:
      versatile_damage_die_choices = []
      for die in self.damage_dice_list:
        if die.damage_type is 'slashing' or 'bludgeoning' or 'piercing':
          versatile_damage_die_choices.append(die)
        else:
          damage_die.append(die)
      try:
        versatile_damage_die_choices.sort(key=lambda x: x.dice_size)
        logging.info('Versatile damage options: {}'.format(versatile_damage_die_choices))
        if two_handed:
          # if wearing a shield pick the lower damage die
          damage_die.append(versatile_damage_die_choices[-1])
        else:
          # if not, take the higher damage die
          damage_die.append(versatile_damage_die_choices[0])
      except AttributeError:
        print('Weapon is marked as versatile but does not have appropriate damage types of "slashing", '
              '"bludgeoning", or "slashing"')
    else:
      # if it is not a versatile weapon then we can count all the damage die
      damage_die = self.damage_dice_list
    return damage_die

  def get_average_damage(self, two_handed=False):
    """returns the average damage that the weapon deals."""
    damage = 0
    damage_die = self.get_appropriate_damage_die(two_handed)

    for die in damage_die:
      damage = damage + (die.dice_size / 2)
    return damage + self.magic_bonus

  def get_melee_damage(self, two_handed=False):
    """give the damage of the weapon (all rolls plus magic damage) and flavor text as a tuple."""
    damage = 0
    damage_die = self.get_appropriate_damage_die(two_handed)

    flavor_text = 'It rolls '
    for die in damage_die:
      dice_roll = randint(1, die.dice_size)
      flavor_text = flavor_text + str(dice_roll) + ' on the ' + str(die.dice_size) + ', and '
      damage = damage + dice_roll

    damage = damage + self.magic_bonus
    flavor_text = flavor_text[:-6]

    return damage, flavor_text


class RangedWeapon(Weapon):

  def __init__(self, name, magic_bonus, damage_die, range_short, range_long,  baseline_magic=False):
    self.name = name
    self.range = range
    self.magic_bonus = magic_bonus
    self.range_short = range_short
    self.range_long = range_long

    self.tmp_damage_dice_list = []
    self.damage_dice_list = []
    for die in damage_die:
      self.tmp_damage_dice_list.append(die)
    for die in self.tmp_damage_dice_list:
      dice_size, damage_type = die
      self.damage_dice_list.append(DamageDie(dice_size, damage_type))


class Armor:

  def __init__(self, name, ac_level, light=False):
    self.name = name
    self.ac = ac_level
    self.light = light


class Shield:

  def __init__(self, name, magic_bonus):
    self.name = name
    self.magic_bonus = magic_bonus


class MonsterWeapon:

  def __init__(self, name, to_hit_bonus, damage_bonus, damage_die, baseline_magic=False):
    self.name = name
    self.to_hit_bonus = to_hit_bonus
    self.damage_bonus = damage_bonus
    self.damage = []

    for die in damage_die:
      dice_size, damage_type = die
      new_die = DamageDie(dice_size, damage_type)
      self.damage.append(new_die)

    self.magical = baseline_magic
