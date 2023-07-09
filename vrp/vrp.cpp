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
#include<ctime>
#include<thread>
#include<random>
#include<chrono>
using namespace std;
const double alpha = 0.2;
const double eps = 1e-7;
const int MAX_ITERATION_TIMES = 100000; 
struct point{
    int d;
    double x, y;
};
double sqr (double x) {return x * x;}
int inc (int x, int n) {x += 1; return x < n ? x : 0;}
int dec (int x, int n) {x -= 1; return x < 0 ? n - 1 : x;}
auto load_node (const char *filename)
{
    auto f = fopen(filename, "r");
    int node_count, vehicle_count, capacity;
    fscanf(f, "%d %d %d", &node_count, &vehicle_count, &capacity);
    vector<point> points;
    for (int i = 0; i < node_count; ++i)
    {
        point p;
        fscanf(f, "%d %lf %lf", &p.d, &p.x, &p.y);
        if (i == 0)
        {
            for (int j = 0; j < vehicle_count; ++j)
                points.push_back(p);
        }
        else
            points.push_back(p);
    }
    fclose(f);
    return make_tuple(points, vehicle_count, capacity);
}
void output_file (const char *filename, vector<int> cur, double cur_dist, int vehicle_count)
{
    auto f = fopen(filename, "w");  // Open the file in write mode
    fprintf(f, "%lf 0\n", cur_dist);
    int n = cur.size();
    fprintf(f, "0 ");
    for (int i = 1; i < n; ++i)
    {
        if (cur[i] < vehicle_count)
        {
            fprintf(f, "0\n");
            fprintf(f, "0 ");
        }
        else
            fprintf(f, "%d ", cur[i] - vehicle_count + 1);
    }
    fprintf(f, "0\n");
    fclose(f);
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
        dist += dist_matrix[sol[i]][sol[i - 1]];
    return dist;
}

auto naive_solution (vector<point> &points, vector<vector<double>> &dist_matrix, int vehicle_count, int capacity)
{
    int n = points.size();
    vector<int> sol;
    vector<vector<int>> arr(vehicle_count);
    vector<int> cap(vehicle_count, capacity);
    vector<bool> vis(n, 0);
    for (int i = vehicle_count; i < n; ++i)
    {
        int now = -1;
        for (int j = vehicle_count; j < n; ++j)
            if (!vis[j] && (now == -1 || points[j].d > points[now].d))
                now = j;
        vis[now] = 1;
        bool flag = 0;
        for (int j = 0; j < vehicle_count; ++j)
            if (cap[j] >= points[now].d)
            {
                cap[j] -= points[now].d;
                arr[j].push_back(now);
                flag = 1;
                break;
            }
        if (!flag)
            puts("ALERT!!!");
    }

    sol.clear();
        
    for (int i = 0; i < vehicle_count; ++i)
    {
        sol.push_back(i);
        int size = arr[i].size();
        for (int j = 0; j < size; ++j)
        {
            sol.push_back(arr[i][j]);
        }
    }
    
    //for (int i = 0; i < sol.size(); ++i) printf("%d\n", sol[i]);
    double sol_dist = get_path_dist(sol, dist_matrix);
    return make_pair(sol, sol_dist);
}

void add_panelty(vector<vector<double>> &dist_matrix, vector<vector<int>> &panelty, vector<int> &cur, double &cur_arg_dist, double lambda)
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
        cur_arg_dist += lambda;
    }
    return;
}

bool check (vector<point> &points, vector<int> cur, int vehicle_count, int capacity)
{
    int n = points.size();
    int cur_d = 0;
    for (int i = 1; i < n; ++i)
    {
        cur_d += points[cur[i]].d;
        if (cur_d > capacity) return false;
        if (cur[i] < vehicle_count)
            cur_d = 0;
    }/*
    for (int i = 1; i < n; ++i)
    {
        cur_d += points[cur[i]].d;
        if (cur[i] < vehicle_count)
            cur_d = 0;
    }*/
    return true;
}
auto guided_local_search(vector<point> &points, vector<vector<double>> &dist_matrix, vector<int> cur, double cur_dist, 
                        int vehicle_count, int capacity)
{
    int n = points.size();
    double lambda = alpha * cur_dist / n;
    double cur_arg_dist = cur_dist;
    double best_dist = cur_dist;
    auto best_sol = cur;
    vector<vector<int>> panelty(n, vector<int>(n, 0));
    for (int T = 0; T < MAX_ITERATION_TIMES; ++T)
    {
        output_file("out.txt", best_sol, best_dist, vehicle_count);
        printf("%d %lf\n", T, best_dist);
        bool flag_changed = 1;
        while (flag_changed)  // not at the local solution point
        {
            flag_changed = 0;
            for (int i = 0; i < n - 1; ++i)
            { 
                for (int p = 1; p <= 30; ++p)
                //for (int j = i + 1; j < n; ++j)
                {
                    int j = rand() % (n - i - 1) + i + 1;
                    int t1 = cur[i], t2 = cur[inc(i, n)];
                    int t3 = cur[j], t4 = cur[inc(j, n)];
                    if (t4 == t1 || t4 == t2 || t1 == t3) continue;
                    double dist_delta = -dist_matrix[t1][t2] - dist_matrix[t3][t4] + dist_matrix[t1][t3] + dist_matrix[t2][t4];
                    int panelty_delta = -panelty[t1][t2] - panelty[t3][t4] + panelty[t1][t3] + panelty[t2][t4];
                    double next_arg_dist = cur_dist + dist_delta + lambda * panelty_delta;
                    if (next_arg_dist + eps < cur_arg_dist)
                    {
                        reverse(cur.begin() + i + 1, cur.begin() + j + 1);
                        if (check(points, cur, vehicle_count, capacity))
                        {
                            cur_arg_dist = next_arg_dist;
                            cur_dist += dist_delta;
                            flag_changed = 1;
                        }
                        else
                            reverse(cur.begin() + i + 1, cur.begin() + j + 1);
                    }
                }
            }
            if (best_dist > cur_dist)
            {
                best_dist = cur_dist;
                best_sol = cur;
            }
        }
        add_panelty(dist_matrix, panelty, cur, cur_arg_dist, lambda);
    }
    return make_pair(best_sol, best_dist);
}

int main (int argc, char *argv[])
{
    srand(19260817);
    if (argc != 2)
    {
        printf("Example: ./vrp data/vrp_5_4_1\n");
        exit(-1);
    }
    auto [points, vehicle_count, capacity] = load_node(argv[1]);
    auto dist_matrix = get_dist_matrix(points);
    auto [cur_sol, cur_sol_dist] = naive_solution(points, dist_matrix, vehicle_count, capacity);
    auto [best_sol, best_sol_dist] = guided_local_search(points, dist_matrix, cur_sol, cur_sol_dist, vehicle_count, capacity);
    return 0;
}
