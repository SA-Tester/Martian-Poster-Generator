# Source: http://www-mars.lmd.jussieu.fr/mars/time/martian_time.html

import math

def checkGivenYear(inputYear):
    # a year is leap if it is a multiple of 4 but not of 100, or if it is a multiple of 400 
    isLeapYear = 0
    
    if(((inputYear % 4)==0 and (inputYear % 100)!=0) or (inputYear % 400) == 0):
        isLeapYear = 1

    return isLeapYear

def convertToJulianDay(year, month, day, hour, minute, second):
    isLeapYear = checkGivenYear(year)
    ref_year = 1968
    ref_jdate = 2.4398565e6; # Julian date for 01/01/1968 00:00:00
    epoch_days = (0,31,59,90,120,151,181,212,243,273,304,334)
    ndays = 0 # number of days
    i = 0

    if(year > ref_year):
        for i in range(ref_year, year):
            ndays += 365

            if(((i % 4)==0 and (i % 100)!=0) or (i % 400)==0):
                ndays += 1
    else:
        for i in range(ref_year, year, -1):
            ndays -= 365

            if(((i % 4)==0 and (i % 100)!=0) or (i % 400)==0):
                ndays -= 1

    ndays = ndays + epoch_days[month-1]
    if(isLeapYear == 1 and month >= 3):
        ndays = ndays + 1

    jdate = ref_jdate + ndays + day
    jdate = ndays*1.0 + day*1.0 + ref_jdate-1.0 - 1.0

    #Adding Time to Julian Date
    jdate = jdate + hour/24 + minute/1440 + second/86400

    return jdate

def converEarthTimeToMartian(year, month, day, hour, minute, second):
    calculatedMartianData = [0,0,0,0] #year, month, ls, sol

    #Solar Longitudes and Sols
    jdate = 0.0
    sol = 0
    ls = 0.0
    martianYear = 0
    martianMonth = 0
    jdate_ref = 2.442765667e6; # 19/12/1975 4:00:00, such that Ls=0 (Begining of 12th Martian Year)
    martianYear_ref = 12
    secInEarthDay = 86400.0 # seconds
    secInMartianDay = 88775.245
    solsInMartianYear = 668.60 # no of sols in a martian year
    
    jdate = convertToJulianDay(year, month, day, hour, minute, second) # converting given date to julian date
    sol = (jdate - jdate_ref)*secInEarthDay/secInMartianDay # julian to sol
    martianYear = martianYear_ref
    
    # Calculate Martian Year Along with Sols
    while(sol >= solsInMartianYear):
        sol -= solsInMartianYear
        martianYear += 1
    
    while(sol < 0):
        sol += solsInMartianYear
        martianYear -= 1
    
    # convert sol number to Ls
    ls = solToLs(sol)

    martianMonth = 1 + math.floor(ls/30.0)
    calculatedMartianData[0] = martianYear
    calculatedMartianData[1] = martianMonth
    calculatedMartianData[2] = round(ls, 2)
    calculatedMartianData[3] = math.floor(sol)
    
    return calculatedMartianData

def solToLs(sol):
    ls = 0
    sols_per_year = 668.6
    perihelion_day = 485.35 
    orbital_eccentricity = 0.09340
    timeForPerihelion = 1.90258341759902 # 2*Pi*(1-Ls(perihelion)/360); Ls(perihelion)=250.99
    radToDeg = 180/math.pi
    
    zdx = 10
    zx0 = 0 # xref: mean anomaly, zx0: eccentric anomaly, zteta: true anomaly

    zz = (sol - perihelion_day)/sols_per_year
    zanom = 2.0*math.pi*(zz - round(zz))
    xref = abs(zanom)

    # Solve Kepler Equation
    zx0 = xref + orbital_eccentricity*math.sin(xref)
    while True:
        zdx = -(zx0-orbital_eccentricity*math.sin(zx0)-xref)/(1.-orbital_eccentricity*math.cos(zx0))
        zx0 += zdx
        if(zdx > 1.e-7):
            break
    
    if (zanom < 0):
        zx0 -= zx0

    zteta = 2*math.atan(math.sqrt((1.+orbital_eccentricity)/(1.-orbital_eccentricity))*math.tan(zx0/2.))

    # computer Ls
    ls = zteta - timeForPerihelion
    if(ls < 0):
        ls = ls+2*math.pi
    if(ls > 2*math.pi):
        ls = ls-2*math.pi

    # convert ls to degrees
    ls = radToDeg*ls

    return ls

#print(converEarthTimeToMartian(2022,9,16,12,54,19))