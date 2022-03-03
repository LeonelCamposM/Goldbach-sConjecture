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

typedef struct shared_data {
  int64_t thread_count;
  int64_t** results;
  int64_t num;
} shared_data_t;

typedef struct private_data {
  int64_t thread_number;
  shared_data_t* shared_data;
} private_data_t;

/**
*@brief generic rutine for init memory, create threads do work and join threads
*@param shared_data ptr to shared data of threads 
*@return ptr to shared data of threads 
*/
int create_threads(shared_data_t* shared_data);

/**
*@brief main rutine for instructions of threads 
*@param data ptr to private data of threads 
*/
void* run(void* data);

/**
*@brief calculates the beginning of the interval where a goldbachWorker
* will look for sums 
*@details STARTVALUE = 2, used for avoid assign ranges that N/A
*@param value work for thread = goldbach num
*@param thread_count number of working threads 
*@param thread_id thread id number
*@return start of thread work 
*/
int64_t calc_start(int64_t value, int64_t thread_count, int64_t thread_id);

/**
*@brief calculates the end of the interval where a goldbachWorker
* will look for sums  
*@param value work for thread = goldbach num
*@param thread_count number of working threads 
*@param thread_id thread id number
*@return finish of thread work 
*/
int64_t calc_finish(int64_t value, int64_t thread_count, int64_t thread_id);

/**
*@brief return min number of two numbers
*@param num1 number 1
*@param num2 number 2
*@return min number 
*/
int64_t min_num(int64_t num1, int64_t num2);

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

/**
*@brief validate user input
*@param value input
*/
bool analize_arguments(int64_t value);

/**
*@brief append a message or a number in Output.txt file
*@param mesage message to be writen
*@param number number to be writen
*@param number_flag true append the number, false append the message
*/
int write_output(char* mesage, size_t number, bool number_flag);

/**
*@brief get goldbach sums of a value
*@param value number 
*/
void calculate_number(int64_t value);

/**
*@brief get goldbach sums of a array
*@param input_numbers number 
*/
void calculate_array(dynamic_array_t* input_numbers);

void init_shared_data(shared_data_t* shared_data, int64_t value) {
  //  Select thread number
  shared_data->thread_count = sysconf(_SC_NPROCESSORS_ONLN);

  // init golbach shrd data
  shared_data->num = value;
  shared_data->results = (int64_t**)
    calloc(shared_data->thread_count, sizeof(int64_t*));
  report_and_exit(shared_data->results == NULL, "init_shared_data");
}

int create_threads(shared_data_t* shared_data) {
  assert(shared_data);
  int error = EXIT_SUCCESS;

  //  arrray of threads
  pthread_t* threads = (pthread_t*) calloc(shared_data->thread_count
    , sizeof(pthread_t));

  //  array of private datas
  private_data_t* private_data = (private_data_t*)
    calloc(shared_data->thread_count, sizeof(private_data_t));

  //  if gets memory
  if (threads && private_data) {
    for (int64_t index = 0; index < shared_data->thread_count; ++index) {
      //  init private_data[index]
      private_data[index].thread_number = index;
      private_data[index].shared_data = shared_data;

        //  create thread and execute run
      if (pthread_create(&threads[index], /*attr*/ NULL, run
        , &private_data[index]) != EXIT_SUCCESS) {
        fprintf(stderr, "error: could not create thread : " "%" PRIi64, index);
        printf("\n");
        error = 21;
        break;
      }
    }
    //  wait threads
    for (int64_t index = 0; index < shared_data->thread_count; ++index) {
      pthread_join(threads[index], /*value_ptr*/ NULL);
    }
    free(threads);
    free(private_data);
  } else {
    fprintf(stderr, "error: could not allocate memory for : " "%" PRIi64
      , shared_data->thread_count);
    printf(" threads \n");
    error = 22;
  }
return error;
}

void* run(void* data) {
  private_data_t* private_data = (private_data_t*)data;
  report_and_exit(private_data == NULL, "run");

  //  initialize data
  int64_t number = private_data->shared_data->num;
  int64_t id = private_data->thread_number;
  int64_t threadCount = private_data->shared_data->thread_count;
  int64_t start = calc_start(number, threadCount, id);
  int64_t finish = calc_finish(number, threadCount, id);

  private_data->shared_data->results[id] =
    goldbach_worker_run(number, start, finish);
  return NULL;
}

int64_t calc_start(int64_t value, int64_t thread_count, int64_t thread_id) {
  int64_t result = 0;
  if (STARTVALUE < thread_count) {
    // Equitable distribution of work for each worker
    int64_t work = thread_id * ( (value-STARTVALUE) / thread_count);
    // Assigns which worker has overload
    int64_t overload = min_num(thread_id, (value-STARTVALUE) % thread_count);
    result = work+overload;
  }else {
    // Equitable distribution of work for each worker
    int64_t work = thread_id * ( value / thread_count);
    // Assigns which worker has overload
    int64_t overload = min_num(thread_id, (value) % thread_count);
    result = work+overload;
  }
  return STARTVALUE + result;
}

int64_t calc_finish(int64_t value, int64_t thread_count, int64_t thread_id) {
  return calc_start(value, thread_count, thread_id + 1);
}

int64_t min_num(int64_t num1, int64_t num2) {
  int64_t result = 0;
  if (num1 < num2) {
    result = num1;
  } else {
    result = num2;
  }
  return result;
}

void print_results(int64_t num_addings, int64_t value, bool list, void* data) {
  shared_data_t* shared_data = (shared_data_t*)data;
  report_and_exit(shared_data == NULL, "print_results");

  bool first = true;
  int64_t sums = 0;
  for (int64_t i = 0; i < shared_data->thread_count; i++) {
    sums += count_array_sums(shared_data->results[i], num_addings);
  }

  for (int64_t index = 0; index < shared_data->thread_count; index++) {
    int64_t thread_sums =
      count_array_sums(shared_data->results[index], num_addings);
    if (list == true) {
      if (index == 0) {
        write_output("-", 0, false);
        write_output("",value, true);
        write_output(": ", 0, false);
        write_output("", sums, true);
        write_output(" sums", 0, false);
        write_output(": ", 0, false);
      }
      if (thread_sums != 0) {
        show_array_addings(shared_data->results[index],
          thread_sums, num_addings, first);
        first = false;
      }
    } else {
      if (index == 0) {
        write_output("",value, true);
        write_output(": ", 0, false);
        write_output("", sums, true);
        write_output(" sums", 0, false);
      }
    }
  }
  write_output("\n",0, false);
}

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
      write_output(", ", 0, false);
    } else {
      if (!first) {
        write_output(", ", 0, false);
      }
    }
    write_output("", array[iterAddings],true);
    write_output(" + ", 0, false);
    if (num_addings == 3) {
      write_output("", array[iterAddings+1],true);
      write_output(" + ", 0, false);
      write_output("", array[iterAddings+2],true);
    } else {
      write_output("", array[iterAddings+1],true);
    }
    iterAddings+=num_addings;
  }
}

int write_output(char* mesage, size_t number, bool number_flag) {
  FILE *file = fopen("Output.txt", "a+");
  report_and_exit (file == NULL, "output\n");
  if(number_flag == false){
    fprintf(file, "%s", mesage);
  }else{
    char str_number[100];
    sprintf(str_number, "%li", number);
    fprintf(file, "%s", str_number);
  }
  fclose(file);
  return EXIT_SUCCESS;
}

void free_results(int64_t** results, int64_t thread_count) {
  for (int64_t index = 0; index < thread_count; index++) {
    free(results[index]);
  }
  free(results);
}

bool analize_arguments(int64_t value) {
  bool valid_number = (value > 5 || value < -5);
  if (!valid_number) {
    write_output("", value, true);
    write_output(": NA\n", 0, false);
  }
  return valid_number;
}

void calculate_number(int64_t value) {
  bool valid_input = analize_arguments(value);
  if (valid_input) {
    shared_data_t* shared_data = (shared_data_t*)
    calloc(1, sizeof(shared_data_t));
    report_and_exit(shared_data == NULL, "calculate_number");

    bool list = false;
    if (value < 0) {
      list = true;
      value *= -1;
    }

    init_shared_data(shared_data, value);

    //  concurrent work
    create_threads(shared_data);

    // 1 thread print
    int num_addings = (value % 2 == 0)? 2 : 3;
    print_results(num_addings, value, list, shared_data);
    free_results(shared_data->results, shared_data->thread_count);
    free(shared_data);
  }
}

void calculate_array(dynamic_array_t* input_numbers) {
  for (size_t number = 0; number < input_numbers->count; number++) {
    int64_t goldbach_number = input_numbers->elements[number];
    bool valid_input = analize_arguments(goldbach_number);
    if (valid_input) {
      calculate_number(goldbach_number);
    }
  }
}

int main() {
  return EXIT_SUCCESS;
}
