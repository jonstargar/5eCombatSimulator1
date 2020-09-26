"""Simulates an encounter in D&D 5e combat and informs a DM how deadly the encounter is.

A D&D 5e encounter pits heroes against monsters (or sometimes other heroes!). The encounter is
designed by the Dungeon Master (DM). Maintaining a balance between the danger and survivability of
an encounter is imperative in maintaining the suspense in a battle. Too easy and the players would
win quickly and thus not feel any danger, too difficult and the players will die. It is such a balancing act!

If only you could know in advance how many times out of a hundred the players would die.

That is the purpose of this script. It will tell you if a battle was performed X times, how many times the
players win and how many times they die. For now that is most useful for testig if the encounter will
kill the players so you can tweak the opponents down a bit.

This script utilizes the SRD 5.1 and Open gaming License (OGL) from Wizards of the Coast available here:
https://media.wizards.com/2016/downloads/DND/SRD-OGL_V5.1.pdf
and in it's distributed form only uses SRD 5.1 content (such as the Hill Troll monster as opponent) and rules (such as
d20 system).

Modifications to this code must be held within the SRD 5.1 and Open Gaming License above and is subject to the GNU
AGPLv3

"""

from CharacterClasses import Monster, PlayerCharacter
from GameConstructs import Team
from random import randint
import logging


def d20_with_modifier(modifier=0):
  """Rolls a d20 (20 sided dice) and adds the given modifier.

  Args:
      modifier (int): The number to add the random roll to.

  Returns:
      roll: random number between 1 and 20 + the modifier
  """
  roll = randint(1, 20)
  logging.info('d20 roll is {} and the modifier is {}'.format(roll, modifier))
  roll = roll + modifier
  return roll


def are_there_any_opponents(own_team, initiative_order):
  """Returns True if there are any opponents still with health.

  Args:
      own_team (GameConstructs/Team): The team as reference to check if other teams have living combatants.
      initiative_order (list): A list of BaseCreature or its subclass objects all taking place in the combat.

  Returns:
      bool: If any members of other teams in the combat are alive return True, if not return False
  """
  for creature in initiative_order:
    if creature.team is own_team:
      continue
    else:
      if creature.current_hp > 0:
        return True
  # If we get here then there are no creatures with > 0 hit points of another team
  return False


def get_potential_opponents(teams, active_creature):
  """Returns a list of the potential opponents for a character.

  Args:
      teams (list): List of GameConstructs/Team participating in the combat.
      active_creature (BaseCreature or subclass of): The character who's turn it is in the combat order.

  Returns:
      list: The list of BaseCreature or subclass thereof that are viable targets of the active_creature.
  """
  potential_opponents = []

  for team in teams:
    if active_creature not in team.team_members:
      for creature in team.team_members:
        if creature.current_hp > 0:
          potential_opponents.append(creature)

  logging.info('{}s list of potential opponents: {}'.format(active_creature.name, potential_opponents))
  return potential_opponents


def print_initiative_order_and_character_state(combatants_with_initiative):
  """Prints and returns the combat initiative order and current state of the combat.

  Args:
      combatants_with_initiative (list): List of the combatants in the combat with BaseCreature and its subclasses
      with BaseCreature.initiative parameter.

  Returns:
      string: The state of the combat, including creature initiative order, HP etc.
  """
  initiative_order_string = '\nInitiative Order and Creature States:'
  initiative_number = 0
  for combatant in combatants_with_initiative:
    initiative_number += 1
    if combatant.current_hp > 0:
      initiative_order_string = initiative_order_string + '\n' + \
                                str(initiative_number) + '(' + str(combatant.initiative) + '): ' + repr(combatant)
    else:
      text = '\n' + str(initiative_number) + '(' + str(combatant.initiative) + '): ' + repr(combatant)
      struck_text = ''
      for char in text:
        struck_text = struck_text + char + '\u0336'
      initiative_order_string = initiative_order_string + struck_text

  print(initiative_order_string)
  logging.info(initiative_order_string)
  return initiative_order_string


def get_initiative_order(list_of_combatants):
  """Take in a list of combatants, roll initiative for each, return an ordered list.

  Args:
      list_of_combatants (list): A list of BaseCreature or its subclasses that will participate in the combat.

  Returns:
      initiative_order: A list of the combatants ordered by the reverse of the newly created BaseCreature.initiative
      parameter (so that the highest initiative is first and lowest is last).
  """
  initiative_order = []

  for character in list_of_combatants:
    logging.info('Character dexterity: {}, Character dexterity bonus: {}'.format(str(character.dexterity),
                 str(character.get_bonus(character.dexterity))))
    character.initiative = d20_with_modifier(character.get_bonus(character.dexterity))
    print('{} gets an initiative score of {}'.format(character.name, character.initiative))
    initiative_order.append(character)

  initiative_order.sort(key=lambda x: x.initiative, reverse=True)
  return initiative_order


def get_scores(teams):
  """Gets the text describing the current scores of which teams have won how many combats.

  Args:
      teams (list): List of GameConstructs/Teams objects.

  Returns:
      string: The text output of the current state of the multi-combat experience.
  """
  score_text = 'And the scores: '
  for team in teams:
    score_text = score_text + '\n{}: {}'.format(team.name, team.score)
  return score_text


def get_players():
  """Creates a list of BaseCreature or its subclasses to fight on the player team.

  Returns:
      list of BaseCreature or its subclasses: A list of creatures to fight on the player team.
  """

  team_members = []

  ancillary_characteristics = {'battle_style': 'berzerker',
                               'skill_proficiencies': ['athletics', 'deception'],
                               'resistances': ['fire']}

  geoff = PlayerCharacter('Geoff', 140, 18, 14, 14, 8, 13, 14, 2, ancillary_characteristics, 13)
  geoff.give_melee_weapon('greatclub', False, False, 1, [(10, 'bludgeoning')])
  geoff.give_light_armor('Studded Leather', 12)
  logging.info('creature 1: ' + str(geoff))
  team_members.append(geoff)

  dave = PlayerCharacter('Dave', 120, 14, 13, 15, 9, 12, 13, 1, ancillary_characteristics, 13, True)
  dave.give_melee_weapon('longsword of scalding', False, True, 1, [(8, 'slashing'), (10, 'slashing')])
  dave.give_shield('Kit Shield', 1)
  logging.info('creature 2: ' + str(dave))
  team_members.append(dave)

  bob = PlayerCharacter('Bob', 120, 14, 15, 14, 8, 13, 14, 1, ancillary_characteristics, 15)
  bob.give_melee_weapon('greataxe of sundering', False, False, 2, [(12, 'slashing')])
  logging.info('creature 3: ' + str(bob))
  team_members.append(bob)

  john = PlayerCharacter('John', 110, 20, 10, 15, 9, 12, 13, 2, ancillary_characteristics, 13)
  john.give_melee_weapon('greatsword', False, False, 0, [(6, 'slashing'), (6, 'slashing')])
  logging.info('creature 4: ' + str(john))
  team_members.append(john)

  return team_members


def get_monsters():
  """Creates a list of BaseCreature or its subclasses to fight on the monster team.
  Returns:
      list of BaseCreature or its subclasses: .
  """
  team_members = []

  giant1 = Monster('Hill Giant 1', 105, 23, 9, 21, 9, 10, 12, 2, 'berzerker', 15)
  giant1.give_melee_weapon('Greatclub', 8, 5, [(8, 'bludgeoning'), (8, 'bludgeoning'), (8, 'bludgeoning')])
  giant2 = Monster('Hill Giant 2', 105, 23, 9, 21, 9, 10, 12, 2, 'berzerker', 15)
  giant2.give_melee_weapon('Greatclub', 8, 5, [(8, 'bludgeoning'), (8, 'bludgeoning'), (8, 'bludgeoning')])
  giant3 = Monster('Hill Giant 3', 70, 23, 9, 21, 9, 10, 12, 2, 'berzerker', 15)
  giant3.give_melee_weapon('Greatclub', 8, 5, [(8, 'bludgeoning'), (8, 'bludgeoning'), (8, 'bludgeoning')])
  team_members.append(giant1)
  team_members.append(giant2)
  team_members.append(giant3)

  return team_members


def characters_from_multiple_teams_alive(teams):
  """Returns True if there are characters with > 0 hit points from multiple teams.

  Args:
      teams (list of GameConstructs/Team): The list of teams to check for alive combatants.

  Returns:
      bool: If there are living creatures from multiple teams this will return True, meaning the battle continues.
      Otherwise it returns False, allowing this iteration of the combat to end.
  """
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

  combat_attempts = 10

  for i in range(combat_attempts):
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
