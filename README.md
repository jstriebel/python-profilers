# Python Profilers Guide
Code to demonstrate profilers and some optimizations.

For more information and more detailed descriptions of Python profilers
see my [**Codical blog posts on Python Profilers**](https://codical.org/python_profilers).

Presented at [PyCon Italia 2023](https://pycon.it/en/event/how-to-tune-your-python-analysis-pipeline-a-profiler-guide).

For more information on optimization strategies for data science applications,
please check my [data-analysis-speedup repo](https://github.com/jstriebel/data-analysis-speedup).


## Profiling Example

In the following steps, the `analysis.py` script will be profiled using different profilers. Additionally, an optimized version is available in `analysis_optimized.py`, which can be used interchangeably. See the [data-analysis-speedup repo](https://github.com/jstriebel/data-analysis-speedup) for more information on this optimization, and the respective PyCon talk about it.

### Installation & Usage
```bash
# use Python 3.8+ with poetry
python3 -m pip install poetry
poetry install
# enter the venv that poetry automatically creates
poetry shell

# generate the data used later
python prepare.py

# to see some small examples of the task, run
python example.py
```

In the shell opened above, you can try different profilers:

### Time Profilers
```bash
# Run just cProfile:
python -m cProfile -s tottime analysis.py | less

python -m cProfile -o profiles/cProfile.prof analysis.py
snakeviz profiles/cProfile.prof

py-spy record -o profiles/py-spy-flamegraph.svg -- python analysis.py
sensible-browser profiles/py-spy-flamegraph.svg

scalene --cpu analysis.py
```

### Memory Profilers
```bash
scalene analysis.py

memray run -o profiles/memray.bin analysis.py
memray flamegraph -o profiles/memray-flamegraph.html profiles/memray.bin
sensible-browser profiles/memray-flamegraph.html
```

### Cleanup
```bash
# To run scalene without having autogenerated files in
# arbitrary locations, you can run
scalene --cli --json --outfile profiles/scalene.json analysis.py
# and load the generate profiles/scalene.json in the page opened with
scalene --viewer

# To remove the files generated before, please run
rm profile.html profile.json
```

## Dev

```bash
./format.sh
```
