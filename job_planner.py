#!/usr/bin/env python
""" 
Job planner for android workers. This version completes jobs by brute force:
all workers work on the same job until it is completed. Once the job is
completed, all workers move on to the next job.

In the future, I hope to improve this planner by handling job assignments
asynchronously, which will be more time-efficient. Moreover, I would like
to incorporate job priority.
"""

from sys import stdin

class Job:
    ''' define a job '''
    def __init__(self, name, tasks, task_time, can_begin, priority):
        self.name = name
        self.tasks = tasks
        self.task_time = task_time
        self.can_begin = int(can_begin)
        self.priority = priority
        self.duration = int(tasks) * int(task_time)

class Worker:
    ''' define an android worker '''
    def __init__(self, name):
        self.name = name

class Order:
    ''' define an order for a worker '''
    def __init__(self, time, worker, job):
        self.time = time
        self.worker = worker
        self.job = job

def main():
    ''' creates a list of orders for Jean '''
    jobs, workers = get_jobs_and_workers()
    orders = generate_orders(jobs, workers)
    print_orders(orders)

def get_jobs_and_workers():
    ''' reads in tuples of jobs and workers '''
    jobs = []
    workers = []

    jobs_and_droids = stdin.readlines()

    for item in jobs_and_droids:
        if item[:3] == "job":
            job = item.split()
            jobs.append(Job(job[1], job[2], job[3], job[4], job[5]))
        elif item[:6] == "worker":
            worker = item.split()
            workers.append(Worker(worker[1]))
        else:
            print "invalid input: not a job or worker"
            exit(1)

    return jobs, workers

def generate_orders(jobs, workers):
    ''' generates orders for Jean's androids '''
    orders = []
    time_now = 0
    num_workers = 0

    for worker in workers:
        num_workers += 1

    for job in jobs:
        orders = assign_new_orders(orders, time_now, job, workers)
        time_now += job.can_begin * num_workers
        time_now += job.duration / num_workers

    return orders

def assign_new_orders(orders, time_now, job, workers):
    ''' assigns initial jobs to workers '''
    for worker in workers:
        orders.append(Order(time_now, worker.name, job.name))

    return orders

def print_orders(orders):
    ''' prints orders to standard output '''
    for order in orders:
        print order.time, order.worker, order.job

if __name__ == "__main__":
    main()
