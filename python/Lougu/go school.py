s,v=map(int,input().split())
t=s/v+10
arrive_time=8*60
depart_time=arrive_time-t
if depart_time<0:
    depart_time+=24*60
h=int(depart_time//60)
m=int(depart_time%60)
print(f"{h:02d}:{m:02d}")