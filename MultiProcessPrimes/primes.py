from multiprocessing import Process, Queue
import sys
import timeit

start = timeit.default_timer()
total_primes = 0
max_process = int(sys.argv[1])
max_number = int(sys.argv[2])
process_list = []
divided_lists = []

q = Queue()

def is_prime(number):
    for divisors in range(2, int(number/2)):
        if number % divisors == 0:
            return False
    return True

def count_primes(*number_list):
    prime_count = 0
    for number in number_list:
        if is_prime(number) == True:
            prime_count += 1
    q.put(prime_count)

if __name__ == '__main__':
    for i in range(0, max_process):
        n_list = []
        divided_lists.append(n_list)

    process_index = 0
    divided_lists[0].append(2)
    for number in range(2, max_number):
        if number % 2 != 0:
            divided_lists[process_index].append(number)
            process_index += 1

            if process_index == max_process:
                process_index = 0

    for i in range(0, max_process):
        p = Process(target=count_primes, args=(divided_lists[i]))
        process_list.append(p)

    for process in process_list:
        process.start()

    for process in process_list:
        total_primes += q.get()
        process.join()

    stop = timeit.default_timer()
    print('\n Time Elapsed: ', stop - start, "seconds", '\n', 'Numbers counted: ', max_number, '\n', 'Primes found: ', total_primes, '\n', 'Using: ', max_process, 'Threads')
