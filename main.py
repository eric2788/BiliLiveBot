import asyncio
from genericpath import exists
import logging
from aiohttp.client import ClientSession
import yaml, json
from bilibili_bot import BiliLiveBot
from plugins_loader import load_plugins
from bilibili_api import get_cookies, login, user_cookies

SESSION_DATA_PATH = 'data/session.json'

async def start_bot(room: int):
    cookies = {}
    # 有上次的 session
    session_exist = exists(SESSION_DATA_PATH)
    if session_exist:
        with open(SESSION_DATA_PATH) as f:
            cookies = json.load(f)
    # 加到 cookies
    user_cookies.update_cookies(cookies)
    async with ClientSession(cookie_jar=user_cookies) as session:
        # 嘗試登入
        success = await login(session)
        # 成功登入
        if success:

            uid = get_cookies('DedeUserID')
            jct = get_cookies('bili_jct')

            if uid == None or jct == None:
                logging.error(f'获取 cookies 失败')
                return
            if not session_exist:

                for cookie in user_cookies:
                    cookies[cookie.key] = cookie.value

                logging.debug(f'已储存 cookies: {cookies}')
                with open(SESSION_DATA_PATH, mode='w') as f:
                    json.dump(cookies, f)

            bot = BiliLiveBot(room_id=room, uid=int(uid), session=session, loop=session._loop)
            await bot.init_room()
            await bot.start()
            logging.info(f'機器人已啟動。')
            #while True:
            #    await asyncio.sleep(60)
            await bot.close()
            logging.info(f'機器人已關閉。')
        else:
            exit()




if __name__ == '__main__':

    with open('config/config.yaml') as f:
        data = yaml.safe_load(f)

    logging.basicConfig(level=logging.INFO if not data['debug'] else logging.DEBUG)
    room = data['roomid']

    BiliLiveBot.BOT_PLUGINS = load_plugins()
    asyncio.run(start_bot(room))


    

