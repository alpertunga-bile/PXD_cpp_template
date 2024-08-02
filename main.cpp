#include "third-party/PXD-STL/includes/logger.hpp"
#include "third-party/PXD-STL/includes/random_gen.hpp"

auto main() -> int {
  PXD_LOG_INFO("TEST");

  for (int i = 0; i < 10; ++i) {
    printf("%f\n", pxd::random::random_value<double>(0.0, 1.0));
  }

  return 0;
}