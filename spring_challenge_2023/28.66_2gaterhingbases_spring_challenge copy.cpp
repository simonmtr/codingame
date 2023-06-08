#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <list>
#include <queue>

using namespace std;

/*------------------------*/

/*------------------------*/

/* DIJSKSTRA*/

// Given an Adjacency List, find all shortest paths from "start" to all other vertices.
vector<pair<int, int>> DijkstraSP(vector<vector<pair<int, int>>> &adjList, int &start)
{
    // cerr << "\nGetting the shortest path from " << start << " to all other nodes.\n";
    vector<pair<int, int>> dist; // First int is dist, second is the previous node.

    // Initialize all source->vertex as infinite.
    int n = adjList.size();
    for (int i = 0; i < n; i++)
    {
        dist.push_back(make_pair(1000000007, i)); // Define "infinity" as necessary by constraints.
    }

    // Create a PQ.
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;

    // Add source to pq, where distance is 0.
    pq.push(make_pair(start, 0));
    dist[start] = make_pair(0, start);
    ;

    // While pq isn't empty...
    while (pq.empty() == false)
    {
        // Get min distance vertex from pq. (Call it u.)
        int u = pq.top().first;
        pq.pop();

        // Visit all of u's friends. For each one (called v)....
        for (int i = 0; i < adjList[u].size(); i++)
        {
            int v = adjList[u][i].first;
            int weight = adjList[u][i].second;

            // If the distance to v is shorter by going through u...
            if (dist[v].first > dist[u].first + weight)
            {
                // Update the distance of v.
                dist[v].first = dist[u].first + weight;
                // Update the previous node of v.
                dist[v].second = u;
                // Insert v into the pq.
                pq.push(make_pair(v, dist[v].first));
            }
        }
    }

    return dist;
}

pair<int, vector<int>> PrintShortestPath_both(vector<pair<int, int>> &dist, int &start, int &end)
{
    vector<int> nodes_path;
    int distance = 0; // adding one to make realistic length (home base counts as path)

    for (int i = 0; i < dist.size(); i++)
    {
        if (i == end)
        {
            distance = dist[i].first;
            int currnode = i;
            nodes_path.push_back(currnode);

            while (currnode != start)
            {
                currnode = dist[currnode].second;
                nodes_path.push_back(currnode);
            }
        }
    }
    return {distance + 1, nodes_path};
}

/* ------- */

struct Cell
{
    int index;
    int type;
    int initial_resources;
    int distance_to_home_base;
    vector<int> route_to_home_base;
    int distance_to_home_base2;
    vector<int> route_to_home_base2;
    vector<pair<int, int>> distance_to_other_cells;
    Cell(int index, int type, int initial_resources, int distance_to_home_base, vector<int> route_to_home_base, vector<pair<int, int>> distance_to_other_cells, int distance_to_home_base2, vector<int> route_to_home_base2)
    {
        this->index = index;
        this->initial_resources = initial_resources;
        this->type = type;
        this->distance_to_home_base = distance_to_home_base;
        this->route_to_home_base = route_to_home_base;
        this->distance_to_home_base2 = distance_to_home_base2;
        this->route_to_home_base2 = route_to_home_base2;
        this->distance_to_other_cells = distance_to_other_cells;
    }
    Cell() {}
};

struct sort_list_dthb
{
    inline bool operator()(const Cell &struct1, const Cell &struct2)
    {
        // if (struct1.initial_resources == struct2.initial_resources)
        // {
        // cerr << "same size" << endl;
        //     return (struct1.distance_to_home_base > struct2.distance_to_home_base);
        // // }
        // return (struct1.initial_resources < struct2.initial_resources);
        return (struct1.distance_to_home_base < struct2.distance_to_home_base);
    }
};

struct sort_list_dthb_2
{
    inline bool operator()(const Cell &struct1, const Cell &struct2)
    {
        // if (struct1.initial_resources == struct2.initial_resources)
        // {
        // cerr << "same size" << endl;
        //     return (struct1.distance_to_home_base > struct2.distance_to_home_base);
        // // }
        // return (struct1.initial_resources < struct2.initial_resources);
        return (struct1.distance_to_home_base2 < struct2.distance_to_home_base2);
    }
};

int main()
{

    int roundcounter = 0;
    vector<Cell> crystal_cells = {};
    vector<int> crystal_indexes = {};
    vector<Cell> egg_cells = {};
    vector<int> egg_indexes = {};
    vector<vector<pair<int, int>>> adjList;
    int max_resources_start = 0;

    int number_of_cells; // amount of hexagonal cells in this map
    cin >> number_of_cells;
    int V = number_of_cells;
    const int n = number_of_cells;
    for (int i = 0; i < n; i++)
    {
        // Create a vector to represent a row, and add it to the adjList.
        vector<pair<int, int>> row;
        adjList.push_back(row);
    }
    vector<int> adj[V];
    /*all dijsktra*/
    vector<Cell> all_cells;
    vector<vector<pair<int, int>>> all_dist;

    /*END*/
    cin.ignore();
    for (int i = 0; i < number_of_cells; i++)
    {
        int type;              // 0 for empty, 1 for eggs, 2 for crystal
        int initial_resources; // the initial amount of eggs/crystals on this cell
        int neigh_0;           // the index of the neighbouring cell for each direction
        int neigh_1;
        int neigh_2;
        int neigh_3;
        int neigh_4;
        int neigh_5;
        cin >> type >> initial_resources >> neigh_0 >> neigh_1 >> neigh_2 >> neigh_3 >> neigh_4 >> neigh_5;
        max_resources_start += initial_resources;
        if (neigh_0 != -1)
        {
            adjList[i].push_back(make_pair(neigh_0, 1));
        }
        if (neigh_1 != -1)
        {
            adjList[i].push_back(make_pair(neigh_1, 1));
        }
        if (neigh_2 != -1)
        {
            adjList[i].push_back(make_pair(neigh_2, 1));
        }
        if (neigh_3 != -1)
        {
            adjList[i].push_back(make_pair(neigh_3, 1));
        }
        if (neigh_4 != -1)
        {
            adjList[i].push_back(make_pair(neigh_4, 1));
        }
        if (neigh_5 != -1)
        {
            adjList[i].push_back(make_pair(neigh_5, 1));
        }
        cin.ignore();

        all_cells.push_back(Cell(i, type, initial_resources, 0, {}, {}, 0, {}));

        if (type == 2)
        {
            crystal_cells.push_back(Cell(i, type, initial_resources, 0, {}, {}, 0, {}));
            crystal_indexes.push_back(i);
        }
        else if (type == 1)
        {
            egg_cells.push_back(Cell(i, type, initial_resources, 0, {}, {}, 0, {}));
            egg_indexes.push_back(i);
        }
    }

    /* create distance list for each cell*/
    // cerr << "running dijkstra for all" << endl;
    for (int i = 0; i < all_cells.size(); i++)
    {
        vector<pair<int, int>> dist = DijkstraSP(adjList, all_cells.at(i).index);
        all_dist.push_back(dist);
        all_cells.at(i).distance_to_other_cells = dist;
    }
    // cerr << "DONE running dijkstra for all" << endl;
    // int cell_to_check = 9;
    // for (int i = 0; i < all_cells.at(cell_to_check).distance_to_other_cells.size(); i++)
    // {
    //     pair<int, vector<int>> distance_path = PrintShortestPath_both(all_cells.at(9).distance_to_other_cells, cell_to_check, all_cells.at(i).index);
    //     int length_of_path = distance_path.first;
    //     cerr << cell_to_check << " to " << i << " = " << length_of_path << endl;
    // }

    int my_base;
    int my_second_base;

    vector<int> my_bases;
    vector<int> enemy_bases;

    int number_of_bases;
    cin >> number_of_bases;
    cin.ignore();
    for (int i = 0; i < number_of_bases; i++)
    {
        int my_base_index;
        cin >> my_base_index;
        cin.ignore();
        my_bases.push_back(my_base_index);
        if (i == 0)
        {
            my_base = my_base_index;
        }
        else
        {
            my_second_base = my_base_index;
        }
    }
    for (int i = 0; i < number_of_bases; i++)
    {
        int opp_base_index;
        cin >> opp_base_index;
        cin.ignore();
        enemy_bases.push_back(opp_base_index);
    }

    // cerr <<
    /* MULTIPLE BASES */
    bool multiple_bases = number_of_bases > 1;
    int my_attacking_base = 0;
    int my_defending_base = 0;
    bool one_base_attacks = false;

    vector<int> route_from_my_attacking_base;
    if (multiple_bases && one_base_attacks)
    {
        int my_nearest_base_to_enemy_base = 0; // will be attacking base
        int current_nearest_distance = 10000;
        vector<int> current_nearest_path;
        for (int i = 0; i < my_bases.size(); i++)
        {
            vector<pair<int, int>> current_home_base_dist = DijkstraSP(adjList, my_bases.at(i));
            for (int j = 0; j < enemy_bases.size(); j++)
            {
                pair<int, vector<int>> distance_path = PrintShortestPath_both(current_home_base_dist, my_bases.at(i), enemy_bases.at(j));
                if (distance_path.first < current_nearest_distance)
                {
                    current_nearest_distance = distance_path.first;
                    current_nearest_path = distance_path.second;
                    my_nearest_base_to_enemy_base = my_bases.at(i);
                }
            }
        }
        my_attacking_base = my_nearest_base_to_enemy_base;
        route_from_my_attacking_base = current_nearest_path;
    }
    // cerr << "attacking: " << my_attacking_base << " taking route:" << endl;
    // for (int i = 0; i < route_from_my_attacking_base.size(); i++)
    // {
    //     cerr << "-> " << route_from_my_attacking_base.at(i) << endl;
    // }
    /* END MULTIPLE BASES */

    // all distance to my base
    vector<pair<int, int>> home_base_dist = DijkstraSP(adjList, my_base);
    for (int i = 0; i < egg_cells.size(); i++)
    {
        pair<int, vector<int>> distance_path = PrintShortestPath_both(home_base_dist, my_base, egg_cells.at(i).index);
        egg_cells.at(i).distance_to_home_base = distance_path.first;
        egg_cells.at(i).route_to_home_base = distance_path.second;
    }
    for (int i = 0; i < crystal_cells.size(); i++)
    {
        pair<int, vector<int>> distance_path = PrintShortestPath_both(home_base_dist, my_base, crystal_cells.at(i).index);
        crystal_cells.at(i).distance_to_home_base = distance_path.first;
        crystal_cells.at(i).route_to_home_base = distance_path.second;
    }
    // second base
    if (multiple_bases)
    {
        vector<pair<int, int>> home_base_dist2 = DijkstraSP(adjList, my_second_base);
        for (int i = 0; i < egg_cells.size(); i++)
        {
            pair<int, vector<int>> distance_path = PrintShortestPath_both(home_base_dist2, my_second_base, egg_cells.at(i).index);
            egg_cells.at(i).distance_to_home_base2 = distance_path.first;
            egg_cells.at(i).route_to_home_base2 = distance_path.second;
        }
        for (int i = 0; i < crystal_cells.size(); i++)
        {
            pair<int, vector<int>> distance_path = PrintShortestPath_both(home_base_dist2, my_second_base, crystal_cells.at(i).index);
            crystal_cells.at(i).distance_to_home_base2 = distance_path.first;
            crystal_cells.at(i).route_to_home_base2 = distance_path.second;
        }
    }

    // game loop
    while (1)
    {
        vector<int> target_route;
        vector<int> attacking_route;

        // sorting cells to nearest to base
        std::sort(egg_cells.begin(), egg_cells.end(), sort_list_dthb());
        std::sort(crystal_cells.begin(), crystal_cells.end(), sort_list_dthb());

        Cell best_crystal_cell = Cell();
        Cell best_egg_cell = Cell();
        int my_ants_total = 0;
        int opp_ants_total = 0;
        int max_crystal_resources_left = 0;

        int my_score;
        int opp_score;
        cin >> my_score >> opp_score; cin.ignore();
        for (int i = 0; i < number_of_cells; i++)
        {
            int resources; // the current amount of eggs/crystals on this cell
            int my_ants;   // the amount of your ants on this cell
            int opp_ants;  // the amount of opponent ants on this cell
            cin >> resources >> my_ants >> opp_ants;
            cin.ignore();
            cerr << "resources on " << i << " are " << resources << endl;
            cerr << "my_ants on " << i << " are " << my_ants << endl;
            cerr << "opp_ants on " << i << " are " << opp_ants << endl;

            my_ants_total = my_ants_total + my_ants;
            opp_ants_total = opp_ants_total + opp_ants;

            // TO OPTIMIZE: optimize with find_if
            if (find(egg_indexes.begin(), egg_indexes.end(), i) != egg_indexes.end())
            {
                for (int j = 0; j < egg_cells.size(); j++)
                {
                    if (egg_cells.at(j).index == i)
                    {
                        if (resources == 0)
                        {
                            // cerr << "EMPTY EGG " << i << endl;
                            int shiftindex = j;
                            while (egg_cells.back().index != i)
                            {
                                std::swap(egg_cells.at(shiftindex), egg_cells.at(shiftindex + 1));
                                shiftindex++;
                            }
                            egg_cells.pop_back();
                        }
                        else
                        {
                            egg_cells.at(j).initial_resources = resources;
                        }
                    }
                }
            }
            if (find(crystal_indexes.begin(), crystal_indexes.end(), i) != crystal_indexes.end())
            {
                for (int j = 0; j < crystal_cells.size(); j++)
                {
                    if (crystal_cells.at(j).index == i)
                    {
                        max_crystal_resources_left += resources;
                        if (resources == 0)
                        {
                            // cerr << "EMPTY CRYSTAL" << i << endl;
                            int shiftindex = j;
                            while (crystal_cells.back().index != i)
                            {
                                std::swap(crystal_cells.at(shiftindex), crystal_cells.at(shiftindex + 1));
                                shiftindex++;
                            }
                            crystal_cells.pop_back();
                        }
                        else
                        {
                            crystal_cells.at(j).initial_resources = resources;
                        }
                    }
                }
            }
        }

        /* chooosing logic */
        Cell sample_cell = Cell();
        /*-----------------*/
        int attacking_ants = 0;
        if (multiple_bases && one_base_attacks)
        {
            cerr << "total ants" << my_ants_total << endl; // TODO MAYBE ERROR
            int attacking_ants = my_ants_total * 0.5;
            my_ants_total = my_ants_total - attacking_ants;
        }

        // set sample cell
        bool enemy_ants_much_higher_than_mine = my_ants_total <= opp_ants_total;
        bool no_focus = true; // TODO IMPLEMENT
        bool egg_focus = max_resources_start > 200 || enemy_ants_much_higher_than_mine;
        bool crystal_focus = false; // TODO IMPLEMENT
        int max_ants_per_field = 1; // gets changed once we have route to all important nodes

        /* GATHERING ANTS */
        while (target_route.size() < my_ants_total)
        {
            if (!multiple_bases)
            {
                cerr << "one base" << endl;
                if (target_route.size() == 0)
                {
                    if (egg_cells.size() != 0 && enemy_ants_much_higher_than_mine && egg_focus)
                    {
                        sample_cell = egg_cells.at(0); // closest egg to my base
                    }
                    else
                    {
                        sample_cell = crystal_cells.at(0); // closest crystal to my base
                    }
                    target_route = sample_cell.route_to_home_base;
                    continue;
                }
            }
            // FIRST TURN MULTIPLE BASES
            else if (!one_base_attacks && multiple_bases) // only if i have 2 gathering bases
            {
                cerr << "two gathering bases " << endl;
                for (int i = 0; i < my_bases.size(); i++)
                {
                    bool base_used = find(target_route.begin(), target_route.end(), my_bases.at(i)) != target_route.end();
                    if (!base_used)
                    {
                        cerr << "base not used" << my_bases.at(i) << endl;
                        if (egg_cells.size() != 0 && enemy_ants_much_higher_than_mine && egg_focus)
                        {
                            std::sort(egg_cells.begin(), egg_cells.end(), sort_list_dthb());
                            sample_cell = egg_cells.at(0); // closest egg to my base
                        }
                        else
                        {
                            std::sort(crystal_cells.begin(), crystal_cells.end(), sort_list_dthb());
                            sample_cell = crystal_cells.at(0); // closest crystal to my base
                        }
                        if (i == 0)
                        {
                            for (int k = 0; k < sample_cell.route_to_home_base.size(); k++)
                            {
                                target_route.push_back(sample_cell.route_to_home_base.at(k));
                            }
                        }
                        else
                        {
                            for (int k = 0; k < sample_cell.route_to_home_base2.size(); k++)
                            {
                                target_route.push_back(sample_cell.route_to_home_base2.at(k));
                            }
                        }

                        continue;
                    }
                }
            }
            cerr << target_route.size() << endl; // I AM HERE

            bool all_important_edges_visited = true;
            int current_shortest_path_length = 1000000;
            vector<int> current_shortest_path_route;
            int current_shortest_path_length_cell_resources = 0;

            /* EGGS */
            if (egg_focus || no_focus)
            {
                for (int i = 0; i < egg_cells.size(); i++)
                {
                    Cell current_iteration_egg_cell = egg_cells.at(i);
                    bool already_visited = find(target_route.begin(), target_route.end(), current_iteration_egg_cell.index) != target_route.end();
                    if (!already_visited) // egg_cell not in route => not visited
                    {
                        for (int j = 0; j < target_route.size(); j++) // for each cell in current route
                        {
                            int index_of_target_route_cell = target_route.at(j); // get cell index
                            // get shortest paths for current egg cell to this cell in path
                            Cell current_egg = all_cells.at(current_iteration_egg_cell.index); // update egg, because its different objects in all_cells and egg_cells
                            pair<int, vector<int>> distance_path_from_egg_cell_to_route = PrintShortestPath_both(current_egg.distance_to_other_cells, current_iteration_egg_cell.index, index_of_target_route_cell);

                            bool same_distance_higher_resources = distance_path_from_egg_cell_to_route.first == current_shortest_path_length && current_iteration_egg_cell.initial_resources > current_shortest_path_length_cell_resources;
                            bool lower_distance = distance_path_from_egg_cell_to_route.first < current_shortest_path_length;
                            if (lower_distance || same_distance_higher_resources)
                            {
                                current_shortest_path_length = distance_path_from_egg_cell_to_route.first;
                                current_shortest_path_route = distance_path_from_egg_cell_to_route.second;
                                current_shortest_path_length_cell_resources = current_iteration_egg_cell.initial_resources;
                                all_important_edges_visited = false;
                            }
                        }
                    }
                }
            }
            /* CRYSTALS */
            if (crystal_focus || no_focus)
            {
                for (int i = 0; i < crystal_cells.size(); i++)
                {
                    Cell current_iteration_crystal_cell = crystal_cells.at(i);
                    bool already_visited = find(target_route.begin(), target_route.end(), current_iteration_crystal_cell.index) != target_route.end();
                    if (!already_visited) // egg_cell not in route => not visited
                    {
                        for (int j = 0; j < target_route.size(); j++) // for each cell in current route
                        {
                            int index_of_target_route_cell = target_route.at(j); // get cell index
                            // get shortest paths for current egg cell to this cell in path
                            Cell current_crystal = all_cells.at(current_iteration_crystal_cell.index); // update crystal, because its different objects in all_cells and egg_cells
                            pair<int, vector<int>> distance_path_from_crystal_cell_to_route = PrintShortestPath_both(current_crystal.distance_to_other_cells, current_iteration_crystal_cell.index, index_of_target_route_cell);

                            bool same_distance_higher_resources = distance_path_from_crystal_cell_to_route.first == current_shortest_path_length && current_iteration_crystal_cell.initial_resources > current_shortest_path_length_cell_resources;
                            bool lower_distance = distance_path_from_crystal_cell_to_route.first < current_shortest_path_length;
                            if (lower_distance || same_distance_higher_resources)
                            {
                                current_shortest_path_length = distance_path_from_crystal_cell_to_route.first;
                                current_shortest_path_route = distance_path_from_crystal_cell_to_route.second;
                                current_shortest_path_length_cell_resources = current_iteration_crystal_cell.initial_resources;
                                all_important_edges_visited = false;
                            }
                        }
                    }
                }
            }

            if (!all_important_edges_visited) // not all eggs and crystals are on route
            {
                for (int i = 0; i < current_shortest_path_route.size(); i++)
                {
                    target_route.push_back(current_shortest_path_route.at(i));
                }
            }
            else // all eggs and crystals are on route
            {
                // -> don't change the routes but increase the weights to max
                // TODO IMPROVE: MAKE SMARTER: routes should have good better weight distribution
                max_ants_per_field = my_ants_total / target_route.size();
                break;
            }
        }
        /* END GATHERING ANTS */

        string printstring = "";
        int goal_index = sample_cell.route_to_home_base.at(0);

        for (int i = 0; i < target_route.size(); i++)
        {

            // TODO: MAX value
            int max_value_to_set = my_ants_total - target_route.size();
            if (max_value_to_set < 0)
            {
                max_value_to_set = 0;
            }
            if (i == 0)
            {
                // most outer edge
                printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(max_ants_per_field) + ";";
            }
            else
            {
                printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(max_ants_per_field) + ";";

                // printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(1) + ";";
            }
        }

        /* ATTACKING ROUTE */
        if (multiple_bases && one_base_attacks)
        {
            int max_attacking_ants = attacking_ants / route_from_my_attacking_base.size();
            for (int i = 0; i < route_from_my_attacking_base.size(); i++)
            {
                printstring = printstring + "BEACON " + to_string(route_from_my_attacking_base.at(i)) + " " + to_string(max_attacking_ants) + ";";
            }
        }

        /* END ATTACKING ROUTE */

        // printstring = "LINE " + to_string(my_base) + " " + to_string(sample_cell.index) + " " + to_string(max_ants_per_field);

        std::cout << printstring << endl;
        // cout << "LINE " << my_base << " " << sample_cell.index << " 10" << endl;
    }
}