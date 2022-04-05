#include <bits/stdc++.h>
using namespace std;
typedef int num;

/*
 * Median of a dynamic array.
 * Add element - O(log n)
 * Remove element - O(log n)
 * Query median - O(1)
 */

num a;
string s;

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
    med m;
    cin >> s;
    while (s != "x") {
        switch (s[0]) {
            case '+':
                m.add(stoi(s.substr(1)));
                break;
            case '-':
                m.remove(stoi(s.substr(1)));
                break;
            case 'q':
                cout << m.query() << endl;
                break;
        }
        cin >> s;
    }
}