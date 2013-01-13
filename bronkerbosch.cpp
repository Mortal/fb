#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <cstdint>
#include <algorithm>

using namespace std;

typedef uint8_t node;
typedef uint16_t Uint;

class edge_set {
    node n;

    vector<vector<node> > adj;

    Uint m_size;

    vector<Uint> indexes;
    vector<node> data;

public:
    edge_set(node n) : n(n), adj(n), m_size(0) {}

    void add(node u, node v) {
	adj[u].push_back(v);
	adj[v].push_back(u);
	m_size += 2;
    }

    void finalize() {
	indexes.resize(n);
	data.resize(m_size);
	Uint wr = 0;
	for (Uint i = 0; i < n; ++i) {
	    indexes[i] = wr;
	    for (Uint j = 0; j < adj[i].size(); ++j) {
		data[wr++] = adj[i][j];
	    }
	    sort(&data[indexes[i]], &data[wr]);
	    wr = unique(&data[indexes[i]], &data[wr]) - &data[0];
	}
	data.resize(wr);
    }

    node nodes() {
	return n;
    }

    node * begin(node u) {
	return &data[indexes[u]];
    }

    node * end(node u) {
	if (u + 1 == n) return &data[data.size()];
	return &data[indexes[u+1]];
    }
};

class BronKerbosch1 {
    edge_set * e;
    vector<char> result;
    node result_size;
    node best_clique;
    vector<node> candidates;
    set<node> exclude;
    map<string, node> * names;

public:
    void operator()(edge_set & e, map<string, node> & names) {
	this->e = &e;
	this->names = &names;
	result_size = 0;
	best_clique = 0;
	result.resize(e.nodes());
	candidates.resize(e.nodes());
	iota(candidates.begin(), candidates.end(), 0);
	go();
    }

private:
    node pick_pivot() {
	if (candidates.size() > 5) return candidates[5];
	return candidates.size() ? *candidates.begin() : *exclude.begin();
    }

    void go(size_t depth = 0) {
	if (candidates.size() == 0 && exclude.size() == 0) {
	    report();
	    return;
	}
	if (depth > 30000) {
	    cout << "This could be bad" << endl;
	}
	vector<node> p = candidates;
	set<node> x = exclude;
	node pivot = pick_pivot();
	for (size_t i = 0; i < p.size(); ++i) {
	    //if (find(e->begin(pivot), e->end(pivot), p[i]) != e->end(pivot)) continue;

	    candidates.resize(result.size());
	    size_t p_size =
		set_intersection(&p[i], &p[p.size()],
				 e->begin(p[i]), e->end(p[i]),
				 candidates.begin())
		- candidates.begin();
	    candidates.resize(p_size);

	    exclude.clear();
	    set_intersection(x.begin(), x.end(),
			     e->begin(p[i]), e->end(p[i]),
			     inserter(exclude, exclude.end()));

	    ++result_size;
	    result[p[i]] = 1;
	    go(depth + 1);
	    result[p[i]] = 0;
	    --result_size;

	    exclude.insert(p[i]);
	}
    }

    void report() {
	if (result_size < best_clique) return;
	best_clique = result_size;
	cout << "Maximal clique (" << static_cast<size_t>(result_size) << "):";
	for (size_t i = 0; i < result.size(); ++i) {
	    if (!result[i]) continue;
	    for (auto j = names->begin(); j != names->end(); ++j) {
		if (i == j->second) {
		    cout << ' ' << j->first;
		    break;
		}
	    }
	}
	cout << '\n';
	//if (result_size == 34) exit(0);
    }
};

int main() {
    Uint n, m;
    cin >> n >> m;
    map<string, node> names;
    for (node i = 0; i < n; ++i) {
	string name;
	cin >> name;
	names[name] = i;
    }

    edge_set e(n);
    for (Uint i = 0; i < m; ++i) {
	string u, v;
	cin >> u >> v;
	e.add(names[u], names[v]);
    }
    e.finalize();
    BronKerbosch1 b;
    b(e, names);
}
// vim:set sw=4:
