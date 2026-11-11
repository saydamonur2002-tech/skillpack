#!/usr/bin/env python3
"""Proleptic Gregorian date to two-part Julian date and MJD. See LICENSE, NOTICE and SOURCE.md."""
from runtime import cli

def calculate(p):
    y=p['year'];m=p['month'];day=p['day'];days=[31,28,31,30,31,30,31,31,30,31,30,31]
    leap=m==2 and y%4==0 and (y%100!=0 or y%400==0)
    if day>days[m-1]+int(leap):raise ValueError('Invalid day for Gregorian month')
    my=int((m-14)/12);iy=y+my
    # Remaining integer dividends are nonnegative within the source's domain.
    mjd=1461*(iy+4800)//4+367*(m-2-12*my)//12-3*((iy+4900)//100)//4+day-2432076
    return {'jd_part1':2400000.5,'jd_part2':float(mjd),'mjd':float(mjd),'jd':2400000.5+mjd}

if __name__=="__main__":
    raise SystemExit(cli(calculate))
