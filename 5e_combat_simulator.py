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


def get_number_and_names_of_teams(combatants):
  """Returns a tuple containing the number of teams and list of names as second entry in tuple."""
  num_teams = 0
  team_names = []
  for combatant in combatants:
    try:
      if combatant.team_name not in team_names:
        team_names.append(combatant.team_name)
        num_teams += 1
    except AttributeError:
      print('ERROR ---Object did not have a team_name property---')
      return num_teams, team_names

  print('Number of teams: {}, Team names: {}'.format(num_teams, team_names))
  return num_teams, team_names


def get_potential_opponents(own_team, combatants):
  """Returns a list of the potential opponents for a character."""
  potential_opponents = []
  for combatant in combatants:
    if combatant.team is not own_team:
      if combatant.hp > 0:
        potential_opponents.append(combatant)
  print('List of potential opponents: {}'.format(potential_opponents))
  return potential_opponents


def print_initiative_order_and_character_state(characters_with_initiative):
  initiative_order_string = '\nInitiative Order:'
  initiative_number = 0
  for character in characters_with_initiative:
    initiative_number += 1
    initiative_order_string = initiative_order_string + '\n' + str(initiative_number) + ': ' + repr(character)
  print(initiative_order_string)


def get_remaining_team_numbers(combatants):
  """Returns a list of tuples containing the names of teams alongside the number of remaining members of the team."""
  team_names = []
  # Array of tuples containing the team name and their numbers
  team_numbers = []
  for combatant in combatants:
    current_team_name = combatant.team_name
    if current_team_name not in team_names:
      team_names.append(combatant.team_name)

  for team in team_names:
    number_in_team = 0
    for combatant in combatants:
      if team is combatant.team_name:
        number_in_team += 1
    team_and_number = (team, number_in_team)
    print(team_and_number)
    team_numbers.append(team_and_number)

  return team_numbers


def get_initiative_order(list_of_combatants):
  """take in a list of combatants, roll initiative for each, return an ordered list"""
  initiative_order = []

  for character in list_of_combatants:
    character.initiative = d20_with_modifier(character.get_bonus(character.dexterity))
    print('{} gets an initiative score of {}'.format(character.name, character.initiative))
    initiative_order.append(character)

  initiative_order.sort(key=lambda x: x.initiative)
  return initiative_order


def main():

  creature1 = generate_character_with_base_stats('red', 'Geoff', 100, 15, 2, 14, 14, 14, 8, 13, 14)
  creature1.give_melee_weapon('axe', 6, 'slashing', False, 1)

  creature2 = generate_character_with_base_stats('blue', 'Dave', 90, 13, 3, 14, 13, 15, 9, 12, 13)
  creature2.give_melee_weapon('longsword', 8, 'slashing', False, 0)

  creature3 = generate_character_with_base_stats('red', 'Bob', 100, 15, 2, 14, 14, 14, 8, 13, 14)
  creature3.give_melee_weapon('axe', 6, 'slashing', False, 1)

  creature4 = generate_character_with_base_stats('blue', 'John', 90, 13, 3, 14, 13, 15, 9, 12, 13)
  creature4.give_melee_weapon('longsword', 8, 'slashing', False, 0)

  round_number = 0
  combatants = [creature1, creature2, creature3, creature4]
  initiative_order = get_initiative_order(combatants)

  while creature1.hp > 0 and creature2.hp > 0:

    print_initiative_order_and_character_state(initiative_order)

    round_number += 1
    print('\nRound {} FIGHT!\n'.format(round_number))

    for creature in initiative_order:
      print(creature)
      potential_targets = get_potential_opponents(creature.team, initiative_order)

    break


if __name__ == '__main__':
  main()