# Failure
Command '['nginx', '-c', '/tmp/nginx_spider.conf']' timed out after 10 seconds
Traceback (most recent call last):
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35880048129/run_experiment_distributed.py", line 732, in <module>
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35880048129/run_experiment_distributed.py", line 395, in main
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35880048129/run_experiment_distributed.py", line 126, in setup_nginx
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/subprocess.py", line 550, in run
    stdout, stderr = process.communicate(input, timeout=timeout)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/subprocess.py", line 1209, in communicate
    stdout, stderr = self._communicate(input, endtime, timeout)
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/subprocess.py", line 2116, in _communicate
    self._check_timeout(endtime, orig_timeout, stdout, stderr)
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/subprocess.py", line 1253, in _check_timeout
    raise TimeoutExpired(
subprocess.TimeoutExpired: Command '['nginx', '-c', '/tmp/nginx_spider.conf']' timed out after 10 seconds
