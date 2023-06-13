#include<stdio.h>
#include<stdlib.h>
#include<iostream>
#include <string>

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

__global__ void matrix_transpose_naive(int *input, int *output, int grid_size) {

	int indexX = threadIdx.x + blockIdx.x * blockDim.x;
	int indexY = threadIdx.y + blockIdx.y * blockDim.y;
	int index = indexY * grid_size + indexX;
	int transposedIndex = indexX * grid_size + indexY;

	output[transposedIndex] = input[index];

	// output[index] = input[transposedIndex];
}

__global__ void matrix_transpose_shared(int *input, int *output, int grid_size) {
    int block_size = blockDim.x;

    extern __shared__ int sharedMemory[];

    int indexX = threadIdx.x + blockIdx.x * blockDim.x;
    int indexY = threadIdx.y + blockIdx.y * blockDim.y;

    int tindexX = threadIdx.x + blockIdx.y * blockDim.x;
    int tindexY = threadIdx.y + blockIdx.x * blockDim.y;

    int localIndexX = threadIdx.x;
    int localIndexY = threadIdx.y;

    int index = indexY * grid_size + indexX;
    int transposedIndex = tindexY * grid_size + tindexX;

    if (threadIdx.x < block_size && threadIdx.y < block_size) {
        sharedMemory[localIndexX * block_size + localIndexY] = input[index];
    }

    __syncthreads();

    output[transposedIndex] = sharedMemory[localIndexY * block_size + localIndexX];
}

void fill_array(int *data, int grid_size) {
	for(int idx=0;idx<(grid_size*grid_size);idx++)
		data[idx] = idx;
}

int matrix_transpose(int test_type, int grid_size, int block_size) {
	int *a, *b;
    int *d_a, *d_b; // device copies of a, b, c

	int size = grid_size * grid_size *sizeof(int);

	a = (int *)malloc(size); fill_array(a, grid_size);
	b = (int *)malloc(size);

	cudaMalloc((void **)&d_a, size);
	cudaMalloc((void **)&d_b, size);

	cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
	cudaMemcpy(d_b, b, size, cudaMemcpyHostToDevice);

	dim3 blockSize(block_size,block_size,1);
	dim3 gridSize(grid_size/block_size,grid_size/block_size,1);

	GpuTimer timer;
	timer.Start();

    if (test_type == 0) {
        matrix_transpose_naive<<<gridSize,blockSize>>>(d_a, d_b, grid_size);
    } else {
        matrix_transpose_shared<<<gridSize,blockSize>>>(d_a, d_b, grid_size);
    }

	cudaMemcpy(b, d_b, size, cudaMemcpyDeviceToHost);

	free(a);
	free(b);
    cudaFree(d_a);
	cudaFree(d_b);
}

int main(void) {
	int grid_sizes[5] = {1024, 2048, 4096, 8192, 16384};
	int block_sizes[5] = {64, 128, 256, 512, 1024};
	int test_types = 2;
	int number_of_retries = 5;

	std::cout << "grid_size;block_size;type;time" << std::endl;

	for (int i = 0; i < sizeof(grid_sizes) / sizeof(grid_sizes)[0]; i++) {
  		for (int j = 0; j < sizeof(block_sizes) / sizeof(block_sizes[0]); j++) {
            for (int test_type = 0; test_type < test_types; test_type++) {
                for (int l = 0; l < number_of_retries; l++) {
                    GpuTimer timer;
                    timer.Start();

                    matrix_transpose(test_type, grid_sizes[i], block_sizes[j]);
                    timer.Stop();

                    float elapsed = timer.Elapsed();
                    std::string type;
                    if (test_type == 0) {
                        type = "naive";
                    } else {
                        type = "shared";
                    }
                    std::cout << grid_sizes[i] << ";" << block_sizes[j] << ";" << type << ";" << elapsed << std::endl;
                }
            }
		}
	}
	return 0;
}