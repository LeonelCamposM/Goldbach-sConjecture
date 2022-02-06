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
  producer_start(data->input_numbers, shrd_queue, data->threads, results);

  #pragma omp parallel for
  for (size_t thread_id = 0; thread_id < data->threads+1; thread_id++)
  {
    consumer_start(shrd_queue, results);
  }

  return results;
}
