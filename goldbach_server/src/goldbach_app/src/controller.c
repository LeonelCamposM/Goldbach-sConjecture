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
#include "prod_cons_omp.h"

#define MAX 100

char* controller_run(int64_t goldbach_num, char* output_string);

void print_results(dynamic_array_t* input, int64_t** results,
  size_t thread_count, char* output_string);

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
    int64_t num_addings, bool first, char* output_string);

/**
*@brief free matrix results
*@param results ptr to matrix results
*@param goldbach_num number to work
*/
void free_results(int64_t** results, int64_t thread_count);

int string_cat(const char* str1, const char* str2, char* buffer, bool number_flag, int64_t number);

void *concat_strings(void* restrict dst, const void* restrict src, int c, size_t n);

char* controller_run(int64_t goldbach_num, char* output_string) {
  int error = EXIT_SUCCESS;

  prod_cons_data_t* data = (prod_cons_data_t*)
    calloc(1, sizeof(prod_cons_data_t));
  report_and_exit(data == NULL, "Could not create producer consumer data");

  data->input_numbers = read_input();
  array_append(data->input_numbers, goldbach_num);

  data->threads = sysconf(_SC_NPROCESSORS_ONLN);

  //int64_t** results
  data->results = (int64_t**)
    calloc(data->threads*data->input_numbers->count, sizeof(int64_t*));
  report_and_exit(data->results == NULL, "could not create results array");

  data->results = prod_cons_omp_start(data, data->results);

  print_results(data->input_numbers, data->results, data->threads, output_string);
  free_results(data->results, data->threads);
  free(data);
  return 0;
}

void print_results(dynamic_array_t* input, int64_t** results,
  size_t thread_count, char* output_string) {
  for (size_t inputIter = 0; inputIter < input->count; inputIter++) {
    // get nex number to be printed
    int64_t value = input->elements[inputIter];

    // Handle N/A Exceptions
    int valido = verify_input(value);

    if (valido == EXIT_SUCCESS) {
      // verify list
      bool list = false;
      if (value < 0) {
        value *= -1;
        list = true;
      }

      // Verify parity of the number
      int numAddings = 0;
      if (value % 2 == 0) {
        numAddings = 2;
      } else {
        numAddings = 3;
      }

      // calc start and finish positions of array
      size_t start = inputIter*thread_count;
      size_t finish = start + thread_count;

      //  count total amount of sums found
      bool first = true;
      int64_t sums = 0;
      for (size_t i = start; i < finish; i++) {
        sums += count_array_sums(results[i], numAddings);
      }

      //  print array stored in results[index]
      for (int64_t index = start; index < finish; index++) {
        int64_t thread_sums =
          count_array_sums(results[index], numAddings);

        //  list sums
        if (list == true) {
          // print format -value : x sums
          if (index == start) {
            string_cat("", "-", output_string, false, 0);
            string_cat(output_string, "", output_string, true, value);
            string_cat(output_string, ": ", output_string, false, 0);
            string_cat(output_string, "", output_string, true, sums);
            string_cat(output_string, " sums", output_string, false, 0);
            string_cat(output_string, ": ", output_string, false, 0);
          }
          // print array
          if (thread_sums != 0) {
            show_array_addings(results[index],
              thread_sums, numAddings, first, output_string);
            first = false;
          }
        } else {
          //  dont list sums
          if (index == start) {
            string_cat("", "", output_string, false, 0);
            string_cat(output_string, "", output_string, true, value);
            string_cat(output_string, ": ", output_string, false, 0);
            string_cat(output_string, "", output_string, true, sums);
            string_cat(output_string, " sums", output_string, false, 0);
          }
        }
      }
      string_cat(output_string, "\n", output_string, false, 0);
    }
  }
}


int64_t count_array_sums(int64_t* array, int num_addings) {
  int64_t sums = 0;
  int64_t iterAddings = 0;
    int64_t num = array[iterAddings];
    while (num != 0) {
      sums +=1;
      iterAddings += num_addings;
      num = array[iterAddings];
    }
  return sums;
}

void show_array_addings(int64_t* array, int64_t sums,
    int64_t num_addings, bool first, char* output_string) {
  int64_t iterAddings = 0;
  while (iterAddings <= (num_addings*sums)-num_addings) {
    if (iterAddings != 0) {
      string_cat(output_string, ", ", output_string, false, 0);
    } else {
      if (!first) {
        string_cat(output_string, ", ", output_string, false, 0);
      }
    }
    string_cat(output_string, "", output_string, true, array[iterAddings]);
    string_cat(output_string, " + ", output_string, false, 0);
    if (num_addings == 3) {
      string_cat(output_string, "", output_string, true, array[iterAddings+1]);
      string_cat(output_string, " + ", output_string, false, 0);
      string_cat(output_string, "", output_string, true, array[iterAddings+2]);
    } else {
      string_cat(output_string, "", output_string, true, array[iterAddings+1]);
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

// https://www.delftstack.com/es/howto/c/concatenate-strings-in-c/
void *concat_strings(void* restrict dst, const void* restrict src, int c, size_t n)
{
  const char *s = src;
  for (char *ret = dst; n; ++ret, ++s, --n)
  {
    *ret = *s;
    if ((unsigned char)*ret == (unsigned char)c)
        return ret + 1;
  }
  return 0;
}

int string_cat(const char* str1, const char* str2, char* buffer, bool number_flag, int64_t number) {
  // no number
  if(number_flag == false){
    concat_strings(concat_strings(buffer, str1, '\0', MAX) - 1, str2, '\0', MAX);
  }else{
    char str[MAX];
    sprintf(str, "%li", number);
    concat_strings(concat_strings(buffer, str1, '\0', MAX) - 1, str, '\0', MAX);
  }
  return 0;
}

int main(int argc, char* argv[]) {
  int error = EXIT_SUCCESS;
  // size_t threads = analyze_arguments(argc, argv);
  // controller_run(threads);
  return error;
}