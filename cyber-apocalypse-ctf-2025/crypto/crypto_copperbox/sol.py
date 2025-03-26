h1_msb = 77759147870011250959067600299812670660963056658309113392093130
h2_msb = 50608194198883881938583003429122755064581079722494357415324546
p = 0x31337313373133731337313373133731337313373133731337313373133732ad
a = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
b = 0xdeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0dedeadc0de

R.<h1_lsb, h2_lsb, x> = PolynomialRing(GF(p)); x0 = x
l1, l2, l3, l4 = [x := a*x + b for _ in range(4)]
f1 = l2 * (h1_msb * 2**48 + h1_lsb) - l1
f2 = l4 * (h2_msb * 2**48 + h2_lsb) - l3
f3 = f1.sylvester_matrix(f2, x0).determinant() 

M = block_matrix(ZZ, [[Matrix(f3.coefficients()).T, 1], [p, 0]])
W = diagonal_matrix([1, 2**-96, 2**-48, 2**-48, 1])
h1_lsb_ = -int(((M*W).LLL()/W)[0, 2])
x = f1.subs(h1_lsb=h1_lsb_).univariate_polynomial().roots()[0][0]
print(bytes.fromhex(f'{int(x):x}')) 
# HTB{sm1th1ng_mY_c0pp3r_fl4G}

