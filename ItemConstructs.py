from DamageConstructs import DamageDie


class Weapon:

  def __init__(self, name, damage_die, damage_type, finesse, magic_bonus):
    self.name = name
    self.damage_die = DamageDie(damage_die, damage_type)
    self.finesse = finesse
    self.magic_bonus = magic_bonus

  def __str__(self):
    if self.magic_bonus is 0:
      return '{} with a d{} damage die'.format(self.name, self.damage_die)
    else:
      return '{} with a +{} weapon with a d{} damage die'.format(self.name,
                                                                 self.magic_bonus,
                                                                 self.damage_die)

  def __repr__(self):
    if self.magic_bonus is 0:
      return '{} with a {} damage die'.format(self.name, self.damage_die)
    else:
      return '{} with a +{} magic weapon with a {} damage die'.format(self.name,
                                                                      self.magic_bonus,
                                                                      self.damage_die)


class RangedWeapon(Weapon):

  def __init__(self, name, damage_die, damage_type, range, finesse, magic_bonus):
    self.name = name
    self.damage_die = DamageDie(damage_die, damage_type)
    self.finesse = finesse
    self.range = range
    self.magic_bonus = magic_bonus


class Armor:

  def __init__(self, name, ac_level):
    self.name = name
    self.ac = ac_level
