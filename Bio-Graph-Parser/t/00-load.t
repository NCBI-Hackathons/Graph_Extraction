#!perl -T
use 5.006;
use strict;
use warnings;
use Test::More;

plan tests => 1;

BEGIN {
    use_ok( 'Bio::Graph::Parser' ) || print "Bail out!\n";
}

diag( "Testing Bio::Graph::Parser $Bio::Graph::Parser::VERSION, Perl $], $^X" );
