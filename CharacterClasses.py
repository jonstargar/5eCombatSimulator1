from DamageConstructs import DamageDie
from ItemConstructs import Weapon, RangedWeapon, MonsterWeapon
from random import choice, randint
import logging


class BaseCreature:

  def __init__(self, name, max_hp, level, strength, dexterity, constitution, intelligence, wisdom,
               charisma, attacks_per_action, bonus_action_attack, battle_style):
    # give the base stats
    self.name = name
    self.hp = max_hp
    self.current_hp = max_hp
    self.strength = strength
    self.dexterity = dexterity
    self.constitution = constitution
    self.intelligence = intelligence
    self.wisdom = wisdom
    self.charisma = charisma

    # Set the base AC of the character to 10 + DEX modifier
    self.ac = 10 + self.get_bonus(self.dexterity)

    # Get the number of attacks
    self.num_attacks = attacks_per_action
    if bonus_action_attack:
      self.num_attacks += 1

    # get the proficiency bonus based on the score
    if level < 5:
      self.proficiency = 2
    elif 5 <= level < 9:
      self.proficiency = 3
    elif 9 <= level < 13:
      self.proficiency = 4
    elif 13 <= level < 17:
      self.proficiency = 5
    else:
      self.proficiency = 6

    # build an array of weapons to add to
    self.weapons = []

    # armour slot
    self.armour = None

    # shield slot
    self.shield = None

    # give a preferred melee weapon slot
    self.preferred_melee_weapon = None

    # define battle behaviour
    self.battle_style = battle_style

  def __str__(self):
    return 'Name: {}, HP: {}, AC: {}, Proficiency Bonus: {}, ' \
           'Strength {}, Dexterity {}, Con: {},' \
           'Int: {}, Wis: {}, Charisma {}. Weapons: {}'.format(self.name,
                                                               self.current_hp,
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
    return 'Name: {}, HP: {}, AC: {}'.format(self.name,
                                             self.current_hp,
                                             self.ac)

  def give_melee_weapon(self, name, finesse, versatile, magic_bonus, damage_die):
    weapon = Weapon(name, finesse, versatile, magic_bonus, damage_die)
    self.weapons.append(weapon)

  def give_ranged_weapon(self, name, damage_die, damage_type, range, magic_bonus):
    ranged_weapon = RangedWeapon(name, damage_die, damage_type, range, True, magic_bonus)
    self.weapons.append(ranged_weapon)

  def give_light_armor(self, armor):
    self.ac = armor.ac + self.get_bonus(self.dex)
    logging.info(self.ac)

  def give_heavy_armor(self, armor):
    self.ac = armor.ac

  def get_bonus(self, stat_score):
    if stat_score <= 0:
      return 0
    else:
      return int(stat_score / 2) - 5

  def pick_target(self, potential_opponents):
    try:
      if self.previous_opponent.current_hp > 0:
        # TODO: insert logic to find out if the creature would change its previous target
        return self.previous_opponent
      else:
        return choice(potential_opponents)
    except AttributeError:
      # If there is no previous opponent then the creature must decide a new target
      return choice(potential_opponents)

  def get_relevant_bonus(self, weapon):
    # If strength is the best relevant ability modifier just use that even if the weapon is finesse
    if self.get_bonus(self.strength) > self.get_bonus(self.dexterity):
      relevant_stat_bonus = self.get_bonus(self.strength)
    # If the strength bonus is NOT greater and the weapon is finesse then use the dex bonus as bonus
    elif weapon.finesse:
      relevant_stat_bonus = self.get_bonus(self.dexterity)
    # This is essentially the base damage of a weapon, weapon damage + strength bonus
    else:
      relevant_stat_bonus = self.get_bonus(self.strength)
    return relevant_stat_bonus

  def get_average_melee_weapon_damage(self, damage_die):
    """takes in a list of damage die and returns an integer of the average damage."""
    average_damage = 0
    for die in damage_die:
      average_damage = average_damage + (damage_die / 2)
    return average_damage

  def choose_melee_weapon(self):
    """Picks and returns a weapon to use."""
    highest_average_damage = 0
    weapon_to_use = None
    for weapon in self.weapons:
      average_weapon_damage = 0
      if weapon.versatile and self.shield:
        average_weapon_damage = weapon.get_average_damage(True)
      else:
        average_weapon_damage = weapon.get_average_damage()
      logging.debug(str(weapon) + 'average weapon damage = '.format(str(average_weapon_damage)))

      weapon_bonus = self.get_relevant_bonus(weapon)
      logging.debug('strength or dexterity modifier: ' + str(weapon_bonus))
      logging.debug('average weapon damage' + str(average_weapon_damage))
      average_weapon_damage = average_weapon_damage + weapon_bonus
      logging.debug('average weapon damage' + str(average_weapon_damage))

      if average_weapon_damage > highest_average_damage:
        weapon_to_use = weapon

    self.preferred_melee_weapon = weapon_to_use
    return weapon_to_use

  def melee_attack(self, target):
    """Performs melee attack."""
    # If the creature has no preferred weapon, get the one with the highest average damage
    if not self.preferred_melee_weapon:
      weapon_to_use = self.choose_melee_weapon()
    else:
      weapon_to_use = self.preferred_melee_weapon

    damage_die = []
    damage = 0
    if not self.shield and weapon_to_use.versatile:
      damage_die = weapon_to_use.get_appropriate_damage_die(True)
    else:
      damage_die = weapon_to_use.get_appropriate_damage_die()

    flavor_text = '{} attacks with the {}'.format(self.name, weapon_to_use)

    critical_hit = False
    d20_roll = randint(1, 20)
    if d20_roll is 20:
      flavor_text = flavor_text + ' and CRITICAL HIT! Rolls '
      critical_hit = True

    if d20_roll is 1:
      flavor_text = flavor_text + ' and OH NO critical miss'
      return flavor_text

    d20_roll_plus_modifiers = d20_roll + weapon_to_use.magic_bonus \
                              + self.proficiency + self.get_relevant_bonus(weapon_to_use)

    if critical_hit:
      for die in damage_die:
        die_roll = randint(1, die.dice_size)
        damage = damage + die_roll
        flavor_text = flavor_text + str(die_roll) + '({})'.format(die.dice_size)
      for die in damage_die:
        die_roll = randint(1, die.dice_size)
        damage = damage + die_roll
        flavor_text = flavor_text + str(die_roll) + '({})'.format(die.dice_size)
    elif d20_roll_plus_modifiers < target.ac:
      flavor_text = flavor_text + ' and misses with a {}'.format(str(d20_roll_plus_modifiers))
      return damage, flavor_text
    else:
      for die in damage_die:
        die_roll = randint(1, die.dice_size)
        damage = damage + die_roll
        flavor_text = flavor_text + str(die_roll) + '({})'.format(str(die.dice_size))

    damage = damage + weapon_to_use.magic_bonus + self.get_relevant_bonus(weapon_to_use)
    flavor_text = flavor_text + ' dealing {} damage'.format(damage)
    target.current_hp = target.current_hp - damage

    return flavor_text


class BaseMonster(BaseCreature):
  def __init__(self, name, max_hp, strength, dexterity, constitution, intelligence, wisdom,
               charisma, attacks_per_action, bonus_action_attack, battle_style, ac):
    super().__init__(name, max_hp, 1, strength, dexterity, constitution, intelligence, wisdom,
               charisma, attacks_per_action, bonus_action_attack, battle_style)

    self.ac = ac

  def give_melee_weapon(self, name, to_hit_bonus, damage_bonus, damage_die):
    weapon = MonsterWeapon(name, to_hit_bonus, damage_bonus, damage_die)
    self.weapons.append(weapon)

  def melee_attack(self, target):
    flavor_text = self.name + ' attacks with '
    logging.info('Number of weapons that {} has is {}'.format(self.name, str(len(self.weapons))))
    if not self.weapons:
      flavor_text = flavor_text + 'fists'
      # TODO add fist logic
    weapon_to_use = None
    if len(self.weapons) > 1:
      weapon_to_use = choice(self.weapons)
    else:
      weapon_to_use = self.weapons[0]

    flavor_text = flavor_text + weapon_to_use.name
    attack_roll = randint(1, 20)

    critical_hit = False
    if attack_roll == 20:
      critical_hit = True
      flavor_text = flavor_text + ' ' + str(attack_roll) + ' CRITICAL HIT! + ' + str(weapon_to_use.to_hit_bonus)
    else:
      flavor_text = flavor_text + ' ' + str(attack_roll) + ' + ' + str(weapon_to_use.to_hit_bonus)

    attack_roll = attack_roll + weapon_to_use.to_hit_bonus

    damage = 0
    if not critical_hit and target.ac > attack_roll:
      flavor_text = flavor_text + ' and misses!'
      return flavor_text
    else:
      flavor_text = flavor_text + ' and rolls '
      for die in weapon_to_use.damage:
        die_roll = randint(1, die.dice_size)
        damage = damage + die_roll
        flavor_text = flavor_text + str(die_roll) + '({})'.format(die.dice_size)
      if critical_hit:
        for die in weapon_to_use.damage:
          die_roll = randint(1, die.dice_size)
          damage = damage + die_roll
          flavor_text = flavor_text + str(die_roll) + '({})'.format(die.dice_size)

    damage = damage + weapon_to_use.damage_bonus
    flavor_text = flavor_text + ' dealing {} damage!'.format(damage)
    target.current_hp = target.current_hp - damage
    if target.current_hp < 1:
      flavor_text = flavor_text + ' knocking {} down!'.format(target.name)

    return flavor_text
