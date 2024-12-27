class VoteService:
    def __init__(self):
        self.votes = {"sim": 0, "nao": 0}

    def reset_votes(self):
        self.votes = {"sim": 0, "nao": 0}

    def calculate_weight(self, points):
        if points >= 10000:
            return 5
        elif points >= 1000:
            return 3
        elif points >= 500:
            return 2
        elif points >= 100:
            return 1
        return 0

    async def process_vote(self, message):
        content = message.content.strip().lower()
        if content.startswith('!sim') or content.startswith('!nao'):
            try:
                parts = content.split()
                command = parts[0]
                points = int(parts[1]) if len(parts) > 1 else 0
                weight = self.calculate_weight(points)

                if weight > 0:
                    if command == '!sim':
                        self.votes["sim"] += weight
                    elif command == '!nao':
                        self.votes["nao"] += weight
                    await message.channel.send(f"{message.author.name} votou '{command[1:]}' com {points} pontos. Peso aplicado: {weight}.")
                else:
                    await message.channel.send(f"{message.author.name}, o mínimo para usar pontos é 100.")
            except (IndexError, ValueError):
                await message.channel.send(f"{message.author.name}, use o comando no formato: !sim 500 ou !nao 1000.")

    def calculate_results(self):
        total_votes = self.votes["sim"] + self.votes["nao"]
        if total_votes == 0:
            return "Nenhum voto registrado."
        
        sim_percentage = round((self.votes["sim"] / total_votes) * 100, 2)
        nao_percentage = round((self.votes["nao"] / total_votes) * 100, 2)
        return f"Sim: {self.votes['sim']} ({sim_percentage}%), Não: {self.votes['nao']} ({nao_percentage}%)."

    def get_votes(self):
        return self.votes
