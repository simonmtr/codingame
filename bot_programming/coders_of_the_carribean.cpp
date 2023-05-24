
#include <algorithm>
#include <bits/stdc++.h>
#include <iostream>
#include <string>
#include <vector>

using namespace std;
// Write an action using cout. DON'T FORGET THE "<< endl"
// To debug: cerr << "Debug messages..." << endl;

class Coordinate {
public:
  int x;
  int y;
  Coordinate(int new_x, int new_y) {
    x = new_x;
    y = new_y;
  }
};

class Ship {
public:
  int x;
  int y;
  int rotation;
  int speed;
  int owner;
  Ship(int new_x, int new_y, int new_owner, int new_speed, int new_rotation) {
    x = new_x;
    y = new_y;
    owner = new_owner;
    speed = new_speed;
    rotation = new_rotation;
  }
};

float get_distance(int x1, int y1, int x2, int y2) {
  return sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2) * 1.0);
}

Coordinate closest_barrel_coordinate(Ship ship, vector<Coordinate> barrels) {
  float current_closest_value = 100;
  Coordinate current_closest_coordinate = Coordinate(100, 100);
  for (int i = 0; i < barrels.size(); i++) {
    float distance = get_distance(ship.x, ship.y, barrels[i].x, barrels[i].y);
    if (distance < current_closest_value) {
    //   cerr << distance << endl;
      current_closest_coordinate = Coordinate(barrels[i].x, barrels[i].y);
      current_closest_value = distance;
    }
  }

  return current_closest_coordinate;
}

Ship closest_enemy_ship(Ship ship, vector<Ship> ships) {
  float current_closest_value = 100;
  Ship current_closest_coordinate = Ship(100,100,0,2,5);
  for (int i = 0; i < ships.size(); i++) {
    float distance = get_distance(ship.x, ship.y, ships[i].x, ships[i].y);
    if (distance < current_closest_value) {
      current_closest_coordinate = Ship(ships[i]);
      current_closest_value = distance;
    }
  }

  return current_closest_coordinate;
}

Coordinate get_position_in_future(Ship nearest_enemy_ship,
                                  int rounds_until_hit) {
  Coordinate future_position =
      Coordinate(nearest_enemy_ship.x, nearest_enemy_ship.y);
  switch (nearest_enemy_ship.rotation) {
  case 0:
    future_position.x += rounds_until_hit * 1;
    break;
  case 1:
    future_position.x += rounds_until_hit * 1;
    future_position.y += rounds_until_hit * -1;
    break;
  case 2:
    future_position.y += rounds_until_hit * -1;
    break;
  case 3:
    future_position.y += rounds_until_hit * -1;
    break;
  case 4:
    future_position.y += rounds_until_hit * 1;
    break;
  case 5:
    future_position.x += rounds_until_hit * 1;
    future_position.y += rounds_until_hit * 1;
    break;
  }
  return future_position;
}

int main() {
  int round = 0;
  int last_mine_round = 0;
  int last_fire_round = 0;
  // game loops
  while (1) {
    round++;

    vector<Coordinate> barrels = {};
    vector<Ship> owned_ships = {};
    vector<Ship> enemy_ships = {};
    string printstring = "";
    int my_ship_count; // the number of remaining ships
    cin >> my_ship_count;
    cin.ignore();
    int entity_count; // the number of entities (e.g. ships, mines or
                      // cannonballs)
    cin >> entity_count;
    cin.ignore();
    for (int i = 0; i < entity_count; i++) {
      int entity_id;
      string entity_type;
      int x;
      int y;
      int arg_1;
      int arg_2;
      int arg_3;
      int arg_4;
      cin >> entity_id >> entity_type >> x >> y >> arg_1 >> arg_2 >> arg_3 >>
          arg_4;
      cin.ignore();
      if (entity_type == "SHIP" && arg_4 == 1) {
        // myship
        owned_ships.push_back(Ship(x, y, arg_4, arg_2, arg_1));
      } else if (entity_type == "SHIP" && arg_4 == 0) {
        enemy_ships.push_back(Ship(x, y, arg_4, arg_2, arg_1));
      }
      if (entity_type == "BARREL") {
        barrels.push_back(Coordinate(x, y));
      }
    }
    for (int i = 0; i < my_ship_count; i++) {
      Ship current_owned_ship = owned_ships.back();
      owned_ships.pop_back();
      cerr << current_owned_ship.x << endl;
      cerr << current_owned_ship.y << endl;
      Coordinate nearest_barrel =
          closest_barrel_coordinate(current_owned_ship, barrels);
      Ship nearest_enemy_ship =
          closest_enemy_ship(current_owned_ship, enemy_ships);
      cerr << nearest_barrel.x << nearest_barrel.y << endl;
      // check if can place mine, if yes then do:
      // if ((last_mine_round + 4) < round) {
      if ((last_mine_round + 100) < round) {
        // can use mine
        printstring = "MINE";
        last_mine_round = round;
      } else if (((last_fire_round + 2) < round) &&
                 current_owned_ship.speed != 0) {
        int rounds_until_hit =
            1 + (get_distance(current_owned_ship.x, current_owned_ship.y,
                              nearest_enemy_ship.x, nearest_enemy_ship.y)) /
                    3;
        cerr << "enemy x and y " << nearest_enemy_ship.x << " - " << nearest_enemy_ship.y << endl;
        Coordinate position_in_rounds_until_hit =
            get_position_in_future(nearest_enemy_ship, rounds_until_hit);
        printstring = "FIRE " + to_string(position_in_rounds_until_hit.x) + " " +
                      to_string(position_in_rounds_until_hit.y);

        last_fire_round = round;
      } else {
        // check if can fire
        printstring = "MOVE " + to_string(nearest_barrel.x) + " " +
                      to_string(nearest_barrel.y);
      }

      cout << printstring
           << endl; // Any valid action, such as "WAIT" or "MOVE x y"
    }
  }
}