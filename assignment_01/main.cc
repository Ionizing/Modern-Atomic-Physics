#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>

using Vecd = std::vector<double>;
using Veci = std::vector<int>;

Vecd     read_data         (const char* file_name);
Vecd     partial_average   (const Vecd& vec, const int step);
double   calc_deviation    (const Vecd& pavgs);

int main(int argc, char* argv[]) {
  Vecd deviations = read_data("./deviation.txt");
  int N = deviations.size();

  Vecd result;
  for (int i=0; i!=N/2; ++i) {
    Vecd   pavgs = partial_average(deviations, i+1);
    double devia = calc_deviation(pavgs);
    result.push_back(devia);
    std::cout << devia << std::endl;
  }
  
  return 0;
}

Vecd read_data(const char* file_name) {
  std::ifstream ifs;
  try {
    ifs.open(file_name);
    if (!ifs.good()) {
      const char* str = "File open failed";
      throw str;
    } else {  }
  } catch (const char* str) {
    std::cerr << str << std::endl;
    std::abort();
  }

  char drop; // '#' at first
  int  N;
  ifs >> drop >> N;
  
  Vecd out(N);
  for (int i=0; i!=N; ++i) {
    ifs >> out[i];
  }

  return out;
}

Vecd partial_average(const Vecd& vec, const int step) {
  Vecd out;
  out.reserve(20);
  for (int i=0; i!=vec.size()/step; ++i) {
    double partial_sum = .0;
    for (int j=i; j!=i+step; ++j) {
      partial_sum += vec[j];
    }
    out.push_back(partial_sum / step);
  }
  return out;
}

double calc_deviation(const Vecd& pavgs) {
  double sum_of_dy2 = .0;
  for (int i=0; i!=pavgs.size() - 1; ++i) {
    sum_of_dy2 += (pavgs[i+1] - pavgs[i]) * (pavgs[i+1] - pavgs[i]);
  }
  return std::sqrt(sum_of_dy2 / (2*pavgs.size() - 2));
}
