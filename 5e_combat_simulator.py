from CharacterClasses import BaseCreature, BaseMonster
from DamageConstructs import DamageDie
from GameConstructs import Team
from random import randint
import logging


def d20_with_modifier(modifier=0):
  roll = randint(1, 20)
  logging.info('d20 roll is {} and the modifier is {}'.format(roll, modifier))
  roll = roll + modifier
  return roll


def generate_character_with_base_stats(name, max_hp, level, strength, dexterity,
                                       constitution, intelligence, wisdom, charisma, attacks_per_action,
                                       bonus_action_attack, battle_style):
  character = BaseCreature(name, max_hp, level, strength, dexterity, constitution, intelligence,
                           wisdom, charisma, attacks_per_action, bonus_action_attack, battle_style)
  return character


def are_there_any_opponents(own_team, initiative_order):
  """Returns True if there are any opponents still with health."""
  for creature in initiative_order:
    if creature.team is own_team:
      continue
    else:
      if creature.current_hp > 0:
        return True
  # If we get here then there are no creatures with > 0 hit points of another team
  return False


def get_potential_opponents(teams, active_creature):
  """Returns a list of the potential opponents for a character."""
  potential_opponents = []

  for team in teams:
    if active_creature not in team.team_members:
      for creature in team.team_members:
        if creature.current_hp > 0:
          potential_opponents.append(creature)

  logging.info('{}s list of potential opponents: {}'.format(active_creature.name, potential_opponents))
  return potential_opponents


def print_initiative_order_and_character_state(combatants_with_initiative):
  initiative_order_string = '\nInitiative Order and Creature States:'
  initiative_number = 0
  for combatant in combatants_with_initiative:
    initiative_number += 1
    if combatant.current_hp > 0:
      initiative_order_string = initiative_order_string + '\n' + str(initiative_number) + '(' + str(combatant.initiative) + '): ' + repr(combatant)
    else:
      text = '\n' + str(initiative_number) + '(' + str(combatant.initiative) + '): ' + repr(combatant)
      struck_text = ''
      for char in text:
        struck_text = struck_text + char + '\u0336'
      initiative_order_string = initiative_order_string + struck_text

  print(initiative_order_string)
  logging.info(initiative_order_string)
  return initiative_order_string


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

  initiative_order.sort(key=lambda x: x.initiative, reverse=True)
  return initiative_order


def get_scores(teams):
  score_text = 'And the scores: '
  for team in teams:
    score_text = score_text + '\n{}: {}'.format(team.name, team.score)
  return score_text


def get_players():

  team_members = []

  geoff = generate_character_with_base_stats('Geoff', 120, 13, 18, 14, 14, 8, 13, 14, 2, False, 'bezerker')
  geoff.give_melee_weapon('greatclub', False, False, 1, [(10, 'bludgeoning')])
  logging.info('creature 1: ' + str(geoff))
  team_members.append(geoff)

  dave = generate_character_with_base_stats('Dave', 130, 13, 14, 13, 15, 9, 12, 13, 1, True, 'composed')
  dave.give_melee_weapon('longsword of scalding', False, True, 1, [(8, 'slashing'), (10, 'slashing')])
  logging.info('creature 2: ' + str(dave))
  team_members.append(dave)

  bob = generate_character_with_base_stats('Bob', 160, 15, 14, 22, 14, 8, 13, 14, 1, False, 'strategic')
  bob.give_melee_weapon('greataxe of sundering', False, False, 2, [(12, 'slashing')])
  logging.info('creature 3: ' + str(bob))
  team_members.append(bob)

  john = generate_character_with_base_stats('John', 110, 13, 20, 22, 15, 9, 12, 13, 2, False, '')
  john.give_melee_weapon('greatsword', False, False, 0, [(6, 'slashing'), (6, 'slashing')])
  logging.info('creature 4: ' + str(john))
  team_members.append(john)

  return team_members


def get_monsters():
  """."""
  team_members = []

  giant1 = BaseMonster('Cloud Giant 1', 170, 29, 10, 22, 12, 16, 16, 2, False, 'berzerker', 14)
  giant1.give_melee_weapon('morningstar', 12, 8, [(8, 'piercing'), (8, 'piercing'), (8, 'piercing')])
  giant2 = BaseMonster('Cloud Giant 2', 170, 29, 10, 22, 12, 16, 16, 2, False, 'berzerker', 14)
  giant2.give_melee_weapon('morningstar', 12, 8, [(8, 'piercing'), (8, 'piercing'), (8, 'piercing')])
  # giant3 = BaseMonster('Cloud Giant 3', 200, 29, 10, 22, 12, 16, 16, 2, False, 'berzerker', 14)
  # giant3.give_melee_weapon('morningstar', 12, 8, [(8, 'piercing'), (8, 'piercing'), (8, 'piercing')])
  team_members.append(giant1)
  team_members.append(giant2)
  # monster_team.team_members.append(giant3)

  return team_members


def characters_from_multiple_teams_alive(teams):
  """Returns True if there are characters with > 0 hit points from multiple teams."""
  teams_with_characters_alive = 0
  for team in teams:
    current_team_alive = False
    for character in team.team_members:
      if character.current_hp > 0:
        current_team_alive = True
    if current_team_alive:
      teams_with_characters_alive += 1

  if teams_with_characters_alive > 1:
    return True
  else:
    return False


def main():

  logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(levelname)s : %(message)s',
                      filename='game_log.log', filemode='w+')

  # Get the teams
  player_team = Team('Players')
  monster_team = Team('Monsters')
  teams = [player_team, monster_team]

  for i in range(100):
    # reset the team members
    player_team.team_members = get_players()
    monster_team.team_members = get_monsters()

    # All the combatants to send for initiative oder
    combatants = []

    for player in player_team.team_members:
      combatants.append(player)
    for monster in monster_team.team_members:
      combatants.append(monster)
    initiative_order = get_initiative_order(combatants)

    round_number = 0

    while characters_from_multiple_teams_alive(teams):

      print_initiative_order_and_character_state(initiative_order)

      round_number += 1
      print('\nRound {} FIGHT!\n'.format(round_number))

      for creature in initiative_order:
        if creature.current_hp < 1:
          logging.info('{} is down'.format(creature.name))
          continue
        potential_targets = get_potential_opponents(teams, creature)

        if not potential_targets:
          break

        target = creature.pick_target(potential_targets)
        print('{} targets {} {} times'.format(creature.name, target.name, creature.num_attacks))
        for attack in range(creature.num_attacks):
          text = creature.melee_attack(target)
          print(text)
          if target.current_hp < 1:
            print('Putting {} on death saving throws!'.format(target.name))
            break

      if not characters_from_multiple_teams_alive(teams):
        # find the team with living members
        for team in teams:
          for creature in team.team_members:
            if creature.current_hp > 0:
              team.score += 1
              break
      print('Player wins: {}'.format(str(player_team.score)))
      print('Monster wins: {}'.format(str(monster_team.score)))

  print(get_scores(teams))


if __name__ == '__main__':
  main()