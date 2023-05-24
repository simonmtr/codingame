import sys
import math
from enum import Enum

"""
logic to implement:
    - get x and y of the monster if not changed and see when hero will reach to know where to go

    - get list of all monsters with values specific for this hero
        - range from him
        - range from base
        - 

every hero checks:
    - before action:
        - if no monster is in sight -> look for monster
        - if monster is in range with target my_base -> control towards just outside of enemy base radius (so it wont target enemy base) (lower or upper side depending on where monster is)
    - after action:
        - if MOVE:
            - is there a different monster that can also be attacked?
                -> YES: move towards middle

every defender:
 - if enemy is in my base
    - play defensively and go to base
defender 0:
 - check 'monsterWouldTakeMyLife': if yes -> do wind if no shield and attack if shield
 - if enemy is 6000 in range of base -> attack that enemy
    - if wind would take it out of base -> do wind in correct direction
    - if not in range -> attack enemy
 - attacking nearest enemy
    - if he can kill -> add to a 'nearest_monster_attacked_will_be_killed' list so no other hero attacks
defender dmg:
 - defending defender 0
    - if enemy is in range to control defender 0 -> control enemy away
    - else: do what defender 0 does

score/attack:
 - get mana in the middle
 - attack nearest monster with priority to attack as many monsters as possible
 - round x(110 maybe) -> get offensive
    - do attacking stuff as seen below (works quite good already)


save:
==
if monsterWouldTakeMyLife(hero_id, monster_id, value[3]) and my_mana >= 10 and shield_value == 0 and not wind_for_defense_used[monster_id]:
    print("monster " + str(monster_id) + " would take life", file=sys.stderr, flush=True)
    wind_for_defense_used[monster_id] = True
    useWindSpellTowardsEnemyBaseByHero(hero_id)
    return
==
---

"""


# seed: seed=3459494860964988900
#------------------------------------------------------------------#
def setHeroToModeV2(hero_id, mode):
    if mode == "score-and-attack":
        monster_in_sight = monster_in_sight_score_and_attack
    elif mode == "defend-only":
        monster_in_sight = monster_in_sight_defend_only
    elif mode == "defend-and-protect":
        monster_in_sight = monster_in_sight_defend_and_protect
# GENERAL FOR EVERY HERO
    # PATROULLING
    distance_hero_to_my_base = distanceBetween(hero_id, -1, -1, -1, -1, GetDistance.HERO_TO_MY_BASE)
    if not monster_in_sight and distance_hero_to_my_base < maxDistanceForRole[mode]:
        patroullingFor(hero_id, mode)
        return
# GENERAL FOR DEFENSE 
    if mode == "defend-only" or mode == "defend-and-protect":
        # SHIELDING
        if applyShieldIfNecessaryDefender(hero_id):
                return
        # CONTROLLING
        monster_in_range_with_my_base_as_target = anyMonsterInRangeOfHeroWithMyBaseAsTarget(hero_id)
        monster_controlled_shortly = monster_in_range_with_my_base_as_target in monster_was_controlled_shortly
        if my_mana >= 10 and monster_in_range_with_my_base_as_target != -1 and not monster_controlled_shortly:
            monster_health = getMonsterHealth(monster_in_range_with_my_base_as_target)
            if monster_health > 10:
                controlMonsterTowardsEnemyBaseRadius(hero_id, monster_in_range_with_my_base_as_target)
                return
        # WIND
        monster_would_target_my_base_next_turn = anyMonsterWouldTargetMyBaseNextTurnAndIsInRangeToWind(hero_id)
        if my_mana >= 10 and monster_would_target_my_base_next_turn != -1:
            monster_health = getMonsterHealth(monster_would_target_my_base_next_turn)
            if monster_health > 10:
                windMonsterTowardsEnemyBaseRadius(hero_id, monster_would_target_my_base_next_turn)
            return
# SPECIFIC FOR ROLE
    if mode == "score-and-attack":
        if mana >= 150 or getGameStage() > 2:
            useSpellsOnMonstersNearToEnemyBase(hero_id)
        # if getGameStage() >= 2:
        #     useSpellsOnMonstersNearToEnemyBase(hero_id)
        else: # remove one part of if
            getMostMana(hero_id)
        return
    elif mode == "defend-only":
        moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id)
        return
    elif mode == "defend-and-protect":
        counter_attack_to_defend_defender_0 = anyEnemyInRangeToControlDefendOnly()
        endangered_hero_id = counter_attack_to_defend_defender_0[0]
        enemy_hero_id_that_can_control_defender = counter_attack_to_defend_defender_0[1]
        if not monster_in_sight:
            patroullingFor(hero_id, mode)
            return
        elif enemy_hero_id_that_can_control_defender != -1 and my_heroes[endangered_hero_id][3] > 1:
            if controlEnemyAttacker(hero_id, endangered_hero_id, enemy_hero_id_that_can_control_defender):
                print("can control enemy attacker", file=sys.stderr, flush=True)
                return
            #moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id)
        elif canUseControlSpellOnEnemyToDefend(hero_id): 
            return
        elif canUseWindSpellOnEnemyToDefend(hero_id):
            return
        moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id)
        return
    return

# COMMANDS
def commandControl(hero_id, monster_id, coordinates, battle_cry):
    moves_for_hero_dict[hero_id] = f"SPELL CONTROL {monster_id} {coordinates[0]} {coordinates[1]} {battle_cry}"
    monster_was_controlled_shortly[monster_id] = getMonsterControlCooldown()
def commandControlEnemy(hero_id, enemy_hero_id, coordinates, battle_cry):
    moves_for_hero_dict[hero_id] = f"SPELL CONTROL {enemy_hero_id} {coordinates[0]} {coordinates[1]} {battle_cry}"
def commandWind(hero_id, coordinates, battle_cry):
    moves_for_hero_dict[hero_id] = f"SPELL WIND {coordinates[0]} {coordinates[1]} {battle_cry}"
def commandMove(hero_id, coordinates, battle_cry):
    moves_for_hero_dict[hero_id] = f"MOVE {coordinates[0]} {coordinates[1]} {battle_cry}"
def commandMoveTowardsTwoMonsterToAttack(hero_id, monster_id_1, monster_id_2):
    x_to_move_to = 0
    y_to_move_to = 0
    x_monster_1 = monsters[monster_id_1][1]
    y_monster_1 = monsters[monster_id_1][2]
    x_monster_2 = monsters[monster_id_2][1]
    y_monster_2 = monsters[monster_id_2][2]
    x_to_move_to = (x_monster_1 + x_monster_2) / 2
    y_to_move_to = (y_monster_1 + y_monster_2) / 2
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_to_move_to))) + " " + str(abs(int(y_to_move_to)))
def commandShield(hero_id, entity_id, battle_cry):
    moves_for_hero_dict[hero_id] = f"SPELL SHIELD {hero_id} {battle_cry}" 


# SPELLS
def controlMonsterTowardsEnemyBaseRadius(hero_id, monster_id):
    coordinates = getEnemyBaseRadiusCoordinates(monster_id)
    commandControl(hero_id, monster_id, coordinates, " control")
    return True
def windMonsterTowardsEnemyBaseRadius(hero_id, monster_id):
    coordinates = getEnemyBaseRadiusCoordinates(monster_id)
    commandWind(hero_id, coordinates, " wind")

def canUseSpellToAnnoy(hero_id):
    if canUseWindSpellToAnnoy(hero_id): # will likely never happen
        print("canUseWindSpellToAnnoy", file=sys.stderr, flush=True)
        return True
    if canUseControlSpellToAnnoy(hero_id): # will likely never happen
        print("canUseControlSpellToAnnoy", file=sys.stderr, flush=True)
        return True
    if canUseShieldSpellToAnnoy(hero_id): # will likely never happen
        return True
    return False

def canUseWindSpellToAnnoy(hero_id):
    return False

def canUseShieldSpellToAnnoy(hero_id):
    return_value = False
    for monster_id, value in monsters.items():
        monster_distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
        monster_distance_needed_for_kill_if_one_enemy_is_there = (12 * 400) + 300
        shield_value = value[3]
        monster_health = value[5]
        if monster_distance_to_enemy_base < monster_distance_needed_for_kill_if_one_enemy_is_there and monster_health > 10 and not shield_value > 0:
            moveHeroTowardsMonsterToShieldNearEnemyBase(hero_id, monster_id)
            return_value = True
    return return_value

def canUseControlSpellToAnnoy(hero_id):
    return_value = False
    for monster_id, value in monsters.items():
#        print("canusecontrolspelltoannoy", file=sys.stderr, flush=True)
        if not isMonsterFacingEnemyBase(hero_id, monster_id) and not return_value:
            return_value = moveHeroTowardsMonsterToControlTowardsEnemyBase(hero_id, monster_id)            
    return return_value

def isMonsterFacingEnemyBase(hero_id, monster_id):
    monster_x = monsters[monster_id][1]
    monster_y = monsters[monster_id][2]
    monster_vx = monsters[monster_id][6]
    monster_vy = monsters[monster_id][7]
    distance_between_monster_and_enemy_base = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
    distance_between_monster_and_enemy_base_future = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE_FUTURE)
    if abs(distance_between_monster_and_enemy_base - distance_between_monster_and_enemy_base_future) > 400:
        print("FALSE: isMonsterFacingEnemyBase " + str(monster_id), file=sys.stderr, flush=True)
        return False
#    print("TRUE: isMonsterFacingEnemyBase", file=sys.stderr, flush=True)
    return True

def canUseSpellToActivateMonsterTowardsEnemyBase(hero_id):
    if canUseWindSpellToActivateMonsterTowardsEnemyBase(hero_id):
        return True
    if canUseControlSpellToActivateMonsterTowardsEnemyBase(hero_id):
        return True
    return False

def canUseSpellToTakeLife(hero_id):
    if canUseWindSpellOnEnemyToTakeLife(hero_id):
        return True
    if canUseControlSpellOnEnemyToTakeLife(hero_id): 
        return True
    if canUseShieldSpellToTakeLife(hero_id):
        return True
    if canUseWindSpellToTakeLife(hero_id):
        return True
    return False

def canUseControlSpellOnEnemyToTakeLife(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToControl(hero_id)
    if enemy_id_near_hero != -1:
        for monster_id, value in monsters.items():
            monster_health = value[5]
            enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
            damage_taken_in_two_rounds = enemy_and_own_heroes_in_range_of_monster * 2 * 2
            remaining_monster_health = monster_health - damage_taken_in_two_rounds
            distance_to_enemy_base = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
            if my_mana >= 10 and remaining_monster_health > 6 and distance_to_enemy_base < 5000 and not enemy_heroes[enemy_id_near_hero][3] > 0:
                commandControlEnemy(hero_id, enemy_id_near_hero, [my_base_x,my_base_y]," O:")
                return_value = True
    return return_value

def enemyNearHeroToControl(hero_id):
    for enemy_hero_id, value in enemy_heroes.items():
        distance_between_hero_and_enemy = distanceBetween(hero_id, -1, enemy_hero_id, -1, -1, GetDistance.HERO_TO_ENEMY)
        if distance_between_hero_and_enemy <= 2200:
            return enemy_hero_id
    return -1

def canUseWindSpellToActivateMonsterTowardsEnemyBase(hero_id):
    return_value = False
    print("trying wind", file=sys.stderr, flush=True)
    for monster_id, value in monsters.items(): # - 2200 - 5000
        distance_to_enemy_base = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
        in_range_for_wind = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO)
        if not value[3] > 0 and distance_to_enemy_base  >= 2200 + 5000 and in_range_for_wind:
            return_value = moveHeroTowardsMonsterToWindTowardsEnemyBase(hero_id, monster_id, "ACTIVATE TARGET!")
        else:
            return_value = False
    return return_value

def moveHeroTowardsMonsterToWindTowardsEnemyBase(hero_id, monster_id, extra_command):
    in_range_to_get_winded = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO)
    if in_range_to_get_winded:
        print("monster id for spell", file=sys.stderr, flush=True)
        moves_for_hero_dict[hero_id] = "SPELL WIND " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " " + extra_command
        return True
    else:
        hero_kill_monster[hero_id] = monster_id
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(monsters[monster_id][1] + monsters[monster_id][6])) + " " + str(abs(monsters[monster_id][2] + monsters[monster_id][7]))
        return True
    return False

def canUseControlSpellToActivateMonsterTowardsEnemyBase(hero_id):
    return_value = False
    for monster_id, value in monsters.items():
        monster_distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
        if (monster_distance_to_enemy_base - 5000) - 400 <= 0 and not return_value:
            return_value = moveHeroTowardsMonsterToControlTowardsEnemyBase(hero_id, monster_id)
    return return_value

def moveHeroTowardsMonsterToControlTowardsEnemyBase(hero_id, monster_id):
    monster_distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
    monster_distance_to_enemy_base_future = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE_FUTURE)
    in_range_to_get_controlled = isInRangeOf(hero_id, -1, -1, monster_id, InRange.CONTROL_BY_HERO)
    if in_range_to_get_controlled and monster_distance_to_enemy_base > 5000 and monster_distance_to_enemy_base_future < (1100 + 7100) and not monster_id in monster_was_controlled_shortly:
        commandControl(hero_id, monster_id, [enemy_base_x, enemy_base_y], " P")
        return True
    else:
        hero_kill_monster[hero_id] = monster_id
        x_and_y_to_move_to = willMoveGeneric(monster_id)
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1]))) + " :S"
        return False

def canUseShieldSpellToTakeLife(hero_id):
    return_value = False
    for monster_id, value in monsters.items():
        monster_distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
        monster_distance_needed_for_kill = (12 * 400) + 300
        monster_steps_to_base = int(((monster_distance_to_enemy_base - 300)/400))
        monster_health = value[5]
        enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
        monster_health_remaining = monster_health - (monster_steps_to_base * (enemy_and_own_heroes_in_range_of_monster * 2))
        shield_value = value[3]

        if not return_value and monster_distance_to_enemy_base < monster_distance_needed_for_kill and monster_health_remaining > 0 and not shield_value > 0:
            moveHeroTowardsMonsterToShieldNearEnemyBase(hero_id, monster_id)
            return_value = True
    return return_value

def moveHeroTowardsMonsterToShieldNearEnemyBase(hero_id, monster_id):
    in_range = isInRangeOf(hero_id, -1, -1, monster_id, InRange.CONTROL_BY_HERO) # shield and control have same range
    if in_range:
        moves_for_hero_dict[hero_id] = "SPELL SHIELD " + str(monster_id) + " O:)"
    else:
        hero_kill_monster[hero_id] = monster_id
        x_and_y_to_move_to = willMoveGeneric(monster_id)
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1])))


def canUseWindSpellToTakeLife(hero_id):
    return_value = False
    for monster_id, value in monsters.items():
        would_take_live_with_wind = ((value[1] + 2200 + 400) - enemy_base_x) >= 0 and ((value[2] + 2200 + 400) - enemy_base_y) >= 0
        hero_is_near_monster = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO)
        shield_value = value[3]
        monster_health = value[5]
        if not return_value and would_take_live_with_wind and hero_is_near_monster and not shield_value > 0 and monster_health > 7:
            commandWind(hero_id, [enemy_base_x, enemy_base_y]," (:")
            return_value = True
    return return_value

def canUseWindSpellOnEnemyToTakeLife(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToWind(hero_id)
    if enemy_id_near_hero != -1:
        for monster_id, value in monsters.items():
            shield_value = value[3]
            distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE)
            enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
            monster_health = value[5]
            damage_taken_in_two_rounds = enemy_and_own_heroes_in_range_of_monster * 2 * 2
            remaining_monster_health = monster_health - damage_taken_in_two_rounds
            if my_mana >= 10 and remaining_monster_health > 6 and shield_value > 0 and distance_to_enemy_base < 5000 and not enemy_heroes[enemy_id_near_hero][3] > 0:
                commandWind(hero_id, [enemy_base_x, enemy_base_y], " -")
                return_value = True
    return return_value

# MOVEMENT AND ATTACKING
def getMostMana(hero_id):
    hero_x_and_y = getHeroXAndY(hero_id)
    shortest_current_distance_monster_id = -1
    shortest_current_distance_to_my_hero = 18000
    second_monster_id_list = []
    for monster_id, monster_values in monsters.items():
        monster_already_being_attacked_outside_base = monster_id in monsters_attacked_by_hero_outside_base
        if not monster_already_being_attacked_outside_base:
            # looking for second monster
            for monster_id_2, monster_value_2 in monsters.items():
                if not monster_id_2 == monster_id:
                    distance_between_monsters = distanceBetween(-1, -1, -1, monster_id, monster_id_2, GetDistance.MONSTER_TO_MONSTER)
                    monsters_are_close = distance_between_monsters < 1599
                    if monsters_are_close:
                        second_monster_id_list.append([monster_id,monster_id_2])
                        continue
            monster_x_and_y = getMonsterXAndY(monster_id)
            threat_of_monster = getMonsterThreat(monster_id)
            distance_to_hero = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.HERO_TO_MONSTER)
            closest_monster_to_my_hero = distance_to_hero < shortest_current_distance_to_my_hero
            if closest_monster_to_my_hero and threat_of_monster != 2:
                shortest_current_distance_monster_id = monster_id
    if second_monster_id_list != [] and second_monster_id_list[0]:
        monsters_attacked_by_hero_outside_base.append(second_monster_id_list[0][0])
        monsters_attacked_by_hero_outside_base.append(second_monster_id_list[0][1])
        commandMoveTowardsTwoMonsterToAttack(hero_id, second_monster_id_list[0][0], second_monster_id_list[0][1])
        return
    if shortest_current_distance_monster_id != -1:
        commandMove(hero_id, monster_x_and_y, f" m {monster_id}")
        return
    patroullingFor(hero_id, "score-and-attack")
def moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id):
    scd_monster_id_in_base = 0
    scd_monster_range_in_base = 18000
    scd_monster_id_outside_base = 0
    scd_monster_range_outside_base = 18000
    scd_monster_id_outside_base_to_control = 0
    scd_monster_range_outside_base_to_control = 18000

    for monster_id, value in monsters.items():
        threat_of_monster = value[9]
        shield_value = value[3]
        distance_to_my_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_MY_BASE)

        if monsterWouldTakeMyLife(hero_id, monster_id, value[3]) and my_mana >= 10 and shield_value == 0 and not wind_for_defense_used[monster_id]:
            print("monster " + str(monster_id) + " would take life", file=sys.stderr, flush=True)
            wind_for_defense_used[monster_id] = True
            commandWind(hero_id, [enemy_base_x, enemy_base_y], " :|")
            return
        
        if distance_to_my_base < 5000:
            if distance_to_my_base < scd_monster_range_in_base:
                scd_monster_id_in_base = monster_id
                scd_monster_range_in_base = distance_to_my_base
                print("monster " + str(monster_id) + " closest with threat", file=sys.stderr, flush=True)
        elif distance_to_my_base < 6000:
            if distance_to_my_base < scd_monster_range_in_base:
                scd_monster_id_in_base = monster_id
                scd_monster_range_in_base = distance_to_my_base
                print("monster " + str(monster_id) + " closest with threat", file=sys.stderr, flush=True)
        elif monster_id not in gets_attacked_by_defense_outside_base: # outside of base
            if distance_to_my_base < scd_monster_range_outside_base and threat_of_monster == 0:
                scd_monster_id_outside_base = monster_id
                scd_monster_range_outside_base = distance_to_my_base
                print("monster " + str(monster_id) + " closest without threat", file=sys.stderr, flush=True)


    if scd_monster_id_in_base != 0:
        monster_in_range_for_wind_by_hero = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO) 
        if my_mana >= 10 and monster_in_range_for_wind_by_hero: # and distance_to_my_base + 2200 > 5000:
            commandWind(hero_id, [enemy_base_x, enemy_base_y], " :I")
        else:
            commandMove(hero_id, getMonsterXAndY(scd_monster_id_in_base), " :T")
    elif scd_monster_id_outside_base != 0:
        x_and_y_to_move_to = willMoveGeneric(scd_monster_id_outside_base)
        gets_attacked_by_defense_outside_base.append(scd_monster_id_outside_base)
        commandMove(hero_id, x_and_y_to_move_to, " :T")
    return
def useSpellsOnMonstersNearToEnemyBase(hero_id):
    if not my_mana < 10:
        if canUseSpellToTakeLife(hero_id):
            return True
        elif canUseSpellToActivateMonsterTowardsEnemyBase(hero_id):
            return True
        elif canUseSpellToAnnoy(hero_id) and my_mana > 200: # will likely never happen, LOW PRIORITY
            return True
        else:
            patroullingFor(hero_id, "score-and-attack")
    else:
        print("No Mana", file=sys.stderr, flush=True)
        patroullingFor(hero_id, "score-and-attack")

# CALCULATIONS REGARDING DECISIONS
def applyShieldIfNecessaryDefender(hero_id):
    my_shield = my_heroes[hero_id][3]
    hero_in_range_of_enemy_control_future = isInRangeOf(hero_id, -1, -1, -1, InRange.HERO_HIT_BY_ENEMY_CONTROL_FUTURE) != -1
    hero_in_range_of_enemy_wind_future = isInRangeOf(hero_id, -1, -1, -1, InRange.HERO_HIT_BY_ENEMY_WIND_FUTURE) != -1
    in_range_of_attack = hero_in_range_of_enemy_control_future or hero_in_range_of_enemy_wind_future
    if my_mana >= 10 and not my_shield > 0 and round_counter > 120 and my_heroes[hero_id][3] == 0 and in_range_of_attack:
        commandShield(hero_id, hero_id, " 0:(")
        return True
    return False

def willMoveGeneric(monster_id):
    monster_x = monsters[monster_id][1]
    monster_x_vector = monsters[monster_id][6]
    monster_y = monsters[monster_id][2]
    monster_y_vector = monsters[monster_id][7]
    monster_future_x = monster_x + monster_x_vector
    monster_future_y = monster_y  + monster_y_vector

    predicted_distance_moved = math.sqrt(abs(monster_x_vector * monster_x_vector) + abs(monster_future_y * monster_future_y))
    moving_angle = math.asin(monster_y_vector/400)
    x_to_add_to_hero = math.cos(abs(moving_angle)) * 399
    y_to_add_to_hero = math.sin(abs(moving_angle)) * 399

    x_to_move_to = monster_future_x
    y_to_move_to = monster_future_y
    if my_base_x == 0:
        x_to_move_to -= x_to_add_to_hero
        y_to_move_to -= y_to_add_to_hero
    else:
        x_to_move_to += x_to_add_to_hero
        y_to_move_to += y_to_add_to_hero
    return [int(x_to_move_to), int(y_to_move_to)]

def controlEnemyAttacker(hero_id, endangered_hero_id, enemy_hero_id):
    distance_from_enemy = distanceBetween(hero_id, -1, enemy_hero_id, -1, -1, GetDistance.HERO_TO_ENEMY)
    if my_mana >= 10 and my_heroes[endangered_hero_id][3] <= 1:
        if distance_from_enemy > 2200:
            moveTowardsEnemy(hero_id, enemy_hero_id)
        else:
            if not enemy_heroes[enemy_hero_id][3] > 0:
                commandControlEnemy(hero_id, enemy_hero_id,[enemy_base_x, enemy_base_y], " :S")
                return True
    return False
def canUseControlSpellOnEnemyToDefend(hero_id):
    return_value = False
    enemy_id_near_hero = anyEnemyNearHeroToGetControlledByHero(hero_id)
    if enemy_id_near_hero != -1:
        for monster_id, value in monsters.items():
            monster_health = value[5]
            enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
            damage_taken_in_two_rounds = enemy_and_own_heroes_in_range_of_monster * 2 * 2
            remaining_monster_health = monster_health - damage_taken_in_two_rounds
            distance_to_enemy_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_ENEMY_BASE) 
            if my_mana >= 10 and remaining_monster_health > 6 and distance_to_enemy_base < 5000 and not enemy_heroes[enemy_id_near_hero][3] > 0:
                commandControlEnemy(hero_id, enemy_id_near_hero, [enemy_base_x, enemy_base_y], " :O")
                return_value = True
    return return_value
def canUseWindSpellOnEnemyToDefend(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToWind(hero_id)
    if enemy_id_near_hero != -1 and my_mana >= 10 and not enemy_heroes[enemy_id_near_hero][3] > 0:
        commandWind(hero_id, [enemy_base_x, enemy_base_y], ":}")
        return_value = True
    return return_value
def enemyNearHeroToWind(hero_id):
    for enemy_hero_id, value in enemy_heroes.items():
        in_range = distanceBetween(hero_id, -1, enemy_hero_id, -1, -1, GetDistance.HERO_TO_ENEMY) <= 1280
        if in_range:
            return enemy_hero_id
    return -1
def moveTowardsEnemy(hero_id, enemy_hero_id):
    print("moving towards enemy " + str(enemy_hero_id), file=sys.stderr, flush=True)
    enemy_hero_x = enemy_heroes[enemy_hero_id][1]
    enemy_hero_y = enemy_heroes[enemy_hero_id][2]
    x_and_y_to_move_to = [enemy_hero_x, enemy_hero_y]
    commandMove(hero_id, x_and_y_to_move_to, " :S")
def monsterWouldTakeMyLife(hero_id, monster_id, shield_value):
    monster_in_range_to_wind_by_hero = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO)
    monster_would_take_life_with_spell = monsterWouldTakeLifeWithSpell(monster_id)
    monster_would_take_life_with_spell_in_two_rounds = monsterWouldTakeLifeWithSpellInTwoRounds(hero_id, monster_id)
    monster_would_not_die_by_attacks =  monsterWouldNotDieByAttacks(monster_id,0)
    monster_would_take_life =  (monster_would_take_life_with_spell or monster_would_take_life_with_spell_in_two_rounds or monster_would_not_die_by_attacks)
    return my_mana >=10 and monster_would_take_life and monster_in_range_to_wind_by_hero
def monsterWouldNotDieByAttacks(monster_id, base_id):
    if base_id == 0: # my base
        if predictedDistanceToAnyBaseForMonster(monster_id, base_id) <= 300 and predictedLifeOfMonster(monster_id) > 0:
            return True
    if base_id == 1: # enemy base
        if predictedDistanceToAnyBaseForMonster(monster_id, base_id) <= 300 and predictedLifeOfMonster(monster_id) > 0:
            return True
    return False
def predictedLifeOfMonster(monster_id):
    return (monsters[monster_id][3] + monsters[monster_id][5]) - (countOfEnemiesOrHeroesNearMonsterToAttack(monster_id) * 2)
def countOfEnemiesOrHeroesNearMonsterToAttack(monster_id):
    attack_range = 799
    enemies_or_players_near = 0
    for key, value in enemy_heroes.items():
        if abs(value[1] - monsters[monster_id][1]) < attack_range or abs(value[2] - monsters[monster_id][2]) < attack_range:
            enemies_or_players_near+=1
    for key, value in my_heroes.items():
        if abs(value[1] - monsters[monster_id][1]) < attack_range or abs(value[2] - monsters[monster_id][2]) < attack_range:
            enemies_or_players_near+=1
    return enemies_or_players_near
def predictedDistanceToAnyBaseForMonster(monster_id, base_id):
    monster_x_and_y = getMonsterXAndYInFuture(monster_id)
    if base_id == 0: # my base
        predicted_distance = calculatePythagorasHypotenuse(monster_x_and_y,[my_base_x, my_base_y])
        return predicted_distance
    elif base_id == 1:
        predicted_distance = calculatePythagorasHypotenuse(monster_x_and_y,[enemy_base_x, enemy_base_y])
        return predicted_distance
    return 0

def monsterWouldTakeLifeWithSpell(monster_id):
    koDistance = 800 # safety
    koDistance += 400 # one step
    koDistance += 300 # distance for doing damage
    monster_health = monsters[monster_id][5]
    monster_hit_by_enemy_wind = isInRangeOf(-1, -1, -1, monster_id, InRange.MONSTER_HIT_BY_ENEMY_WIND)
    if monster_hit_by_enemy_wind:
        koDistance += 2200
    distance_between_monster_to_my_base = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_MY_BASE)
    if distance_between_monster_to_my_base <= koDistance and monster_health > 4:
        return True
    return False

def monsterWouldTakeLifeWithSpellInTwoRounds(hero_id, monster_id):
    # todo: predict hero place
    koDistance = 800 # safety
    koDistance += 800 # two steps
    koDistance += 300 # distance for doing damage
    monster_health = monsters[monster_id][5]
    monster_in_range_for_enemy_wind = isInRangeOf(-1, -1, -1, monster_id, InRange.MONSTER_HIT_BY_ENEMY_WIND)
    hero_in_range_for_enemy_wind = isInRangeOf(hero_id, -1, -1, -1, InRange.HERO_HIT_BY_ENEMY_WIND_FUTURE)
    if monster_in_range_for_enemy_wind and not hero_in_range_for_enemy_wind:
        koDistance += 2200
    distance_between_monster_to_my_base = distanceBetween(-1, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_MY_BASE)
    if distance_between_monster_to_my_base <= koDistance and monster_health > 6:
        printstatement("monster " + str(monster_id) + " could take life in two rounds")
        return True
    return False
# INFO
def anyEnemyNearHeroToGetControlledByHero(hero_id):
    for enemy_hero_id, value in enemy_heroes.items():
        is_in_range = isInRangeOf(hero_id, -1, enemy_hero_id, -1, InRange.CONTROL_BY_HERO)
        if is_in_range:
            return enemy_hero_id
    return -1

def anyEnemyInRangeToControlDefendOnly():
    defender_0_id = 0
    if my_base_x != 0:
        defender_0_id = 3
    enemy_id_for_control_hit = isInRangeOf(defender_0_id, -1, -1, -1, InRange.HERO_HIT_BY_ENEMY_CONTROL_FUTURE)
    enemy_id_for_wind_hit = isInRangeOf(defender_0_id, -1, -1, -1,  InRange.HERO_HIT_BY_ENEMY_WIND_FUTURE)
    if enemy_id_for_control_hit != -1 or enemy_id_for_wind_hit != -1:
        if enemy_id_for_control_hit != -1 and enemy_id_for_wind_hit != -1:
            return [defender_0_id, enemy_id_for_control_hit]
        elif enemy_id_for_control_hit != -1 and enemy_id_for_wind_hit == -1:
            return [defender_0_id, enemy_id_for_control_hit]
        else:
            return [defender_0_id, enemy_id_for_wind_hit]
    return [defender_0_id, -1]

def anyMonsterInRangeOfHeroWithMyBaseAsTarget(hero_id):
    for monster_id, monster_values in monsters.items():
        threat_of_monster = getMonsterThreat(monster_id)
        monster_in_range = isInRangeOf(hero_id, -1, -1, monster_id, InRange.CONTROL_BY_HERO)
        distance_monster_to_my_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_MY_BASE)
        if monster_in_range and distance_monster_to_my_base >= 5400 and threat_of_monster == 1:
            return monster_id
    return -1
def anyMonsterWouldTargetMyBaseNextTurnAndIsInRangeToWind(hero_id):
    for monster_id, monster_values in monsters.items():
        threat_of_monster = monster_values[9]
        monster_in_range = isInRangeOf(hero_id, -1, -1, monster_id, InRange.WIND_BY_HERO)
        distance_monster_to_my_base = distanceBetween(hero_id, -1, -1, monster_id, -1, GetDistance.MONSTER_TO_MY_BASE)
        monster_is_in_wind_range_of_base = distance_monster_to_my_base >= 5000 and distance_monster_to_my_base < 6000
        if monster_in_range and monster_is_in_wind_range_of_base and threat_of_monster == 1:
            printstatement(f"winding {monster_id} with range {distance_monster_to_my_base}")
            return monster_id
    return -1
def isInRangeOf(hero_id, second_hero_id, enemy_hero_id, monster_id, inRange):
    hero_x_and_y = getHeroXAndY(hero_id)
    second_hero_x = getHeroXAndY(second_hero_id)
    monster_x_and_y = getMonsterXAndY(monster_id)
    enemy_hero_x_and_y = getEnemyXAndY(enemy_hero_id)
    if inRange == InRange.CONTROL_BY_HERO:
        return distanceBetween(hero_id, second_hero_id, enemy_hero_id, monster_id, -1, GetDistance.HERO_TO_MONSTER) <= 2200
    if inRange == InRange.WIND_BY_HERO:
        return distanceBetween(hero_id, second_hero_id, enemy_hero_id, monster_id, -1, GetDistance.HERO_TO_MONSTER) <= 1280
    if inRange == InRange.HERO_HIT_BY_ENEMY_CONTROL_FUTURE:
        spell_range = 2200
        enemy_that_can_control = -1
        for enemy_hero_id, value in enemy_heroes.items():
            distance_from_enemy = calculatePythagorasHypotenuse(hero_x_and_y, enemy_hero_x_and_y)
            if enemy_mana >= 10 and not enemy_heroes[enemy_hero_id][3] > 0 and distance_from_enemy <= spell_range + 800:  # 800 is one step
                enemy_that_can_control = enemy_hero_id
        return enemy_that_can_control
    if inRange == InRange.HERO_HIT_BY_ENEMY_WIND_FUTURE:
        spell_range = 1280
        enemy_that_can_control = -1
        for enemy_hero_id, value in enemy_heroes.items():
            distance_from_enemy = calculatePythagorasHypotenuse(hero_x_and_y, enemy_hero_x_and_y)
            if enemy_mana >= 10 and distance_from_enemy + 800 <= spell_range: # 800 is one step
                enemy_that_can_control = enemy_hero_id
        return enemy_that_can_control
    if inRange == InRange.MONSTER_HIT_BY_ENEMY_WIND:
        spell_range = 1280
        enemy_in_range_for_spell = False
        for key, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy_now = distanceBetween(-1, -1, enemy_hero_id, monster_id, -1, GetDistance.ENEMY_TO_MONSTER)
            if enemy_mana >= 10 and distance_from_enemy_now <= spell_range:
                enemy_in_range_for_spell = True
        return enemy_in_range_for_spell
    return False
def distanceBetween(hero_id, second_hero_id, enemy_hero_id, monster_id, second_monster_id, getDistance):
    hero_x_and_y = getHeroXAndY(hero_id)
    second_hero_x = getHeroXAndY(second_hero_id)
    monster_x_and_y = getMonsterXAndY(monster_id)
    second_monster_x_and_y = getMonsterXAndY(second_monster_id)
    enemy_hero_x_and_y = getEnemyXAndY(enemy_hero_id)

    if getDistance == GetDistance.HERO_TO_MY_BASE:
        return calculatePythagorasHypotenuse(hero_x_and_y, [my_base_x, my_base_y])
    if getDistance == GetDistance.HERO_TO_MONSTER:
        return calculatePythagorasHypotenuse(hero_x_and_y, monster_x_and_y)
    if getDistance == GetDistance.HERO_TO_ENEMY:
        return calculatePythagorasHypotenuse(hero_x_and_y, enemy_hero_x_and_y)
    if getDistance == GetDistance.MONSTER_TO_MY_BASE:
        return calculatePythagorasHypotenuse(monster_x_and_y, [my_base_x, my_base_y])
    if getDistance == GetDistance.MONSTER_TO_ENEMY_BASE:
        return calculatePythagorasHypotenuse(monster_x_and_y, [enemy_base_x, enemy_base_y])
    if getDistance == GetDistance.MONSTER_TO_ENEMY_BASE_FUTURE:
        move_to = willMoveGeneric(monster_id)
        return calculatePythagorasHypotenuse(move_to, [enemy_base_x, enemy_base_y])
    if getDistance == GetDistance.MONSTER_TO_MONSTER:
        return calculatePythagorasHypotenuse(monster_x_and_y, second_monster_x_and_y)
    if getDistance == GetDistance.ENEMY_TO_MONSTER:
        return calculatePythagorasHypotenuse(enemy_hero_x_and_y,monster_x_and_y)
    return -1
def inPatroullingPosition(hero_id, position):
    hero_x_and_y = getHeroXAndY(hero_id)
    return (hero_x_and_y[0] - patroulling_points[position][0]) < 300 and abs(hero_x_and_y[1] - patroulling_points[position][1]) < 300
def getGameStage():
    if round_counter > 165:
        return 3
    elif round_counter > 110:
        return 2
    elif round_counter > 65:
        return 1
    else:
        return 0
# UTILITY
def printstatement(printmessage):
    print(printmessage, file=sys.stderr, flush=True)
def calculatePythagorasHypotenuse(first_array, second_array):
    return math.sqrt(abs(first_array[0]-second_array[0]) * abs(first_array[0]-second_array[0]) + abs(first_array[1]-second_array[1]) * abs(first_array[1]-second_array[1]))
def getEnemyBaseRadiusCoordinates(monster_id):
    monster_x_and_y = getMonsterXAndY(monster_id)
    if monster_x_and_y[1] > 4500:
        if enemy_base_x == 0:
            return [0, 5000]
        else:
            return [enemy_base_x - 5000, enemy_base_y]
    else:
        if enemy_base_x == 0:
            return [5000, 0]
        else:
            return [enemy_base_x, 9000 - 5000]
def getHeroXAndY(hero_id):
    if hero_id != -1:
        return [my_heroes[hero_id][1], my_heroes[hero_id][2]]
    return [-1,-1]
def getMonsterXAndY(monster_id):
    if monster_id != -1:
        return [monsters[monster_id][1], monsters[monster_id][2]]
    return [-1,-1]
def getMonsterXAndYInFuture(monster_id):
    if monster_id != -1:
        return [monsters[monster_id][1] + monsters[monster_id][6], monsters[monster_id][2]+ monsters[monster_id][7]]
    return [-1,-1]
def getMonsterThreat(monster_id):
    return monsters[monster_id][9]
def getMonsterHealth(monster_id):
    return monsters[monster_id][5]
def getEnemyXAndY(enemy_hero_id):
    if enemy_hero_id != -1:
        return [enemy_heroes[enemy_hero_id][1], enemy_heroes[enemy_hero_id][2]]
    return [0,0]
# HARD CODED
class GetDistance(Enum):
     HERO_TO_MONSTER = 1
     MONSTER_TO_MY_BASE = 2
     HERO_TO_MY_BASE = 3
     MONSTER_TO_MONSTER = 4
     HERO_TO_ENEMY = 5
     MONSTER_TO_ENEMY_BASE = 6
     ENEMY_TO_MONSTER = 7
     MONSTER_TO_ENEMY_BASE_FUTURE = 8
class InRange(Enum):
    WIND_BY_HERO = 1
    CONTROL_BY_HERO = 2
    HERO_HIT_BY_ENEMY_CONTROL_FUTURE = 3
    HERO_HIT_BY_ENEMY_WIND_FUTURE = 4
    MONSTER_HIT_BY_ENEMY_WIND = 5
def getMonsterControlCooldown():
    return 4
# PATROULLING
def patroullingFor(hero_id, patroulling_for):
    if patroulling_heroes[hero_id][0] == 0 and inPatroullingPosition(hero_id, patroulling_for + "-0"):
        patroulling_heroes[hero_id][0] = 1
        patroulling_heroes[hero_id][1] = 0
    elif patroulling_heroes[hero_id][0] == 1 and inPatroullingPosition(hero_id, patroulling_for + "-1"):
        patroulling_heroes[hero_id][0] = 0
        patroulling_heroes[hero_id][1] = 1
    moveToPatroullingFor(hero_id, patroulling_for)
def moveToPatroullingFor(hero_id, patroulling_for):
    move_x = 0
    move_y = 0
    if patroulling_heroes[hero_id][0] == 0:
        move_x = patroulling_points[patroulling_for + "-0"][0]
        move_y = patroulling_points[patroulling_for + "-0"][1]
    elif patroulling_heroes[hero_id][0] == 1:
        move_x = patroulling_points[patroulling_for + "-1"][0]
        move_y = patroulling_points[patroulling_for + "-1"][1]
    commandMove(hero_id, [move_x,move_y], "JUST WALKING")
# SETUP
def setInitialMaxDistanceForRole():
    maxDistanceForRole["defend-only"] = 7100
    maxDistanceForRole["defend-and-protect"] = 7100
    maxDistanceForRole["score-and-attack"] = 7100
    return
def setRolesForHeroesInitialV2():
    if game_stage == 0:
        roles_for_heroes[my_heroes_ids[0]] = "defend-only"
        roles_for_heroes[my_heroes_ids[1]] = "defend-and-protect"
        roles_for_heroes[my_heroes_ids[2]] = "score-and-attack"
        setPatroullingHeroesInitialValueV2(2,1)
    elif game_stage == 1:
        roles_for_heroes[my_heroes_ids[0]] = "defend-only"
        roles_for_heroes[my_heroes_ids[1]] = "defend-and-protect"
        roles_for_heroes[my_heroes_ids[2]] = "score-and-attack"
        setPatroullingHeroesInitialValueV2(2,1)
    elif game_stage == 2:
        roles_for_heroes[my_heroes_ids[0]] = "defend-only"
        roles_for_heroes[my_heroes_ids[1]] = "defend-and-protect"
        roles_for_heroes[my_heroes_ids[2]] = "score-and-attack"
        setPatroullingHeroesInitialValueV2(2,1)
    else:
        roles_for_heroes[my_heroes_ids[0]] = "defend-only"
        roles_for_heroes[my_heroes_ids[1]] = "defend-and-protect"
        roles_for_heroes[my_heroes_ids[2]] = "score-and-attack"
        setPatroullingHeroesInitialValueV2(2,1)
def setPatroullingHeroesInitialValueV2(defend_amount, score_and_attack_amount):
    for key, value in my_heroes.items():
        patroulling_heroes[key] = [0,1]
def setInitialPatroullingPointsV2():
    setDefendOnlyPoints()
    setDefendAndProtectPoints()
    setScoreAndAttackPoints()
def setDefendOnlyPoints():
    patroulling_x_0 = abs(my_base_x - 6000 - 500) 
    patroulling_y_0 = abs(my_base_y - 2200)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["defend-only-0"] = patroulling_point_0

    patroulling_x_1 = abs(my_base_x - 3375) 
    patroulling_y_1 = abs(my_base_y - 3375)
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["defend-only-1"] = patroulling_point_1
def setDefendAndProtectPoints():
    patroulling_x_0 = abs(my_base_x - 2200) 
    patroulling_y_0 = abs(my_base_y - 6000 - 500)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["defend-and-protect-0"] = patroulling_point_0

    patroulling_x_1 = abs(my_base_x - 3375) 
    patroulling_y_1 = abs(my_base_y - 3375)
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["defend-and-protect-1"] = patroulling_point_1
def setScoreAndAttackPoints():
    patroulling_x_0 = abs(int(17630/2)) 
    patroulling_y_0 = abs(int(9000/2))
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["score-and-attack-0"] = patroulling_point_0

    patroulling_x_1 = abs(enemy_base_x - 2000) 
    patroulling_y_1 = abs(enemy_base_y - 2000)
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["score-and-attack-1"] = patroulling_point_1
# GAME
moves_for_hero_dict = {}
my_heroes = {}
patroulling_heroes = {}
enemy_heroes = {}
patroulling_points = {}
monsters = {}
hero_kill_monster = {}
monster_in_sight = False
monster_in_sight_offense = False
monster_in_sight_score_and_attack = False
monster_in_sight_defend_only = False
monster_in_sight_defend_and_protect = False
wind_for_defense_used = {}
monsters_attacked_by_hero_outside_base = []
monster_was_controlled_shortly = {}
roles_for_heroes = {}
maxDistanceForRole = {}
gets_attacked_by_defense_outside_base = []
my_heroes_ids = []
game_stage = -1
old_game_stage = -1
round_counter = 0
# GAME VARIABLES
enemy_base_x = 0
enemy_base_y = 0
my_health = 3
my_mana = 0
enemy_health = 3
enemy_mana = 0
my_base_x, my_base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())  # Always 3

while True:
    round_counter += 1
    if my_base_x == 0: # enemy base is X=17630, Y=9000
        enemy_base_x = 17630
        enemy_base_y = 9000
    for i in range(2):
        health, mana = [int(j) for j in input().split()]
        if i == 0:
            my_health = health
            my_mana = mana
        else:
            enemy_health = health
            enemy_mana = mana
    entity_count = int(input())  # Amount of heros and monsters you can see
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        if _type == 1:
            my_heroes[_id] = [_type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for]
            my_heroes_ids.append(_id)
            if not _id in hero_kill_monster:
                hero_kill_monster[_id] = -1
        elif _type == 2:
            enemy_heroes[_id] = [_type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for]
        elif _type == 0:
            monsters[_id] = [_type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for]
            wind_for_defense_used[_id] = False
            monster_in_sight = True
            x_smaller_offense = abs((x + 1100) - enemy_base_x) < 7100
            y_smaller_offense = abs((y + 1100) - enemy_base_y) < 7100
            x_smaller_score = abs((x + 1100) - enemy_base_x) > 7100
            y_smaller_score = abs((y + 1100) - enemy_base_y) > 7100
            if  (x_smaller_score and y_smaller_score) or (x_smaller_offense and y_smaller_offense):
                monster_in_sight_score_and_attack = True
            x_smaller_defend_only = abs((x + 1100) - my_base_x) < 8200
            y_smaller_defend_only = abs((y + 1100) - my_base_y) < 8200
            if  x_smaller_defend_only and y_smaller_defend_only:
                monster_in_sight_defend_only = True
            x_smaller_defend_and_protect = abs((x + 1100) - my_base_x) < 10000
            y_smaller_defend_and_protect = abs((y + 1100) - my_base_y) < 10000
            if  x_smaller_defend_and_protect and y_smaller_defend_and_protect:
                monster_in_sight_defend_and_protect = True

    game_stage = getGameStage()
    if round_counter == 1:
        setInitialPatroullingPointsV2()
        setInitialMaxDistanceForRole()
    if game_stage != old_game_stage:
        roles_for_heroes = {}
        setRolesForHeroesInitialV2()
        if game_stage != old_game_stage:
            old_game_stage = old_game_stage + 1
    counter = 0
    for key, value in my_heroes.items():
        if counter == 0:
            setHeroToModeV2(key, roles_for_heroes[key])
        elif counter == 1:
            setHeroToModeV2(key, roles_for_heroes[key])
        else:
            setHeroToModeV2(key, roles_for_heroes[key])
        counter += 1
    
    # clean up
    my_heroes = {}
    enemy_heroes = {}
    monsters = {}
    my_heroes_ids = []
    monsters_attacked_by_hero_outside_base = []
    monster_in_sight = False
    monster_in_sight_offense = False
    monster_in_sight_score_and_attack = False
    monster_in_sight_defend_only = False
    monster_in_sight_defend_and_protect = False
    gets_attacked_by_defense_outside_base = []
    # clean up controlled monsters
    keys_to_delete_from_monster_was_controlled_shortly = []
    for key, value in monster_was_controlled_shortly.items():
        if value == 0:
            keys_to_delete_from_monster_was_controlled_shortly.append(key)
        else:
            monster_was_controlled_shortly[key] = value - 1
    for key in keys_to_delete_from_monster_was_controlled_shortly:
        del monster_was_controlled_shortly[key]
    keys_to_delete_from_monster_was_controlled_shortly = []

    # print commands
    for key, value in moves_for_hero_dict.items():
        print(value)

# V1"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

def setHeroToMode(hero_id, monster_in_sight, mode):
    if mode == "defend":
        if not monster_in_sight:
            print("patroulling defense", file=sys.stderr, flush=True)
            patroullingDefensive(hero_id)
        else:
            print("doing else", file=sys.stderr, flush=True)
            if applyShieldIfNecessaryDefender(hero_id):
                return
            else:
                print("doing else 2", file=sys.stderr, flush=True)
                moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id)
    elif mode == "defend-dmg":
        counter_attack_to_defend_defender_0 = anyEnemyInRangeToControlDefendOnly()
        endangered_hero_id = counter_attack_to_defend_defender_0[0]
        enemy_hero_id_that_can_control_defender = counter_attack_to_defend_defender_0[1]
        if not monster_in_sight:
            patroullingDefensive(hero_id)
            return
        elif enemy_hero_id_that_can_control_defender != -1 and my_heroes[endangered_hero_id][3] > 1:
            if controlEnemyAttacker(hero_id, endangered_hero_id, enemy_hero_id_that_can_control_defender):
                print("can control enemy attacker", file=sys.stderr, flush=True)
                return
            moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id)
        elif canUseControlSpellOnEnemyToDefend(hero_id): 
            return
        elif canUseWindSpellOnEnemyToDefend(hero_id):
            return
        else:
            moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id)
    elif mode == "attack":
        if getDistanceBetween(hero_id, "null","null", "hero-to-enemy-base") > 6500 or not monster_in_sight_offense:
            patroullingAttack(hero_id)
        else:
            useSpellsOnMonstersNearToEnemyBase(hero_id)
    elif mode == "score":
        if (getDistanceBetween(hero_id, "null","null", "hero-to-my-base") < 7100 or getDistanceBetween(hero_id, "null","null", "hero-to-enemy-base") < 7100) or not monster_in_sight_score_and_attack:
            patroullingScore(hero_id)
        else:
            moveTowardsNearestMonsterToAnyHeroToAttack(hero_id)
    elif mode == "getting-mana-to-attack":
        if my_mana > 150:
            roles_for_heroes[hero_id] = "attack"
            setHeroToMode(hero_id, monster_in_sight, "attack")
        if (getDistanceBetween(hero_id, "null","null", "hero-to-my-base") < 6400 or getDistanceBetween(hero_id, "null","null", "hero-to-enemy-base") < 6400) and not monster_in_sight:
            patroullingScore(hero_id)
        else:
            moveTowardsNearestMonsterToAnyHeroToAttack(hero_id)
    elif mode == "defend-V2":
        if not monster_in_sight_defend_only:
            V2_moveTowardsDefensivePatroullingPoint(hero_id)
            return
        else:
            print("doing else", file=sys.stderr, flush=True)
            if applyShieldIfNecessaryDefender(hero_id):
                return
            else:
                print("doing else 2", file=sys.stderr, flush=True)
                V2_moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id)
    elif mode == "defend-dmg-V2":
        counter_attack_to_defend_defender_0 = anyEnemyInRangeToControlDefendOnly()
        endangered_hero_id = counter_attack_to_defend_defender_0[0]
        enemy_hero_id_that_can_control_defender = counter_attack_to_defend_defender_0[1]
        if not monster_in_sight_defend_only:
            V2_moveTowardsDefensiveDmgPatroullingPoint(hero_id)
            return
        elif enemy_hero_id_that_can_control_defender != -1 and my_heroes[endangered_hero_id][3] > 1:
            if controlEnemyAttacker(hero_id, endangered_hero_id, enemy_hero_id_that_can_control_defender):
                return
            moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id)
        elif canUseControlSpellOnEnemyToDefend(hero_id): 
            return
        elif canUseWindSpellOnEnemyToDefend(hero_id):
            return
        else:
            moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id)







def currentDistanceToBaseForMonster(monster_id):
    return math.sqrt(abs(monsters[monster_id][1]-my_base_x) * abs(monsters[monster_id][1]-my_base_x) + abs(monsters[monster_id][2]-my_base_y) * abs(monsters[monster_id][2]-my_base_y))

def currentDistanceToBaseForHero(hero_id, base_id):
    if base_id == 0:
        return math.sqrt(abs(my_heroes[hero_id][1]-my_base_x) * abs(my_heroes[hero_id][1]-my_base_x) + abs(my_heroes[hero_id][2]-my_base_y) * abs(my_heroes[hero_id][2]-my_base_y))
    elif base_id == 1:
        return math.sqrt(abs(my_heroes[hero_id][1]-enemy_base_x) * abs(my_heroes[hero_id][1]-enemy_base_x) + abs(my_heroes[hero_id][2]-enemy_base_y) * abs(my_heroes[hero_id][2]-enemy_base_y))

def setRolesForHeroesInitial():
    if game_stage == 0:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "score"
        setPatroullingHeroesInitialValue(2,1,0)
    elif game_stage == 1:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "score"
        setPatroullingHeroesInitialValue(2,1,0)
    elif game_stage == 2:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)
    else:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)

def setRolesForHeroesInitialOffensive():
    if game_stage == 0:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "score"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(1,1,1)
    elif game_stage == 1:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)
    elif game_stage == 2:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)
    else:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)

def setRolesForHeroesTwoLifesLeft():
    if game_stage == 0:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)
    elif game_stage == 1:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "defend-dmg"
        setPatroullingHeroesInitialValue(3,0,0)
    elif game_stage == 2:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "defend-dmg"
        setPatroullingHeroesInitialValue(3,0,0)
    else:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)

def setRolesForHeroesOneLifesLeft():
    if game_stage == 0:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(2,0,1)
    elif game_stage == 1:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "defend-dmg"
        setPatroullingHeroesInitialValue(3,0,0)
    elif game_stage == 2:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "defend-dmg"
        roles_for_heroes[my_heroes_ids[2]] = "defend-dmg"
        setPatroullingHeroesInitialValue(3,0,0)
    else:
        roles_for_heroes[my_heroes_ids[0]] = "defend"
        roles_for_heroes[my_heroes_ids[1]] = "attack"
        roles_for_heroes[my_heroes_ids[2]] = "attack"
        setPatroullingHeroesInitialValue(1,0,2)





def setPatroullingHeroesInitialValue(defend_amount, score_amount, attack_amount):
    if defend_amount == 2:
        current_defender_count = 0
        for key, value in roles_for_heroes.items():
            if value == "defend" or value == "defend-dmg":
                if current_defender_count == 0:
                    patroulling_heroes[key] = [0,1]
                    current_defender_count += 1
                else:
                    patroulling_heroes[key] = [2,1]
            else:
                patroulling_heroes[key] = [1,0]
    elif defend_amount == 3:
        current_defender_count = 0
        for key, value in roles_for_heroes.items():
            if value == "defend" or value == "defend-dmg":
                if current_defender_count == 0:
                    patroulling_heroes[key] = [0,1]
                    current_defender_count += 1
                elif current_defender_count == 1:
                    patroulling_heroes[key] = [2,1]
                    current_defender_count += 1
                else:
                    patroulling_heroes[key] = [1,2]
            else:
                patroulling_heroes[key] = [1,0]
    else:
        for key, value in my_heroes.items():
            patroulling_heroes[key] = [1,0] # goes to defend-1, comes form defend-0

def setPatroullingPoints():
    setDefensePatroullingPoints()
    setScorePatroullingPoints()
    setAttackPatroullingPoints()
    setDefensePatroullingPoints_V2()
    setDefenseDmgPatroullingPoints_V2()

def setDefensePatroullingPoints():
    patroulling_x_0 = abs(my_base_x - 6000 - 500) # 6000 is base sight range, 2200 is hero sight range
    patroulling_y_0 = abs(my_base_y - 2200)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["defend-0"] = patroulling_point_0

    patroulling_x_1 = abs(my_base_x - 4242 - 333)
    patroulling_y_1 = abs(my_base_y - 4242 - 333)
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["defend-1"] = patroulling_point_1

    patroulling_x_2 = abs(my_base_x - 2200)
    patroulling_y_2 = abs(my_base_y - 6000 - 500) # 6000 is base sight range, 2200 is hero sight range
    patroulling_point_2 = [patroulling_x_2, patroulling_y_2]
    patroulling_points["defend-2"] = patroulling_point_2

def setDefensePatroullingPoints_V2():
    patroulling_x_0 = abs(my_base_x - 2200) # 6000 is base sight range, 2200 is hero sight range
    patroulling_y_0 = abs(my_base_y - 5000 - 1100)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["defend-V2"] = patroulling_point_0

def setDefenseDmgPatroullingPoints_V2():
    patroulling_x_0 = abs(my_base_x - 5000 - 1100) # 6000 is base sight range, 2200 is hero sight range
    patroulling_y_0 = abs(my_base_y - 2200)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["defend-dmg-V2"] = patroulling_point_0


def setScorePatroullingPoints():
    patroulling_x_0 = abs(int(17630/3 * 2)) 
    patroulling_y_0 = abs(1700) # 2200 is hero sight range
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["score-0"] = patroulling_point_0

    patroulling_x_1 = abs(int(17630/2))
    patroulling_y_1 = abs(int(9000/2))
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["score-1"] = patroulling_point_1

    patroulling_x_2 = abs(int(17630/3))
    patroulling_y_2 = abs(9000-1700) 
    patroulling_point_2 = [patroulling_x_2, patroulling_y_2]
    patroulling_points["score-2"] = patroulling_point_2

def setAttackPatroullingPoints():
    patroulling_x_0 = abs(enemy_base_x - 3375) 
    patroulling_y_0 = abs(enemy_base_y - 1700)
    patroulling_point_0 = [patroulling_x_0, patroulling_y_0]
    patroulling_points["attack-0"] = patroulling_point_0

    patroulling_x_1 = abs(enemy_base_x - 2199)
    patroulling_y_1 = abs(enemy_base_y - 2199)
    patroulling_point_1 = [patroulling_x_1, patroulling_y_1]
    patroulling_points["attack-1"] = patroulling_point_1

    patroulling_x_2 = abs(enemy_base_x - 1700)
    patroulling_y_2 = abs(enemy_base_y - 3375 ) # 6000 is base sight range, 2200 is hero sight range
    patroulling_point_2 = [patroulling_x_2, patroulling_y_2]
    patroulling_points["attack-2"] = patroulling_point_2

def isNearEnemyBase(hero_id):
    if getDistanceBetween(hero_id, "null", "null", "hero-to-enemy-base") * 1.5 < getDistanceBetween(hero_id, "null", "null", "hero-to-my-base"):
        return True
    return False



def getDistanceBetweenTwoMonsters(monster_id, monster_id_2):
    monster_x = monsters[monster_id][1]
    monster_y = monsters[monster_id][2]
    monster_x_2 = monsters[monster_id_2][1]
    monster_y_2 = monsters[monster_id_2][2]
    return math.sqrt(abs(monster_x-monster_x_2) * abs(monster_x-monster_x_2) + abs(monster_y-monster_y_2) * abs(monster_y-monster_y_2))

def getDistanceBetween(hero_id, monster_id, enemy_id, distance_to_check):
    my_hero_x = 0
    my_hero_y = 0
    monster_x_future = 0
    monster_y_future = 0
    monster_x_now = 0
    monster_y_now = 0
    if hero_id != "null":
        my_hero_x = my_heroes[hero_id][1]
        my_hero_y = my_heroes[hero_id][2]
    if monster_id != "null":
        monster_x_future = monsters[monster_id][1] + monsters[monster_id][6]
        monster_y_future = monsters[monster_id][2] + monsters[monster_id][7]
        monster_x_now = monsters[monster_id][1]
        monster_y_now = monsters[monster_id][2]

    if distance_to_check == "hero-to-monster":
        return math.sqrt(abs(monster_x_now-my_hero_x) * abs(monster_x_now-my_hero_x) + abs(monster_y_now-my_hero_y) * abs(monster_y_now-my_hero_y))
    if distance_to_check == "hero-to-enemy":
        enemy_x = enemy_heroes[enemy_id][1]
        enemy_y = enemy_heroes[enemy_id][2]
        return math.sqrt(abs(my_hero_x-enemy_x) * abs(my_hero_x-enemy_x) + abs(my_hero_y-enemy_y) * abs(my_hero_y-enemy_y))
    if distance_to_check == "hero-to-my-base":
        return math.sqrt(abs(my_hero_x-my_base_x) * abs(my_hero_x-my_base_x) + abs(my_hero_y-my_base_y) * abs(my_hero_y-my_base_y))
    if distance_to_check == "hero-to-enemy-base":
        return math.sqrt(abs(my_hero_x-enemy_base_x) * abs(my_hero_x-enemy_base_x) + abs(my_hero_y-enemy_base_y) * abs(my_hero_y-enemy_base_y))
    if distance_to_check == "monster-to-my-base":
        return math.sqrt(abs(monster_x_now-my_base_x) * abs(monster_x_now-my_base_x) + abs(monster_y_now-my_base_y) * abs(monster_y_now-my_base_y))
    if distance_to_check == "monster-to-my-base-future":
        return math.sqrt(abs(monster_x_future-my_base_x) * abs(monster_x_future-my_base_x) + abs(monster_y_future-my_base_y) * abs(monster_y_future-my_base_y))
    if distance_to_check == "monster-to-enemy-base":
        return math.sqrt(abs(monster_x_now-enemy_base_x) * abs(monster_x_now-enemy_base_x) + abs(monster_y_now-enemy_base_y) * abs(monster_y_now-enemy_base_y))
    if distance_to_check == "current-monster-to-enemy-base":
        return math.sqrt(abs(monsters[monster_id][1]-enemy_base_x) * abs(monsters[monster_id][1]-enemy_base_x) + abs(monsters[monster_id][2]-enemy_base_y) * abs(monsters[monster_id][2]-enemy_base_y))
    if distance_to_check == "enemy-to-monster":
        enemy_hero_x = enemy_heroes[enemy_id][1]
        enemy_hero_y = enemy_heroes[enemy_id][2]
        return math.sqrt(abs(monster_x_now-enemy_hero_x) * abs(monster_x_now-enemy_hero_x) + abs(monster_y_now-enemy_hero_y) * abs(monster_y_now-enemy_hero_y))
    if distance_to_check == "ko-distance-to-my-base":
        circle_point_x = abs(my_base_x - 3375)
        circle_point_y = abs(my_base_y - 3375)
        return math.sqrt(abs(circle_point_x) * abs(circle_point_x) + abs(circle_point_y) * abs(circle_point_y))
    return 0

def enemyInRangeToControlMonster(monster_id):
    enemy_id_for_control_hit = monsterHitByEnemyControl(monster_id)
    enemy_id_for_wind_hit = monsterHitByEnemyWind(monster_id)
    if enemy_id_for_control_hit != -1 or enemy_id_for_wind_hit != -1:
        if enemy_id_for_control_hit != -1 and enemy_id_for_wind_hit != -1:
            return  enemy_id_for_control_hit
        elif enemy_id_for_control_hit != -1 and enemy_id_for_wind_hit == -1:
            return enemy_id_for_control_hit
        else:
            return enemy_id_for_wind_hit
    return -1

def monsterHitByEnemyWind(monster_id):
    spell_range = 1280
    enemy_in_range_for_spell = False
    for key, value in enemy_heroes.items():
        distance_from_enemy_now = getDistanceBetween("null", monster_id, key, "enemy-to-monster")
        if enemy_mana >= 10 and distance_from_enemy_now <= spell_range:
            return key
    return -1

def monsterHitByEnemyControl(monster_id):
    spell_range = 2200
    enemy_in_range_for_spell = False
    for key, value in enemy_heroes.items():
        distance_from_enemy_now = getDistanceBetween("null", monster_id, key, "enemy-to-monster")
        if enemy_mana >= 10 and distance_from_enemy_now <= spell_range:
            return key
    return -1      

def enemyNearHeroToControl(hero_id):
    for enemy_hero_id, value in enemy_heroes.items():
        if getDistanceBetween(hero_id, "null", enemy_hero_id, "hero-to-enemy") <= 2200:
            return enemy_hero_id
    return -1

def enemyNearHeroToWind(hero_id):
    for enemy_hero_id, value in enemy_heroes.items():
        if getDistanceBetween(hero_id, "null", enemy_hero_id, "hero-to-enemy") <= 1280:
            return enemy_hero_id
    return -1




def isMonsterInRange(hero_id, monster_id, type_to_check): # todo: rename to "isInRange"
    my_hero_x = 0
    my_hero_y = 0
    monster_x_future = 0
    monster_y_future = 0
    monster_x_now = 0
    monster_y_now = 0

    if not hero_id == "null":
        my_hero_x = my_heroes[hero_id][1]
        my_hero_y = my_heroes[hero_id][2]
    if not monster_id == "null":
        monster_x_future = monsters[monster_id][1] + monsters[monster_id][6]
        monster_y_future = monsters[monster_id][2] + monsters[monster_id][7]
        monster_x_now = monsters[monster_id][1]
        monster_y_now = monsters[monster_id][2]

    if type_to_check == "to-control-by-hero":  
        distance_from_hero_now = math.sqrt(abs(my_hero_x-monster_x_now) * abs(my_hero_x-monster_x_now) + abs(my_hero_y-monster_y_now) * abs(my_hero_y-monster_y_now))
        if distance_from_hero_now <= 2200:
            return True
        return False
    if type_to_check == "to-shield-by-hero":  
        distance_from_hero_now = math.sqrt(abs(my_hero_x-monster_x_now) * abs(my_hero_x-monster_x_now) + abs(my_hero_y-monster_y_now) * abs(my_hero_y-monster_y_now))
        if distance_from_hero_now <= 2200:
            return True
        return False
    if type_to_check == "wind-hero": # WIND 1280
        distance_from_hero_now = math.sqrt(abs(my_hero_x-monster_x_now) * abs(my_hero_x-monster_x_now) + abs(my_hero_y-monster_y_now) * abs(my_hero_y-monster_y_now))
        if distance_from_hero_now <= 1280:
            return True
        return False
    if type_to_check == "hero-hit-by-enemy-control-future":
        spell_range = 2200
        enemy_that_can_control = -1
        for enemy_hero_id, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy = math.sqrt(abs(enemy_hero_x-my_hero_x) * abs(enemy_hero_x-my_hero_x) + abs(enemy_hero_y-my_hero_y) * abs(enemy_hero_y-my_hero_y))
            if enemy_mana >= 10 and not enemy_heroes[enemy_hero_id][3] > 0 and distance_from_enemy <= spell_range + 800:  # 800 is one step
                enemy_that_can_control = enemy_hero_id
        return enemy_that_can_control
    if type_to_check == "hero-hit-by-enemy-wind-future":
        spell_range = 1280
        enemy_that_can_control = -1
        for enemy_hero_id, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy = math.sqrt(abs(enemy_hero_x-my_hero_x) * abs(enemy_hero_x-my_hero_x) + abs(enemy_hero_y-my_hero_y) * abs(enemy_hero_y-my_hero_y))
            if enemy_mana >= 10 and distance_from_enemy + 800 <= spell_range: # 800 is one step
                enemy_that_can_control = enemy_hero_id
        return enemy_that_can_control
    if type_to_check == "hero-hit-by-enemy-control":
        spell_range = 2200
        hero_in_range_for_spell = False
        for key, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy = math.sqrt(abs(enemy_hero_x-my_hero_x) * abs(enemy_hero_x-my_hero_x) + abs(enemy_hero_y-my_hero_y) * abs(enemy_hero_y-my_hero_y))
            if enemy_mana >= 10 and distance_from_enemy <= spell_range:
                hero_in_range_for_spell = True
        return hero_in_range_for_spell
    if type_to_check == "hero-hit-by-enemy-wind":
        spell_range = 1280
        hero_in_range_for_spell = False
        for key, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy = math.sqrt(abs(enemy_hero_x-my_hero_x) * abs(enemy_hero_x-my_hero_x) + abs(enemy_hero_y-my_hero_y) * abs(enemy_hero_y-my_hero_y))
            if enemy_mana >= 10 and distance_from_enemy <= spell_range:
                hero_in_range_for_spell = True
        return hero_in_range_for_spell 
    if type_to_check == "monster-hit-by-enemy-wind":
        spell_range = 1280
        enemy_in_range_for_spell = False
        for key, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy_now = getDistanceBetween(hero_id, monster_id, key, "enemy-to-monster")
            if enemy_mana >= 10 and distance_from_enemy_now <= spell_range:
                enemy_in_range_for_spell = True
        return enemy_in_range_for_spell 
    if type_to_check == "monster-hit-by-enemy-control":
        spell_range = 2200
        enemy_in_range_for_spell = False
        for key, value in enemy_heroes.items():
            enemy_hero_x = value[1]
            enemy_hero_y = value[2]
            distance_from_enemy_now = getDistanceBetween(hero_id, monster_id, key, "enemy-to-monster")
            if enemy_mana >= 10 and distance_from_enemy_now <= spell_range:
                enemy_in_range_for_spell = True
        return enemy_in_range_for_spell      
    if type_to_check == "to-dmg-enemy-with-wind": # do damage to enemy base with doing a WIND spell
        distance_from_enemy_base_now = math.sqrt(abs(enemy_base_x-monster_x_now)*abs(enemy_base_x-monster_x_now)+abs(enemy_base_y-monster_y_now)*abs(enemy_base_y-monster_y_now))
        if isMonsterInRange(hero_id, monster_id, "wind-hero") and abs((distance_from_enemy_base_now + 2200)) >= 0:
            return True
    return False
    

def isInPosition(hero_id, position_to_check):
    my_hero_x = my_heroes[hero_id][1]
    my_hero_y = my_heroes[hero_id][2]
    if position_to_check == "defend":
        return  my_hero_x == abs(my_base_x - 3375) and my_hero_y ==  abs(my_base_y - 3375)
    if position_to_check == "patroulling-defend-0":
        return my_hero_x == patroulling_points["defend-0"][0] and patroulling_points["defend-0"][1]
    if position_to_check == "patroulling-defend-1":
        return my_hero_x == patroulling_points["defend-1"][0] and patroulling_points["defend-1"][1]
    if position_to_check == "patroulling-defend-2":
        return my_hero_x == patroulling_points["defend-2"][0] and patroulling_points["defend-2"][1]
    if position_to_check == "patroulling-defend-0":
        return my_hero_x == patroulling_points["score-0"][0] and patroulling_points["score-0"][1]
    if position_to_check == "patroulling-score-1":
        return my_hero_x == patroulling_points["score-1"][0] and patroulling_points["score-1"][1]
    if position_to_check == "patroulling-score-2":
        return my_hero_x == patroulling_points["score-2"][0] and patroulling_points["score-2"][1]
    if position_to_check == "patroulling-attack-0":
        return my_hero_x == patroulling_points["attack-0"][0] and patroulling_points["attack-0"][1]
    if position_to_check == "patroulling-attack-1":
        return my_hero_x == patroulling_points["attack-1"][0] and patroulling_points["attack-1"][1]
    if position_to_check == "patroulling-attack-2":
        return my_hero_x == patroulling_points["attack-2"][0] and patroulling_points["attack-2"][1]
#------------------------------------------------------------------#
# ACTIONS
#------------------------------------------------------------------#

def willMoveGeneric(monster_id):
    monster_x = monsters[monster_id][1]
    monster_x_vector = monsters[monster_id][6]
    monster_y = monsters[monster_id][2]
    monster_y_vector = monsters[monster_id][7]
    monster_future_x = monster_x + monster_x_vector
    monster_future_y = monster_y  + monster_y_vector

    predicted_distance_moved = math.sqrt(abs(monster_x_vector * monster_x_vector) + abs(monster_future_y * monster_future_y))
    moving_angle = math.asin(monster_y_vector/400)
    x_to_add_to_hero = math.cos(abs(moving_angle)) * 399
    y_to_add_to_hero = math.sin(abs(moving_angle)) * 399

    x_to_move_to = monster_future_x
    y_to_move_to = monster_future_y
    if my_base_x == 0:
        x_to_move_to -= x_to_add_to_hero
        y_to_move_to -= y_to_add_to_hero
    else:
        x_to_move_to += x_to_add_to_hero
        y_to_move_to += y_to_add_to_hero
    return [x_to_move_to, y_to_move_to]

def useShieldSpellOnHero(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL SHIELD " + str(hero_id) + " o.O"

def useWindSpellTowardsEnemyBaseByHero(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL WIND " + str(enemy_base_x) + " " + str(enemy_base_y) + " >:|"

def useWindSpellTowardsEnemyBaseByHeroAttack(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL WIND " + str(enemy_base_x) + " " + str(enemy_base_y) + " :P"

def moveHeroTowardsMonsterToDefend(hero_id, monster_id):
    hero_kill_monster[hero_id] = monster_id
    x_and_y_to_move_to = willMoveGeneric(monster_id)
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1]))) + " o.o"

def moveHeroTowardsMonsterToOnlyKill(hero_id, monster_id):
    hero_kill_monster[hero_id] = monster_id
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(monsters[monster_id][1] + monsters[monster_id][6])) + " " + str(abs(monsters[monster_id][2] + monsters[monster_id][7])) + " :("

def controlEnemyAttacker(hero_id, endangered_hero_id, enemy_hero_id):
    distance_from_enemy = getDistanceBetween(hero_id, "null", enemy_hero_id, "hero-to-enemy")
    if my_mana >= 10 and my_heroes[endangered_hero_id][3] <= 1:
        if distance_from_enemy > 2200:
            moveTowardsEnemy(hero_id, enemy_hero_id)
        else:
            if not enemy_heroes[enemy_hero_id][3] > 0:
                useControlSpellOnEnemy(hero_id, enemy_hero_id)
                return True
    return False

def moveTowardsEnemy(hero_id, enemy_hero_id):
    print("moving towards enemy " + str(enemy_hero_id), file=sys.stderr, flush=True)
    enemy_hero_x = enemy_heroes[enemy_hero_id][1]
    enemy_hero_y = enemy_heroes[enemy_hero_id][2]
    print("x = " + str(enemy_hero_x) + " y = " + str(enemy_hero_y), file=sys.stderr, flush=True)
    x_and_y_to_move_to = [enemy_hero_x, enemy_hero_y]
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1]))) + " :-S"  

def useControlSpellOnEnemy(hero_id, enemy_hero_id):
    moves_for_hero_dict[hero_id] = "SPELL CONTROL " + str(enemy_hero_id) + " " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " :D"

def useControlSpellOnEnemyOwnBase(hero_id, enemy_hero_id):
    hero_x = my_heroes[hero_id][1]
    hero_y = my_heroes[hero_id][2]
    enemy_x = enemy_heroes[enemy_hero_id][1]
    enemy_y = enemy_heroes[enemy_hero_id][2]
    control_towards_x = my_base_x
    control_towards_y = my_base_y
    if abs(enemy_x-enemy_base_x) < abs(hero_x-enemy_base_x) and abs(enemy_y-enemy_base_y) < abs(hero_y-enemy_base_y):
        control_towards_x = hero_x
        control_towards_y = hero_y
    moves_for_hero_dict[hero_id] = "SPELL CONTROL " + str(enemy_hero_id) + " " + str(abs(control_towards_x)) + " " + str(abs(control_towards_y)) + " :-D"

def useControlSpellOnEnemyEnemyBase(hero_id, enemy_hero_id):
    hero_x = my_heroes[hero_id][1]
    hero_y = my_heroes[hero_id][2]
    enemy_x = enemy_heroes[enemy_hero_id][1]
    enemy_y = enemy_heroes[enemy_hero_id][2]
    control_towards_x = enemy_base_x
    control_towards_y = enemy_base_y
    if abs(enemy_x-my_base_x) < abs(hero_x-my_base_x) and abs(enemy_y-my_base_y) < abs(hero_y-my_base_y):
        control_towards_x = hero_x
        control_towards_y = hero_y
    moves_for_hero_dict[hero_id] = "SPELL CONTROL " + str(enemy_hero_id) + " " + str(abs(control_towards_x)) + " " + str(abs(control_towards_y)) + " :-D"

def useWindSpellOnEnemyOwnBase(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL WIND "  + str(abs(my_base_x)) + " " + str(abs(my_base_y)) + " BYE"

def useWindSpellOnEnemyEnemyBase(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL WIND "  + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " BYE"


def moveHeroTowardsMonsterToControlTowardsEnemyBase(hero_id, monster_id):
    if isMonsterInRange(hero_id, monster_id, "to-control-by-hero") and getDistanceBetween(hero_id, monster_id, "null", "current-monster-to-enemy-base") > 5000 and getDistanceBetween(hero_id, monster_id, "null", "monster-to-enemy-base") < (1100 + 7100) and not monster_id in monster_was_controlled_shortly:
        controlMonsterTowardsEnemyBase(hero_id, monster_id)
        return True
    else:
        hero_kill_monster[hero_id] = monster_id
        x_and_y_to_move_to = willMoveGeneric(monster_id)
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1]))) + " :S"
        return False

def controlMonsterTowardsEnemyBase(hero_id, monster_id):
    moves_for_hero_dict[hero_id] = "SPELL CONTROL " + str(monster_id) + " " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " :O"
    monster_was_controlled_shortly[monster_id] = 6

def moveHeroTowardsMonsterToControlTowardsEnemyBaseDefensively(hero_id, monster_id):
    if isMonsterInRange(hero_id, monster_id, "to-control-by-hero") and getDistanceBetween(hero_id, monster_id, "null", "current-monster-to-enemy-base") > 5000 and not monster_id in monster_was_controlled_shortly:
        moves_for_hero_dict[hero_id] = "SPELL CONTROL " + str(monster_id) + " " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " :O"
        monster_was_controlled_shortly[monster_id] = 6
        print(str(moves_for_hero_dict), file=sys.stderr, flush=True)
    else:
        hero_kill_monster[hero_id] = monster_id
        x_and_y_to_move_to = willMoveGeneric(monster_id)
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1]))) + " :S"

def moveHeroTowardsMonsterToWindTowardsEnemyBase(hero_id, monster_id, extra_command):
    if isMonsterInRange(hero_id, monster_id, "wind-hero"):
        print("monster id for spell", file=sys.stderr, flush=True)
        moves_for_hero_dict[hero_id] = "SPELL WIND " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " " + extra_command
        return True
    else:
        hero_kill_monster[hero_id] = monster_id
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(monsters[monster_id][1] + monsters[monster_id][6])) + " " + str(abs(monsters[monster_id][2] + monsters[monster_id][7]))
        return True
    return False

def windTowardsEnemyBase(hero_id):
    moves_for_hero_dict[hero_id] = "SPELL WIND " + str(abs(enemy_base_x)) + " " + str(abs(enemy_base_y)) + " :-)"

def moveHeroTowardsMonsterToShieldNearEnemyBase(hero_id, monster_id):
    if isMonsterInRange(hero_id, monster_id, "to-shield-by-hero"):
        moves_for_hero_dict[hero_id] = "SPELL SHIELD " + str(monster_id) + " O:)"
    else:
        hero_kill_monster[hero_id] = monster_id
        x_and_y_to_move_to = willMoveGeneric(monster_id)
        moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1])))
        
def moveHeroTowardsMonsterToAttack(hero_id, monster_id):
    x_and_y_to_move_to = willMoveGeneric(monster_id)
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_and_y_to_move_to[0]))) + " " + str(abs(int(x_and_y_to_move_to[1])))

def moveHeroTowardsTwoMonsterToAttack(hero_id, monster_id_1, monster_id_2):
    x_to_move_to = 0
    y_to_move_to = 0
    x_monster_1 = monsters[monster_id_1][1]
    y_monster_1 = monsters[monster_id_1][2]
    x_monster_2 = monsters[monster_id_2][1]
    y_monster_2 = monsters[monster_id_2][2]

    x_to_move_to = (x_monster_1 + x_monster_2) / 2
    y_to_move_to = (y_monster_1 + y_monster_2) / 2
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(int(x_to_move_to))) + " " + str(abs(int(y_to_move_to)))

#------------------------------------------------------------------#
# DEFENSE
#------------------------------------------------------------------#





def moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToDefend(hero_id):
    shortest_current_distance_monster_id_to_control = 0
    shortest_current_distance_monster_id_with_threat = 0
    shortest_current_distance_with_threat = 18000
    shortest_current_distance_monster_id_without_threat = 0
    shortest_current_distance_without_threat = 18000
    ko_distance_to_base = getDistanceBetween(hero_id,"null", "null", "ko-distance-to-my-base")

    for monster_id, value in monsters.items():
        threat_of_monster = value[9]
        shield_value = value[3]
        distance_to_my_base = getDistanceBetween(hero_id, monster_id,"null","monster-to-my-base")

        if roles_for_heroes[hero_id] == "defend" and distance_to_my_base > 7100 + 400: # 400 for attack range of hero
            continue
        if monsterWouldTakeMyLife(hero_id, monster_id, value[3]) and my_mana >= 10:
            if shield_value == 0 and not wind_for_defense_used[monster_id]:
                wind_for_defense_used[monster_id] = True
                useWindSpellTowardsEnemyBaseByHero(hero_id)
                return
        if distance_to_my_base < shortest_current_distance_with_threat and distance_to_my_base <= ko_distance_to_base and threat_of_monster == 1: # threat to my base
            shortest_current_distance_with_threat = distance_to_my_base
            shortest_current_distance_monster_id_with_threat = monster_id
        elif distance_to_my_base < 12000 and distance_to_my_base > 5900:
            shortest_current_distance_monster_id_to_control = monster_id
        elif distance_to_my_base < shortest_current_distance_without_threat and threat_of_monster == 0: # no threat
            shortest_current_distance_without_threat = distance_to_my_base
            shortest_current_distance_monster_id_without_threat = monster_id
        else:
            patroullingDefensive(hero_id)

    if shortest_current_distance_monster_id_with_threat == 0 and shortest_current_distance_monster_id_without_threat == 0 and shortest_current_distance_monster_id_to_control == 0:
        patroullingDefensive(hero_id)
    
    if shortest_current_distance_monster_id_with_threat != 0 and (shortest_current_distance_with_threat <= ko_distance_to_base or shortest_current_distance_with_threat < shortest_current_distance_without_threat):
        moveHeroTowardsMonsterToDefend(hero_id, shortest_current_distance_monster_id_with_threat)
    elif my_mana >= 10 and shortest_current_distance_monster_id_to_control != 0:
        print("controlling defensively for monster " + str(shortest_current_distance_monster_id_to_control), file=sys.stderr, flush=True)
        moveHeroTowardsMonsterToControlTowardsEnemyBaseDefensively(hero_id, shortest_current_distance_monster_id_to_control)
        return
    elif shortest_current_distance_monster_id_without_threat != 0:
        moveHeroTowardsMonsterToAttack(hero_id, shortest_current_distance_monster_id_without_threat)

def moveTowardsThreatfulMonsterClosestToMyBaseToAnyHeroToOnlyKill(hero_id):
    shortest_current_distance_monster_id_with_threat = 0
    shortest_current_distance_with_threat = 18000
    shortest_current_distance_monster_id_without_threat = 0
    shortest_current_distance_without_threat = 18000
    ko_distance_to_base = getDistanceBetween(hero_id,"null", "null","ko-distance-to-my-base")
    monster_would_take_life = False
    for monster_id, value in monsters.items():
        threat_of_monster = value[9]
        shield_value = value[3]
        distance_to_my_base = getDistanceBetween(hero_id, monster_id,"null","monster-to-my-base")
        if roles_for_heroes[hero_id] == "defend" and distance_to_my_base > 7100 + 400: # 400 for attack range of hero
            continue
        if monsterWouldTakeMyLife(hero_id, monster_id, value[3]) and my_mana >= 10:
            if shield_value == 0 and not wind_for_defense_used[monster_id]:
                monster_would_take_life = True
                wind_for_defense_used[monster_id] = True
                useWindSpellTowardsEnemyBaseByHero(hero_id)
                return
        if shield_value > 0 and distance_to_my_base < shortest_current_distance_with_threat and distance_to_my_base <= ko_distance_to_base and threat_of_monster == 1: # threat to my base
            shortest_current_distance_with_threat = distance_to_my_base
            shortest_current_distance_monster_id_with_threat = monster_id
        elif shield_value == 0 and distance_to_my_base < shortest_current_distance_with_threat and distance_to_my_base <= ko_distance_to_base and threat_of_monster == 1: # threat to my base
            shortest_current_distance_with_threat = distance_to_my_base
            shortest_current_distance_monster_id_with_threat = monster_id
        elif distance_to_my_base < shortest_current_distance_without_threat and threat_of_monster == 0: # no threat
            shortest_current_distance_without_threat = distance_to_my_base
            shortest_current_distance_monster_id_without_threat = monster_id
    if shortest_current_distance_monster_id_with_threat == 0 and shortest_current_distance_monster_id_without_threat == 0:
        patroullingDefensive(hero_id)
    if not monster_would_take_life and shortest_current_distance_monster_id_with_threat != 0 and (shortest_current_distance_with_threat <= ko_distance_to_base or shortest_current_distance_with_threat < shortest_current_distance_without_threat):
        moveHeroTowardsMonsterToOnlyKill(hero_id, shortest_current_distance_monster_id_with_threat)
    elif not monster_would_take_life and shortest_current_distance_monster_id_without_threat != 0:
        moveHeroTowardsMonsterToOnlyKill(hero_id, shortest_current_distance_monster_id_without_threat)

def setHeroBaseMoveTowardsOwnBase(hero_id):
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(my_base_x - 3375)) + " " + str(abs(my_base_y - 3375))

def moveTowardsDefensivePatroullingPoint(hero_id):
    move_x = 0
    move_y = 0
    if patroulling_heroes[hero_id][0] == 0:
        move_x = patroulling_points["defend-0"][0]
        move_y = patroulling_points["defend-0"][1]
    elif patroulling_heroes[hero_id][0] == 1:
        move_x = patroulling_points["defend-1"][0]
        move_y = patroulling_points["defend-1"][1]
    elif patroulling_heroes[hero_id][0] == 2:
        move_x = patroulling_points["defend-2"][0]
        move_y = patroulling_points["defend-2"][1]
    moves_for_hero_dict[hero_id] = "MOVE " + str(move_x) + " " + str(move_y)

def V2_moveTowardsDefensivePatroullingPoint(hero_id):
    move_x = patroulling_points["defend-V2"][0]
    move_y = patroulling_points["defend-V2"][1]
    moves_for_hero_dict[hero_id] = "MOVE " + str(move_x) + " " + str(move_y)

def V2_moveTowardsDefensiveDmgPatroullingPoint(hero_id):
    move_x = patroulling_points["defend-dmg-V2"][0]
    move_y = patroulling_points["defend-dmg-V2"][1]
    moves_for_hero_dict[hero_id] = "MOVE " + str(move_x) + " " + str(move_y)

def patroullingDefensive(hero_id):
    # if patroulling_heroes[hero_id][0] == 0 and isInPosition(hero_id, "patroulling-defend-0"):
    #     patroulling_heroes[hero_id][0] = 1
    #     patroulling_heroes[hero_id][1] = 0
    # elif patroulling_heroes[hero_id][0] == 1 and isInPosition(hero_id, "patroulling-defend-1"):
    #     if patroulling_heroes[hero_id][1] == 0: # comes from point 0
    #         patroulling_heroes[hero_id][0] = 2
    #     else: # comes from point 2
    #         patroulling_heroes[hero_id][0] = 0
    #     patroulling_heroes[hero_id][1] = 1
    # elif patroulling_heroes[hero_id][0] == 2 and isInPosition(hero_id, "patroulling-defend-2"):
    #     patroulling_heroes[hero_id][0] = 1
    #     patroulling_heroes[hero_id][1] = 2
    moveTowardsDefensivePatroullingPoint(hero_id)



#------------------------------------------------------------------#
# ATTACK
#------------------------------------------------------------------#
def setHeroBaseMoveTowardsEnemyBase(hero_id):
    moves_for_hero_dict[hero_id] = "MOVE " + str(abs(enemy_base_x - 3375)) + " " + str(abs(enemy_base_y - 3375))



def patroullingAttack(hero_id):
    if patroulling_heroes[hero_id][0] == 0 and isInPosition(hero_id, "patroulling-attack-0"):
        patroulling_heroes[hero_id][0] = 1
        patroulling_heroes[hero_id][1] = 0
    elif patroulling_heroes[hero_id][0] == 1 and isInPosition(hero_id, "patroulling-attack-1"):
        if patroulling_heroes[hero_id][1] == 0: # comes from point 0
            patroulling_heroes[hero_id][0] = 2
        else: # comes from point 2
            patroulling_heroes[hero_id][0] = 0
        patroulling_heroes[hero_id][1] = 1
    elif patroulling_heroes[hero_id][0] == 2 and isInPosition(hero_id, "patroulling-attack-2"):
        patroulling_heroes[hero_id][0] = 1
        patroulling_heroes[hero_id][1] = 2
    # print("after setting points: " + str(patroulling_heroes), file=sys.stderr,flush=True)
    moveTowardsAttackPatroullingPoint(hero_id)

def moveTowardsAttackPatroullingPoint(hero_id):
    move_x = 0
    move_y = 0
    if patroulling_heroes[hero_id][0] == 0:
        move_x = patroulling_points["attack-0"][0]
        move_y = patroulling_points["attack-0"][1]
    elif patroulling_heroes[hero_id][0] == 1:
        move_x = patroulling_points["attack-1"][0]
        move_y = patroulling_points["attack-1"][1]
    elif patroulling_heroes[hero_id][0] == 2:
        move_x = patroulling_points["attack-2"][0]
        move_y = patroulling_points["attack-2"][1]
    moves_for_hero_dict[hero_id] = "MOVE " + str(move_x) + " " + str(move_y)



def canUseWindSpellOnEnemyToDefend(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToWind(hero_id)
    if enemy_id_near_hero != -1 and my_mana >= 10 and not enemy_heroes[enemy_id_near_hero][3] > 0:
        useWindSpellOnEnemyEnemyBase(hero_id)
        return_value = True
    return return_value

def canUseControlSpellOnEnemyToTakeLife(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToControl(hero_id)
    if enemy_id_near_hero != -1:
        for monster_id, value in monsters.items():
            monster_health = value[5]
            enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
            damage_taken_in_two_rounds = enemy_and_own_heroes_in_range_of_monster * 2 * 2
            remaining_monster_health = monster_health - damage_taken_in_two_rounds
            distance_to_enemy_base = getDistanceBetween(hero_id, monster_id, "null", "monster-to-enemy-base")
            if my_mana >= 10 and remaining_monster_health > 6 and distance_to_enemy_base < 5000 and not enemy_heroes[enemy_id_near_hero][3] > 0:
                useControlSpellOnEnemyOwnBase(hero_id, enemy_id_near_hero)
                return_value = True
    return return_value

def canUseControlSpellOnEnemyToDefend(hero_id):
    return_value = False
    enemy_id_near_hero = enemyNearHeroToControl(hero_id)
    if enemy_id_near_hero != -1:
        for monster_id, value in monsters.items():
            monster_health = value[5]
            enemy_and_own_heroes_in_range_of_monster = 1 # see how many enemy heroes are in the square from the enemy base to the monster
            damage_taken_in_two_rounds = enemy_and_own_heroes_in_range_of_monster * 2 * 2
            remaining_monster_health = monster_health - damage_taken_in_two_rounds
            distance_to_enemy_base = getDistanceBetween(hero_id, monster_id, "null", "monster-to-enemy-base")
            if my_mana >= 10 and remaining_monster_health > 6 and distance_to_enemy_base < 5000 and not enemy_heroes[enemy_id_near_hero][3] > 0:
                useControlSpellOnEnemyEnemyBase(hero_id, enemy_id_near_hero)
                return_value = True
    return return_value

# ----------------------------------------------------------------V1
# SCORE
#------------------------------------------------------------------#
def moveTowardsNearestMonsterToAnyHeroToAttack(hero_id):
    shortest_current_distance_monster_id = 0
    shortest_current_distance = 18000
    control_monster_id = 0
    second_monster_id_list = []

    for monster_id, value in monsters.items():
        distance_to_my_hero = getDistanceBetween(hero_id, monster_id,"null", "hero-to-monster")
        distance_to_my_base = getDistanceBetween(hero_id, monster_id,"null", "monster-to-my-base")
        predicted_distance_to_my_base = getDistanceBetween(hero_id, monster_id,"null", "monster-to-my-base-future")
        if my_mana >= 150 and not distance_to_my_base < 7100 and (distance_to_my_base - predicted_distance_to_my_base) > 200 and distance_to_my_hero <= 2200:
             control_monster_id = monster_id
        if not distance_to_my_base < 7100 and distance_to_my_hero < shortest_current_distance and monster_id not in monsters_attacked_by_hero_outside_base:
            shortest_current_distance_monster_id = monster_id
            for monster_id_2, value_2 in monsters.items():
                if not monster_id_2 == monster_id:
                    distance_between_monsters = getDistanceBetweenTwoMonsters(monster_id, monster_id_2)
                    if distance_between_monsters < 1599:
                        second_monster_id_list.append([monster_id,monster_id_2])

    if shortest_current_distance_monster_id == 0 or control_monster_id == 0:
        if roles_for_heroes[hero_id] == "score":
            patroullingScore(hero_id)
    if  my_mana >= 150 and control_monster_id != 0:
         controlMonsterTowardsEnemyBase(hero_id, control_monster_id)
    if second_monster_id_list != [] and second_monster_id_list[0]:
        monsters_attacked_by_hero_outside_base.append(second_monster_id_list[0][0])
        monsters_attacked_by_hero_outside_base.append(second_monster_id_list[0][1])
        moveHeroTowardsTwoMonsterToAttack(hero_id, second_monster_id_list[0][0], second_monster_id_list[0][1])
    elif shortest_current_distance_monster_id != 0:
        monsters_attacked_by_hero_outside_base.append(shortest_current_distance_monster_id)
        moveHeroTowardsMonsterToAttack(hero_id, shortest_current_distance_monster_id)

def patroullingScore(hero_id):
    if patroulling_heroes[hero_id][0] == 0 and isInPosition(hero_id, "patroulling-score-0"):
        patroulling_heroes[hero_id][0] = 1
        patroulling_heroes[hero_id][1] = 0
    elif patroulling_heroes[hero_id][0] == 1 and isInPosition(hero_id, "patroulling-score-1"):
        if patroulling_heroes[hero_id][1] == 0: # comes from point 0
            patroulling_heroes[hero_id][0] = 2
        else: # comes from point 2
            patroulling_heroes[hero_id][0] = 0
        patroulling_heroes[hero_id][1] = 1
    elif patroulling_heroes[hero_id][0] == 2 and isInPosition(hero_id, "patroulling-score-2"):
        patroulling_heroes[hero_id][0] = 1
        patroulling_heroes[hero_id][1] = 2
    moveTowardsScorePatroullingPoint(hero_id)
    return True

def moveTowardsScorePatroullingPoint(hero_id):
    move_x = 0
    move_y = 0
    if patroulling_heroes[hero_id][0] == 0:
        move_x = patroulling_points["score-0"][0]
        move_y = patroulling_points["score-0"][1]
    elif patroulling_heroes[hero_id][0] == 1:
        move_x = patroulling_points["score-1"][0]
        move_y = patroulling_points["score-1"][1]
    elif patroulling_heroes[hero_id][0] == 2:
        move_x = patroulling_points["score-2"][0]
        move_y = patroulling_points["score-2"][1]
    moves_for_hero_dict[hero_id] = "MOVE " + str(move_x) + " " + str(move_y)
    return True


