%%cu
#include<stdio.h>
#include<stdlib.h>
#include<iostream>

struct GpuTimer
{
      cudaEvent_t start;
      cudaEvent_t stop;

      GpuTimer()
      {
            cudaEventCreate(&start);
            cudaEventCreate(&stop);
      }

      ~GpuTimer()
      {
            cudaEventDestroy(start);
            cudaEventDestroy(stop);
      }

      void Start()
      {
            cudaEventRecord(start, 0);
      }

      void Stop()
      {
            cudaEventRecord(stop, 0);
      }

      float Elapsed()
      {
            float elapsed;
            cudaEventSynchronize(stop);
            cudaEventElapsedTime(&elapsed, start, stop);
            return elapsed;
      }
};

void host_add(int *a, int *b, int *c, int N) {
	for(int idx=0;idx<N;idx++)
		c[idx] = a[idx] + b[idx];
}

__global__ void device_add(int *a, int *b, int *c) {

	int index = threadIdx.x + blockIdx.x * blockDim.x;
        c[index] = a[index] + b[index];
}


void fill_array(int *data, int N) {
	for(int idx=0;idx<N;idx++)
		data[idx] = idx;
}

void print_output(int *a, int *b, int*c, int N) {
	for(int idx=0;idx<N;idx++)
		printf("\n %d + %d  = %d",  a[idx] , b[idx], c[idx]);
}

void add_vectors(int threads_per_block, int N) {
	int *a, *b, *c;
    int *d_a, *d_b, *d_c;
	int no_of_blocks=0;

	int size = N * sizeof(int);

	a = (int *)malloc(size); fill_array(a, N);
	b = (int *)malloc(size); fill_array(b, N);
	c = (int *)malloc(size);

	cudaMalloc((void **)&d_a, size);
	cudaMalloc((void **)&d_b, size);
	cudaMalloc((void **)&d_c, size);

	cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
	cudaMemcpy(d_b, b, size, cudaMemcpyHostToDevice);

	GpuTimer timer;
	no_of_blocks = N/threads_per_block;

	timer.Start();

	device_add<<<no_of_blocks,threads_per_block>>>(d_a,d_b,d_c);

    cudaMemcpy(c, d_c, size, cudaMemcpyDeviceToHost);

	timer.Stop();

	// print_output(a,b,c, N);

	free(a); free(b); free(c);
    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);

	float elapsed = timer.Elapsed();
    std::cout << threads_per_block << ";" << N << ";" << elapsed << std::endl;
}

int main(void) {
	int threads_per_block[5] = {4, 16, 64, 128, 256};
	int vector_sizes[5] = {3355443, 3355443 * 2, 3355443 * 3, 3355443 * 4, 3355443 * 5};
	int number_of_retries = 5;

    std::cout << "threads_per_block;vector_size;time" << std::endl;

	for (int i = 0; i < sizeof(threads_per_block) / sizeof(threads_per_block)[0]; i++) {
			for (int j = 0; j < sizeof(vector_sizes) / sizeof(vector_sizes[0]); j++) {
					for (int k = 0; k < number_of_retries; k++) {
						add_vectors(threads_per_block[i], vector_sizes[j]);
					}
			}
	}

	return 0;
}
