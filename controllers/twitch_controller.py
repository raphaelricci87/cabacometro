from twitchio.ext import commands
from services.vote_service import VoteService

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.getenv('TWITCH_TOKEN'),
                         client_id=os.getenv('TWITCH_CLIENT_ID'),
                         nick=os.getenv('TWITCH_NICK'),
                         prefix='!',
                         initial_channels=[os.getenv('TWITCH_CHANNEL')])
        self.voting_active = False
        self.vote_service = VoteService()

    async def event_ready(self):
        print(f"Bot conectado como {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        if self.voting_active:
            await self.vote_service.process_vote(message)
        await self.handle_commands(message)

    @commands.command(name="iniciarvotacao")
    async def iniciar_votacao(self, ctx):
        self.vote_service.reset_votes()
        self.voting_active = True
        await ctx.send("Votação iniciada! Use !sim <pontos> ou !nao <pontos> para votar com peso.")

    @commands.command(name="finalizarvotacao")
    async def finalizar_votacao(self, ctx):
        self.voting_active = False
        results = self.vote_service.calculate_results()
        await ctx.send(f"Votação encerrada! {results}")
        print(f"Resultados: {results}")
