#!/usr/bin/env perl

use strict;
use warnings;

use File::Slurp;
use JSON5;
use TOML::Dumper;

sub json52toml {
    my $json5       = read_file(@_) or die "[Error] JSON5 文件读取错误，请检查路径是否完全和正确";
    my $perl_scalar = decode_json5 $json5;
    my $toml        = TOML::Dumper->new->dump($perl_scalar);
    $toml =~ s!\\/!/!g;

    ( my $new_file ) = @_;
    $new_file =~ s/\.json5?$/\.toml/;

    open( OUT, ">:encoding(UTF-8)", $new_file );
    print OUT "$toml";
    close(OUT);
}

if ( @ARGV == 0 ) {
    print "[Info.Auto] 未提供传入参数，将启动自动匹配转换\n";
    my @PATH  = ( "./", "/ql/data/config/", "/ql/config/", "/usr/local/app/script/Lists/" );
    my @NAME  = ( "check.json5", "check.json", "notify.json5", "notify.json" );
    my @files = ( $ENV{CHECK_CONFIG}, $ENV{NOTIFY_CONFIG_PATH} );
    foreach my $path (@PATH) {
        foreach my $name (@NAME) {
            push @files, "$path$name";
        }
    }

    foreach my $file (@files) {
        if ( $file and -e $file ) {
            print "\t[Info] $file 存在\n";
            my $new_file = $file;
            $new_file =~ s/\.json5?$/\.toml/;
            if ( -e $new_file ) {
                print "\t\t[Info.Quit] $new_file 已存在，放弃转换\n";
            }
            else {
                print "\t\t[Info.GoOn] $new_file 不存在，开始转换\n";
                json52toml($file);
            }
        }
    }
}

elsif ( @ARGV == 1 ) { json52toml $ARGV[0] }

else {
    die
"\tUsage: perl $0 <待转换的全路径文件名>\n\te.g. perl $0 /usr/local/app/script/Lists/check.json5\n\t[Error] 用法错误，已退出!!!";
}
