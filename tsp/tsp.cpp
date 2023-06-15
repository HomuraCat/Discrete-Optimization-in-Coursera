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
#include<chrono>
using namespace std;
const double alpha = 0.2;
const double eps = 1e-7;
const int MAX_ITERATION_TIMES = 10000;
const double K = 50;
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
void output_file (const char *filename, vector<int> cur, double cur_dist)
{
    auto f = fopen(filename, "w");  // Open the file in write mode
    fprintf(f, "%lf\n", cur_dist);
    int n = cur.size();
    for (int i = 0; i < n; ++i)
    {
        fprintf(f, "%d ", cur[i]);
    }
}
auto get_k_neighbor (vector<point> &points)
{
    int n = points.size();
    vector<vector<pair<double, int>>> dist_matrix(n, vector<pair<double, int>>(n));
    for (int i = 0; i < n; ++i)
        for (int j = 0; j < n; ++j)
            dist_matrix[i][j] = make_pair(sqrt(sqr(points[i].x - points[j].x) + sqr(points[i].y - points[j].y)), j); 
    for (int i = 0; i < n; ++i)
        sort(dist_matrix[i].begin(), dist_matrix[i].end());
    for (int i = 0; i < n; ++i)
    {
        dist_matrix[i].erase(dist_matrix[i].begin() + K + 1, dist_matrix[i].end());
        dist_matrix[i].erase(dist_matrix[i].begin(), dist_matrix[i].begin() + 1); // the first one is itself
    }
    return dist_matrix;
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

auto greedy (vector<point> &points, vector<vector<double>> &dist_matrix, vector<vector<pair<double, int>>> &k_neighbor)
{
    int n = points.size();
    vector<int> sol(n);
    vector<bool> vis(n, 0); 
    for (int i = 0; i < n; ++i) sol[i] = i;
    vis[0] = 1;
    for (int i = 1; i < n; ++i)
    {
        int j = -1;
        int u = sol[i - 1];
        for (int k = 0; k < K; ++k)
        {
            pair<double, int> now = k_neighbor[u][k];
            if (vis[now.second] == 1) continue;
            j = now.second;
            break;
        }
        if (j == -1)
        {
            j = i;
            for (int k = i + 1; k < n; ++k)
                if (dist_matrix[sol[i - 1]][sol[k]] < dist_matrix[sol[i - 1]][sol[j]])
                    j = k;
        }
        swap(sol[i], sol[j]);
    }
    double sol_dist = get_path_dist(sol, dist_matrix);
    return make_pair(sol, sol_dist);
}

//#define depanel
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
#ifdef depanel
        printf("%d %d\n", x, y);
#endif
    }
    return;
}

#define debug
auto guided_local_search(vector<point> &points, vector<vector<double>> &dist_matrix, vector<vector<pair<double, int>>> &k_neighbor, vector<int> cur, double cur_dist)
{
    int n = points.size();
    double lambda = alpha * cur_dist / n;
    double cur_arg_dist = cur_dist;
    double best_dist = cur_dist;
    auto best_sol = cur;
    vector<vector<int>> panelty(n, vector<int>(n, 0));
    vector<int> pos(n);
    for (int i = 0; i < n; ++i) pos[cur[i]] = i;
    for (int T = 0; T < MAX_ITERATION_TIMES; ++T)
    {
#ifdef debug
    printf("%d %lf %lf\n", T, cur_dist, best_dist);
    //printf("%lf %lf", points[0].x, points[0].y);
#endif
        bool flag_changed = 1;
        while (flag_changed)  // not at the local solution point
        {
            flag_changed = 0;
            for (int i = 0; i < n; ++i)
            { 
                for (int j = 0; j < K; ++j)
                {
                   int t1 = cur[i], t2 = cur[inc(i, n)];
#ifdef debugl
    printf("%d %d\n", i, j);
    for (int i = 0; i < n; ++i) printf("%d ", cur[i]);
    puts("");
    for (int i = 0; i < n; ++i) printf("%d ", pos[i]);
    puts("");
#endif
                    int t3 = k_neighbor[t1][j].second;
                    int t4 = cur[inc(pos[t3], n)];
#ifdef debugl
                    printf("t1 = %d t2 = %d t3 = %d t4 = %d\n", t1, t2, t3, t4);
#endif
                    if (t4 == t1 || t4 == t2 || t1 == t3) continue;
                    double dist_delta = -dist_matrix[t1][t2] - dist_matrix[t3][t4] + dist_matrix[t1][t3] + dist_matrix[t2][t4];
                    int panelty_delta = -panelty[t1][t2] - panelty[t3][t4] + panelty[t1][t3] + panelty[t2][t4];
                    double next_arg_dist = cur_dist + dist_delta + lambda * panelty_delta;
                    
                    int x = inc(i, n), y = pos[t3];
                    if (next_arg_dist + eps < cur_arg_dist)
                    {
                        if (x < y)
                        {
                            reverse(cur.begin() + x, cur.begin() + y + 1);
                            for (int k = x; k <= y; ++k) pos[cur[k]] = k;
                        }
                        else
                        {
                            x = dec(x, n), y = inc(y, n);
                            swap(x, y);
                            reverse(cur.begin() + x, cur.begin() + y + 1);
                            for (int k = x; k <= y; ++k) pos[cur[k]] = k;
                        }
                        cur_arg_dist = next_arg_dist;
                        cur_dist += dist_delta;
                        flag_changed = 1;
#ifdef debugl
    printf("%d %d\n", i, j);
    printf("t1 ~ t4 = %d %d %d %d\n", t1, t2, t3, t4);
    for (int i = 0; i < n; ++i) printf("%d ", cur[i]);
    puts("");
    for (int i = 0; i < n; ++i) printf("%d ", pos[i]);
    puts("");
    printf("cur_dist = %lf  dist_delta = %lf  lambda = %lf  panelty_delta = %d\n", cur_dist, dist_delta, lambda, panelty_delta);
    printf("get_path_dist = %lf\n", get_path_dist(cur, dist_matrix));
    assert(abs(cur_dist - get_path_dist(cur, dist_matrix)) < eps);
#endif
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
    if (argc != 2)
    {
        printf("Example: ./tsp data/tsp_51_1\n");
        exit(-1);
    }
    auto points = load_node(argv[1]);
    auto k_neighbor = get_k_neighbor(points);
    auto dist_matrix = get_dist_matrix(points);
    auto [cur_sol, cur_sol_dist] = greedy(points, dist_matrix, k_neighbor);
    auto [best_sol, best_sol_dist] = guided_local_search(points, dist_matrix, k_neighbor, cur_sol, cur_sol_dist);
    
    /*
    for (C = 1; C < 20; C++)
        for (alpha = 0.01; alpha < 0.2; alpha += 0.01)
        {
            auto [best_sol, best_sol_dist] = guided_local_search(points, dist_matrix, cur_sol, cur_sol_dist);
            printf("%lf %lf %d\n", best_sol_dist, alpha, C);
        }
    */
    printf("%lf\n", best_sol_dist);
    output_file("out6.txt", best_sol, best_sol_dist);
    return 0;
}
