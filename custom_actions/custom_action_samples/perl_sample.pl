#!/usr/bin/perl
# Use loop to print out all arguments passed to the script.
foreach my $arg(@ARGV)
{
	print "Found argument: $arg\n";
}