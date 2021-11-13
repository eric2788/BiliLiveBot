from plugin import BotPlugin, DanmakuMessage
from datetime import datetime

class TimeChecker(BotPlugin):
    async def on_command_received(self, cmd, data):
        if cmd != 'DANMU_MSG':
            return
        danmu = DanmakuMessage.from_command(data['info'])
        if danmu.msg != '!时间':
            return
        now = datetime.now()
        show = now.strftime('%Y{y}%m{m}%d{d}').format(y='年', m='月', d='日')
        await self.send_message(f'现在的时间为: {show}')