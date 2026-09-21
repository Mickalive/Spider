# Failure
Object of type bool is not JSON serializable
Traceback (most recent call last):
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35572179326/run_experiment_distributed.py", line 765, in <module>
    status,outcome=main()
                   ^^^^^^
  File "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35572179326/run_experiment_distributed.py", line 696, in main
    with open(EXPERIMENT_DIR / "result.json","w") as f: json.dump(result,f,indent=2)
                                                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/__init__.py", line 179, in dump
    for chunk in iterable:
                 ^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 406, in _iterencode_dict
    yield from chunks
  [Previous line repeated 2 more times]
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.14/x64/lib/python3.12/json/encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type bool is not JSON serializable
