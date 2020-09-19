class DamageDie:

  def __init__(self, dice_size, damage_type):
    self.dice_size = dice_size
    self.damage_type = damage_type

  def __repr__(self):
    return 'd{} {}'.format(self.dice_size, self.damage_type)

  def __str__(self):
    return 'd{} {}'.format(self.dice_size, self.damage_type)
