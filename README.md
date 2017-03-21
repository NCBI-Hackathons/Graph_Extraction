# Graphy McBrowserface

This is a toy example of a graph genome browser. We did the following:

1. Generate a population of chromosomes (GRCh38 chr22) with randomly-generated structural variants inserted, using [SVGen](http://svgen.openbioinformatics.org).
2. Build a population graph of the generated chromosomes plus the reference genome, using [TuPaCo](https://github.com/medvedevgroup/TwoPaCo). Dump the graph to [GFA](https://github.com/GFA-spec).
3. Create a GFA to [JSONGraph](https://github.com/jsongraph/json-graph-specification).
4. Implement several different Javascript-based viewers for JSONGraph data, using:
    * Force-directed graph layout
    * [Sequence Tube Maps](https://github.com/wolfib/sequenceTubeMap)
    * Chord graphs

## Installation

1. Use the [Makefile]() to install SVGen and TuPaCo.
