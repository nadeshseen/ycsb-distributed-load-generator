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



How to run?
1. All the nodes should have python rest_server.py files called as Rest Agent in the text.
2. Run all Rest Agents.
3. To start the benchmark start rest_client.py using - python3 rest_client.py
4. Choose one mode and the benchmark will start according to the dlg_config.json