def summa(x,y):
    return x+y

def dif(x,y):
    return x-y

def mult(x,y):
    return x*y

def div(x,y):
    return x/y

def get_operation(x:float,oper:str,y:float):
    operations = {'+':summa,'-':dif,'*':mult,'/':div}
    return_oper = operations.get(oper)#получаем функцию , которая может принимать на вход числа и при вводе операции вычислять из них, то что имеется в словаре с др. вычислительными функциями
    # print(return_oper)
    if not return_oper:
        return 'у нас нет такой операции'
    return return_oper(x,y)
    
def calculate(new_exp:list):
    res = 0.0
    for op in '*/+-':  
        while op in new_exp:
            i = new_exp.index(op)
            res = get_operation(new_exp[i - 1], op,  new_exp[i + 1])#вычисляем считываемую по порядку операцию с числами, которе находятся перед и после операции
            new_exp = new_exp[:i - 1] + [res] + new_exp[i + 2:]#здесь остается список с еще "невычисленными" цифрами и операциями 
           
    return res

def get_expression(exp:str):
    res = []
    number = ""
    for s in exp:
        if s.isdigit() or s == '.':
            number += s#добавляем число в отдельную строку 
            
        else:
            if number:
                res.append(float(number))#добавляем полученное число в список с разбитыми частями выражения, если после итерации строка с числами не пустая
            number = ""#обнуляем строку , чтоб добавлять каждое число отдельно 
            res.append(s)#добавляем операцию отдельно
            
    else:
        if number:
            res.append(float(number))#собираем получившийся список из чисел и операций 
            
    return res