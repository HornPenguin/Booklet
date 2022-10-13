from datetime import datetime, tzinfo, timedelta
from typing import Union

def get_local_utc():
    dt = datetime.now() - datetime.utcnow()
    sec = dt.seconds
    hour = int(sec / 3600)
    min = int((sec % 3600)/60)
    return timedelta(hours = hour, minutes = min)

def parsing_pdf_time(pdf_time:str):
    if not isinstance(pdf_time, str):
        raise TypeError("Not a string")
    vaild = True
    vaild_command = ""
    if "D:" not in pdf_time:
        vaild = False
        vaild_command = "No \'D:\'"
        
    pdf_time = "D:"+pdf_time.split("D:")[1]
    length = len(pdf_time)

    if length !=23:
        if ("z" in pdf_time or "Z" in pdf_time) and length != 17:
            vaild = False
            vaild_command = "length is not 17 for UT time"
        elif ("+" in pdf_time or "-" in pdf_time) and length == 22:
            pdf_time = pdf_time + "'"
        else: 
            vaild = False
            vaild_command = "length is not 23 for UTC time"
    
    local_time = pdf_time[2:16]
    timezone = pdf_time[16:]

    # time zone 
    times_zone = timezone.split('\'')
    utc_symbol = times_zone[0][0]
    if utc_symbol not in ["+", "-", "z", "Z"]:
        vaild = False
        vaild_command = f"Invaild timezone symbol, {utc_symbol}"
    else:
        if length == 23:
            utc_h = int(times_zone[0][1:])
            utc_m = int(times_zone[1] )
        else: 
            utc_h = 0
            utc_m = 0
        if utc_symbol == "-":
            utc_h = -utc_h
            utc_m = -utc_m
    # Local time
    try:
        Year = int(local_time[0:4])
        Month = int(local_time[4:6])
        Day = int(local_time[6:8])
        Hour = int(local_time[8:10])
        Minute = int(local_time[10:12])
        Second = int(local_time[12:14])
    except:
        raise ValueError("Invaild date time")

    if not vaild:
        raise ValueError(f"Not a vaild time string, {vaild_command}, {pdf_time}")

    return datetime(Year, Month, Day, Hour, Minute, Second), timedelta(hours=utc_h, minutes = utc_m)

def pdf2local_time(pdf_time):
    date_time, utc = parsing_pdf_time(pdf_time)
    utc_time_of_file = date_time + utc
    local_utc = get_local_utc()
    local_time = utc_time_of_file - local_utc
    return local_time

def local2local2_time(time1, utc1, utc2):
    return time1 + utc1 -utc2

def datetime_to_pdf_time(dt:datetime, utc:Union[timedelta, None]=None):
    if utc is None:
        utc = get_local_utc()
    dt_string = dt.strftime(r"%Y%m%d%H%M%S")
    td = abs(utc)
    if td == timedelta(0):
        utc_string = "Z"  
    else:
        sign = "+" if td.days == 0 else "-"
        sec = abs(td).seconds
        minutes = int((sec%3600)/60)
        hours = int(sec/3600)
        utc_string = f"'{sign}{hours}'{minutes}"
    return f"D:{dt_string}{utc_string}"

def local_pdf_time_now():
    td = get_local_utc()
    if td == timedelta(0):
        utc_string = "Z"  
    else: 
        sign = "+" if td.days == 0 else "-"
        sec = abs(td).seconds
        minutes = int((sec%3600)/60)
        hours = int(sec/3600)
        utc_string = f"'{sign}{hours}'{minutes}"
    current = datetime.now().strftime(r"%Y%m%d%H%M%S")
    return f"D:{current}{utc_string}"


if __name__ == "__main__":
    print(local_pdf_time_now())
    print(len(local_pdf_time_now()))
    print(parsing_pdf_time(local_pdf_time_now()))