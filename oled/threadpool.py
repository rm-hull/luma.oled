# -*- coding: utf-8 -*-
# Copyright (c) 2016 Richard Hull and contributors
# See LICENSE.rst for details.

# Adapted from http://code.activestate.com/recipes/577187-python-thread-pool/
# Attribution: Created by Emilio Monti on Sun, 11 Apr 2010 (MIT License).

from threading import Thread


class worker(Thread):
    """
    Thread executing tasks from a given tasks queue
    """
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            self.tasks.task_done()


class threadpool:
    """
    Pool of threads consuming tasks from a queue
    """
    def __init__(self, num_threads):
        try:
            from Queue import Queue
        except ImportError:
            from queue import Queue

        self.tasks = Queue(num_threads)
        for _ in range(num_threads):
            worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        """
        Add a task to the queue
        """
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        """
        Wait for completion of all the tasks in the queue
        """
        self.tasks.join()
