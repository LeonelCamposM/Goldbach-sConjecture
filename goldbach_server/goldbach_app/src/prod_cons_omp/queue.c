// Copyright 2021 Jeisson Hidalgo-Cespedes <jeisson.hidalgo@ucr.ac.cr> CC-BY-4
// Implements a thread-safe queue

#include <assert.h>
#include <stdlib.h>
#include "queue.h"

void queue_remove_first_unsafe(queue_t* queue);
bool queue_is_empty_unsafe(const queue_t* queue);

int queue_init(queue_t* queue) {
  assert(queue);
  queue->head = NULL;
  queue->tail = NULL;
  return 0;
}

int queue_destroy(queue_t* queue) {
  queue_clear(queue);
  return 0;
}

bool queue_is_empty_unsafe(const queue_t* queue) {
  assert(queue);
  return queue->head == NULL;
}

bool queue_is_empty(queue_t* queue) {
  assert(queue);
  bool result = true;
  #pragma omp critical
  {
  result = queue_is_empty_unsafe(queue);
  }
  return result;
}

int queue_enqueue(queue_t* queue, const work_unit_t data) {
  assert(queue);
  int error = EXIT_SUCCESS;

  queue_node_t* new_node = (queue_node_t*)
    calloc(1, sizeof(queue_node_t));

  if (new_node) {
    new_node->data = data;

    #pragma omp critical
    {
    if (queue->tail) {
      queue->tail = queue->tail->next = new_node;
    } else {
      queue->head = queue->tail = new_node;
    }
    }
  } else {
    error = EXIT_FAILURE;
  }

  return error;
}

int queue_dequeue(queue_t* queue, work_unit_t* data) {
  assert(queue);
  int error = 0;

  #pragma omp critical
  {
    if (!queue_is_empty_unsafe(queue)) {
      if (data) {
        *data = queue->head->data;
      }
      queue_remove_first_unsafe(queue);
    } else {
      error = EXIT_FAILURE;
    }
  }

  return error;
}

void queue_remove_first_unsafe(queue_t* queue) {
  assert(queue);
  assert(!queue_is_empty_unsafe(queue));
  queue_node_t* node = queue->head;
  queue->head = queue->head->next;
  free(node);
  if (queue->head == NULL) {
    queue->tail = NULL;
  }
}

void queue_clear(queue_t* queue) {
  assert(queue);
  #pragma omp critical
  {
    while (!queue_is_empty_unsafe(queue)) {
      queue_remove_first_unsafe(queue);
    }
  }
}
