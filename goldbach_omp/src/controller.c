#include "input_handler.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include <pthread.h>
#include <unistd.h>
#include "common.h"
#include "goldbach_worker.h"
#include "dynamic_array.h"
#include "queue.h"
#include "producer.h"

int controller_run(size_t threads);

/**
*@brief print GolbachModel results
*@param num_addings  number of addings 
*@param value user input (goldbach number)
*@param list  number of addings 
*@param data  ptr to shared data 
*@return error code
*/
void print_results(int64_t num_addings, int64_t value, bool list, void* data);

/**
*@brief counts the number of sums in array
*@details counts the number of sums found in the array by iterating the 
* number of addings / Strong conjecture = 2, Weak conjecture = 3
*@param array array of addings to count
*@param num_addings : number of addings
*@return number of sums found in array
*/
int64_t count_array_sums(int64_t* array, int num_addings);

/**
*@brief show all addings stored in array
*@param array to print
*@param num_addings : number of addings
*@param sums : amount of sums 
*/
void show_array_addings(int64_t* array, int64_t sums,
    int64_t num_addings, bool first);

/**
*@brief free matrix results
*@param results ptr to matrix results
*@param thread_count number of working threads
*/
void free_results(int64_t** results, int64_t thread_count);

int controller_run(size_t threads) {
  int error = EXIT_SUCCESS;

  dynamic_array_t* input_numbers = read_input();
  array_print(input_numbers);

  queue_t* queue = (queue_t*)
    calloc(1, sizeof(queue_t));
  report_and_exit(queue == NULL, "Could not create queue");
  queue_init(queue);

  threads = threads != 0 ? threads : sysconf(_SC_NPROCESSORS_ONLN);

  int64_t** results = (int64_t**)
    calloc(threads, sizeof(int64_t*));
  report_and_exit(results == NULL, "could not create results array");

  // Produce all work
  producer_start(input_numbers, queue, threads, results);


  // //  concurrent work
  // error = create_threads(shared_data);

  // // 1 thread print
  // int num_addings = (value % 2 == 0)? 2 : 3;
  // print_results(num_addings, value, list, shared_data);
  // printf("\n");
  // free_results(shared_data->results, shared_data->thread_count);
  // free(shared_data);
  return error;
}

// void* run(void* data) {
//   private_data_t* private_data = (private_data_t*)data;
//   report_and_exit(private_data == NULL, "could not create GoldbachWorker Private Data");

//   //  initialize data
//   int64_t number = private_data->shared_data->num;
//   int64_t id = private_data->thread_number;
//   int64_t threadCount = private_data->shared_data->thread_count;
//   int64_t start = calc_start(number, threadCount, id);
//   int64_t finish = calc_finish(number, threadCount, id);
  
//   // Now str contains the integer as characters
//   //  save worker array in results
//   private_data->shared_data->results[id] =
//     goldbach_worker_run(number, start, finish);
//   return NULL;
// }

// void print_results(int64_t num_addings, int64_t value, bool list, void* data) {
//   shared_data_t* shared_data = (shared_data_t*)data;
//   report_and_exit(shared_data == NULL, "could not create GoldbachWorker Private Data");

//   bool first = true;
//   int64_t sums = 0;
//   for (int64_t i = 0; i < shared_data->thread_count; i++) {
//     sums += count_array_sums(shared_data->results[i], num_addings);
//   }

//   for (int64_t index = 0; index < shared_data->thread_count; index++) {
//     int64_t thread_sums =
//       count_array_sums(shared_data->results[index], num_addings);

//     if (list == true) {
//       if (index == 0) {
//         printf("-");
//         printf("%" PRIi64 ": ", value);
//         printf("%" PRIi64 " sums", sums);
//         printf(": ");
//       }
//       if (thread_sums != 0) {
//         show_array_addings(shared_data->results[index],
//           thread_sums, num_addings, first);
//         first = false;
//       }
//     } else {
//       if (index == 0) {
//         printf("%" PRIi64 ": ", value);
//         printf("%" PRIi64 " sums", sums);
//       }
//     }
//   }
// }

int64_t count_array_sums(int64_t* array, int num_addings) {
  int64_t sums = 0;
  int64_t iterAddings = 0;
    while (array[iterAddings] != 0) {
      sums +=1;
      iterAddings += num_addings;
    }
  return sums;
}

void show_array_addings(int64_t* array, int64_t sums,
    int64_t num_addings, bool first) {
  int64_t iterAddings = 0;
  while (iterAddings <= (num_addings*sums)-num_addings) {
    if (iterAddings != 0) {
      printf(", ");
    } else {
      if (!first) {
        printf(", ");
      }
    }
    printf("%" PRIi64 " + ", array[iterAddings]);
    if (num_addings == 3) {
      printf("%" PRIi64 " + ", array[iterAddings+1]);
      printf("%" PRIi64 , array[iterAddings+2]);
    } else {
      printf("%" PRIi64 , array[iterAddings+1]);
    }
    iterAddings+=num_addings;
  }
}

void free_results(int64_t** results, int64_t thread_count) {
  for (int64_t index = 0; index < thread_count; index++) {
    free(results[index]);
  }
  free(results);
}

int main(int argc, char* argv[]) {
  int error = EXIT_SUCCESS;
  //int threads = analyze_arguments(argc, argv);
  size_t threads = 12;
  controller_run(threads);
  return error;
}