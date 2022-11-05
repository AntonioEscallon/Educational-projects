def mod_exp(x,y,p):
    result =1 
    counter = 0 
    while (1<< counter) <= y:
        if(y & (1<<counter)) > 0:
            result = (result*x)%p
        x = (x*x)%p
        counter = counter + 1
    return result

result = mod_exp(3, 4, 19)

print(result)