#include <array>
#include <cstdint>
#include <cstdlib>
#include <memory>
#include <omp.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <errno.h>
#include <time.h>
#include <vector>
#include <algorithm>
#include <cstdlib>

#define TIME_SCALE_FACTOR 1e6
#define TIME_MEASURE_BEGIN(x) ((x) = omp_get_wtime() * TIME_SCALE_FACTOR)
#define TIME_MEASURE_END(x) ((x) = omp_get_wtime() * TIME_SCALE_FACTOR - (x))

using Data_t = double;
using ArrSize_t = uint64_t;
using BucketSize_t = uint64_t;
using BucketCount_t = uint64_t;
using ThreadCount_t = int32_t;
using SeriesCount_t = int32_t;

struct Args {
  ArrSize_t arr_size;
  BucketCount_t n_buckets;
  ThreadCount_t n_threads;
  SeriesCount_t n_series;
} g_args;

struct ExpCfg {
  Args args;
  BucketSize_t bucket_size;
  SeriesCount_t series_id;
};

struct ExpResult {
  ExpCfg cfg;
  double total_time;
  double draw_time;
  double scatter_time;
  double sort_time;
  double gather_time;

  static void print_header() {
    printf("sid,arrsize,bsize,nthreads,total,draw,scatter,sort,gather\n");
  }
  void print_as_csv() const {
    printf("%d,%ld,%ld,%d,%lf,%lf,%lf,%lf,%lf\n",
        cfg.series_id, cfg.args.arr_size, cfg.bucket_size, cfg.args.n_threads, total_time,
        draw_time, scatter_time, sort_time, gather_time);
  }
};

static void parse_args(const int argc, char *argv[], Args *out);
static void dump_cfg();
static void print_arr(const Data_t * const arr, const ArrSize_t size);
static void print_buckets(const std::vector<Data_t> *buckets, const BucketCount_t n_buckets, const int32_t tid);
static bool summary(Data_t *data, const Args &args);

inline static int32_t init_rand_state(uint16_t *rstate);

ExpResult bucket_sort_sync(Data_t *data, ExpCfg cfg) {
  ExpResult result;
  result.cfg = cfg;

  std::vector<std::vector<Data_t>> buckets(cfg.args.n_buckets);

  TIME_MEASURE_BEGIN(result.total_time);

  TIME_MEASURE_BEGIN(result.draw_time);
  for (ArrSize_t i = 0; i < cfg.args.arr_size; ++i)
    data[i] = drand48();
  TIME_MEASURE_END(result.draw_time);

  TIME_MEASURE_BEGIN(result.scatter_time);
  for (ArrSize_t i = 0; i < cfg.args.arr_size; ++i)
    buckets[(static_cast<int>(data[i] * cfg.args.n_buckets))].push_back(data[i]);
  TIME_MEASURE_END(result.scatter_time);

  TIME_MEASURE_BEGIN(result.sort_time);
  for (auto &bucket : buckets)
    std::sort(std::begin(bucket), std::end(bucket));
  TIME_MEASURE_END(result.sort_time);

  TIME_MEASURE_BEGIN(result.gather_time);
  ArrSize_t el_i = 0;
  for (auto &bucket : buckets)
    for (Data_t el : bucket)
      data[el_i++] = el;
  TIME_MEASURE_END(result.gather_time);

  TIME_MEASURE_END(result.total_time);

  return result;
}

ExpResult bucket_sort_1(Data_t *data, ExpCfg cfg) {
  uint16_t rstate[3];

  ExpResult result{};
  result.cfg = cfg;

  std::vector<std::vector<Data_t>> buckets(cfg.args.n_buckets);

  TIME_MEASURE_BEGIN(result.total_time);
  #pragma omp parallel private(rstate) shared(data, buckets, cfg)
  {
    ExpResult p_result{};

    TIME_MEASURE_BEGIN(p_result.draw_time);
    const int tid = init_rand_state(rstate);
    #pragma omp for schedule(static)
    for (ArrSize_t i = 0; i < cfg.args.arr_size; ++i) {
      data[i] = erand48(rstate);
    }
    TIME_MEASURE_END(p_result.draw_time);
    
    TIME_MEASURE_BEGIN(p_result.scatter_time);
    #pragma omp for schedule(static)
    for (ArrSize_t i = 0; i < cfg.args.arr_size; ++i) {
        #pragma omp critical
        {
            buckets[(static_cast<int>(data[i] * cfg.args.n_buckets))].push_back(data[i]);
        }
    }
    TIME_MEASURE_END(p_result.scatter_time);

    TIME_MEASURE_BEGIN(p_result.sort_time);
    #pragma omp for schedule(static)
    for (BucketCount_t i = 0; i < cfg.args.n_buckets; ++i) {
      std::sort(std::begin(buckets[i]), std::end(buckets[i])); 
    }
    TIME_MEASURE_END(p_result.sort_time);

    TIME_MEASURE_BEGIN(p_result.gather_time);
    ArrSize_t prev_el_count = 0;
    BucketCount_t last_j = 0;
    
    #pragma omp for schedule(static)
    for (BucketCount_t i = 0; i < cfg.args.n_buckets; ++i) {
      for (BucketCount_t j = last_j; j < i; ++j) {
        prev_el_count += buckets[j].size();
      }
      last_j = i;
      ArrSize_t el_i = prev_el_count;
      for (Data_t el : buckets[i]) {
        data[el_i++] = el;
      }
    }
    TIME_MEASURE_END(p_result.gather_time);

    if (tid == 0) {
      result.draw_time = p_result.draw_time;
      result.scatter_time = p_result.scatter_time;
      result.sort_time = p_result.sort_time;
      result.gather_time = p_result.gather_time;
    }
  }
  TIME_MEASURE_END(result.total_time);
  return result;
}

int main(int argc, char * argv[]) {
  parse_args(argc, argv, &g_args);
  srand48(time(nullptr));

  Data_t *data = new Data_t[g_args.arr_size];
  assert((data != nullptr && "Memory allocated"));
  
  ExpCfg cfg;
  cfg.args = g_args;
  cfg.bucket_size = g_args.arr_size / g_args.n_buckets;

  ExpResult::print_header();
  for (SeriesCount_t sid = 0; sid < g_args.n_series; ++sid) {
    cfg.series_id = sid;
    bucket_sort_sync(data, cfg).print_as_csv();
  }

  delete[] data;
	return 0;
}

static void parse_args(const int argc, char *argv[], Args *out) {
  assert(((argc == 5) && "Four arguments are expected"));

  out->arr_size = std::strtoull(argv[1], nullptr, 10);
  assert((errno == 0 && "Correct conversion for arr_size"));

  out->n_threads = std::strtol(argv[2], nullptr, 10);
  assert((errno == 0 && "Correct conversion for n_threads"));

  out->n_buckets = std::strtol(argv[3], nullptr, 10);
  assert((errno == 0 && "Correct conversion for n_buckets"));

  out->n_series = std::strtol(argv[4], nullptr, 10);
  assert((errno == 0 && "Correct conversion for n_series"));
}

static void print_arr(const Data_t * const arr, const ArrSize_t size) {
  for (uint64_t i = 0; i < size; ++i) {
    printf("%lf\n", arr[i]);
  }
}

#ifdef _OPENMP
// Should be executed only in OpenMP parallel execution context
inline static int32_t init_rand_state(uint16_t *rstate) {
  int32_t tid = omp_get_thread_num();

  time_t ctime = time(nullptr);

  rstate[0] = (ctime + tid * 3 + 11) % UINT16_MAX;
  rstate[1] = (ctime + tid * 7 + 13) % UINT16_MAX;
  rstate[2] = (ctime + tid * 31 + 29) % UINT16_MAX;
  return tid;
}
#endif // _OPENMP

static void print_buckets(const std::vector<Data_t> *buckets, const BucketCount_t n_buckets, const int32_t tid) {
  printf("------------\n");
  for (int i = 0; i < n_buckets; ++i) {
    printf("%d: ", i);
    for (Data_t el : buckets[i]) {
      printf("%lf ", el);
    }
    printf("\n");
  }
  printf("------------\n");
}
