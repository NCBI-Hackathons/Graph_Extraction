# Graphy McBrowserface

This is a toy example of a graph genome browser.

## Motivation

To date, the reference genome assemblies for most species, including human, have been represented as linear, haploid sequences. With the advent of population-scale sequencing, graph structures have been proposed as a better way to represent genomes. A graph has the advantage of naturally representing variation as forking edges (“bubbles”) and individuals as paths through the graph. Read alignment to graph genomes, and variant calling from those alignments, has been shown to be both more sensitive and more specific than using linear genomes. However, the migration to graph-based genomes is hindered by 1) the non-interoperability of most existing bioinformatics tools with sequence graphs; 2) the substantial challenge and degree of effort involved in adapting those tools; 3) new challenges in annotating and visualizing graph-based references and alignments. Genome browsers are among the most widely used tools among both novices and experts in genomics. To motivate the transition to graph genomes, we developed a simple graph-based genome browser that is accessible at http://graphymcbrowserface.umbc.in.

## Results

We did the following:

1. Generate a population of chromosomes (GRCh38 chr22) with randomly-generated structural variants inserted, using [SVGen](http://svgen.openbioinformatics.org).
2. Build a population graph of the generated chromosomes plus the reference genome, using [TwoPaCo](https://github.com/medvedevgroup/TwoPaCo). Dump the graph to [GFA](https://github.com/GFA-spec).
3. Create a GFA to [JSONGraph](https://github.com/jsongraph/json-graph-specification) converter.
4. Implement several different Javascript-based viewers for JSONGraph data, using:
    * Force-directed graph layout
    * [Sequence Tube Maps](https://github.com/wolfib/sequenceTubeMap)
    * Chord graphs

## Dependencies

* JSON.pm
* python (2.x)
* Web Server (Apache, nginx etc) for web components

## Installation

Use the [Makefile]() to install SVGen and TwoPaCo.

```
export SRV_INSTALL_PATH=/var/www && make build && make install
```

## Manuscript

[Draft](https://docs.google.com/document/d/1mY2KMSLe1XM-KQ5Gd6FzxJmw2DAPLChPy-zluR6TMAk)

## Contributors

* Nathan Bouk
* [John Didion](https://github.com/jdidion)
* [Lin DasSarma](https://github.com/l1n)
* Paul Meric
* Lisa Federer
* Ben Busby
