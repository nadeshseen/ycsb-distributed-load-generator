## Abstract
Storage is often the slowest component in a system. Therefore, it needs
to be rigorously tested to choose the best available options. Different im-
plementations of Distributed File systems have a significant impact on the
performance of the storage. The problem we have right now is the realis-
tic evaluation of Distributed File System(DFS). Developers use traditional
file system benchmarks to evaluate newly designed Distributed File systems.
This report presents an extension of YCSB(Yahoo Cloud Serving Benchmark)
that can simultaneously generate unique workloads from different machines
and allows the user to coordinate between workload generators to have a
more realistic workload.

## Overview
Figure - 4.1 gives an overview of the proposed design of the distributed Load
Generator. Here, we have a controller node from where the user controls
the type of workload and all other configurations needed. Worker Nodes
are running on different machines containing KV-replay instances. Target
System is the system we want to benchmark.

## Setup
In Figure - 4.1, the worker nodes shown are installed on the ub-04 machine
(Intel Xeon E5-2683 v4 and 128GB RAM) with ubuntu 18.04 installed. Every
VM has ubuntu-server 20.04 installed with 8GB RAM and four cores of CPU
allocated. Three VMs (VM1, VM2, and VM3) are used for the KV-replay
instances. We use the Redis cluster as our Target System and these use three
VMs (VM4, VM5, and VM6) as described in section 4.7.

How to run?
1. All the nodes should have python rest_server.py files called as Rest Agent in the text.
2. Run all Rest Agents.
3. To start the benchmark start rest_client.py using - python3 rest_client.py
4. Choose one mode and the benchmark will start according to the dlg_config.json