#include <iostream>
#include "Poly.h"
using namespace std;

Poly::Poly() {
  //  cout << "Poly constructor" << endl;
}

Poly::~Poly() {
  cout << "(virtual) Poly destructor" << endl;
}

// Poly& Poly::operator=(const Poly &other) {
//   cout << "Poly assignment from" << &other;
//   //  return;
// }

// constructor from another object, to make a copy
Poly::Poly(const Poly &other) {

}

