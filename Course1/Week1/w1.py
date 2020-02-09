class Number:
    def __init__(self, data, negative):
        self.data = data
        self.negative = negative


def basic_multi(aa: Number, bb: Number) -> Number:
    res = []
    add = 0
    for i in range(len(aa.data)-1, -1, -1):
        product = aa.data[i]*bb.data[0]
        res.insert(0, (add+product) % 10)
        add = int((add + product) / 10)
    if add > 0:
        res.insert(0, add)

    r = Number([], False)
    r.data = res
    if aa.negative and bb.negative:
        r.negative = False
    if not aa.negative and not bb.negative:
        r.negative = False
    if aa.negative and not bb.negative:
        r.negative = True
    if not aa.negative and bb.negative:
        r.negative = True
    return r


def basic_add(aa: Number, bb: Number) -> Number:
    a = Number([], False)
    b = Number([], False)
    if aa.negative and bb.negative:
        a.data = aa.data[:]
        b.data = bb.data[:]
        a.negative = False
        b.negative = False
        tmp = basic_add(a, b)
        tmp.negative = True
        return tmp

    if aa.negative and not bb.negative:
        return basic_sub(bb, aa)

    if not aa.negative and bb.negative:
        return basic_sub(aa, bb)

    res = []
    a = aa.data[:]
    b = bb.data[:]
    if len(a) < len(b):
        while len(a) != len(b):
            a.insert(0, 0)
    if len(b) < len(a):
        while len(a) != len(b):
            b.insert(0, 0)

    add = 0
    for i in range(len(a)-1, -1, -1):
        sum = a[i] + b[i]
        res.insert(0, (sum + add) % 10)
        add = int((sum + add)/10)
    if add > 0:
        res.insert(0, add)
    r = Number([], False)
    r.data = res
    r.negative = False
    return r


def basic_sub(aa: Number, bb: Number) -> Number:
    res = []
    a = aa.data[:]
    b = bb.data[:]
    if len(a) < len(b):
        while len(a) != len(b):
            a.insert(0, 0)
    if len(b) < len(a):
        while len(a) != len(b):
            b.insert(0, 0)
    sub = 0
    for i in range(len(a)-1, -1, -1):
        sum = a[i] - b[i] - sub
        if sum < 0:
            sum += 10
            sub = 1
        else:
            sub = 0
        res.insert(0, sum)
    if sub == 1:
        hehe = basic_sub(bb, aa)   # some ugly code
        hehe.negative = True
        return hehe
    while res[0] == 0:
        res = res[1:]
        if len(res) == 0:
            return Number([0], False)

    r = Number([], False)
    r.data = res
    r.negative = False
    return r


def karatsuba(x: Number, y: Number) -> Number:
    if len(x.data) == 1:
        return basic_multi(y, x)
    if len(y.data) == 1:
        return basic_multi(x, y)
    while len(x.data) > len(y.data):
        y.data.insert(0, 0)
    while len(x.data) < len(y.data):
        x.data.insert(0, 0)

    a = Number(x.data[:int(len(x.data)/2)], False)
    b = Number(x.data[int(len(x.data)/2):], False)
    c = Number(y.data[:int(len(y.data)/2)], False)
    d = Number(y.data[int(len(y.data)/2):], False)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ab = basic_add(a, b)
    cd = basic_add(c, d)
    abcd = karatsuba(ab, cd)
    tmp = basic_sub(basic_sub(abcd, bd), ac)
    for i in range(0, len(b.data) + len(d.data)):
        ac.data.append(0)
    for i in range(0, len(d.data)):
        tmp.data.append(0)
    return basic_add(basic_add(tmp, ac), bd)


def main():
    a_str = '3141592653589793238462643383279502884197169399375105820974944592'
    b_str = '2718281828459045235360287471352662497757247093699959574966967627'
    a_list = []
    b_list = []
    for index in range(0, len(a_str)):
        a_list.append(ord(a_str[index])-ord('0'))

    for index in range(0, len(b_str)):
        b_list.append(ord(b_str[index])-ord('0'))

    result = karatsuba(Number(a_list, False), Number(b_list, False))
    while result.data[0] == 0:
        result.data = result.data[1:]
    for i in range(0, len(result.data)):
        print(result.data[i], end='')


if __name__ == "__main__":
    main()
