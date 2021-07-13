#include <bits/stdc++.h>
using namespace std;
typedef int num;

/*
 * Median of a dynamic array.
 * Add element - O(log n)
 * Remove element - O(log n)
 * Query median - amortized O(1)
 */

num n, k, a;
vector<num> as;

typedef struct {
    priority_queue<num> lo, hi;
    multiset<num> lorem, hirem;

    num query() {
        if (lo.empty()) {
            return -1;
        }
        adjust();
        while (lorem.find(lo.top()) != lorem.end()) {
            lorem.erase(lorem.find(lo.top()));
            lo.pop();
        }
        return lo.top();
    }

    void adjust() {
        while (((num) lo.size() - (num) lorem.size()) - ((num) hi.size() - (num) hirem.size()) > 1) {
            if (lorem.find(lo.top()) != lorem.end()) {
                lorem.erase(lorem.find(lo.top()));
                lo.pop();
            } else {
                hi.push(-lo.top());
                lo.pop();
            }
        }
        while (((num) hi.size() - (num) hirem.size()) > ((num) lo.size() - (num) lorem.size())) {
            if (hirem.find(hi.top()) != hirem.end()) {
                hirem.erase(hirem.find(hi.top()));
                hi.pop();
            } else {
                lo.push(-hi.top());
                hi.pop();
            }
        }
    }

    void add(num x) {
        if (lo.empty()) {
            lo.push(x);
        } else {
            if (x <= query()) {
                lo.push(x);
            } else {
                hi.push(-x);
            }
        }
        adjust();
    }

    void remove(num x) {
        if (x <= query()) {
            lorem.insert(x);
        } else {
            hirem.insert(-x);
        }
        adjust();
    }
} med;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    cin >> n >> k;
    for (int i = 0; i < n; ++i) {
        cin >> a;
        as.emplace_back(a);
    }

    med m;
    for (int i = 0; i < k; ++i) {
        m.add(as[i]);
    }
    
    num mx = m.query();

    for (int i = k; i < n; ++i) {
        m.remove(as[i-k]);
        m.add(as[i]);
        mx = max(mx, m.query());
    }

    cout << mx;
}