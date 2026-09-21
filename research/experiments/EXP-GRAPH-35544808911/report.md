# Failure
PosixPath('/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/testbed_server.py') and PosixPath('/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/testbed_server.py') are the same file
Traceback (most recent call last):
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/run_experiment_distributed.py", line 768, in <module>
    status,outcome=main()
                   ^^^^^^
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/run_experiment_distributed.py", line 368, in main
    shutil.copy2(src,dst)
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/shutil.py", line 475, in copy2
    copyfile(src, dst, follow_symlinks=follow_symlinks)
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/shutil.py", line 240, in copyfile
    raise SameFileError("{!r} and {!r} are the same file".format(src, dst))
shutil.SameFileError: PosixPath('/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/testbed_server.py') and PosixPath('/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35544808911/testbed_server.py') are the same file
