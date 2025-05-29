from shiny import App, render, ui, reactive
from datetime import datetime
import pandas as pd
from shinywidgets import output_widget, render_widget
import plotly.express as px
import plotly.graph_objects as go

# Taxa por hora do estacionamento
TAXA_POR_HORA = 5.00
VAGAS_TOTAIS = 50

# Cores personalizadas
COLORS = {
    "dark": "#1a1a2e",
    "primary": "#4e54c8",
    "secondary": "#7978FF",
    "accent": "#f64c72",
    "light": "#f8f9fa",
    "success": "#2ecc71",
    "danger": "#e74c3c",
    "warning": "#f39c12"
}

# Criar DataFrames vazios com estrutura correta
def create_empty_df():
    return pd.DataFrame(columns=["Nome", "Modelo", "Placa", "Cor", "Tipo", "Entrada"])

def create_empty_history_df():
    return pd.DataFrame(columns=["Nome", "Modelo", "Placa", "Cor", "Tipo", "Entrada", "Saida", "Valor", "Tempo"])

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"),
        ui.tags.style(f"""
            :root {{
                --dark: {COLORS["dark"]};
                --primary: {COLORS["primary"]};
                --secondary: {COLORS["secondary"]};
                --accent: {COLORS["accent"]};
                --light: {COLORS["light"]};
                --success: {COLORS["success"]};
                --danger: {COLORS["danger"]};
                --warning: {COLORS["warning"]};
            }}
            
            body {{
                background-color: var(--dark);
                color: var(--light);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }}
            
            .navbar {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                padding: 15px 0;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                margin-bottom: 30px;
            }}
            
            .card {{
                background-color: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 10px;
                padding: 25px;
                margin-bottom: 25px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
                background-color: rgba(255, 255, 255, 0.08);
            }}
            
            .card-title {{
                color: var(--secondary);
                font-weight: 600;
                margin-bottom: 20px;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            
            .btn {{
                border: none;
                border-radius: 50px;
                padding: 10px 20px;
                font-weight: 600;
                transition: all 0.3s ease;
                display: inline-flex;
                align-items: center;
                gap: 8px;
            }}
            
            .btn-primary {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                color: white;
            }}
            
            .btn-primary:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(78, 84, 200, 0.4);
            }}
            
            .btn-danger {{
                background: linear-gradient(135deg, var(--danger), #c0392b);
                color: white;
            }}
            
            .btn-danger:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(231, 76, 60, 0.4);
            }}
            
            .form-control {{
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
                border-radius: 5px;
                padding: 10px 15px;
            }}
            
            .form-control:focus {{
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
                border-color: var(--secondary);
                box-shadow: 0 0 0 0.25rem rgba(78, 84, 200, 0.25);
            }}
            
            .selectize-input {{
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: white !important;
                border-radius: 5px !important;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            th {{
                background-color: var(--primary);
                color: white;
                padding: 12px;
                text-align: left;
            }}
            
            td {{
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            tr:hover {{
                background-color: rgba(255, 255, 255, 0.05);
            }}
            
            .value-card {{
                background: linear-gradient(135deg, var(--primary), var(--secondary));
                padding: 20px;
                border-radius: 10px;
                color: white;
                margin-top: 20px;
                font-family: monospace;
                white-space: pre-wrap;
            }}
            
            .stats-container {{
                display: flex;
                gap: 15px;
                margin-bottom: 30px;
                flex-wrap: wrap;
            }}
            
            .stat-card {{
                flex: 1;
                min-width: 200px;
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
                text-align: center;
            }}
            
            .stat-value {{
                font-size: 2rem;
                font-weight: bold;
                color: var(--secondary);
                margin: 10px 0;
            }}
            
            .stat-label {{
                color: rgba(255, 255, 255, 0.7);
                font-size: 0.9rem;
            }}
            
            .icon {{
                margin-right: 10px;
            }}
            
            .control-label {{
                color: var(--light) !important;
                margin-bottom: 8px;
                font-weight: 500;
            }}
            
            ::placeholder {{
                color: rgba(255, 255, 255, 0.5) !important;
            }}
            
            .parking-slot {{
                width: 30px;
                height: 50px;
                border-radius: 5px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                margin: 3px;
                font-size: 10px;
                transition: all 0.3s ease;
            }}
            
            .parking-grid {{
                display: grid;
                grid-template-columns: repeat(10, 1fr);
                gap: 10px;
                margin-top: 20px;
            }}
            
            .notification {{
                position: fixed;
                bottom: 20px;
                right: 20px;
                padding: 15px 25px;
                border-radius: 5px;
                background-color: var(--success);
                color: white;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                opacity: 0;
                transition: opacity 0.5s ease;
                z-index: 1000;
            }}
            
            .notification.show {{
                opacity: 1;
            }}
            
            @media (max-width: 768px) {{
                .stats-container {{
                    flex-direction: column;
                }}
                .parking-grid {{
                    grid-template-columns: repeat(5, 1fr);
                }}
            }}
        """)
    ),
    
    # Notificação
    ui.div(id="notification", class_="notification", style="display: none;"),
    
    # Navbar
    ui.div(
        {"class": "navbar"},
        ui.div(
            {"class": "container-fluid"},
            ui.h2(
                {"style": "color: white; margin: 0;"},
                ui.tags.i({"class": "fas fa-parking icon"}), 
                "Parking Manager Pro"
            ),
            ui.div(
                {"style": "color: white; font-size: 1rem;"},
                ui.output_text("current_time")
            )
        )
    ),
    
    ui.div(
        {"class": "container-fluid"},
        
        # Estatísticas
        ui.div(
            {"class": "stats-container"},
            ui.div(
                {"class": "stat-card"},
                ui.div({"class": "stat-label"}, "Veículos Ativos"),
                ui.div({"class": "stat-value"}, ui.output_text("contador_ativos")),
                ui.tags.i({"class": "fas fa-car", "style": "font-size: 1.5rem; color: var(--secondary);"})
            ),
            ui.div(
                {"class": "stat-card"},
                ui.div({"class": "stat-label"}, "Faturamento Hoje"),
                ui.div({"class": "stat-value"}, ui.output_text("faturamento_hoje")),
                ui.tags.i({"class": "fas fa-money-bill-wave", "style": "font-size: 1.5rem; color: var(--secondary);"})
            ),
            ui.div(
                {"class": "stat-card"},
                ui.div({"class": "stat-label"}, "Média por Veículo"),
                ui.div({"class": "stat-value"}, ui.output_text("media_veiculo")),
                ui.tags.i({"class": "fas fa-chart-line", "style": "font-size: 1.5rem; color: var(--secondary);"})
            ),
            ui.div(
                {"class": "stat-card"},
                ui.div({"class": "stat-label"}, "Vagas Disponíveis"),
                ui.div({"class": "stat-value"}, ui.output_text("vagas_disponiveis")),
                ui.tags.i({"class": "fas fa-parking", "style": "font-size: 1.5rem; color: var(--secondary);"})
            )
        ),
        
        # Gráficos
        ui.div(
            {"class": "row"},
            ui.div(
                {"class": "col-md-6"},
                ui.div(
                    {"class": "card"},
                    ui.h3({"class": "card-title"}, ui.tags.i({"class": "fas fa-chart-pie icon"}), "Ocupação do Estacionamento"),
                    output_widget("grafico_ocupacao")
                )
            ),
            ui.div(
                {"class": "col-md-6"},
                ui.div(
                    {"class": "card"},
                    ui.h3({"class": "card-title"}, ui.tags.i({"class": "fas fa-chart-bar icon"}), "Tipos de Veículos"),
                    output_widget("grafico_tipos")
                )
            )
        ),
        
        # Visualização do Estacionamento
        ui.div(
            {"class": "card"},
            ui.h3({"class": "card-title"}, ui.tags.i({"class": "fas fa-map-marked-alt icon"}), "Mapa do Estacionamento"),
            ui.p("Vagas ocupadas estão em vermelho, vagas disponíveis em verde"),
            ui.output_ui("parking_slots_ui")  # Alterado para output_ui
        ),
        
        # Card para adicionar veículos
        ui.div(
            {"class": "row"},
            ui.div(
                {"class": "col-md-6"},
                ui.div(
                    {"class": "card"},
                    ui.h3(
                        {"class": "card-title"},
                        ui.tags.i({"class": "fas fa-car-side icon"}),
                        "Adicionar Veículo"
                    ),
                    ui.input_text("nome", "Nome do Proprietário", placeholder="Digite o nome"),
                    ui.input_text("modelo", "Modelo do Veículo", placeholder="Digite o modelo"),
                    ui.input_text("placa", "Placa do Veículo", placeholder="Digite a placa"),
                    ui.input_select("cor", "Cor do Veículo", 
                                   choices=["Branco", "Preto", "Prata", "Vermelho", "Azul", "Verde", "Amarelo", "Outro"]),
                    ui.input_select("tipo", "Tipo de Veículo", 
                                   choices=["Carro", "Moto", "SUV", "Caminhonete", "Van", "Outro"]),
                    ui.input_action_button(
                        "adicionar", 
                        ui.tags.span(ui.tags.i({"class": "fas fa-plus-circle me-2"}), "Adicionar Veículo"), 
                        class_="btn-primary"
                    )
                )
            ),
            
            # Card para remover veículos
            ui.div(
                {"class": "col-md-6"},
                ui.div(
                    {"class": "body"},
                    ui.h3(
                        {"class": "card-title"},
                        ui.tags.i({"class": "fas fa-sign-out-alt icon"}),
                        "Remover Veículo"
                    ),
                    ui.input_select(
                        "veiculo_selecionado", 
                        "Selecione o Veículo (Placa)", 
                        choices=[]
                    ),
                    ui.output_ui("veiculo_info"),
                    ui.input_action_button(
                        "remover", 
                        ui.tags.span(ui.tags.i({"class": "fas fa-minus-circle me-2"}), "Remover Veículo"), 
                        class_="btn-danger"
                    ),
                    ui.div(
                        {"class": "value-card"},
                        ui.output_text_verbatim("valor_pagar")
                    )
                )
            )
        ),
        
        # Tabela de veículos no estacionamento
        ui.div(
            {"class": "card"},
            ui.h3(
                {"class": "card-title"},
                ui.tags.i({"class": "fas fa-clipboard-list icon"}),
                "Veículos no Estacionamento"
            ),
            ui.output_table("tabela_veiculos")
        ),
        
        # Tabela de histórico
        ui.div(
            {"class": "card"},
            ui.h3(
                {"class": "card-title"},
                ui.tags.i({"class": "fas fa-history icon"}),
                "Histórico de Veículos"
            ),
            ui.input_slider("historico_dias", "Mostrar últimos dias:", min=1, max=30, value=7),
            ui.output_table("tabela_historico")
        )
    )
)

def server(input, output, session):
    # Dados reativos
    veiculos = reactive.Value(create_empty_df())
    historico = reactive.Value(create_empty_history_df())
    faturamento_dia = reactive.Value(0.0)
    
    # Atualizar hora atual (com invalidação controlada)
    @reactive.Effect
    def update_time():
        reactive.invalidate_later(1)
        ui.update_text("current_time", value=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    
    # Atualizar as escolhas do select input
    @reactive.Effect
    def update_select():
        df = veiculos.get()
        choices = df["Placa"].tolist() if not df.empty else []
        ui.update_select("veiculo_selecionado", choices=choices)
    
    # Renderizar slots de estacionamento (substitui o update_html)
    @output
    @render.ui
    def parking_slots_ui():
        df = veiculos.get()
        ocupadas = df["Placa"].tolist() if not df.empty else []
        
        slots = []
        for i in range(VAGAS_TOTAIS):
            slot_style = f"background-color: {COLORS['danger']}; color: white;" if i < len(ocupadas) else f"background-color: {COLORS['success']}; color: white;"
            slots.append(ui.div(str(i+1), {"class": "parking-slot", "style": slot_style}))
        
        return ui.div({"class": "parking-grid"}, *slots)
    
    # Info do veículo selecionado
    @output
    @render.ui
    def veiculo_info():
        placa = input.veiculo_selecionado()
        if placa:
            df = veiculos.get()
            veiculo = df[df["Placa"] == placa].iloc[0]
            return ui.div(
                ui.p(f"Proprietário: {veiculo['Nome']}"),
                ui.p(f"Modelo: {veiculo['Modelo']}"),
                ui.p(f"Cor: {veiculo['Cor']}"),
                ui.p(f"Tipo: {veiculo['Tipo']}"),
                ui.p(f"Entrada: {veiculo['Entrada'].strftime('%d/%m/%Y %H:%M:%S')}"),
                class_="mb-3"
            )
        return ""
    
    # Adicionar veículo
    @reactive.Effect
    @reactive.event(input.adicionar)
    def add_vehicle():
        nome = input.nome()
        modelo = input.modelo()
        placa = input.placa()
        cor = input.cor()
        tipo = input.tipo()
        
        if nome and modelo and placa:
            # Verifica se já existe um veículo com a mesma placa
            df = veiculos.get()
            if not df.empty and placa in df["Placa"].values:
                ui.notification_show("Já existe um veículo com esta placa!", duration=3, type="error")
                return
            
            if len(df) >= VAGAS_TOTAIS:
                ui.notification_show("Estacionamento lotado!", duration=3, type="warning")
                return
            
            novo_veiculo = pd.DataFrame({
                "Nome": [nome],
                "Modelo": [modelo],
                "Placa": [placa],
                "Cor": [cor],
                "Tipo": [tipo],
                "Entrada": [datetime.now()]
            })
            
            # Atualiza o DataFrame de veículos
            if df.empty:
                df = create_empty_df()
            df = pd.concat([df, novo_veiculo], ignore_index=True)
            veiculos.set(df)
            
            # Limpa os inputs
            ui.update_text("nome", value="")
            ui.update_text("modelo", value="")
            ui.update_text("placa", value="")
            
            ui.notification_show("Veículo adicionado com sucesso!", duration=3, type="message")
    
    # Remover veículo
    @reactive.Effect
    @reactive.event(input.remover)
    def remove_vehicle():
        placa = input.veiculo_selecionado()
        if placa:
            df_veiculos = veiculos.get()
            df_historico = historico.get()
            
            # Encontra o veículo a ser removido
            veiculo = df_veiculos[df_veiculos["Placa"] == placa].iloc[0]
            
            # Calcula o valor a pagar
            entrada = veiculo["Entrada"]
            saida = datetime.now()
            horas = (saida - entrada).total_seconds() / 3600
            valor = round(horas * TAXA_POR_HORA, 2)
            
            # Adiciona ao histórico
            novo_registro = pd.DataFrame({
                "Nome": [veiculo["Nome"]],
                "Modelo": [veiculo["Modelo"]],
                "Placa": [veiculo["Placa"]],
                "Cor": [veiculo["Cor"]],
                "Tipo": [veiculo["Tipo"]],
                "Entrada": [entrada],
                "Saida": [saida],
                "Valor": [valor],
                "Tempo": [horas]
            })
            
            if df_historico.empty:
                df_historico = create_empty_history_df()
            df_historico = pd.concat([df_historico, novo_registro], ignore_index=True)
            historico.set(df_historico)
            
            # Atualiza o faturamento do dia
            faturamento_dia.set(faturamento_dia.get() + valor)
            
            # Remove do DataFrame de veículos ativos
            df_veiculos = df_veiculos[df_veiculos["Placa"] != placa]
            veiculos.set(df_veiculos)
            
            ui.notification_show(f"Veículo removido. Valor: R$ {valor:.2f}", duration=5, type="message")
    
    # Outputs
    @output
    @render.text
    def contador_ativos():
        return str(len(veiculos.get()))
    
    @output
    @render.text
    def faturamento_hoje():
        return f"R$ {faturamento_dia.get():.2f}"
    
    @output
    @render.text
    def media_veiculo():
        total = faturamento_dia.get()
        count = len(historico.get())
        if count > 0:
            return f"R$ {total/count:.2f}"
        return "R$ 0.00"
    
    @output
    @render.text
    def vagas_disponiveis():
        return f"{VAGAS_TOTAIS - len(veiculos.get())}/{VAGAS_TOTAIS}"
    
    @output
    @render.text
    def current_time():
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    @output
    @render.text
    def valor_pagar():
        placa = input.veiculo_selecionado()
        if placa:
            df = veiculos.get()
            veiculo = df[df["Placa"] == placa].iloc[0]
            entrada = veiculo["Entrada"]
            saida = datetime.now()
            horas = (saida - entrada).total_seconds() / 3600
            valor = round(horas * TAXA_POR_HORA, 2)
            return f"Valor a pagar para {veiculo['Nome']}:\nR$ {valor:.2f}\nTempo: {horas:.1f} horas\nModelo: {veiculo['Modelo']}\nCor: {veiculo['Cor']}"
        return "Selecione um veículo para calcular o valor"
    
    @output
    @render.table
    def tabela_veiculos():
        df = veiculos.get().copy()
        if not df.empty:
            df["Entrada"] = df["Entrada"].dt.strftime("%d/%m/%Y %H:%M:%S")
            df = df.sort_values("Entrada", ascending=False)
        return df
    
    @output
    @render.table
    def tabela_historico():
        df = historico.get().copy()
        if not df.empty:
            # Filtrar pelos últimos dias selecionados
            dias = input.historico_dias()
            data_limite = datetime.now() - pd.Timedelta(days=dias)
            df = df[df["Saida"] >= data_limite]
            
            df["Entrada"] = df["Entrada"].dt.strftime("%d/%m/%Y %H:%M:%S")
            df["Saida"] = df["Saida"].dt.strftime("%d/%m/%Y %H:%M:%S")
            df["Valor"] = df["Valor"].apply(lambda x: f"R$ {x:.2f}")
            df["Tempo"] = df["Tempo"].apply(lambda x: f"{x:.1f} horas")
            df = df.sort_values("Saida", ascending=False)
        return df
    
    @output
    @render_widget
    def grafico_ocupacao():
        count = len(veiculos.get())
        
        fig = px.pie(
            names=["Ocupado", "Vago"],
            values=[count, max(0, VAGAS_TOTAIS - count)],
            title="Ocupação do Estacionamento",
            color_discrete_sequence=[COLORS["primary"], COLORS["dark"]],
            hole=0.4
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=COLORS["light"],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        return fig
    
    @output
    @render_widget
    def grafico_tipos():
        df = veiculos.get()
        if not df.empty:
            tipos = df["Tipo"].value_counts().reset_index()
            tipos.columns = ["Tipo", "Quantidade"]
            
            fig = px.bar(
                tipos,
                x="Tipo",
                y="Quantidade",
                title="Distribuição por Tipo de Veículo",
                color="Tipo",
                color_discrete_sequence=[COLORS["primary"], COLORS["secondary"], COLORS["accent"], COLORS["success"]]
            )
        else:
            fig = go.Figure()
            fig.add_annotation(text="Nenhum veículo no estacionamento",
                             xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False)
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font_color=COLORS["light"],
            xaxis_title="",
            yaxis_title="Quantidade",
            showlegend=False
        )
        
        return fig

app = App(app_ui, server)	