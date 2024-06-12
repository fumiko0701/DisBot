import discord
import json
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(current_directory, 'commandlist.json')

with open(caminho_arquivo, 'r') as listaDeComandos:
    TodosComandos = json.load(listaDeComandos)

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

        menuOptions = [
            discord.SelectOption(label="Membros", description="Gerenciar membros do servidor", emoji="👪"),
            discord.SelectOption(label="Permissões", description="Gerenciar permissões ou cargos no servidor", emoji="🙇"),
            discord.SelectOption(label="Canais", description="Gerenciar canais ou eventos no servidor", emoji="💬"),
        ]
        
        selectOptions = discord.ui.Select(
            placeholder="Precisa de ajuda em algo?...",
            min_values=1,
            max_values=1,
            options=menuOptions,
        )

        async def callback(interaction: discord.Interaction):
            selected_value = selectOptions.values[0]
            if selected_value == "Membros":
                minhaEmbed = discord.Embed(title="Gestão de membros 🪛",
                description=f"""**Lá vamos nós!**
                Aqui vai uma lista de comandos úteis para lhe auxiliar na gestão de membros...

                ```{membergest}```                        
                                           
                                           
                                           """,
                color=discord.Color.blue())
                minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)

            elif selected_value == "Permissões":
                minhaEmbed = discord.Embed(title="Permissões", description="Gerenciar permissões ou cargos no servidor", color=discord.Color.green())
                minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)
        
            elif selected_value == "Canais":
                minhaEmbed = discord.Embed(title="Canais", description="Gerenciar canais ou eventos no servidor", color=discord.Color.red())
                minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)
        
            await interaction.response.edit_message(embed=minhaEmbed, view=minhaView)
        
        selectOptions.callback = callback

        minhaView = discord.ui.View()
        minhaView.add_item(selectOptions)

        minhaEmbed.set_footer(text="Todos os direitos reservados. ©")
        minhaEmbed.set_author(name="CRUD Assistance's Guidance", icon_url=client.user.avatar.url)

        return minhaEmbed, minhaView
