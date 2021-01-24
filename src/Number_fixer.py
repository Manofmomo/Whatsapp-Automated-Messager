def phone_number_fixer(num):
    temp=str(num)
    if len(temp)==0:
        return None
    num=""
    Handle=True
    for i in temp:
        if ord(i)>47 and ord(i)<58:
            num=num+i
        if i=='+':
            Handle=False
        if i==':':
            break

    i=0
    if num[0]=='0':
        i=1
        num=num[1:-1]
    if num[i]=='9' or num[i]=='8' or num[i]=='7':

        if Handle:
            if len(num)==10 and num[0]!="1":
                num="91"+num
        print(temp," --->> ",num)
        return int(num)
    else:
        return None
