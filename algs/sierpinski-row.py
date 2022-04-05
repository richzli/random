def row(n):
    n += 1
    ans = ""
    i = 2**0
    for c in bin(n)[:1:-1]:
        if c == "1":
            if ans == "":
                ans = "1" * i
            else:
                ans = ans + "0" * (i - n % i) + ans
        i <<= 1
    print(ans)

if __name__ == "__main__":
    for i in range(64):
        row(i)
