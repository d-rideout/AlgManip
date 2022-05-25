#include <iostream>

#include "Poly.h"
using namespace std;

Poly::Poly() {
  cout << "Poly bare constructor" << endl;
  cout << "DELETE ME?" << endl;
}

Poly::Poly(int nterms, int p[]) {
  cout << "Poly array constructor" << endl;
  this->n = nterms;
  //for (int i=0; i<nterms; ++i) this->p.push_back(p[i]); // memcpy()??
  this->p.resize(2*nterms);
  copy(p, p+2*nterms, this->p.begin());
  for (unsigned int i=0; i<this->p.size(); ++i) cout << this->p.at(i) << ' ';
  cout << endl;
}

Poly::~Poly() {
  cout << "(virtual) Poly destructor" << endl;
  cout << this->n << " terms" << endl;
  for (const int& i : this->p) cout << i << "  ";
  cout << endl;
}

// Poly& Poly::operator=(const Poly &other) {
//   cout << "Poly assignment from" << &other;
//   //  return;
// }

// constructor from another object, to make a copy
Poly::Poly(const Poly &other) {
  cout << "Poly copy constructor" << endl;
}

