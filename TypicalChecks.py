def password_check(password):
    if len(password) < 10:
        return False
    all_symb = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    test = 0
    nums = '0123456789'
    for el in password:
        if el in nums:
            test += 1
        if el in all_symb:
            test += 1
    if test >= 2:
        return True
    else:
        return False
