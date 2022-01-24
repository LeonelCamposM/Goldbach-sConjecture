// Copyright 2021 Jeisson Hidalgo-Cespedes <jeisson.hidalgo@ucr.ac.cr> CC-BY-4
// Simulates a producer and a consumer that share a unbounded buffer

#include <stdbool.h>
#include <stdio.h>
#include <queue.h>
#include "common.h"
#include "consumer.h"
#include "goldbach_worker.h"

// /**
// *@brief The consumer pull work intervals for each number, make Golbach Work and 
// * Store Results in CondSafe array
// *@param data ptr to Prod-Cons data
// */
// // TODO(checK) optimization01: Consumers implementation
// void* consume(void* data) {
//   simulation_t* simulation = (simulation_t*)data;

//   while (true) {
//     sem_wait(&simulation->can_access_consumed_count);
//     if (simulation->consumed_count >=
//         simulation->unit_count*simulation->consumer_count) {
//       sem_post(&simulation->can_access_consumed_count);
//       break;
//     }
//     ++simulation->consumed_count;
//     sem_post(&simulation->can_access_consumed_count);

//     sem_wait(&simulation->can_consume);

//     workInterval_t value;

//     // The consumer pull work intervals for each number
//     queue_dequeue(&simulation->queue, &value);

//     // make Golbach Work and Store Results in CondSafe array
//     GoldbachWorker_t* worker = GoldbachWorker_create();
//     value.results[value.resultsID] =
//     GoldbachWorker_run(worker, value.golbachNumber, value.start, value.finish);

//     GoldbachWorker_destroy(worker);
//   }

//   return NULL;
// }
