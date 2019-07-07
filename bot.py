import csv
import discord
import re

from settings import SECRET_TOKEN


client = discord.Client()


class KarinClient(discord.Client):
    def __init__(self):
        super().__init__()
        self.mana = []
        with open('./data/mana.csv') as mana_csv:
            reader = csv.DictReader(mana_csv)
            for idx, row in enumerate(reader):
                assert int(row['level']) == idx + 1
                self.mana.append(int(row['mana_required']))
        self.char_exp = []
        with open('./data/char_exp.csv') as char_csv:
            reader = csv.DictReader(char_csv)
            for idx, row in enumerate(reader):
                assert int(row['level']) == idx + 1
                self.char_exp.append(int(row['exp_required']))
        self.player_exp = []
        with open('./data/player_exp.csv') as player_csv:
            reader = csv.DictReader(player_csv)
            for idx, row in enumerate(reader):
                assert int(row['level']) == idx + 1
                self.player_exp.append(int(row['exp_required']))

        self.mana_regex = re.compile(r'!카린 +마나 +(?P<from>\d+) *(->)? *(?P<to>\d+) *((?P<count>\d+)명)?')
        self.char_exp_regex = re.compile(r'!카린 +경험치 +(?P<from>\d+) *(->)? *(?P<to>\d+) *((?P<count>\d+)명)?')

    async def on_ready(self):
        print('Logged in as : {} ({})'.format(self.user.name, self.user.id))

    async def on_message(self, message):
        if message.content.startswith('!카린'):
            mana_pattern = self.mana_regex.fullmatch(message.content)
            char_exp_pattern = self.char_exp_regex.fullmatch(message.content)

            if mana_pattern:
                from_lv = int(mana_pattern['from'])
                to_lv = int(mana_pattern['to'])
                count = 1 if mana_pattern['count'] is None else int(mana_pattern['count'])
                if count == 1:
                    await message.channel.send('Lv {} 에서 Lv {} 까지 필요한 총 마나는 **{:,}** 입니다'.format(
                        from_lv, to_lv, sum(self.mana[from_lv - 1:to_lv - 1] * 4)))
                else:
                    await message.channel.send('Lv {} 에서 Lv {} 까지 {}명에게 필요한 총 마나는 **{:,}** 입니다'.format(
                        from_lv, to_lv, count, count * sum(self.mana[from_lv - 1:to_lv - 1] * 4)))
            elif char_exp_pattern:
                from_lv = int(char_exp_pattern['from'])
                to_lv = int(char_exp_pattern['to'])
                count = 1 if char_exp_pattern['count'] is None else int(char_exp_pattern['count'])

                required = sum(self.char_exp[from_lv - 1:to_lv - 1]) * count
                if count == 1:
                    await message.channel.send(('Lv {} 에서 Lv {} 까지 필요한 총 경험치는 {:,} 로,\n'
                                                '메가 포션 **{:.2f}**개 또는 하이 포션 **{:.2f}**개가 필요합니다.').format(
                        from_lv, to_lv, required, required / 7500, required / 1500))
                else:
                    await message.channel.send(('Lv {} 에서 Lv {} 까지 {}명에게 필요한 총 경험치는 {:,} 로,\n'
                                                '메가 포션 **{:.2f}**개 또는 하이 포션 **{:.2f}**개가 필요합니다.').format(
                        from_lv, to_lv, count, required, required / 7500, required / 1500))


if __name__ == '__main__':
    client = KarinClient()
    client.run(SECRET_TOKEN)
