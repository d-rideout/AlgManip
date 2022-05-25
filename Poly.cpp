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

// constructor from another object, to make a copy
Poly::Poly(const Poly &other) {
  cout << "Poly copy constructor" << endl;
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

void Poly::display() {
  int& n = this->n;
  cout << n << "-term polynomial:" ;
  for (int t=0; t<n; ++t) {
    int c = this->p[2*t];
    int& e = this->p[2*t+1];
    if (c==-1) cout << " -";
    else cout << ' ' << c; // leaving 0 terms for now
    if (e) cout << " q";
    if (e>1) cout << '^' << e;
  }
  cout << endl;
}
