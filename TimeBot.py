import time
import asyncio
from traceback import print_exc
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ONE_SEC = 1
ONE_MIN = 60 * ONE_SEC
ONE_HOUR = 60 * ONE_MIN
QQHOOKBOT_KEYS=[
	'<should be your qqhookbot key>',
	'<should be your qqhookbot key2 if need>',
	...
	]

async def tell_time(qqhookbot_key):
	time_ = time.strftime('uzilla为您报时：现在是北京时间%H点整~')
	request = Request(
		'https://app.qun.qq.com/cgi-bin/api/hookrobot_send?key=%s' % qqhookbot_key,
		data=('{"content":[{"type":0,"data":"%s"}]}' % time_).encode(),
		headers={'Content-Type': 'application/json'},
		method='POST')
	try:
		urlopen(request)
	except HTTPError as e:
		print_exc()
		print(e)

async def main():
	now = list(time.localtime())
	now[4] = 0  # Minute
	now[5] = 0  # Second
	next_time = time.mktime(
		time.struct_time(now)) + ONE_HOUR

	while True:
		if time.time() >= next_time:
			asyncio.ensure_future(
				asyncio.gather(
					*map(tell_time, QQHOOKBOT_KEYS)))
			next_time += ONE_HOUR
		await asyncio.sleep(20 * ONE_SEC)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())