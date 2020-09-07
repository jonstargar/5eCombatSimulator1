from CharacterClasses import BaseCreature
from random import randint


def d20_with_modifier(modifier=0):
  roll = randint(1, 20)
  print('d20 roll is {} and the modifier is {}'.format(roll, modifier))
  roll = roll + modifier
  return roll


def generate_character_with_base_stats(team, name, hp, ac, proficiency, strength, dexterity,
                                       constitution, intelligence, wisdom, charisma):
  character = BaseCreature(team, name, hp, ac, proficiency, strength, dexterity, constitution, intelligence,
                           wisdom, charisma)
  return character


def get_initiative_order(list_of_combatants):
  """take in a list of combatants, roll initiative for each, return an ordered list"""
  initiative_order = []

  for character in list_of_combatants:
    character.initiative = d20_with_modifier(character.get_bonus(character.dexterity))
    print('{} gets an initiative score of {}'.format(character.name, character.initiative))
    initiative_order.append(character)

  initiative_order.sort(key=lambda x: x.initiative)

  for i in initiative_order:
    print(i)

  return initiative_order


def main():

  creature1 = generate_character_with_base_stats('red', 'Geoff', 100, 15, 2, 14, 14, 14, 8, 13, 14)
  creature1.give_melee_weapon('axe', 6, 'slashing', False, 1)

  creature2 = generate_character_with_base_stats('blue', 'Dave', 90, 13, 3, 14, 13, 15, 9, 12, 13)
  creature2.give_melee_weapon('longsword', 8, 'slashing', False, 0)

  round_number = 0

  print(creature1)
  print(creature2)

  combatants = [creature1, creature2]

  get_initiative_order(combatants)

  while creature1.hp > 0 and creature2.hp > 0:

    round_number += 1
    print('Round {} FIGHT'.format(round_number))

    creature1_attack = d20_with_modifier(creature1.get_bonus(creature1.strength)
                                         + creature1.weapons[0].magic_bonus
                                         + creature1.proficiency)
    print('creature 1 attacks with a {}'.format(creature1_attack))

    if creature1_attack >= creature2.ac:
      damage = randint(1, creature1.weapons[0].damage_die.dice_size)
      damage = damage + creature1.get_bonus(creature1.strength)
      print('It HIT! dealing {} damage'.format(damage))
      creature2.hp = creature2.hp - damage
    else:
      print('It missed!')

    creature2_attack = d20_with_modifier(creature2.get_bonus(creature1.strength)
                                         + creature2.weapons[0].magic_bonus
                                         + creature2.proficiency)
    print('creature 2 attacks with a {}'.format(creature2_attack))

    if creature2_attack >= creature1.ac:
      damage = randint(1, creature2.weapons[0].damage_die.dice_size)
      damage = damage + creature2.get_bonus(creature1.strength)
      print('It HIT! dealing {} damage'.format(damage))
      creature1.hp = creature1.hp - damage
    else:
      print('It missed!')

    print('current state of battle: creature1 has {} HP, creature2 has {} HP'.format(creature1.hp, creature2.hp))


if __name__ == '__main__':
  main()