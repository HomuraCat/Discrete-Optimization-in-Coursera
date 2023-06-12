//HomuraCat codes it!
#include<cstdio>
#include<algorithm>
#include<cstring>
#include<bitset>
#include<queue>
#include<vector>
#include<set>
#include<cstdlib>
#include<iostream>
#include<utility>
#include<map>
#include<cmath>
using namespace std;
const double alpha = 1;
const double eps = 1e-7;
const int MAX_ITERATION_TIMES = 10000; 
struct point{
    double x, y;
};
double sqr (double x) {return x * x;}
int inc (int x, int n) {x += 1; return x < n ? x : n;}
int dec (int x, int n) {x -= 1; return x < 0 ? n - 1 : x;}
auto load_node (const char *filename)
{
    auto f = fopen(filename, "r");
    int node_count;
    fscanf(f, "%d", &node_count);
    vector<point> points;
    for (int i = 0; i < node_count; ++i)
    {
        point p;
        fscanf(f, "%lf %lf", &p.x, &p.y);
        points.push_back(p);
    }
    fclose(f);
    return points;
}

auto get_dist_matrix (vector<point> &points)
{
    int n = points.size();
    vector<vector<double>> dist_matrix(n, vector<double>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            dist_matrix[i][j] = sqrt(sqr(points[i].x - points[j].x) + sqr(points[i].y - points[j].y));
    return dist_matrix;
}

auto get_path_dist (vector<int> &sol, vector<vector<double>> &dist_matrix)
{
    int n = sol.size();
    double dist = dist_matrix[sol[0]][sol[n - 1]];
    for (int i = 1; i < n; ++i)
        dist += dist_matrix[sol[0]][sol[n - 1]];
    return dist;
}

auto greedy (vector<point> &points, vector<vector<double>> &dist_matrix)
{
    int n = points.size();
    vector<int> sol(n);
    for (int i = 0; i < n; ++i) sol[i] = i;
    for (int i = 1; i < n; ++i)
    {
        int j = i;
        for (int k = i + 1; k < n; ++k)
            if (dist_matrix[sol[i - 1]][sol[k]] < dist_matrix[sol[i - 1]][sol[j]])
                j = k;
        swap(sol[i], sol[j]);
    }
    double sol_dist = get_path_dist(sol, dist_matrix);
    return make_pair(sol, sol_dist);
}


void add_panelty(vector<vector<double>> &dist_matrix, vector<vector<int>> &panelty, vector<int> &cur)
{
    int n = cur.size();
    vector<int> max_util_list = {0};
    double max_util = dist_matrix[cur[0]][cur[n - 1]] / (1 + panelty[cur[0]][cur[n - 1]]);
    for (int i = 1; i < n; ++i)
    {
        double util = dist_matrix[cur[i - 1]][cur[i]] / (1 + panelty[cur[i - 1]][cur[i]]);
        if (util > max_util)
        {
            util = max_util;
            max_util_list = {i};
        }
        else if (util + eps > max_util && max_util + eps > util)
            max_util_list.push_back(i);
    }
    for (auto i : max_util_list)
    {
        int x = cur[dec(i, n)], y = cur[i];
        panelty[x][y]++;
        panelty[y][x]++;
    }
    return;
}

auto guided_local_search(vector<point> &points, vector<vector<double>> &dist_matrix, vector<int> cur, double cur_dist)
{
    int n = points.size();
    double lambda = alpha * cur_dist / n;
    double cur_arg_dist = cur_dist;
    double best_dist = cur_dist;
    auto  best_sol = cur;
    vector<vector<int>> panelty(n, vector<int>(n, 0));
    for (int T = 0; T < MAX_ITERATION_TIMES; ++T)
    {
        bool flag_changed = 1;
        while (flag_changed)  // not at the local solution point
        {
            flag_changed = 0;
            for (int i = 0; i < n; ++i)
            {
                int t1 = cur[i], t2 = cur[inc(i, n)];
                for (int j = i + 1; j < n; ++j)
                {
                    int t3 = cur[j], t4 = cur[inc(i, n)];
                    double dist_delta = -dist_matrix[t1][t2] - dist_matrix[t3][t4] + dist_matrix[t1][t3] + dist_matrix[t2][t4];
                    int panelty_delta = -panelty[t1][t2] - panelty[t3][t4] + panelty[t1][t3] + panelty[t2][t4];
                    double next_arg_dist = cur_dist + dist_delta + lambda * panelty_delta;
                    if (next_arg_dist < cur_arg_dist)
                    {
                        reverse(cur.begin() + i, cur.begin() + j + 1);
                        cur_arg_dist = next_arg_dist;
                        cur_dist += dist_delta;
                        flag_changed = 1;
                    }
                }
            }
            if (best_dist > cur_dist)
            {
                best_dist = cur_dist;
                best_sol = cur;
            }
        }
        add_panelty(dist_matrix, panelty, cur);
    }
    return make_pair(best_dist, best_sol);
}

int main (int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Example: ./tsp data/tsp_51_1\n");
        exit(-1);
    }
    auto points = load_node(argv[1]);
    auto dist_matrix = get_dist_matrix(points);
    auto [cur_sol, cur_sol_dist] = greedy(points, dist_matrix);
    auto [best_sol, best_sol_dist] = guided_local_search(points, dist_matrix, cur_sol, cur_sol_dist);
    return 0;
}
