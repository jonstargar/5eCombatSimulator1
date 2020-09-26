from DamageConstructs import DamageDie
from ItemConstructs import Weapon, RangedWeapon, MonsterWeapon, Armor, Shield
from random import choice, randint
import logging


class BaseCreature:
  """A class containing the base attributes and actions available of a creature in a combat scenario for 5e d&d.

  This is the super class of any combatant in the fight automator tool '5e_combat_simulator.py'. Objects of this class
  can have all the attributes needed to fulfil a combat encounter. Its subclasses add features specific to a character
  class or monster ability.

  Create a BaseCreature like so:
  creature = BaseCreature('NAME', Max_HP, Level, Str, Dex, Con, Int, Wis, Cha, Attacks_per_round,
  ancillary_characteristics)
  """

  def __init__(self, name, max_hp, strength, dexterity, constitution, intelligence, wisdom, charisma,
               attacks_per_action, ancillary_characteristics):
    """Creating objects of this class need many attributes in order to complete a combat.

    Args:
        name (str): The name of the creature.
        max_hp (int): The max hit points of the creature.
        strength (int): The strength score of the creature.
        dexterity (int): The dexterity score of the creature.
        constitution (int): The constitution score of the creature.
        intelligence (int): The intelligence score of the creature.
        wisdom (int): The wisdom score of the creature.
        charisma (int): The charisma score of the creature.
        attacks_per_action (int): The number of attacks the creature can make per round as an ACTION.
    """

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

    # build an array of weapons to add to
    self.weapons = []

    # give a preferred melee weapon slot
    self.preferred_melee_weapon = None

    try:
      self.battle_style = ancillary_characteristics['battle_style']
    except (KeyError, TypeError):
      self.battle_style = ''

    try:
      self.resistances = ancillary_characteristics['resistances']
    except (KeyError, TypeError):
      self.resistances = []

    try:
      self.resistances = ancillary_characteristics['immunities']
    except (KeyError, TypeError):
      self.immunities = []

  def deal_damage(self, damage, type):
    """Deals damage to this creature. If the creature is resistant it will half the damage.

    Args:
        damage (int): the integer number of the damage before it is modified by resistances etc.
        type (str): A string representing the damage that the creature takes.
    """
    if type in self.resistances:
      damage = int(damage / 2)
    if type in self.immunities:
      damage = 0
    self.current_hp = self.current_hp - damage

  def get_bonus(self, stat_score):
    """Gets the modifier of a certain ability.

    The modifier of a given stat score is half of the score minus five and that is how the skills are derived.
    e.g. a strength score of 14 returns +2 or a 7 returns -2.
    TODO: retool this to receive a string of the ability score and get that from the object attributes

    Args:
        stat_score (int): The integer score of the parameter.

    Returns:
        The modifier of the attribute.
    """
    if stat_score <= 0:
      return 0
    else:
      return int(stat_score / 2) - 5

  def pick_target(self, potential_opponents):
    """basic logic for a creature to determine what its target is.

    Args:
        potential_opponents (`list` of :obj:`BaseCreature` or subclasses): A list of BaseCreature or subclass objects
          that are potential targets of the current creature.

    Returns:
      :obj: `BaseCreature` or subclasses: The target of the current attack
    """
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
    """Depending on the weapon, the bons used for attack rolls may be strength or dexterity.

    This determines which of those abilities to use for the selected weapon

    Args:
        weapon (:obj: Weapon): The weapon that the creature is using for the attack.

    Returns:
        (int): The best ability score bonus that the creature has for the given weapon.
    """
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
    """Takes in a list of damage die and returns an integer of the average damage.

    Args:
        damage_die (list of :obj:DamageDie): A list of DamageDie objects for which to get the average damage, therefore
        choosing the one with the highest average damage.

    Returns:
        The calculated average damage of the damage die, and adding the relevant bonus (strength or dex depending on
        the ability scores of the creature.
    """
    average_damage = 0
    for die in damage_die:
      average_damage = average_damage + (die.dice_size / 2)
    return average_damage

  def choose_melee_weapon(self):
    """Picks and returns a weapon to use.

    Returns:
        (:obj:Weapon) Picks the best weapon based on the creatures ability scores and the power of the weapons.
    """
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


class PlayerCharacter(BaseCreature):
  """A class containing the base attributes for combat PLUS some specific for player characters.

  Create a PlayerCharacter like so:
  creature = PlayerCharacter('NAME', Max_HP, Str, Dex, Con, Int, Wis, Cha, Attacks_per_round, ancillary_characteristics
  Bonus_action_attack)
  """

  def __init__(self, name, max_hp, strength, dexterity, constitution, intelligence, wisdom,
               charisma, attacks_per_action, ancillary_characteristics, level, bonus_action_attack=False):
    """Creating objects of this class has the same attributes needed as BaseCreature object plus its level.

    Args:
        name (str): The name of the creature.
        max_hp (int): The max hit points of the creature.
        strength (int): The strength score of the creature.
        dexterity (int): The dexterity score of the creature.
        constitution (int): The constitution score of the creature.
        intelligence (int): The intelligence score of the creature.
        wisdom (int): The wisdom score of the creature.
        charisma (int): The charisma score of the creature.
        attacks_per_action (int): The number of attacks the creature can make per round as an ACTION.
        level (int): The character level determines the proficiency bonus (applies to weapon attacks, skills etc when
          they are proficient)
        bonus_action_attack (bool, optional): Some PCs get a weapon attack as a bonus action, which may increase their
          attacks per round (e.g. War cleric, monk etc)
    """
    # call the super class for the base stats and shared attributes
    super().__init__(name, max_hp, strength, dexterity, constitution, intelligence, wisdom, charisma,
                     attacks_per_action, ancillary_characteristics)

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

    # If the PC can use a bonus action to attack (such as War domain Cleric, Monk) We add one to the total attacks
    if bonus_action_attack:
      self.num_attacks += 1

    # define battle behaviour
    try:
      self.battle_style = ancillary_characteristics['battle_style']
    except (KeyError, TypeError):
      self.battle_style = ''

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

  def give_melee_weapon(self, name, finesse, versatile, magic_bonus, damage_die, baseline_magic=False):
    """Gives the Player creature a weapon to add to their self.weapon list.

    Args:
        name (str): The name of the weapon.
        finesse (bool): If the weapon has the finesse property this should be True. Finesse allows the creature to use
          their dexterity bonus instead of strength as weapon ability
        versatile (bool): If the weapon is versatile it may be used one or two handed, and the damage die changes
          depending on whether the creature is using a shield.
        magic_bonus (int): If the weapon has a magical bonus e.g. a +1 longsword this property defines the magical
          bonus.
        damage_die (list of :obj:DamageDie): Defines the damage die of the weapon.
        baseline_magic (bool): If the weapon is magical then it overcomes certain resistances.
    """
    weapon = Weapon(name, finesse, versatile, magic_bonus, damage_die, baseline_magic)
    self.weapons.append(weapon)

  def give_ranged_weapon(self, name, magic_bonus, damage_die, range_short, range_long, baseline_magic=False):
    """Give the creature a ranged weapon.

    Args:
        name (str): The name of the weapon.
        magic_bonus (int): If the weapon has a magical bonus e.g. a +1 longsword this property defines the magical
          bonus.
        damage_die (list of :obj:DamageDie): Defines the damage die of the weapon.
        range_short (int): The short range of the weapon (within which there is no disadvantage applied)
        range_long (int): The long range of the weapon, after which the weapon is ineffective. If the target is between
          the short and long range values the attack has disadvantage.
        baseline_magic (bool): If the weapon is magical then it overcomes certain resistances.
    """
    ranged_weapon = RangedWeapon(name, magic_bonus, damage_die, range_short, range_long, baseline_magic)
    self.weapons.append(ranged_weapon)

  def give_light_armor(self, name, base_ac):
    """Gives the player character light armour and applies the relevant new Armour Class (AC).

    Args:
        name (str): The name of the armour.
        base_ac (int): The base AC of the armour. For example leather armour has a base AC of 12 + the creatures
          dexterity modifier.
    """
    # To avoid lowering the AC set the minumum AC to 10 + dexterity modifier
    if base_ac < 10:
      base_ac = 10
    armor = Armor(name, base_ac, True)
    self.armour = armor
    self.ac = armor.ac + self.get_bonus(self.dexterity)
    if self.shield:
      self.ac = self.ac + 2 + self.shield.magic_bonus
    logging.info('BaseCreature.give_light_armor: {} AC becomes {}'.format(self.name, str(self.ac)))

  def give_heavy_armor(self, name, base_ac):
    """Gives the player character heavy or medium armour which base value is the new Armour Class (AC).

    Args:
        name (str): The name of the armour.
        base_ac (int): The base AC of the armour. For example leather armour has a base AC of 12 + the creatures
          dexterity modifier.
    """
    # To avoid lowering the AC set the minumum AC to 10 + dexterity modifier
    if base_ac < 10:
      base_ac = 10
    armor = Armor(name, base_ac)
    self.armour = armor
    self.ac = armor.ac
    if self.shield:
      self.ac = self.ac + 2 + self.shield.magic_bonus
    logging.info('BaseCreature.give_heavy_armor: {} AC becomes {}'.format(self.name, str(self.ac)))

  def give_shield(self, name, magic_bonus=0):
    """Gives the creature a shield and applies the new AC for holding a shield (baseline of +2 plus the magic bonus).

    Args:
        name (str): The name of the shield.
        magic_bonus (int): If the shield is magical it further .
    """
    shield = Shield(name, magic_bonus)
    if self.shield:
      if self.shield.magic_bonus > magic_bonus:
        return

    self.shield = shield
    self.ac = self.ac + 2 + shield.magic_bonus

  def melee_attack(self, target):
    """Performs melee attack.

    Args:
        target (:obj:BaseCreature or subclass): The target of the melee attack.
    """
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


class Monster(BaseCreature):
  """A class containing the base attributes for combat PLUS some specific for monsters or other generic creatures.

  Create a Monster like so:
  creature = Monster('NAME', Max_HP, Str, Dex, Con, Int, Wis, Cha, Attacks_per_round, ancillary_characteristics, AC)
  """

  def __init__(self, name, max_hp, strength, dexterity, constitution, intelligence, wisdom,
               charisma, attacks_per_action, ancillary_characteristics, ac):
    """Creating objects of this class has the same attributes needed as BaseCreature object plus monster properties.

    Args:
        name (str): The name of the creature.
        max_hp (int): The max hit points of the creature.
        strength (int): The strength score of the creature.
        dexterity (int): The dexterity score of the creature.
        constitution (int): The constitution score of the creature.
        intelligence (int): The intelligence score of the creature.
        wisdom (int): The wisdom score of the creature.
        charisma (int): The charisma score of the creature.
        attacks_per_action (int): The number of attacks the creature can make per round as an ACTION.
        ac (int): The AC of the creature. Monsters typically have a pre-defined AC instead of dynamic defined like
          players with different types of armour or shields
    """
    super().__init__(name, max_hp, strength, dexterity, constitution, intelligence, wisdom,
                     charisma, attacks_per_action, ancillary_characteristics)

    self.ac = ac

  def give_melee_weapon(self, name, to_hit_bonus, damage_bonus, damage_die, baseline_magic=False):
    """Gives the Monster creature a weapon to add to their self.weapon list.

    Args:
        name (str): The name of the weapon.
        to_hit_bonus (int): The bonus for the attack roll of the given weapon.
          their dexterity bonus instead of strength as weapon ability
        damage_bonus (int): The damage bonus of attacking with this weapon.
        damage_die (list of :obj:DamageDie): Defines the damage die of the weapon.
        baseline_magic (bool): If the weapon is magical then it overcomes certain resistances.
    """
    weapon = MonsterWeapon(name, to_hit_bonus, damage_bonus, damage_die, baseline_magic)
    self.weapons.append(weapon)

  def melee_attack(self, target):
    """Performs melee attack.

    Args:
        target (:obj:BaseCreature or subclass): The target of the melee attack.
    """
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
