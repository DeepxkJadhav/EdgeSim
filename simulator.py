from __future__ import annotations
import heapq
import random
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple

"""
EdgeSim/simulator.py

A small discrete-event edge computing simulator.

Features:
- Devices with compute capacity (cycles/sec) and network latency between devices.
- Tasks with arrival time, required cycles, and optional origin device.
- Simple greedy offloading policy: try local device, else offload to a target device if beneficial.
- Event-driven simulation with basic statistics.

Usage:
    python simulator.py
"""



@dataclass(order=True)
class Event:
    time: float
    priority: int
    action: str = field(compare=False)
    obj: object = field(compare=False)


@dataclass
class Task:
    id: int
    arrival: float
    cycles: float  # cycles required to complete
    origin: str  # id of originating device
    assigned: Optional[str] = None
    start_time: Optional[float] = None
    finish_time: Optional[float] = None


class Device:
    def __init__(self, id_: str, compute_capacity: float):
        """
        compute_capacity: cycles per second
        """
        self.id = id_
        self.compute_capacity = compute_capacity
        self.queue: List[Task] = []
        self.busy_until = 0.0
        self.completed: List[Task] = []

    def estimate_wait_and_service(self, now: float, task: Task) -> Tuple[float, float]:
        """
        Return (wait_time, service_time) if task is assigned now.
        """
        wait_time = max(0.0, self.busy_until - now)
        service_time = task.cycles / self.compute_capacity
        return wait_time, service_time

    def assign_task(self, now: float, task: Task) -> Event:
        """
        Assign task to this device, schedule its completion event.
        Returns the completion Event.
        """
        service_time = task.cycles / self.compute_capacity
        start_time = max(now, self.busy_until)
        finish_time = start_time + service_time
        self.busy_until = finish_time
        task.assigned = self.id
        task.start_time = start_time
        task.finish_time = finish_time
        # store in completed list on finish via event
        evt = Event(time=finish_time, priority=1, action="complete", obj=task)
        return evt


class Network:
    def __init__(self):
        # simple symmetric latency map in seconds
        self.latencies: Dict[Tuple[str, str], float] = {}

    def set_latency(self, a: str, b: str, latency: float):
        self.latencies[(a, b)] = latency
        self.latencies[(b, a)] = latency

    def latency(self, a: str, b: str) -> float:
        if a == b:
            return 0.0
        return self.latencies.get((a, b), 0.05)  # default small latency


class Simulator:
    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.network = Network()
        self.event_queue: List[Event] = []
        self.now = 0.0
        self.tasks: Dict[int, Task] = {}
        self.next_task_id = 0

    def add_device(self, id_: str, compute_capacity: float):
        self.devices[id_] = Device(id_, compute_capacity)

    def set_latency(self, a: str, b: str, latency: float):
        self.network.set_latency(a, b, latency)

    def schedule_task_arrival(self, arrival: float, cycles: float, origin: str):
        t = Task(id=self.next_task_id, arrival=arrival, cycles=cycles, origin=origin)
        self.tasks[t.id] = t
        evt = Event(time=arrival, priority=0, action="arrival", obj=t)
        heapq.heappush(self.event_queue, evt)
        self.next_task_id += 1

    def run(self, until: Optional[float] = None, verbose: bool = False):
        while self.event_queue:
            evt = heapq.heappop(self.event_queue)
            if until is not None and evt.time > until:
                break
            self.now = evt.time
            if evt.action == "arrival":
                self._handle_arrival(evt.obj, verbose)
            elif evt.action == "complete":
                self._handle_completion(evt.obj, verbose)
        # advance time to until if provided
        if until is not None:
            self.now = until

    def _handle_arrival(self, task: Task, verbose: bool):
        if verbose:
            print(f"[{self.now:.3f}] Task {task.id} arrived at {task.origin} needing {task.cycles} cycles")
        # simple policy: evaluate local vs all other devices, include network latency
        best_device = None
        best_finish = float("inf")
        for dev_id, dev in self.devices.items():
            net_delay = self.network.latency(task.origin, dev_id)
            wait, service = dev.estimate_wait_and_service(self.now + net_delay, task)
            finish = self.now + net_delay + wait + service
            if finish < best_finish:
                best_finish = finish
                best_device = dev
        # simulate transmission time by scheduling assignment after latency
        assert best_device is not None
        latency = self.network.latency(task.origin, best_device.id)
        assign_time = self.now + latency
        # create a wrapper event that assigns the task at assign_time
        assign_evt = Event(time=assign_time, priority=0, action="assign", obj=(task, best_device.id))
        heapq.heappush(self.event_queue, assign_evt)

    def _handle_completion(self, task: Task, verbose: bool):
        dev = self.devices[task.assigned]
        dev.completed.append(task)
        if verbose:
            print(f"[{self.now:.3f}] Task {task.id} completed on {dev.id} (arrival {task.arrival:.3f}, start {task.start_time:.3f}, finish {task.finish_time:.3f})")

    def _assign_now(self, task: Task, device_id: str):
        dev = self.devices[device_id]
        evt = dev.assign_task(self.now, task)
        # push completion event
        heapq.heappush(self.event_queue, evt)

    def _process_events(self):
        # Not used; kept for extension
        pass

    def handle_assign_event(self, task: Task, device_id: str, verbose: bool):
        if verbose:
            print(f"[{self.now:.3f}] Assigning Task {task.id} to {device_id}")
        self._assign_now(task, device_id)

    # integrate assign events into main loop
    def run_until_idle(self, verbose: bool = False):
        while self.event_queue:
            evt = heapq.heappop(self.event_queue)
            self.now = evt.time
            if evt.action == "arrival":
                self._handle_arrival(evt.obj, verbose)
            elif evt.action == "assign":
                task, device_id = evt.obj
                self.handle_assign_event(task, device_id, verbose)
            elif evt.action == "complete":
                self._handle_completion(evt.obj, verbose)

    def stats(self) -> Dict[str, float]:
        all_tasks = [t for t in self.tasks.values() if t.finish_time is not None]
        if not all_tasks:
            return {}
        latencies = [t.finish_time - t.arrival for t in all_tasks]
        makespan = max(t.finish_time for t in all_tasks) - min(t.arrival for t in all_tasks)
        return {
            "tasks_completed": len(all_tasks),
            "avg_latency": sum(latencies) / len(latencies),
            "max_latency": max(latencies),
            "makespan": makespan,
        }


def example_run():
    sim = Simulator()
    # add devices: edge (fast), cloud (very fast but higher latency), device local (slow)
    sim.add_device("device", compute_capacity=1e6)  # 1 MHZ cycles/sec
    sim.add_device("edge", compute_capacity=5e6)
    sim.add_device("cloud", compute_capacity=20e6)
    # set latencies (s)
    sim.set_latency("device", "edge", 0.02)
    sim.set_latency("device", "cloud", 0.15)
    sim.set_latency("edge", "cloud", 0.05)

    random.seed(0)
    # schedule some random tasks arriving at the device
    t = 0.0
    for i in range(20):
        inter = random.expovariate(1 / 0.1)
        t += inter
        cycles = random.uniform(5e5, 5e6)  # between 0.5M and 5M cycles
        sim.schedule_task_arrival(arrival=t, cycles=cycles, origin="device")

    # run simulation
    sim.run_until_idle(verbose=True)
    print("Stats:", sim.stats())


if __name__ == "__main__":
    example_run()