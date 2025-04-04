import bcrypt

def test_pass():
    return bcrypt.hashpw("some password".encode('utf-8'), bcrypt.gensalt())

# slow
result = [test_pass() for _ in range(1)]
print('result', result)

# # 10 times faster
# tasks = asyncio.gather(*[loop.run_in_executor(None, test_pass) for _ in range(100)])
# result = await tasks