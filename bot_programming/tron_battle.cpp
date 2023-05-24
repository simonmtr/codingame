#include <algorithm>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

class Tron {
public:
  int current_x;
  int current_y;
  int tail_x;
  int tail_y;
  Tron(int tail_x_new, int tail_y_new, int current_x_new, int current_y_new) {
    current_x = current_x_new;
    current_y = current_y_new;
    tail_x = tail_x_new;
    tail_y = tail_y_new;
  }
  Tron() {}
};

string get_best_move(int board[30][20], Tron current_tron) {

    return "DOWN";
}

string next_move(int board[30][20], Tron current_tron) {

return "DOWN";
}



int main() {
  int max_x = 30;
  int max_y = 20;
  int board[30][20] = {};

  int round = 0;
  // game loop
  while (1) {
    string current_direction = "";
    round++;
    Tron mytron = Tron();
    vector<Tron> enemytrons = {};
    int n; // total number of players (2 to 4).
    int p; // your player number (0 to 3).
    cin >> n >> p;
    cin.ignore();
    for (int i = 0; i < n; i++) {
      int x0; // starting X coordinate of lightcycle (or -1)
      int y0; // starting Y coordinate of lightcycle (or -1)
      int x1; // starting X coordinate of lightcycle (can be the same as X0 if
              // you play before this player)
      int y1; // starting Y coordinate of lightcycle (can be the same as Y0 if
              // you play before this player)
      cin >> x0 >> y0 >> x1 >> y1;
      // setting board
      if (round == 1) {
        board[x0][y0] = 1;
      }
      board[x1][y1] = 1;

      cin.ignore();
      if (i == p) {
        mytron = Tron(x0, y0, x1, y1);
      } else {
        enemytrons.push_back(Tron(x0, y0, x1, y1));
      }
    }
    // cerr << board[mytron.current_x][mytron.current_y] << endl;

    // Write an action using cout. DON'T FORGET THE "<< endl"
    // To debug: cerr << "Debug messages..." << endl;

    // edgetesting
    bool mytron_right_edge = (mytron.current_x+1) == max_x;
    bool mytron_left_edge = (mytron.current_x) <= 0;
    bool mytron_edge_down = (mytron.current_y+1) == max_y;
    bool mytron_edge_up = (mytron.current_y) <= 0;

    cerr << "y: " << mytron.current_y << endl;
    cerr << "y-1: " << mytron_edge_up << endl;
    cerr << mytron_edge_up << endl;

    if (mytron_right_edge || mytron_left_edge) {
      cerr << "will hit wall x" << endl;
    cerr << mytron.current_y << endl;
    cerr << max_y << endl;
      if (mytron.current_y == max_y) { // has to go up because in corner
        current_direction = "UP";
      } else if (mytron.current_y <= 0) { // has to go down because in corner
        current_direction = "DOWN";
      } else {
        bool up_is_line = board[mytron.current_x][mytron.current_y - 1] == 1;
        bool down_is_line = board[mytron.current_x][mytron.current_y + 1] == 1;
        if (up_is_line) {
          cerr << 'd' << endl;
          current_direction = "DOWN";
        } else if (down_is_line) {
          cerr << 'u' << endl;
          current_direction = "UP";
        } else {
            if (current_direction != "DOWN") {
                current_direction = "UP";
            } else if (current_direction != "UP") {
                current_direction = "DOWN";
            }
        }
      }
    }
    if ((current_direction != "") && (mytron_edge_down || mytron_edge_up)) {
      cerr << "will hit wall y" << endl;

      if (mytron.current_x == max_x) { // has to go left because in corner
        current_direction = "LEFT";
      } else if (mytron.current_x <
                 0) { // has to go right because in corner
        current_direction = "RIGHT";
      } else {
        bool right_is_line = board[mytron.current_x - 1][mytron.current_y] == 1;
        bool left_is_line = board[mytron.current_x + 1][mytron.current_y] == 1;
        if (left_is_line) {
          cerr << 'l' << endl;
          current_direction = "LEFT";
        } else if (right_is_line) {
          cerr << 'r' << endl;
          current_direction = "RIGHT";
        } else {
            if (current_direction != "LEFT") {
                current_direction = "RIGHT";
            } else if (current_direction != "RIGHT"){
                current_direction = "LEFT";
            }
        }
      }
    }
    if (current_direction == "") {
        current_direction = "LEFT";
    }
    cout << current_direction << endl;
  }
}