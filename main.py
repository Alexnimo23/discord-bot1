from keep_alive import keep_alive
keep_alive()

import discord
from discord.ext import commands
import random
import asyncio
import re

# ===============================
# Bot Ayarları
# ===============================
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)

# ===============================
# Go to Profile Butonu
# ===============================
class GoToProfileView(discord.ui.View):
    def __init__(self, profile_url: str):
        super().__init__()
        link_button = discord.ui.Button(
            label="Go to MMS Profile",
            style=discord.ButtonStyle.link,
            url=profile_url
        )
        self.add_item(link_button)

# ===============================
# MM Request Modal (Ticket)
# ===============================
class MMRequestModal(discord.ui.Modal, title="Middleman Service Request"):
    trading_with = discord.ui.TextInput(label="Who Are You Trading With?", placeholder="Paste their Discord user ID", required=True)
    your_side = discord.ui.TextInput(label="What's Your Side Of The Trade?", placeholder="Enter what you are giving", required=True)
    their_side = discord.ui.TextInput(label="What's Their Side Of The Trade?", placeholder="Enter what they are giving", required=True)
    tip = discord.ui.TextInput(label="Are You Willing To Tip Anything?", placeholder="Optional", required=False)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("❌ Ticket cannot be created in DMs.", ephemeral=True)
            return

        member = guild.get_member(interaction.user.id)
        if member is None:
            await interaction.response.send_message("❌ Member not found.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)  # type: ignore
        }

        ticket_channel = await guild.create_text_channel(f"ticket-{member.name}", overwrites=overwrites)

        embed = discord.Embed(title="🎫 Middleman Ticket Created", color=0x141e75)
        embed.add_field(name="Who Are You Trading With?", value=self.trading_with.value, inline=False)
        embed.add_field(name="Your Side", value=self.your_side.value, inline=False)
        embed.add_field(name="Their Side", value=self.their_side.value, inline=False)
        embed.add_field(name="Tip", value=self.tip.value if self.tip.value else "None", inline=False)

        await ticket_channel.send(f"{member.mention} created a new middleman ticket!", embed=embed)
        await interaction.response.send_message("✅ Ticket successfully created!", ephemeral=True)

# ===============================
# MM Request View
# ===============================
class MMRequestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="MM Request", style=discord.ButtonStyle.blurple)
    async def mm_request(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(MMRequestModal())

# ===============================
# Ticket Setup Komutu
# ===============================
@bot.command()
async def ticketsetup(ctx):
    description = (
        "ㅤㅤㅤㅤ **Middleman Service**\n"
        "✦︰ To request a middleman from this server, click the blue \"Request Middleman\" button on this message.\n\n"
        "ㅤㅤㅤㅤㅤ **How does middleman work?**\n"
        "⨯︰ Example: Trade is NFR Crow for Robux.\n"
        "Seller gives NFR Crow to middleman\n"
        "Buyer pays seller robux (After middleman confirms receiving pet)\n"
        "Middleman gives buyer NFR Crow (After seller confirmed receiving robux)\n\n"
        "ㅤㅤㅤㅤㅤ **NOTES:**\n"
        "1. You must both agree on the deal before using a middleman. Troll tickets will have consequences.\n"
        "2. Specify what you're trading (e.g. FR Frost Dragon in Adopt me > $20 USD LTC). Don't just put \"adopt me\" in the embed."
    )

    embed = discord.Embed(description=description, color=0x141e75)
    view = MMRequestView()
    await ctx.send(embed=embed, view=view)

# ===============================
# Roblox Link Komutları
# ===============================
@bot.command()
async def itsukimm(ctx):
    url = "https://www.roblox.com/tr/users/292809900/profile"
    view = GoToProfileView(url)
    await ctx.send(url, view=view)

@bot.command()
async def hanmm(ctx):
    url = "https://www.roblox.com/tr/users/3213597286/profile"
    view = GoToProfileView(url)
    await ctx.send(url, view=view)

@bot.command()
async def ashmm(ctx):
    url = "https://www.roblox.com/tr/users/3445254687/profile"
    view = GoToProfileView(url)
    await ctx.send(url, view=view)

@bot.command()
async def strmm(ctx):
    url = "https://www.roblox.com/tr/users/8464704554/profile"
    view = GoToProfileView(url)
    await ctx.send(url, view=view)

@bot.command()
async def jacemm2(ctx):
    embed = discord.Embed(
        title="Join JACE's MM2 Server",
        description="Click the button below to join the server!",
        color=0x141e75
    )
    view = discord.ui.View()
    button = discord.ui.Button(
        label="Join to the server",
        style=discord.ButtonStyle.link,
        url="https://www.roblox.com/share?code=9f781bba27fd3d4881fcb2cdc72d6f07&type=Server"
    )
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def jaceamp(ctx):
    embed = discord.Embed(
        title="Join JACE's Adopt Me Server",
        description="Click the button below to join the server!",
        color=0x141e75
    )
    view = discord.ui.View()
    button = discord.ui.Button(label="Join to the server", style=discord.ButtonStyle.link, url="https://www.roblox.com/share?code=3db5192eff27764aa0f14c303c7e6b18&type=Server")
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

@bot.command()
async def jacegag(ctx):
    embed = discord.Embed(
        title="Join JACE's GAG Server",
        description="Click the button below to join the server!",
        color=0x141e75
    )
    view = discord.ui.View()
    button = discord.ui.Button(
        label="Join to the server",
        style=discord.ButtonStyle.link,
        url="https://www.roblox.com/share?code=3db5192eff27764aa0f14c303c7e6b18&type=Server"
    )
    view.add_item(button)
    await ctx.send(embed=embed, view=view)

# ===============================
# MM Info Komutu
# ===============================
@bot.command()
async def mminfo(ctx):
    embed = discord.Embed(
        title="ℹ️ How does a middleman work?",
        description=(
            "1️⃣ Seller gives item to the middleman.\n\n"
            "2️⃣ Middleman confirms receiving the item.\n\n"
            "3️⃣ Buyer pays the seller directly (e.g., with Robux, money, crypto, etc.).\n\n"
            "4️⃣ Seller confirms they got the payment.\n\n"
            "5️⃣ Middleman gives the item to the buyer."
        ),
        color=0x141e75
    )
    await ctx.send(embed=embed)

# ===============================
# Confirm Komutu
# ===============================
class ConfirmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.green)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"✅ {interaction.user.mention} confirmed the trade!", ephemeral=False)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"❌ {interaction.user.mention} canceled the trade!", ephemeral=False)

@bot.command()
async def confirm(ctx):
    embed = discord.Embed(
        title="🔒 Do You Confirm The Trade?",
        description="Please click one of the buttons below.",
        color=0x141e75
    )
    view = ConfirmView()
    await ctx.send(embed=embed, view=view)

# ===============================
# Rules Komutu
# ===============================
@bot.command()
async def rules(ctx):
    embed = discord.Embed(
        title="📜 JACE'S MM SERVICE | RULES",
        description=(
            "| 🔹 AVOID ARGUMENTS, AND TOXICITY\n"
            "| - Do not start, partake, or instigate drama.\n"
            "| - Do not troll, bully, or bother other members in the server.\n"
            "| - Profanity is fine up to some extent, although refrain from using it at all, if possible.\n"
            "| - Do not disrespect any staff or MMs in any way.\n\n"
            "| 🔹 DON'T SCAM\n"
            "| - Scamming will result in you receiving the DWC role and a possible ban.\n"
            "| - It may also lead to a mass ban over Roblox servers.\n\n"
            "| 🔹 NO DOXXING, ADVERTISING, IMPERSONATION, THREATS OR ANYTHING OF THE SORT\n"
            "| - Posting private information such as selfies, addresses, phone numbers, or emails is strictly prohibited.\n"
            "| - Simply put, do not doxx anyone. Giving someone death threats may lead to a warn, mute or a ban.\n"
            "| - No advertising within the server.\n"
            "| - Do NOT impersonate MMs or staff members. Doing so will lead to a ban.\n\n"
            "| 🔹 DON'T BE IMMATURE\n"
            "| - Be appropriate in the voice channels.\n"
            "| - Do not scream into your mic or force-play loud audio.\n"
            "| - Don't ping others and provoke them to start arguments.\n"
            "| - Do not annoy staff.\n"
            "| - No asking for donations, or begging for money.\n"
            "| - Stay on topic, use the appropriate text channels in the server.\n\n"
            "| 🔹 BE OBEDIENT\n"
            "| - Staff have the authority, meaning they have the final say.\n"
            "| - Failure to abide by rules will result in a ban/kick from the server.\n\n"
            "| 🔹 FLOODING AND SPAM\n"
            "| - Flooding or spamming unwanted comments will result in a warn/mute.\n"
            "| - Do not post any NSFW-related content within the server.\n"
            "| - This includes pornography and gore.\n\n"
            "| 🔹 DISCORD TERMS OF SERVICE\n"
            "| - JMS abides by Discord’s official TOS.\n"
            "| - Violating the Discord TOS will obviously result in a ban.\n"
            "〃 https://discord.com/guidelines\n"
            "〃 https://discord.com/terms"
        ),
        color=0x141e75
    )
    await ctx.send(embed=embed)

# ===============================
# Trusted MM Komutu
# ===============================
@bot.command()
async def trustedmm(ctx):
    embed = discord.Embed(
        title="🔗 JACE'S TRUSTED MM LINKS",
        description="https://discord.gg/xvbArmKzha\nhttps://discord.gg/adWKpv9NnX\nhttps://discord.gg/xv5Ty7CVSw",
        color=0x141e75
    )
    await ctx.send(embed=embed)

# ===============================
# Start Komutu
# ===============================
@bot.command()
async def start(ctx):
    embed = discord.Embed(
        title="Please reply to all questions, then ping me to continue!",
        description=(
            "What is your Roblox username?\n\n"
            "What item are you offering for this trade?\n\n"
            "Do you know how the middleman process works?"
        ),
        color=0x141e75
    )
    await ctx.send(embed=embed)

# ===============================
# Market Komutu
# ===============================
@bot.command()
async def market(ctx):
    view = discord.ui.View()

    button = discord.ui.Button(
        label="Market",
        style=discord.ButtonStyle.primary,
        emoji="🛒"
    )

    async def button_callback(interaction: discord.Interaction):
        # Buradaki kontrol kaldırıldı, herkes kullanabilir
        await interaction.response.send_message(
            "Here are the market links:\nhttps://jaces.xyz/\nhttps://discord.gg/fQbPUNvCFx", ephemeral=True)

    button.callback = button_callback
    view.add_item(button)

    await ctx.send(" ", view=view)



# ===============================
# Ticket Control View (Close - Open - Delete buttons)
# ===============================
class TicketControlView(discord.ui.View):
    def __init__(self, ticket_creator: discord.Member, ticket_channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.ticket_creator = ticket_creator
        self.ticket_channel = ticket_channel

    @discord.ui.button(label="Open", style=discord.ButtonStyle.green)
    async def open_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ticket_channel.set_permissions(self.ticket_creator, read_messages=True, send_messages=True)
        await interaction.response.send_message(f"Ticket is opened again: {self.ticket_creator.mention}", ephemeral=True)

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.ticket_channel.delete()
        await interaction.response.send_message("Ticket is deleted", ephemeral=True)

# ===============================
# Close Ticket Komutu
# ===============================
@bot.command()
async def close(ctx):
    channel = ctx.channel
    guild = ctx.guild

    if guild is None:
        await ctx.send("This Only Can be used in servers")
        return

    if not channel.name.startswith("ticket-"):
        await ctx.send("only use this command in ticket channels.")
        return

    creator_name = channel.name.replace("ticket-", "")
    ticket_creator = None
    for member in guild.members:
        if member.name == creator_name:
            ticket_creator = member
            break

    if ticket_creator is None:
        await ctx.send("cant found the ticket creator.")
        return

    await channel.set_permissions(ticket_creator, read_messages=False, send_messages=False)

    embed = discord.Embed(
        title="🔒 Ticket Closed",
        description=f"Ticket {channel.mention} closed by {ctx.author.mention}",
        color=0xff0000
    )
    view = TicketControlView(ticket_creator, channel)
    await ctx.send(embed=embed, view=view)

# ===============================
# Giveaway Sistemi
# ===============================
active_giveaway = None

def parse_duration(duration_str: str) -> int | None:
    match = re.match(r"^(\d+)([smh])$", duration_str)
    if not match:
        return None
    value, unit = match.groups()
    value = int(value)
    return value if unit == "s" else value * 60 if unit == "m" else value * 3600

def format_time(seconds: int) -> str:
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")
    return " ".join(parts)

class GiveawayView(discord.ui.View):
    def __init__(self, prize: str, winners_count: int, duration: int, ctx):
        super().__init__(timeout=None)
        self.prize = prize
        self.winners_count = winners_count
        self.duration = duration
        self.participants = []
        self.host = ctx.author

    @discord.ui.button(label="🎉 Join Giveaway", style=discord.ButtonStyle.green)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user in self.participants:
            await interaction.response.send_message("❌ You have already joined this giveaway!", ephemeral=True)
            return
        self.participants.append(interaction.user)
        await interaction.response.send_message("✅ You successfully joined the giveaway!", ephemeral=True)

@bot.command()
async def giveaway(ctx, winners: int, duration: str, *, prize: str):
    global active_giveaway
    if active_giveaway is not None:
        await ctx.send("❌ There is already an active giveaway. End it first with `.endgiveaway`.")
        return
    seconds = parse_duration(duration)
    if seconds is None:
        await ctx.send("❌ Invalid duration format! Use `30s`, `10m`, `2h`.")
        return
    embed = discord.Embed(
        title="🎉 Giveaway Started!",
        description=(f"**Prize:** {prize}\n**Winners:** {winners}\n**Hosted by:** {ctx.author.mention}\n**Time Left:** {format_time(seconds)}\n\nClick the button below to join!"),
        color=0x141e75
    )
    view = GiveawayView(prize, winners, seconds, ctx)
    message = await ctx.send(embed=embed, view=view)
    active_giveaway = {"message": message, "view": view, "seconds": seconds, "winners": winners, "prize": prize, "ctx": ctx}

    while active_giveaway and active_giveaway["seconds"] > 0:
        await asyncio.sleep(5)
        active_giveaway["seconds"] -= 5
        new_embed = embed.copy()
        new_embed.description = f"**Prize:** {prize}\n**Winners:** {winners}\n**Hosted by:** {ctx.author.mention}\n**Time Left:** {format_time(active_giveaway['seconds'])}\n\nClick the button below to join!"


# ===============================
# .callhit Komutu ve Butonları
# ===============================
class CallHitView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Join", style=discord.ButtonStyle.blurple)
    async def join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            "Here is your invite link: https://discord.gg/p76mWhJJ",
            ephemeral=True
        )

    @discord.ui.button(label="Don't Join", style=discord.ButtonStyle.red)
    async def dont_join_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"{interaction.user.mention} don't wants to join!",
            ephemeral=False
        )

@bot.command()
async def callhit(ctx):
    embed = discord.Embed(
        title="GET SCAMMED",
        description=(
            "But you can make an easy profit if you join us and become a hitter!\n\n"
            "When you scam someone you will split 50/50 with the middleman, sometimes you get 100%!\n\n"
            "So join our team and make easy profit with us!"
        ),
        color=discord.Color.blue()
    )
    view = CallHitView()
    await ctx.send(embed=embed, view=view)
log_channel_id = None

@bot.command()
async def log(ctx):
    """Logs kanalını ayarlar veya oluşturur."""
    global log_channel_id
    if ctx.guild is None:
        await ctx.send("❌ Bu komut sadece sunucularda çalışır.")
        return
    log_channel = discord.utils.get(ctx.guild.text_channels, name="logs")
    if not log_channel:
        log_channel = await ctx.guild.create_text_channel("logs")
    log_channel_id = log_channel.id
    await ctx.send(f"✅ Log kanalı ayarlandı: {log_channel.mention}")

async def log_to_channel(guild, embed: discord.Embed):
    global log_channel_id
    if log_channel_id is None:
        return
    channel = guild.get_channel(log_channel_id)
    if channel is None:
        return
    await channel.send(embed=embed)

# Ticket açılırken modalda log gönderme (mevcut MMRequestModal içine ekle!)
original_on_submit = MMRequestModal.on_submit
async def new_on_submit(self, interaction: discord.Interaction):
    await original_on_submit(self, interaction)  # Önce orjinal işlem

    guild = interaction.guild
    member = guild.get_member(interaction.user.id)

    global log_channel_id
    if log_channel_id is None:
        return
    log_channel = guild.get_channel(log_channel_id)
    if log_channel is None:
        return

    log_embed = discord.Embed(title="🎫 Ticket Açıldı", color=0x00FF00)
    log_embed.add_field(name="Kullanıcı", value=member.mention)
    log_embed.add_field(name="Ticket Kanalı", value=f"ticket-{member.name}")
    log_embed.add_field(name="Trading With", value=self.trading_with.value)
    log_embed.add_field(name="Your Side", value=self.your_side.value)
    log_embed.add_field(name="Their Side", value=self.their_side.value)
    log_embed.add_field(name="Tip", value=self.tip.value if self.tip.value else "None")
    await log_channel.send(embed=log_embed)
MMRequestModal.on_submit = new_on_submit

# Ticket kapatma komutunda log gönderme (mevcut close komutuna ekle)
original_close = bot.get_command("close").callback
async def new_close(ctx):
    await original_close(ctx)

    channel = ctx.channel
    guild = ctx.guild
    global log_channel_id
    if log_channel_id is None:
        return
    log_channel = guild.get_channel(log_channel_id)
    if log_channel is None:
        return

    log_embed = discord.Embed(title="🔒 Ticket Kapandı", color=0xFF0000)
    log_embed.add_field(name="Ticket Kanalı", value=channel.mention)
    log_embed.add_field(name="Kapatıldı By", value=ctx.author.mention)
    await log_channel.send(embed=log_embed)
bot.get_command("close").callback = new_close

# Mesaj silme eventi
@bot.event
async def on_message_delete(message):
    if message.guild is None or message.author.bot:
        return
    global log_channel_id
    if log_channel_id is None:
        return
    channel = message.guild.get_channel(log_channel_id)
    if channel is None:
        return

    embed = discord.Embed(title="🗑️ Mesaj Silindi", description=f"{message.author.mention} mesajı silindi.", color=0xFF0000)
    embed.add_field(name="İçerik", value=message.content or "Mesaj boştu", inline=False)
    embed.add_field(name="Kanal", value=message.channel.mention)
    await channel.send(embed=embed)
@bot.command()
async def endgiveaway(ctx):
    global active_giveaway
    if active_giveaway is None:
        await ctx.send("❌ There is no active giveaway to end.")
        return

    view = active_giveaway["view"]
    winners = active_giveaway["winners"]
    prize = active_giveaway["prize"]

    if not view.participants:
        await ctx.send("❌ No participants joined the giveaway!")
    else:
        winners_list = random.sample(view.participants, min(winners, len(view.participants)))
        mentions = ", ".join(winner.mention for winner in winners_list)
        await ctx.send(f"🎉 Congratulations {mentions}! You won **{prize}**")

    active_giveaway = None
    await ctx.send("✅ Giveaway has been ended manually.")
@bot.command()
async def supportersetup(ctx):
    embed = discord.Embed(
        title="Claim Supporter Role",
        description="> **Equip Server Tag:** ⚡JMS\n> **Account must be at least 30 days old**",
        color=0x141e75
    )

    view = discord.ui.View()
    button = discord.ui.Button(
        label="Claim Supporter Role",
        style=discord.ButtonStyle.blurple
    )

    async def button_callback(interaction: discord.Interaction):
        await interaction.response.send_message("❌ Supporter role is not available right now.", ephemeral=True)

    button.callback = button_callback
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


import os
bot.run(os.getenv("TOKEN"))


