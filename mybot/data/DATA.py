import discord
import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(current_directory, 'commandlist.json')

with open(caminho_arquivo, 'r') as listaDeComandos:
    TodosComandos = json.load(listaDeComandos)

# Suponho que 'membergest' seja uma lista de comandos relacionados a membros
membergest = ', '.join(TodosComandos['membergest'])

class COMMAND_data:
    @staticmethod
    async def menu(client, prefixo, ctx=None, interaction=None):
        if ctx is not None:
            apelidoDoServidor = ctx.author.display_name
        elif interaction is not None:
            apelidoDoServidor = interaction.user.name
        
        minhaEmbed = discord.Embed(
            description=f"""**Olá {apelidoDoServidor}!**.
            
            Eu sou o CRUD, Um ChatBot criado com a finalidade de proporcionar recursos simples e práticos de gestão para servidores
            
            **Prefixo:** {prefixo}
            **Ajuda:** {prefixo}help
            
            Encontrou algum bug ou precisa de suporte?
            [Servidor de Suporte](https://youtube.com)  ━  [Reportar um erro!](https://youtube.com)""",
            color=discord.Color.red())

        # Ordem das cogs e emojis correspondentes
        cog_order = ["General", "Fun", "Image", "Moderation", "Admin"]
        cog_emojis = ["💬", "😄", "📷", "📊", "🛠️"]

        menuOptions = []
        
        # Para cada cog na ordem especificada
        for cog_name, emoji in zip(cog_order, cog_emojis):
            cog_commands = client.get_cog(cog_name).get_commands()
            command_descriptions = []

            # Montar descrições dos comandos para a cog atual
            for command in cog_commands:
                if not command.hidden:
                    # Limitar a descrição ao primeiro pedaço antes de "\n"
                    description = command.help.split("\n")[0] if command.help else "Nenhuma descrição fornecida."
                    command_descriptions.append(f"`{prefixo}{command.name}` - {description}")

            # Adicionar opção de menu para a cog atual
            menuOptions.append(discord.SelectOption(label=cog_name, description=f"Comandos de {cog_name}", emoji=emoji))

        selectOptions = discord.ui.Select(
            placeholder="Selecione uma categoria...",
            min_values=1,
            max_values=1,
            options=menuOptions,
        )

        async def callback(interaction: discord.Interaction):
            selected_value = selectOptions.values[0]
            cog_commands = client.get_cog(selected_value).get_commands()
            
            # Montar a lista de comandos da cog selecionada
            command_descriptions = []
            for command in cog_commands:
                if not command.hidden:
                    # Limitar a descrição ao primeiro pedaço antes de "\n"
                    description = command.help.split("\n")[0] if command.help else "Nenhuma descrição fornecida."
                    command_descriptions.append(f"`{prefixo}{command.name}` - {description}")
            
            # Criar a embed com os comandos da cog selecionada
            minhaEmbed = discord.Embed(title=f"Comandos de {selected_value}",
                                       description="\n".join(command_descriptions) or "Nenhum comando encontrado.",
                                       color=discord.Color.blue())
            minhaEmbed.set_footer(text=f"Use {prefixo}help para mais informações")
            minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)

            await interaction.response.edit_message(embed=minhaEmbed, view=minhaView)
        
        selectOptions.callback = callback

        minhaView = discord.ui.View()
        minhaView.add_item(selectOptions)

        minhaEmbed.set_footer(text="Todos os direitos reservados. ©")
        minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)

        return minhaEmbed, minhaView
