#ifndef goldbach_worker_H
#define goldbach_worker_H
#include "goldbach_worker.h"
#include <inttypes.h>
#include <stddef.h>

/**
*@brief main rutine of a GoldbachWorker 
*@details works with 64-bit positive integers
*@param num number of 64-bit positive integers
*@param start work start value for worker
*@param finish work finish value for worker
*@return array with solution numbers, null if cannot be created
*/
int64_t*  goldbach_worker_run(int64_t num, int64_t start, int64_t finish);

#endif  // goldbach_worker_H
