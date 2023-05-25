#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <list>
#include <bits/stdc++.h>
#include <queue>

using namespace std;

/*------------------------*/
void addEdge(std::vector<int> adj[], int u, int v)
{

    if (!count(adj[u].begin(), adj[u].end(), v))
    {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
}

// A utility function to print the adjacency list
// representation of graph
void printGraph(vector<int> adj[], int V)
{
    for (int v = 0; v < V; ++v)
    {
        cerr << "\n Adjacency list of vertex " << v
             << "\n head " << endl;
        for (auto x : adj[v])
            cerr << "-> " << x << endl;
        cerr << endl;
    }
}
/*------------------------*/


/* DIJSKSTRA*/
// Given an Adjacency List, find all shortest paths from "start" to all other vertices.
vector<int> DijkstraSP(vector< vector<pair<int, int> > > &adjList, int &start)
    {
    cout << "\nGetting the shortest path from " << start << " to all other nodes.\n";
    vector<int> dist;
    
    // Initialize all source->vertex as infinite.
    int n = adjList.size();
    for(int i = 0; i < n; i++)
        {
        dist.push_back(1000000007); // Define "infinity" as necessary by constraints.
        }
        
    // Create a PQ.
    priority_queue<pair<int, int>, vector< pair<int, int> >, greater<pair<int, int> > > pq;
    
    // Add source to pq, where distance is 0.
    pq.push(make_pair(start, 0));
    dist[start] = 0;
    
    // While pq isn't empty...
    while(pq.empty() == false)
        {
        // Get min distance vertex from pq. (Call it u.)
        int u = pq.top().first;
        pq.pop();
        
        // Visit all of u's friends. For each one (called v)....
        for(int i = 0; i < adjList[u].size(); i++)
            {
            int v = adjList[u][i].first;
            int weight = adjList[u][i].second;
            
            // If the distance to v is shorter by going through u...
            if(dist[v] > dist[u] + weight)
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
    
void PrintShortestPath(vector<int> &dist, int &start)
    {
    cout << "\nPrinting the shortest paths for node " << start << ".\n";
    for(int i = 0; i < dist.size(); i++)
        {
        cout << "The distance from node " << start << " to node " << i << " is: " << dist[i] << endl;
        }
    }

/* ------- */

struct Cell
{
    int index;
    int type;
    int initial_resources;
    Cell(int index, int type, int initial_resources)
    {
        this->index = index;
        this->initial_resources = initial_resources;
        this->type = type;
    }
    Cell() {}
};

struct less_than_key
{
    inline bool operator()(const Cell &struct1, const Cell &struct2)
    {
        return (struct1.initial_resources < struct2.initial_resources);
    }
};

int main()
{
    vector<Cell> crystal_cells = {};
    vector<Cell> egg_cells = {};
    int my_base;

    int number_of_cells; // amount of hexagonal cells in this map
    cin >> number_of_cells;
    int V = number_of_cells;
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
        cerr << "cell " << i << " - neigh " << neigh_0 << endl;
        if (neigh_0 != -1)
        {
            addEdge(adj, i, neigh_0);
        }
        if (neigh_1 != -1)
        {
            addEdge(adj, i, neigh_1);
        }
        if (neigh_2 != -1)
        {
            addEdge(adj, i, neigh_2);
        }
        if (neigh_3 != -1)
        {
            addEdge(adj, i, neigh_3);
        }
        if (neigh_4 != -1)
        {
            addEdge(adj, i, neigh_4);
        }
        if (neigh_5 != -1)
        {
            addEdge(adj, i, neigh_5);
        }
        cin.ignore();
        if (type == 2)
        {
            crystal_cells.push_back(Cell(i, type, initial_resources));
        }
        else if (type == 1)
        {
            egg_cells.push_back(Cell(i, type, initial_resources));
        }
    }
    printGraph(adj, V);
    // todo here: get distances for important points and save in map


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
    for (int i = 0; i < number_of_bases; i++)
    {
        int opp_base_index;
        cin >> opp_base_index;
        cin.ignore();
    }
    std::sort(crystal_cells.begin(), crystal_cells.end(), less_than_key());
    std::sort(egg_cells.begin(), egg_cells.end(), less_than_key());

    // game loop
    while (1)
    {
        Cell sample_cell = Cell();
        if (egg_cells.size() != 0)
        {
            sample_cell = egg_cells.back();
        }
        else
        {
            sample_cell = crystal_cells.back();
        }

        for (int i = 0; i < number_of_cells; i++)
        {
            int resources; // the current amount of eggs/crystals on this cell
            int my_ants;   // the amount of your ants on this cell
            int opp_ants;  // the amount of opponent ants on this cell
            cin >> resources >> my_ants >> opp_ants;
            cin.ignore();

            if (i == sample_cell.index && resources == 0)
            {
                if (sample_cell.type == 1)
                {
                    egg_cells.pop_back();
                    if (egg_cells.size() != 0)
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
           cout  << "LINE " << my_base << " " << sample_cell.index << " 10" << endl;
    }
}