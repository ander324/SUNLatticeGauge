#!/usr/bin/awk -f

BEGIN {
    x=0;
    y=0;
}
{
    x+= $2;
    y+= $3;
}
END {
    print FILENAME ".real = " x/NR;
    print FILENAME ".imag = " y/NR;
}
