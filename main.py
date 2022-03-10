import os
import discord

from bsedata.bse import BSE
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
TOKEN = dict(os.environ)


@client.event
async def on_ready():
    print('Logged in')


@client.event
async def on_message(message):
    b = BSE()
    c = b.getScripCodes()
    if message.author == client.user:
        return

    if message.content.lower() == '$help':
        await message.channel.send(
            'Use $topgainers and $toplosers to respectively find Top 5 Gaining companies and top 5 losing '
            'companies\n\n '
            'Use $search <company-name> to get all the information about the company\n\n Use $month <company-name> to '
            'get the stock price of the previous 30 days of the company')

    if message.content.lower() == '$topgainers':
        for item in b.topGainers():
            code = item['scripCode']
            if c.get(code) is not None:
                await message.channel.send(
                    'Name : ' + c[code] + '\nLast Traded Price : ' + item['LTP'] + '\nChange % : ' + item[
                        'pChange'] + '\n')

    if message.content.lower() == '$toplosers':
        for item in b.topLosers():
            code = item['scripCode']
            if c.get(code) is not None:
                await message.channel.send(
                    'Name : ' + c[code] + '\nLast Traded Price : ' + item['LTP'] + '\nChange % : ' + item[
                        'pChange'] + '\n')

    if message.content.startswith('$search'):
        msg = str(message.content[8:])
        key_list = list(c.keys())
        val_list = list(c.values())
        pos = val_list.index(msg)
        key = key_list[pos]
        ans = b.getQuote(key)
        await message.channel.send('Company Name : ' +
                                   ans['companyName'] + '\n' + 'Current Value : ' + ans[
                                       'currentValue'] + '\n' + 'Change : ' + ans['change'] + '\n' + 'Change % : ' +
                                   ans['pChange'] + '\n' + 'Day High :' + ans['dayHigh'] + '\n' + 'Day Low :' + ans[
                                       'dayLow'] + '\n' + '52 week High :' + ans[
                                       '52weekHigh'] + '\n' + '52 week Low :' + ans['52weekLow'] + '\n')

    if message.content.startswith('$month'):
        msg = str(message.content[7:])
        key_list = list(c.keys())
        val_list = list(c.values())
        pos = val_list.index(msg)
        key = key_list[pos]
        monthlytrend = b.getPeriodTrend(key, '1M')
        ans = ''
        for item in monthlytrend:
            ans = ans + ('Date : ' + item['date'] +
                         ', Value : ' + str(item['value']) + '\n')
        await message.channel.send(ans)

client.run(TOKEN['TK'])
