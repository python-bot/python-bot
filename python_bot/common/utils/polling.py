import threading

try:
    import Queue as python_queue
except ImportError:
    import queue as python_queue

import sys

import six
import time

from python_bot.bot.bot import bot_logger

__stop_polling = threading.Event()


def stop_polling():
    __stop_polling.set()


def start_polling(retrieve_updates, none_stop=False, interval=1):
    bot_logger.info('Started polling.')
    __stop_polling.clear()
    error_interval = .25

    polling_thread = ThreadPool(num_threads=len(retrieve_updates))

    while not __stop_polling.wait(interval):
        try:
            for retrieve_update in retrieve_updates:
                polling_thread.put(retrieve_update)

            polling_thread.raise_exceptions()

            error_interval = .25
        except KeyboardInterrupt:
            bot_logger.info("KeyboardInterrupt received.")
            __stop_polling.set()
            polling_thread.close()
            break
        except Exception as e:
            bot_logger.error(e)
            if not none_stop:
                __stop_polling.set()
                bot_logger.info("Exception occurred. Stopping.")
            else:
                polling_thread.clear_exceptions()
                bot_logger.info("Waiting for {0} seconds until retry".format(error_interval))
                time.sleep(error_interval)
                error_interval *= 2

    bot_logger.info('Stopped polling.')


class ThreadPool:
    def __init__(self, num_threads=2):
        self.tasks = python_queue.Queue()
        self.workers = [WorkerThread(self.on_exception, self.tasks) for _ in range(num_threads)]
        self.num_threads = num_threads

        self.exception_event = threading.Event()
        self.exc_info = None

    def put(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def on_exception(self, worker_thread, exc_info):
        self.exc_info = exc_info
        self.exception_event.set()
        worker_thread.continue_event.set()

    def raise_exceptions(self):
        if self.exception_event.is_set():
            six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

    def clear_exceptions(self):
        self.exception_event.clear()

    def close(self):
        for worker in self.workers:
            worker.stop()
        for worker in self.workers:
            worker.join()


class WorkerThread(threading.Thread):
    count = 0

    def __init__(self, exception_callback=None, queue=None, name=None):
        if not name:
            name = "WorkerThread{0}".format(self.__class__.count + 1)
            self.__class__.count += 1
        if not queue:
            queue = python_queue.Queue()

        threading.Thread.__init__(self, name=name)
        self.queue = queue
        self.daemon = True

        self.received_task_event = threading.Event()
        self.done_event = threading.Event()
        self.exception_event = threading.Event()
        self.continue_event = threading.Event()

        self.exception_callback = exception_callback
        self.exc_info = None
        self._running = True
        self.start()

    def run(self):
        while self._running:
            try:
                task, args, kwargs = self.queue.get(block=True, timeout=.5)
                self.continue_event.clear()
                self.received_task_event.clear()
                self.done_event.clear()
                self.exception_event.clear()
                bot_logger.debug("Received task")
                self.received_task_event.set()

                task(*args, **kwargs)
                bot_logger.debug("Task complete")
                self.done_event.set()
            except python_queue.Empty:
                pass
            except:
                bot_logger.debug("Exception occurred")
                self.exc_info = sys.exc_info()
                self.exception_event.set()

                if self.exception_callback:
                    self.exception_callback(self, self.exc_info)
                self.continue_event.wait()

    def put(self, task, *args, **kwargs):
        self.queue.put((task, args, kwargs))

    def raise_exceptions(self):
        if self.exception_event.is_set():
            six.reraise(self.exc_info[0], self.exc_info[1], self.exc_info[2])

    def clear_exceptions(self):
        self.exception_event.clear()
        self.continue_event.set()

    def stop(self):
        self._running = False
