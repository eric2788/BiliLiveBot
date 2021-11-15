from plugin import BotPlugin, GiftMessage


class ThanksGift(BotPlugin):

    async def on_command_received(self, cmd, data):
        if cmd != 'SEND_GIFT':
            return

        gift = GiftMessage.from_command(data['data'])
        await self.send_message(f'感谢 {gift.uname} 送出的 {gift.gift_name} x{gift.num}')