#include <iostream>

int main() {
  for (int i = 3; i > 0; std::cout << i-- << "... ");
  std::cout << "Hello, World!\n";
  return 0;
}
