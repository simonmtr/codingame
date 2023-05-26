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
    int index_of_closest_important_node;
    Cell(int index, int type, int initial_resources, int distance_to_home_base, int index_of_closest_important_node, vector<int> route_to_home_base)
    {
        this->index = index;
        this->initial_resources = initial_resources;
        this->type = type;
        this->distance_to_home_base = distance_to_home_base;
        this->route_to_home_base = route_to_home_base;
        this->index_of_closest_important_node = index_of_closest_important_node;
        ;
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
        return (struct1.initial_resources < struct2.initial_resources);
    }
};

int main()
{
    vector<Cell> crystal_cells = {};
    vector<int> crystal_indexes = {};
    vector<Cell> egg_cells = {};
    vector<int> egg_indexes = {};
    int my_base;
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
        if (type == 2)
        {
            crystal_cells.push_back(Cell(i, type, initial_resources, 0, 0, {}));
            crystal_indexes.push_back(i);
        }
        else if (type == 1)
        {
            egg_cells.push_back(Cell(i, type, initial_resources, 0, 0, {}));
            egg_indexes.push_back(i);
        }
    }

    int number_of_bases;
    cin >> number_of_bases;
    cin.ignore();
    for (int i = 0; i < number_of_bases; i++)
    {
        int my_base_index;
        cin >> my_base_index;
        cin.ignore();
        my_base = my_base_index;
    }

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

    // Cell test_cell = egg_cells.back();
    // cerr << test_cell.initial_resources << endl;

    for (int i = 0; i < number_of_bases; i++)
    {
        int opp_base_index;
        cin >> opp_base_index;
        cin.ignore();
    }

    // game loop
    while (1)
    {
        vector<int> target_route;

        // sorting cells to nearest to base
        std::sort(egg_cells.begin(), egg_cells.end(), sort_list_dthb());
        std::sort(crystal_cells.begin(), crystal_cells.end(), sort_list_dthb());

        Cell best_crystal_cell = Cell();
        Cell best_egg_cell = Cell();
        int my_ants_total = 0;
        int opp_ants_total = 0;
        int max_crystal_resources_left = 0;

        for (int i = 0; i < number_of_cells; i++)
        {
            int resources; // the current amount of eggs/crystals on this cell
            int my_ants;   // the amount of your ants on this cell
            int opp_ants;  // the amount of opponent ants on this cell
            cin >> resources >> my_ants >> opp_ants;
            cin.ignore();

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

        // set sample cell
        bool enemy_ants_much_higher_than_mine = my_ants_total <= opp_ants_total;
        bool egg_focus = max_resources_start > 300;
        egg_focus = true;
        vector<int> visited_end_nodes;

        int max_ants_per_field = 1; // gets changed once we have route to all important nodes

        while (target_route.size() < my_ants_total)
        {
            cerr << "WHILE " << my_ants_total << " " << target_route.size() << endl;
            // 1. no target_route -> target cell has to be closest to home base
            // 2. find nearest cell to route to
            // 3. find shortest path from my base or one of the cells in current route
            // 4. add this path to target_route

            // first turn
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
                visited_end_nodes.push_back(target_route.at(0));
                cerr << "first step to " << target_route.at(0) << endl;
                continue;
            }
            cerr << "finding next step" << endl;

            // 2.
            vector<pair<int, int>> last_cell_dist = DijkstraSP(adjList, target_route.at(0));
            int nearest_cell_index = my_base;
            Cell nearest_cell = Cell();
            int start_to_nearest_cell_index = 10000;
            int temp_min_distance = 10000;
            for (int i = 0; i < egg_cells.size(); i++)
            {
                bool already_visited = find(target_route.begin(), target_route.end(), egg_cells.at(i).index) != target_route.end(); // TODO
                cerr << "already visited:" << egg_cells.at(i).index << " - " << already_visited << endl;
                if (egg_cells.at(i).index != target_route.at(0) && !already_visited)
                {
                    pair<int, vector<int>> distance_path = PrintShortestPath_both(last_cell_dist, target_route.at(0), egg_cells.at(i).index);
                    if (distance_path.first != 0 && distance_path.first < temp_min_distance)
                    {
                        nearest_cell_index = egg_cells.at(i).index;
                        nearest_cell = egg_cells.at(i);
                        start_to_nearest_cell_index = target_route.at(0);
                        temp_min_distance = distance_path.first;
                    }
                }
                pair<int, vector<int>> distance_path_home = PrintShortestPath_both(home_base_dist, my_base, egg_cells.at(i).index);
                if (distance_path_home.first != 0 && distance_path_home.first < temp_min_distance && !already_visited)
                {
                    nearest_cell_index = egg_cells.at(i).index;
                    nearest_cell = egg_cells.at(i);
                    start_to_nearest_cell_index = my_base;
                    temp_min_distance = distance_path_home.first;
                }
            }
            for (int i = 0; i < crystal_cells.size(); i++)
            {
                bool already_visited = find(target_route.begin(), target_route.end(), crystal_cells.at(i).index) != target_route.end();
                if (crystal_cells.at(i).index != target_route.at(0) && !already_visited)
                {
                    pair<int, vector<int>> distance_path = PrintShortestPath_both(last_cell_dist, target_route.at(0), crystal_cells.at(i).index);
                    if (distance_path.first != 0 && distance_path.first < temp_min_distance)
                    {
                        nearest_cell_index = crystal_cells.at(i).index;
                        nearest_cell = crystal_cells.at(i);
                        start_to_nearest_cell_index = target_route.at(0);
                        temp_min_distance = distance_path.first;
                    }
                }
                pair<int, vector<int>> distance_path_home2 = PrintShortestPath_both(home_base_dist, my_base, crystal_cells.at(i).index);
                if (distance_path_home2.first != 0 && distance_path_home2.first < temp_min_distance && !already_visited)
                {
                    nearest_cell_index = crystal_cells.at(i).index;
                    nearest_cell = crystal_cells.at(i);
                    start_to_nearest_cell_index = my_base;
                    temp_min_distance = distance_path_home2.first;
                }
            }
            if (start_to_nearest_cell_index != 10000)
            {
                for (int i = 0; i < nearest_cell.route_to_home_base.size(); i++)
                {
                    target_route.push_back(nearest_cell.route_to_home_base.at(i));
                }
                cerr << "going to" << nearest_cell.index << " from " << start_to_nearest_cell_index << endl;
                cerr << "second: going to" << nearest_cell.index << " from " << start_to_nearest_cell_index << endl;
            }
            else
            {
                // all important nodes visited
                // -> don't change the routes but increase the weights to max
                int max_ants_per_field = my_ants_total / target_route.size();
                break;
            }
        }

        /* WHAT DOES THIS CODE DO????
        IS IT NEEDED???*/
        // // check if current route is in target route
        // if (target_route.size() == 0)
        // { // first turn
        //     target_route = sample_cell.route_to_home_base;
        // }
        // else if (target_route.at(0) == sample_cell.route_to_home_base.at(0))
        // {
        //     cerr << "route in target route" << endl;
        // }
        // else
        // {
        //     cerr << "route NOT in target route" << endl;
        //     vector<int> temp_route = sample_cell.route_to_home_base;
        //     for (int i = 0; i < target_route.size(); i++)
        //     {
        //         temp_route.push_back(target_route.at(i));
        //     }
        //     target_route = temp_route;
        //     // cerr << target_route.at(0) << " - " << sample_cell.route_to_home_base.at(0) << endl;
        // }

        // check if enough ants to sent to next point
        // if (target_route.size() < my_ants_total)
        // {
        //     // TODO: increase routes
        //     // at least one ant available for each cell in route -> route established to home
        //     // todo: set new sample cell, keep old route
        //     if (target_route.size() == 0)
        //     {
        //         target_route = sample_cell.route_to_home_base;
        //     }
        //     else
        //     {
        //         // todo
        //     }
        // }
        /* END OF CONFUSION*/

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

                printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(max_ants_per_field) + ";";
            }
            else
            {
                printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(max_ants_per_field) + ";";

                // printstring = printstring + "BEACON " + to_string(target_route.at(i)) + " " + to_string(1) + ";";
            }
        }
        // printstring = "LINE " + to_string(my_base) + " " + to_string(sample_cell.index) + " " + to_string(max_ants_per_field);
        std::cout << printstring << endl;
        // cout << "LINE " << my_base << " " << sample_cell.index << " 10" << endl;
    }
}