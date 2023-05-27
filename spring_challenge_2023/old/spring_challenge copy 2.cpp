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
vector<int> DijkstraSP(vector<vector<pair<int, int>>> &adjList, int &start)
{
    cerr << "\nGetting the shortest path from " << start << " to all other nodes.\n"
         << endl;
    vector<int> dist;

    // Initialize all source->vertex as infinite.
    int n = adjList.size();
    for (int i = 0; i < n; i++)
    {
        dist.push_back(1000000007); // Define "infinity" as necessary by constraints.
    }
    // Create a PQ.
    priority_queue<pair<int, int>, vector<pair<int, int>>, greater<pair<int, int>>> pq;
    // Add source to pq, where distance is 0.
    pq.push(make_pair(start, 0));
    dist[start] = 0;
    // While pq isn't empty...
    while (pq.empty() == false)
    {
        // Get min distance vertex from pq. (Call it u.)
        int u = pq.top().first;
        pq.pop();
        // Visit all of u's friends. For each one (called v)
        for (int i = 0; i < adjList[u].size(); i++)
        {
            int v = adjList[u][i].first;
            int weight = adjList[u][i].second;
            // If the distance to v is shorter by going through u
            if (dist[v] > dist[u] + weight)
            {
                // Update the distance of v.
                dist[v] = dist[u] + weight;
                // Insert v into the pq.
                pq.push(make_pair(v, dist[v]));
            }
        }
    }

    return dist;
}
void PrintShortestPath_steps(vector<int> &dist, int &start)
    {
    cerr << "\nPrinting the shortest paths for node " << start << ".\n" << endl;
    for(int i = 0; i < dist.size(); i++)
        {
        cerr << "The distance from node " << start << " to node " << i << " is: " << dist[i] << endl;
        
        int currnode = i;
        cerr << "The path is: " << currnode << endl;
        while(currnode != start)
            {
            currnode = dist[currnode];
            cerr << " <- " << currnode << endl;
            }
        cerr << endl << endl;
        }
    }

void PrintShortestPath(vector<int> &dist, int &start)
{
    cerr << "\nPrinting the shortest paths for node " << start << ".\n";
    for (int i = 0; i < dist.size(); i++)
    {
        cerr << "The distance from node " << start << " to node " << i << " is: " << dist[i] << endl;
    }
}

/* ------- */

struct Cell
{
    int index;
    int type;
    int initial_resources;
    int distance_to_home_base;
    int index_of_closest_important_node;
    Cell(int index, int type, int initial_resources, int distance_to_home_base, int index_of_closest_important_node)
    {
        this->index = index;
        this->initial_resources = initial_resources;
        this->type = type;
        this->distance_to_home_base = distance_to_home_base;
        this->index_of_closest_important_node = index_of_closest_important_node;
        ;
    }
    Cell() {}
};

struct less_than_key
{
    inline bool operator()(const Cell &struct1, const Cell &struct2)
    {
        if (struct1.initial_resources == struct2.initial_resources)
        {
            cerr << "same size" << endl;
            return (struct1.distance_to_home_base > struct2.distance_to_home_base);
        }
        return (struct1.initial_resources < struct2.initial_resources);
    }
};

int main()
{
    vector<Cell> crystal_cells = {};
    vector<Cell> egg_cells = {};
    int my_base;

    vector<vector<pair<int, int>>> adjList;

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
            crystal_cells.push_back(Cell(i, type, initial_resources, 0, 0));
        }
        else if (type == 1)
        {
            egg_cells.push_back(Cell(i, type, initial_resources, 0, 0));
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
    vector<int> home_base_dist = DijkstraSP(adjList, my_base);
    for (int i = 0; i < egg_cells.size(); i++)
    {
        egg_cells.at(i).distance_to_home_base = home_base_dist[egg_cells.at(i).index];
    }
    for (int i = 0; i < crystal_cells.size(); i++)
    {
        crystal_cells.at(i).distance_to_home_base = home_base_dist[crystal_cells.at(i).index];
    }
    std::sort(egg_cells.begin(), egg_cells.end(), less_than_key());
    std::sort(crystal_cells.begin(), crystal_cells.end(), less_than_key());

    Cell test_cell = egg_cells.back();
    cerr << test_cell.initial_resources << endl;
    cerr << "distance from base to " << test_cell.index << "with dtb " << test_cell.distance_to_home_base << " is " << home_base_dist[test_cell.index] << endl;
    PrintShortestPath(home_base_dist, my_base);
    PrintShortestPath_steps(home_base_dist, my_base);

    for (int i = 0; i < number_of_bases; i++)
    {
        int opp_base_index;
        cin >> opp_base_index;
        cin.ignore();
    }

    // game loop
    while (1)
    {
        Cell sample_cell = Cell();

        for (int i = 0; i < number_of_cells; i++)
        {
            int resources; // the current amount of eggs/crystals on this cell
            int my_ants;   // the amount of your ants on this cell
            int opp_ants;  // the amount of opponent ants on this cell
            cin >> resources >> my_ants >> opp_ants;
            cin.ignore();

            if (egg_cells.size() != 0 && my_ants <= opp_ants)
            {
                sample_cell = egg_cells.back();
            }
            else
            {
                sample_cell = crystal_cells.back();
            }

            if (i == sample_cell.index && resources == 0)
            {
                if (sample_cell.type == 1)
                {
                    egg_cells.pop_back();
                    if (egg_cells.size() != 0 && my_ants <= opp_ants)
                    {
                        sample_cell = egg_cells.back();
                    }
                    else
                    {
                        sample_cell = crystal_cells.back();
                    }
                }
                else
                {
                    crystal_cells.pop_back();
                    sample_cell = crystal_cells.back();
                }
            }
        }

        // Write an action using cout. DON'T FORGET THE "<< endl"
        // To debug: cerr << "Debug messages..." << endl;
        // WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
        //  << "BEACON " << sample_cell.index << " 10;"
        cout << "LINE " << my_base << " " << sample_cell.index << " 10" << endl;
    }
}