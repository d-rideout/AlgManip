#ifndef POLY_H_
#define POLY_H_

#include <vector>
using namespace std;

class Poly {
 private:
	int n=1;
	vector<int> p;
 public:
	Poly();
	Poly(int nterms, int p[]);
	// See also stackoverflow.com/questions/4118025/brace-enclosed-initializer-list-constructor
	// en.cppreference.com/w/cpp/language/list_initialization (25may022)
	Poly(const Poly &other);

	virtual ~Poly();

	//Poly& operator=(const Poly &other);

	void display(); // display polynomial
};

#endif /* POLY_H_ */
