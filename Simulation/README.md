# Simulation of an assembly graph

We use SVGen to simulate structural variants in chromosome 22 of the reference (GRCh38). We then use TwoPaCo to assemble a graph from the simulated chromosomes.

```
# Simulate 12 chromosomes.
export SVGEN_BASE=~/SVGen
Simulation/generate_sequences.sh $SVGEN_BASE 12
```

```
# Assemble the graph, convert it to GFA format, then convert to JSONGraph.
Simulation/assemble.sh $SVGEN_BASE
```
