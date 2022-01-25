#include "common.h"
#include "consumer.h"
#include "goldbach_worker.h"
#include "common.h"
#include <stdlib.h>
#include <stdio.h>

void consumer_start(queue_t* queue, int64_t** ress){
  work_unit_t* new_work = (work_unit_t*)
    calloc(1, sizeof(work_unit_t));

  while (true) {
    int error = queue_dequeue(queue, new_work);
    if(error == 0) {
      int64_t* res;
      #pragma omp critical 
      {
      printf("consumed \n");
      printf("%" PRIi64 " -> start\n", new_work->start);
      printf("%" PRIi64 " -> finish\n", new_work->finish);
      printf("%" PRIi64 " -> goldbach_number\n", new_work->goldbach_number);
      printf("%" PRIi64 " -> results_id\n", new_work->results_id);
      printf("\n");

      res = goldbach_worker_run(new_work->goldbach_number, new_work->start, new_work->finish);
      printf(" Array -> ");
        size_t ind = 0;
        while (res[ind] != 0)
        {
          printf("%" PRIi64 " + ", res[ind]);
          ind++;
        }
      printf("\n");
      ress[new_work->results_id] = res;
      int64_t* arr = ress[new_work->results_id];
      printf(" Array de work -> ");
      size_t indw = 0;
      while (arr[indw] != 0)
      {
        printf("%" PRIi64 " + ", arr[indw]);
        indw++;
      }
      printf("\n");
      }
    } else {
      break;
    }
  }
  printf("consumer finished \n");
}