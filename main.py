import discord
import os
from keep_alive import keep_alive
import sys
import json
from discord.ext.commands import command, cooldown
from io import StringIO
import contextlib, random, time

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old
client = discord.Client()
@client.event
async def on_ready():
    print("I'm in")
@cooldown(1, 1, discord.ext.commands.BucketType.user)
@client.event
async def on_message(message):
  if message.author != client.user:
    if message.content == "f!help":
      await message.channel.send(f'''**----遊戲列表----**
       前綴：`f!`
       查看排名：`f!rank`
       如果你沒有帳戶，要開始遊戲：`f!str`
       攻擊：`f!attack`
       尋找更多士兵：`f!look`
       訓練軍隊：`f!train`
       攻擊他人：`f!attack_other（用戶名）`
       領取每小時獎勵：`f!hourly`
       領取每日獎勵：`f!daily`
      ''')
    elif message.content == "f!str":
      if os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，您已經有一個帳戶 {message.author}!")
      else:
        with open(str(message.author) + ".json", "w") as x:
          start_dict = {"name": str(message.author), "money": 100, "army": 10, "level": 1, "xp": 0, "attack_force": 20, "defend_force": 20, "xp_on_this": 50, "Silver Swords": 0, "Golden Swords": 0, "Diamond Swords": 0, "Next Daily": time.time(), "Next Hourly": time.time()}
          json.dump(start_dict, x)
        await message.channel.send(f''' 你的帳戶已創建，{message.author}。 你的統計數據是：
         用戶名：`{start_dict["name"]}`
         級別：`{start_dict["level"]}`
         XP：`{start_dict["xp"]}`
         升級所需的 XP：`{start_dict["xp_on_this"]}`
         軍隊：`{start_dict["army"]}`
         陸軍攻擊力：`{start_dict["attack_force"]}`
         陸軍國防軍：`{start_dict["defend_force"]}`
         銀劍：`{start_dict["Silver Swords"]}`
         金劍：`{start_dict["Golden Swords"]}`
         鑽石劍：`{start_dict["Diamond Swords"]}`''')
    elif message.content == "f!rank":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，{message.author}，你沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      else:
        with open(f"{message.author}.json", "r") as f:
          stats = json.load(f)
        await message.channel.send(f'''**---- 📈統計📉 ----**
         用戶名：`{stats["name"]}`
         級別：`{stats["level"]}`
         XP：`{stats["xp"]}`
         升級所需的 XP：`{stats["xp_on_this"]}`
         軍隊：`{stats["army"]}`
         陸軍攻擊力：`{stats["attack_force"]}`
         陸軍國防軍：`{stats["defend_force"]}`
         錢：`{stats["money"]}`
         銀劍：`{stats["Silver Swords"]}`
         金劍：`{stats["Golden Swords"]}`
         鑽石劍：`{stats["Diamond Swords"]}`''')

    elif message.content[ : 5] == "f!rank":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，{message.author}，您沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!gamehelp` 來查看幫助指南。")
      elif not os.path.exists(f"{message.content[6: ]}.json"):
        await message.channel.send(f"抱歉，{message.author}，找不到這用戶名的帳戶。")
      else:
        with open(f"{message.content[6: ]}.json", "r") as f:
          stats = json.load(f)
        await message.channel.send(f'''**---- 📈統計📉 ----**
         用戶名：`{stats["name"]}`
         級別：`{stats["level"]}`
         XP：`{stats["xp"]}`
         升級所需的 XP：`{stats["xp_on_this"]}`
         軍隊：`{stats["army"]}`
         陸軍攻擊力：`{stats["attack_force"]}`
         陸軍國防軍：`{stats["defend_force"]}`
         錢：`{stats["money"]}`
         銀劍：`{stats["Silver Swords"]}`
         金劍：`{stats["Golden Swords"]}`
         鑽石劍：`{stats["Diamond Swords"]} `''')
    elif message.content == "f!train":
      if os.path.exists(f"{message.author}.json"):
        with open(f"{message.author}.json", "r") as dat:
          data = json.load(dat)
        defense_plus = random.randint(1, 10) * data['level']
        attack_plus = random.randint(1, 10) * data['level']
        xp_plus = random.randint(1, 5)
        await message.channel.send("訓練軍隊...")
        time.sleep(2)
        data['defend_force'] += defense_plus
        data['attack_force'] += attack_plus
        data['xp'] += xp_plus
        if data['xp'] >= data['xp_on_this']:
          await message.channel.send(f"{message.author}，你剛剛升級!!! ")
          data['xp'] = data['xp'] - data['xp_on_this']
          data['level'] += 1
          data['money'] += random.randint(1, 100)
          data['xp_on_this'] = data['xp_on_this'] * 2
        with open(f"{message.author}.json", "w") as fil:
          json.dump(data, fil)
        await message.channel.send(f'''**---- 軍隊訓練----**
         陸軍國防軍獲得：`{defense_plus}`
         獲得陸軍攻擊力：`{attack_plus}`
         獲得的經驗值：`{xp_plus}`''')
        


      else:
        await message.channel.send(f"⚠️抱歉，{message.author}，你還沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
    elif message.content == "f!look":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"⚠️抱歉，{message.author}，你還沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      else:
        with open(f"{message.author}.json", "r") as s:
          dat = json.load(s)
        army_up = random.randint(1, dat['level'] * 5)
        xp_plus = random.randint(1, 4)
        await message.channel.send("🔍尋找志願者...")
        time.sleep(2)
        dat['army'] += army_up
        dat['xp'] += xp_plus 
        if dat['xp'] >= dat['xp_on_this']:
          await message.channel.send(f"{message.author}，你剛剛升級!!!")
          dat['xp'] = data['xp'] - dat['xp_on_this']
          dat['level'] += 1
          dat['money'] += random.randint(1, 100)
          dat['xp_on_this'] = dat['xp_on_this'] * 2
        with open(f"{message.author}.json", "w") as fil:
          json.dump(dat, fil)
        await message.channel.send(f'''**---- 💼找到志願者 ----**
       志願者人數：{army_up}
         獲得的 XP：{xp_plus}''')

    elif message.content == "f!attack":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"⚠️抱歉，{message.author}，你還沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      else:
        with open(f"{message.author}.json", "r") as s1:
          player_stats = json.load(s1)
        player_full_force = player_stats['attack_force'] * player_stats['defend_force'] * player_stats['level'] * player_stats['army'] * 1.2
        enemy_attack_force = random.randint(player_stats['attack_force'] - 10, player_stats['attack_force'] + 10)
        enemy_defend_force = random.randint(player_stats['defend_force'] - 10, player_stats['defend_force'] + 10)
        enemy_army = random.randint(player_stats['army'] - 10, player_stats['army'] + 10)
        if player_stats['level'] == 1:
          enemy_level = 1
        else:
          enemy_level = random.randint(player_stats['level'] - 1, player_stats['level'] + 1)
        enemy_full_force = enemy_attack_force * enemy_defend_force * enemy_level * enemy_army
        await message.channel.send(f'''**---- 📃戰斗數據📃----**
         你的等級：`{player_stats["level"]}`
         你的軍隊：`{player_stats['army']}`
         你的攻擊力：`{player_stats['attack_force']}`
         你的防守力量：`{player_stats['defend_force']}`
         --------------------------------------------------
         敵人等級：`{enemy_level}`
         敵軍：`{enemy_army}`
         敵人攻擊力：`{enemy_attack_force}`
         敵人防禦力量：`{enemy_defend_force}`
        
        *戰鬥...**
        ''')
        time.sleep(2)
        if enemy_full_force  <= player_full_force:
          xp_plus = random.randint(1, 15) * player_stats['level']
          army_plus = random.randint(1, 10) * player_stats['level']
          player_stats['xp'] += xp_plus
          player_stats['army'] += army_plus
          if player_stats['xp'] >= player_stats['xp_on_this']:
            player_stats['xp'] = player_stats['xp'] - player_stats['xp_on_this']
            player_stats['level'] += 1
            player_stats['money'] += random.randint(1, 100)
            player_stats['xp_on_this'] = player_stats['xp_on_this'] * 2
            await message.channel.send(f"{message.author}，你剛剛升級!!!")
          with open(f"{message.author}.json", "w") as f:
            json.dump(player_stats, f)
          await message.channel.send(f'''**---- 勝利----**
           獲得軍隊：`{army_plus}`
           XP獲得：`{xp_plus}`''')
        else:
          army_minus = random.randint(1, 10) * player_stats['level']
          if army_minus < player_stats['army']:
            player_stats['army'] -= army_minus
            with open(f"{message.author}.json", "w") as xl:
              json.dump(player_stats, xl)
            await message.channel.send(f'''** ---失敗--- **
             軍隊損失：`{army_minus}`
             獲得的 XP：`0`''')
          else:
             await message.channel.send(f'''** ---失敗--- **
             軍隊損失：`0`
             獲得的 XP：`0`''')
    elif message.content[ :13] == "f!attack_other":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，{message.author}，你沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      else:
        enemy = message.content[ 14: ]
        if not os.path.exists(f"{enemy}.json"):
          await message.channel.send(f"哦不!{enemy} 帳戶似乎不存在...")
        else:
          with open(f"{message.author}.json", "r") as s1:
            player_stats = json.load(s1)
          with open(f"{enemy}.json") as s2:
            enemy_stats = json.load(s2)
          player_full_force = player_stats['attack_force'] * player_stats['defend_force'] * player_stats['level'] * player_stats['army']
          enemy_attack_force = enemy_stats['attack_force']
          enemy_defend_force = enemy_stats['defend_force']
          enemy_army = enemy_stats['army']
          enemy_level = enemy_stats['level']
          enemy_full_force = enemy_attack_force * enemy_defend_force * enemy_level * enemy_army
          await message.channel.send(f'''**---- 戰鬥統計----**
           你的等級：`{player_stats["level"]}`
           你的軍隊：`{player_stats['army']}`
           你的攻擊力：`{player_stats['attack_force']}`
           你的防守力量：`{player_stats['defend_force']}`
           --------------------------------------------------
           敵人等級：`{enemy_level}`
           敵軍：`{enemy_army}`
           敵人攻擊力：`{enemy_attack_force}`
           敵人防禦力量：`{enemy_defend_force}`
          
          **戰鬥...**
          ''')
          time.sleep(2)
          if enemy_full_force <= player_full_force:
            xp_plus = random.randint(1, 15) * player_stats['level']
            army_plus = random.randint(1, 10) * player_stats['level']
            player_stats['xp'] += xp_plus
            player_stats['army'] += army_plus
            if player_stats['xp'] >= player_stats['xp_on_this']:
              player_stats['xp'] = player_stats['xp'] - player_stats['xp_on_this']
              player_stats['level'] += 1
              player_stats['money'] += random.randint(1, 100)
              player_stats['xp_on_this'] = player_stats['xp_on_this'] * 2
              await message.channel.send(f"{message.author}，你剛剛升級!!!")
            if army_plus <= enemy_stats['army']:
              enemy_stats['army'] -= army_plus
            with open(f"{message.author}.json", "w") as f:
              json.dump(player_stats, f)
            with open(f"{enemy}.json", "w") as f2:
              json.dump(enemy_stats, f2)
            await message.channel.send(f'''**---- 勝利----**
             獲得軍隊：`{army_plus}`
             XP獲得：`{xp_plus}`''')
          else:
            army_minus = random.randint(1, 10) * player_stats['level']
            if army_minus < player_stats['army']:
              player_stats['army'] -= army_minus
              enemy_stats['army'] += army_minus
              with open(f"{message.author}.json", "w") as xl:
                json.dump(player_stats, xl)
              with open(f"{enemy}.json", "w") as xl2:
                json.dump(enemy_stats, xl2)
              await message.channel.send(f'''** ---失敗--- **
             軍隊損失：`{army_minus}`
             獲得的 XP：`0`''')
            else:
              await message.channel.send(f'''** ---失敗--- **
             軍隊損失：`0`
             獲得的 XP：`0`''')

  
    elif message.content == "f!daily":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，{message.author}，你沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      
      else:
        with open(f"{message.author}.json", "r") as IDK:
          stuf = IDK.read()
        idk = json.loads(stuf)
        if idk["Next Daily"] > time.time():
          await message.channel.send("您需要等待24 小時才能再次使用 f!Daily 並且距離你上次使用 f!Daily 還沒有過去 24 小時")

        
        else:
          await message.channel.send(".")
          time.sleep(1)
          if os.path.exists(f"Upgrades/{message.author}.json"):
            with open(f"Upgrades/{message.author}.json") as upgs:
              upgs2 = json.load(upgs)
            if upgs2['Better Dailies'] == True:
              multi = random.randint(2, 8)
              Luck = random.randint(1, 250)
            else:
              multi = 1
              Luck = 1
          else:
            multi = 1
            Luck = 1
          reward = random.randint(Luck, 1000)
          if reward <= 900:
            await message.channel.send("請稍等...")
            XP = random.randint(1, 50) * multi
            time.sleep(1)
            await message.channel.send(f'''**---- 每天獎勵----**
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as Daily:
              stuff = Daily.read()
            daily = json.loads(stuff)
            daily["Next Daily"] = time.time() + 86400
            daily["xp"] += XP
            if daily["xp"] >= daily["xp_on_this"]:
              daily["xp"] = 0
              daily["level"] += 1
              daily['xp_on_this'] = daily['xp_on_this'] * 2
              daily["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}，你剛剛升級！！!")
            with open(f"{message.author}.json", "w") as dump:
              json.dump(daily, dump)
        
          if reward <= 950 and reward > 900:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 75) * multi
            Money = random.randint(1, 25) * multi
            await message.channel.send(f'''**---- 每天獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as Daily:
              stuff = Daily.read()
            daily = json.loads(stuff)
            daily["Next Daily"] = time.time() + 86400
            daily["xp"] += XP
            if daily["xp"] >= daily["xp_on_this"]:
              daily["xp"] = 0
              daily["level"] += 1
              daily['xp_on_this'] = daily['xp_on_this'] * 2
              daily["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}，你剛剛升級！！!")
            daily["money"] += Money
            with open(f"{message.author}.json", "w") as dump:
              json.dump(daily, dump)
          
          if reward <= 995 and reward > 950:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 250) * multi
            Money = random.randint(1, 150) * multi
            await message.channel.send(f'''**---- 每天獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as Daily:
              stuff = Daily.read()
            daily = json.loads(stuff)
            
            daily["Next Daily"] = time.time() + 86400
            daily["xp"] += XP
            if daily["xp"] >= daily["xp_on_this"]:
              daily["xp"] = 0
              daily["level"] += 1
              daily['xp_on_this'] = daily['xp_on_this'] * 2
              daily["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}，你剛剛升級！！!")
            daily["money"] += Money
            with open(f"{message.author}.json", "w") as dump:
              json.dump(daily, dump)
          
          if reward <= 1000 and reward > 995:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 1000) * multi
            Money = random.randint(1, 750) * multi
            await message.channel.send(f'''**---- 獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as Daily:
              stuff = Daily.read()
            daily = json.loads(stuff)
            daily["Next Daily"] = time.time() + 86400
            daily["xp"] += XP
            if daily["xp"] >= daily["xp_on_this"]:
              daily["xp"] = 0
              daily["level"] += 1
              daily['xp_on_this'] = daily['xp_on_this'] * 2
              daily["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}，你剛剛升級！！")
            daily["money"] += Money
            with open(f"{message.author}.json", "w") as dump:
              json.dump(daily, dump)
#Silver Swords Golden Swords Diamond Swords

    elif message.content == "f!hourly":
      if not os.path.exists(f"{message.author}.json"):
        await message.channel.send(f"抱歉，{message.author}，你沒有帳戶。 輸入 `f!str` 來創建一個，輸入 `f!help` 來查看幫助指南。")
      
      else:
        with open(f"{message.author}.json", "r") as IDK:
          stuf = IDK.read()
        idk = json.loads(stuf)
        if idk["Next Hourly"] > time.time():
          await message.channel.send("你需要等待1 小時才能再次使用 f!Hourly 並且自上次使用 f!Hourly 以來還沒有過去 1 小時")

        
        else:
          await message.channel.send("請稍等...")
          time.sleep(1)
          if os.path.exists(f"Upgrades/{message.author}.json"):
            with open(f"Upgrades/{message.author}.json") as upgs:
              upgs2 = json.load(upgs)
            if upgs2['Better Hourlies'] == True:
              multi = random.randint(2, 8)
              Luck = random.randint(1, 2500)
            else:
              multi = 1
              Luck = 1
          else:
            multi = 1
            Luck = 1
          reward = random.randint(Luck, 10000)
          if reward <= 9900:
            await message.channel.send("")
            XP = random.randint(1, 25) * multi
            time.sleep(1)
            await message.channel.send(f'''**---- 獎勵----**
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as dad: 
              stuf = dad.read()
            idk = json.loads(stuf)
            idk["Next Hourly"] = time.time() + 3600
            idk["xp"] += XP
            if idk["xp"] >= idk["xp_on_this"]:
              idk["xp"] = 0
              idk["level"] += 1
              idk['xp_on_this'] = idk['xp_on_this'] * 2
              idk["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}，你剛剛升級！！")
            with open(f"{message.author}.json", "w") as dum:
              json.dump(idk, dum)
        
          if reward <= 99750 and reward > 99000:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 50) * multi
            Money = random.randint(1, 15) * multi
            await message.channel.send(f'''**---- 獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as mom:
              stu = mom.read()
            idk = json.loads(stu)
            idk["Next Hourly"] = time.time() + 3600
            idk["xp"] += XP
            if idk["xp"] >= idk["xp_on_this"]:
              idk["xp"] = 0
              idk["level"] += 1
              idk["money"] += random.randint(1, 100)
              idk['xp_on_this'] = idk['xp_on_this'] * 2
              await message.channel.send(f"{message.author}，你剛剛升級！！")
            idk["money"] += Money
            with open(f"{message.author}.json", "w") as du:
              json.dump(idk, du)
          
          if reward <= 99950 and reward > 99750:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 150) * multi
            Money = random.randint(1, 75) * multi
            await message.channel.send(f'''**---- 獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as son:
              st = son.read()
            idk = json.loads(st)
            idk["Next Hourly"] = time.time() + 3600
            idk["xp"] += XP
            if idk["xp"] >= idk["xp_on_this"]:
              idk["xp"] = 0
              idk["level"] += 1
              idk["money"] += random.randint(1, 100)
              idk['xp_on_this'] = idk['xp_on_this'] * 2
              await message.channel.send(f"{message.author}，你剛剛升級！！")
            idk["money"] += Money
            with open(f"{message.author}.json", "w") as d:
              json.dump(idk, d)
          
          if reward <= 100000 and reward > 99950:
            await message.channel.send("請稍等...")
            time.sleep(1)
            XP = random.randint(1, 500) * multi
            Money = random.randint(1, 250) * multi
            await message.channel.send(f'''**---- 獎勵----**
             金錢：`{money}`
             XP：`{XP}`''')
            with open(f"{message.author}.json", "r") as Dal:
              s = Dal.read()
            idk = json.loads(s)
            idk["Next Hourly"] = time.time() + 3600
            idk["xp"] += XP
            if idk["xp"] >= idk["xp_on_this"]:
              idk["xp"] = 0
              idk["level"] += 1
              idk['xp_on_this'] = idk['xp_on_this'] * 2
              idk["money"] += random.randint(1, 100)
              await message.channel.send(f"{message.author}, you just leveled up!!")
            idk["money"] += Money
            with open(f"{message.author}.json", "w") as ba:
              json.dump(idk, ba)
      
          
                

          
keep_alive()
token = os.environ.get
client.run("ODQ1ODg5MTE3MTg3NDczNDE5.YKnhoQ.o8zR9UCgBQN7wAI6MuSlgwsfsAs")
