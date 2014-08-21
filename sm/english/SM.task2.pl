#!/usr/bin/perl

use strict;

die "Usage: $0 <dir> <annotation>\n" unless @ARGV == 2;
my $dirstr = $ARGV[0];
my $annotation = $ARGV[1];

my $file;
my @dir;
my $line;
my $topic; 
my $fl; 
my $fl_rank; 
my $fl_score; 
my $sl; 
my $sl_rank; 
my $sl_score;
my $pair;
my %fl_pool=();
my %sl_pool=();
my %pair_pool=();
my %label=();

my %h_count;
my %h_score;
my %h_topic;
my %h_topic_count;
my $key;
my $value;

open SRC, $annotation or die "can't open annotation file!";
while ($line = <SRC>)
{
	if ($line =~ m/^(.*?)\t(.*?)\t(.*?)\t(.*?)\n/)
	{
		$topic = $1;
		$fl = $2;
		$sl = $3;
		$pair = $topic."\t".$fl."\t".$sl;
		$label{$pair} = $4;
	}
	else
	{
		die "line format error: $line";
	}
}
close(SRC);

opendir (DIR, $dirstr) or die "can't open the directory!";
@dir = readdir DIR;
foreach $file (@dir) 
{
	if (($file eq ".") || ($file eq ".."))
	{
		next;
	}
	#system("c:\\perl\\bin\\perl D:\\Liuyiqun\\study\\项目工作\\NTCIR-IMine\\Results\\check_format.pl $dirstr\\$file");
	#[TopicID];0;[1st level Subtopic];[Rank1];[Score1];0;[2nd level Subtopic];[Rank2];[Score2];[RunName]\n
	#0051;0;Microsoft Windows;1;0.99;0;Windows 8;1;0.98;MSRA-S-E-1A

	$file = $dirstr."\\".$file;
	print $file."\n";
	%h_count=();
	%h_score=();
	%h_topic=();
	%h_topic_count=();
	
	open SRC, $file or die "can't open file $file!";
	while ($line = <SRC>)
	{
		if ($line =~ m/^(.*?)\;0\;(.*?)\;(.*?)\;(.*?)\;0\;(.*?)\;(.*?)\;(.*?)\;/)
		{
			$topic = $1;
			$fl = $2;
			$fl_rank = $3;
			$fl_score = $4;
			$sl = $5;
			$sl_rank = $6;
			$sl_score = $7;
			
			$pair = $topic."\t".$fl."\t".$sl;
			$fl_rank = $topic."\t".$fl_rank;
			
			if (($topic>33 && $topic<51)||($topic>83 && $topic<101)||($topic>134 && $topic<151))
			{
				next;
			}
			
			if (!exists $h_count{$fl_rank})
			{
				$h_count{$fl_rank} = 0;
				$h_score{$fl_rank} = 0;
			}
			$h_count{$fl_rank} ++;
						
			if (exists $label{$pair})
			{
				if ($label{$pair}==1)
				{
					$h_score{$fl_rank}++;
				}
			}
		}
		else
		{
			print "Line format error: $line";
		}
	}
	close(SRC);
	
	while (($key,$value) = each %h_count)
	{
		if ($key =~ m/^(.*?)\t(.*?)$/)
		{
			$topic = $1;
			$fl_rank = $2;
			if (!exists $h_topic{$topic})
			{
				$h_topic{$topic} = 0;
				$h_topic_count{$topic} = 0;
			}
			$h_topic{$topic} += $h_score{$key}/$value;
			$h_topic_count{$topic}++;
		}
	}
	
	$file = $file.".h-score";
	open DST, ">$file" or die "cannot open file to write\n";
	while (($key,$value) = each %h_topic)
	{
		print DST $key."\t".$h_topic_count{$key}."\t".$value."\n";
	}
	close(DST);

	
}

