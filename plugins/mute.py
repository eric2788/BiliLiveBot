from plugin import BotPlugin, DanmakuMessage, load_config

class MuteUser(BotPlugin):

    def __init__(self) -> None:
        super().__init__()
        data = load_config('mute.yml')
        self.bad_danmaku = data['bad_danmaku'] if data != None else []
        print(f'禁言弹幕: {self.bad_danmaku}')

    async def on_command_received(self, cmd, data):
        if cmd != 'DANMU_MSG':
            return
        danmu = DanmakuMessage.from_command(data['info'])
        if danmu.msg not in self.bad_danmaku:
            return
        uid = danmu.uid
        # 需要管理员权限进行禁言
        if await self.mute_user(uid):
            await self.send_message(f'{danmu.uname}, 你已被禁言!')
        else:
            print('禁言失败，可能没有权限')