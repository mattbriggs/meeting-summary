def add_zero(instring):
    if len(instring) == 1:
        outstring = "0" + instring
    else:
        outstring = instring
    return outstring


def clean_timestamp(intimestring):
    slots = intimestring.split(":")
    print(slots)
    newstring = add_zero(slots[0]) + ":" + add_zero(slots[1]) + ":" +  add_zero(slots[2])
    return newstring

print(clean_timestamp("0:1:18"))