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
      res = goldbach_worker_run(new_work->goldbach_number, new_work->start, new_work->finish);
      ress[new_work->results_id] = res;
    } else {
      break;
    }
  }
}