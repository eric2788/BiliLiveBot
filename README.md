> [!IMPORTANT]
> 本项目目前因为B站直播改版已经作废，如果希望启动重写项目，可以[点击这里](https://github.com/eric2788/BiliLiveBot/discussions/6)

---

## BiliLiveBot

可插件化管理的B站直播间机器人

目前机器人可以执行
- 发送弹幕
- 禁言用户 (需要房管权限)
- 全局禁言 (需要房管权限)
- 新增屏蔽字 (需要房管权限)
- 删除屏蔽字 (需要房管权限)


__WebSocket 库:  [xfgryujk/blivedm](https://github.com/xfgryujk/blivedm)__


### 运行

目前有三种方式运行

#### 1. 直接使用 python 指令运行
此运行方式将包含范例插件在内

1. 建置 python 環境
2. 下載源碼
3. 輸入 python main.py 運行

#### 2. 到 releases 下载 exe 运行
此运行方式无需要python环境

1. 到 releases 下载最新版zip
2. 提取你的环境的档案 (.exe 为 windows, binary 为 linux)
3. 打开程序直接运行

#### 3. 使用 Docker 运行
此运行方式需要熟悉Docker环境

1. 下载源码
2. 使用 docker build 建置 image
3. 使用 docker run 运行

你可能需要预先扫描二维码並复制 data/session.json 以略过在 docker container 内扫描

### 新增插件

插件需要放在 ``plugins/`` 文件夹底下

#### 步骤
1. 在 ``plugins/`` 文件夹下新增一个新的 ``.py`` 档案
2. 在 py 档案中，新增一个 class 並继承 ``plugins.BotPlugin``
3. 在 class 中实作 ``async def on_command_received(self, cmd, data) `` 方法
4. 完成，使用 ``python main.py`` 指令运行程序

__如需要使用设定, 可调用 ``plugins.load_config(yml, 默認設定)`` 来获取 在 config 目录下的 yaml 设定__

#### 范例

以下所有范例档案均在 ``plugins/`` 文件夹底下。

1# 透过關鍵字触发时间显示

```py
# plugins/time.py
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
```

2# 从 yaml 设定提取禁言弹幕列表 (需要有房管权限)

```yaml
# config/mute.yml
bad_danmaku:
  - '主播是个大伞兵'
  - '主播你寄吧谁啊'
  - '主播NMSL'
```

```py
# plugins/mute.py
from plugin import BotPlugin, DanmakuMessage, load_config

# 默認設定
DEFAULT_CONTENT = {
    'bad_danmaku': [
        '主播是个大伞兵',
        '主播你寄吧谁啊',
        '主播NMSL'
    ]
}


class MuteUser(BotPlugin):

    def __init__(self) -> None:
        super().__init__()
        # 使用 load_config 从 config/ 目录加载 mute.yml
        # 如果 找不到 mute.yml 則使用 默認設定 生成一個 yml 並保存
        data = load_config('mute.yml', DEFAULT_CONTENT) 
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
```

3# 感谢礼物

```py
# plugins/thanks_gift.py
class ThanksGift(BotPlugin):

    async def on_command_received(self, cmd, data):
        if cmd != 'SEND_GIFT':
            return

        gift = GiftMessage.from_command(data['data'])
        await self.send_message(f'感谢 {gift.uname} 送出的 {gift.gift_name} x{gift.num}')
```

### 参考

```py
class BotPlugin:

    def __init__(self) -> None:
        self.botid = -1 # bot 的 uid, 可以在收到指令时使用

    """
    收到指令时
    """
    @abstractmethod
    async def on_command_received(self, cmd, data):
        pass

    """
    收到人气时
    """
    @abstractmethod
    async def on_receive_popularity(self, popularity: int):
        pass

    """
    发送弹幕
    """
    async def send_message(self,
                        danmaku: str, 
                        fontsize: int = 25, 
                        color: int = 0xffffff, 
                        pos: DanmakuPosition = DanmakuPosition.NORMAL
                    ) -> bool:
        pass

    """
    以下所有操作全部需要房管权限

    """
    """
    禁言用户
    """
    async def mute_user(self, uid: int) -> bool:
        pass

    """
    全局禁言
    """
    # "level" | "medal" | "member"
    async def room_slient_on(self, slientType: str, minute: int, level: int) -> bool:
        pass

    """
    全局禁言关闭
    """
    async def room_slient_off(self) -> bool:
        pass

    """
    新增屏蔽字
    """
    async def add_badword(self, badword: str) -> bool:
        pass

    """
    删除屏蔽字
    """
    async def remove_badword(self, badword: str) -> bool:
        pass
```

除此之外，你也可以使用 [xfgryujk/blivedm](https://github.com/xfgryujk/blivedm) 的 API来让WS数据物件化:

```py
async def on_command_received(self, cmd, command):
    if cmd == 'DANMU_MSG': # 弹幕数据物件化
        DanmakuMessage.from_command(command['info'])
    elif cmd == 'SEND_GIFT': # 礼物数据物件化
        GiftMessage.from_command(command['data'])
    elif cmd == 'GUARD_BUY': # 舰长数据物件化
        GuardBuyMessage.from_command(command['data'])
    elif cmd == 'SUPER_CHAT_MESSAGE': # SC数据物件化
        SuperChatMessage.from_command(command['data'])
    elif cmd == 'SUPER_CHAT_MESSAGE_DELETE': # SC删除数据物件化
        SuperChatDeleteMessage.from_command(command['data'])
```

[__视频演示__](https://www.bilibili.com/video/BV1LT4y1R7Xk)

### 鸣谢

- [blivedm](https://github.com/xfgryujk/blivedm)
- [bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)
