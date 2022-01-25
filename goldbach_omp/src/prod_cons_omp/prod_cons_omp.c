#include "prod_cons_omp.h"
#include "producer.h"
#include "consumer.h"
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include "queue.h"

int64_t** prod_cons_omp_start(prod_cons_data_t* data, int64_t** results) {
  queue_t* shrd_queue = (queue_t*)
    calloc(1, sizeof(queue_t));
  report_and_exit(shrd_queue == NULL, "Could not create queue");
  queue_init(shrd_queue);

  

  // Produce all work
  #pragma omp parallel for
  for (size_t thread_id = 0; thread_id < data->threads+1; thread_id++)
  {
    if( thread_id == 0){
      printf("produzcoo -> %u\n",omp_get_thread_num());
      producer_start(data->input_numbers, shrd_queue, data->threads, results);
    }else {
      printf("consumo -> %u\n",omp_get_thread_num());
      sleep(5);
      consumer_start(shrd_queue, results);
    }
  }

  // for (int64_t i = 0; i < 12; i++) {
  //   printf(" cheking results[%zu]  \n", i);

  //     printf(" <-Array");
  //     size_t ind = 0;
  //     while (results[i][ind] != 0)
  //     {
  //       int64_t* ab = results[i];
  //       printf("%" PRIi64 " + ", ab[ind]);
  //       ind++;
  //     }

     
  // }
  return results;
}