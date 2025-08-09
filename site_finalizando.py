# calculadora_streamlit.py

# ==================================================================================================
# BIBLIOTECAS
# ==================================================================================================
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols, sympify, diff, integrate, limit, oo, latex, lambdify, Rational
from matplotlib.patches import Rectangle
import io
import imageio.v2 as imageio

# ==================================================================================================
# CONFIGURAÇÃO DA PÁGINA E ESTADO DA SESSÃO
# ==================================================================================================
st.set_page_config(layout="wide")

# Inicializa as variáveis de estado da sessão se elas não existirem
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'home'
if 'limite_eixo' not in st.session_state:
    st.session_state.limite_eixo = 10
# Adiciona o tema ao estado da sessão, com 'Escuro' como padrão
if 'theme' not in st.session_state:
    st.session_state.theme = 'Escuro'

# ==================================================================================================
# CABEÇALHO COM CONFIGURAÇÕES GLOBAIS
# ==================================================================================================
# Layout em colunas para o título e o botão de configurações
col_titulo, col_config = st.columns([0.9, 0.1])

with col_titulo:
    # NOME DO SITE ATUALIZADO
    st.markdown("""
        <h1 style='text-align: left;'>🧠 Cálculo (Dora)</h1>
    """, unsafe_allow_html=True)

with col_config:
    # O Popover cria o menu de configurações que aparece ao clicar no ícone
    with st.popover("⚙️"):
        st.markdown("##### Configurações Gerais")
        # Slider para o intervalo dos eixos
        st.session_state.limite_eixo = st.slider(
            "Intervalo dos eixos do gráfico:",
            min_value=1,
            max_value=50,
            value=st.session_state.limite_eixo,
            help="Define o intervalo de visualização para os eixos X e Y, de -Valor a +Valor."
        )
        # Seletor de tema claro/escuro
        st.session_state.theme = st.radio(
            "Tema do Site:",
            ('Escuro', 'Claro'),
            key='theme_selector',
            index=0 if st.session_state.theme == 'Escuro' else 1
        )

st.markdown("<hr style='border: 1px solid #ccc; margin-top: -10px;' />", unsafe_allow_html=True)


# ==================================================================================================
# MENU LATERAL (SIDEBAR)
# ==================================================================================================
with st.sidebar:
    st.markdown("### 🧭 Navegação")
    if st.button("🏠 Início"):
        st.session_state.pagina_atual = "home"
    
    with st.expander("🎥 EXEMPLOS"):
        if st.button("🎥 Bisseção"):
            st.session_state.pagina_atual = "ex_bissecao" 
        if st.button("🎥 Falsa posição"):
            st.session_state.pagina_atual = "ex_falsaposicao"           
    
    with st.expander("📘 Cálculo 1"):
        if st.button("✏️ Derivadas"):
            st.session_state.pagina_atual = "derivadas"
        if st.button("📐 Integrais"):
            st.session_state.pagina_atual = "integrais"
        if st.button("📏 Limites"):
            st.session_state.pagina_atual = "limites"
            
    with st.expander("📙 Cálculo 2"):
        if st.button("📊 Séries de Taylor"):
            st.session_state.pagina_atual = "taylor"
        if st.button("🔁 Integrais Duplas"):
            st.session_state.pagina_atual = "integrais_duplas"
        if st.button("🌀 Equações Diferenciais"):
            st.session_state.pagina_atual = "equacoes_diferenciais"
            
    with st.expander("📗 Cálculo Numérico"):
        if st.button("🔍 Método Gráfico"):
            st.session_state.pagina_atual = "metodo_grafico"
        if st.button("🔍 Bisseção"):
            st.session_state.pagina_atual = "bissecao"
        if st.button("🔍 Falsa Posição"):
            st.session_state.pagina_atual = "falsa_posicao"
        if st.button("⚙️ Ponto Fixo"):
            st.session_state.pagina_atual = "ponto_fixo"
        if st.button("⚙️ Método de Newton"):
            st.session_state.pagina_atual = "newton"
        if st.button("⚙️ Secante"):
            st.session_state.pagina_atual = "secante"
        if st.button("Jacobi-Richardson"):
            st.session_state.pagina_atual = "jacobi"
            
        
# ==================================================================================================
# CONTEÚDO DAS PÁGINAS
# ==================================================================================================
pagina = st.session_state.pagina_atual
# PÁGINA HOME (VERSÃO COM LAYOUT CORRIGIDO FINAL) =================================================

# PÁGINA HOME (VERSÃO COM LAYOUT CORRIGIDO FINAL) =================================================
if pagina == "home":

    # INJEÇÃO DE CSS PARA FORÇAR O LAYOUT WIDE APENAS NESTA PÁGINA
    # Este CSS é mais "agressivo" e remove as restrições de layout do Streamlit.
    st.markdown("""
        <style>
            /* Remove o padding do container principal do Streamlit */
            .main .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 0rem;
                padding-right: 0rem;
            }
            /* Força o iframe a ocupar a tela inteira */
            iframe {
                width: 100%;
                min-height: 95vh; /* Usa a altura da tela como referência */
                border: none;
            }
        </style>
        """, unsafe_allow_html=True)

    # Determina as classes e cores com base no tema selecionado no estado da sessão
    theme_mode = st.session_state.get('theme', 'Escuro')
    theme_class = "light-mode" if theme_mode == 'Claro' else ''
    particle_color_js = 'rgba(0, 0, 0, 0.08)' if theme_mode == 'Claro' else 'rgba(255, 255, 255, 0.1)'

    # O f-string é usado para injetar a classe de tema e a cor da partícula no HTML
    html_code = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Explorador de Cálculo - Início</title>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

            :root {{
                --bg-color: #121212;
                --text-color: #e0e0e0;
                --subtle-text-color: #a0a0a0;
                --header-color: #ffffff;
                --card-bg: rgba(255, 255, 255, 0.05);
                --card-border: rgba(255, 255, 255, 0.1);
                --card-shadow: rgba(0, 0, 0, 0.4);
                --card-list-border: rgba(255, 255, 255, 0.08);
                --card-title-color: #4dabf7;
                --footer-color: #666;
            }}

            .light-mode {{
                --bg-color: #f0f2f5;
                --text-color: #1c1e21;
                --subtle-text-color: #606770;
                --header-color: #000000;
                --card-bg: rgba(255, 255, 255, 0.8);
                --card-border: rgba(0, 0, 0, 0.1);
                --card-shadow: rgba(0, 0, 0, 0.1);
                --card-list-border: rgba(0, 0, 0, 0.1);
                --card-title-color: #1877f2;
                --footer-color: #888;
            }}

            * {{ margin: 0; padding: 0; box-sizing: border-box; }}

            body {{
                font-family: 'Poppins', sans-serif;
                background-color: var(--bg-color);
                color: var(--text-color);
                overflow: hidden;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                text-align: center;
            }}

            #background-canvas {{
                position: fixed; top: 0; left: 0;
                width: 100%; height: 100%; z-index: -1;
            }}

            .main-container {{
                width: 100%;
                padding: 40px 5%;
                z-index: 1; display: flex; flex-direction: column;
                align-items: center; gap: 40px;
            }}

            header {{ margin-bottom: 20px; }}

            /* Animação de digitação */
            .typing-title {{
                font-size: 3.5rem;
                font-weight: 700;
                color: var(--header-color);
                text-shadow: 0 0 15px rgba(100, 100, 255, 0.3);
                overflow: hidden;
                border-right: .12em solid var(--card-title-color);
                white-space: nowrap;
                margin: 0 auto;
                letter-spacing: .1em;
                animation: typing 3s steps(20, end), blink-caret .75s step-end infinite;
            }}

            @keyframes typing {{
              from {{ width: 0 }}
              to {{ width: 100% }}
            }}

            @keyframes blink-caret {{
              from, to {{ border-color: transparent }}
              50% {{ border-color: var(--card-title-color); }}
            }}
            
            header p {{
                font-size: 1.2rem; color: var(--subtle-text-color); margin-top: 20px; max-width: 600px;
            }}
            
            .cards-container {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 25px; width: 100%;
            }}

            .card {{
                background: var(--card-bg);
                backdrop-filter: blur(10px);
                border: 1px solid var(--card-border);
                border-radius: 15px; padding: 25px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}

            .card:hover {{
                transform: translateY(-10px);
                box-shadow: 0 10px 30px var(--card-shadow);
            }}

            .card h3 {{
                font-size: 1.5rem; margin-bottom: 15px; color: var(--card-title-color);
            }}
            
            .card ul {{
                list-style: none; text-align: left; padding-left: 0;
            }}

            .card ul li {{
                padding: 8px 0; border-bottom: 1px solid var(--card-list-border);
            }}

            .card ul li:last-child {{ border-bottom: none; }}
            
            footer {{
                margin-top: 30px; color: var(--footer-color); font-size: 0.9rem;
            }}
        </style>
    </head>
    <body class="{theme_class}">
        <canvas id="background-canvas"></canvas>

        <div class="main-container">
            <header>
                <h1 class="typing-title">🧠 Cálculo (Dora)</h1>
                <p>Sua plataforma interativa para explorar o universo do Cálculo. Navegue pelos tópicos no menu lateral.</p>
            </header>

            <div class="cards-container">
                <div class="card">
                    <h3>📘 Cálculo 1</h3>
                    <ul><li>✏️ Derivadas</li><li>📐 Integrais</li><li>📏 Limites</li></ul>
                </div>
                <div class="card">
                    <h3>📙 Cálculo 2</h3>
                    <ul><li>📊 Séries de Taylor</li><li>🔁 Integrais Duplas</li><li>🌀 Equações Diferenciais</li></ul>
                </div>
                <div class="card">
                    <h3>📗 Cálculo Numérico</h3>
                    <ul><li>🔍 Métodos de Raízes</li><li>⚙️ Interpolação</li><li>📈 Ajuste de Curvas</li></ul>
                </div>
            </div>

            <footer>
                <p>🚀 Projeto desenvolvido por Lucas Matias.</p>
            </footer>
        </div>

        <script>
            const canvas = document.getElementById('background-canvas');
            const ctx = canvas.getContext('2d');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const symbols = ['∫', '∂', '∑', '∞', 'α', 'β', 'π', 'lim', '√', 'ƒ(x)'];
            const particles = [];
            const numberOfParticles = 40;

            class Particle {{
                constructor() {{
                    this.x = Math.random() * canvas.width;
                    this.y = Math.random() * canvas.height;
                    this.size = Math.random() * 15 + 10;
                    this.speedX = Math.random() * 1 - 0.5;
                    this.speedY = Math.random() * 1 - 0.5;
                    this.symbol = symbols[Math.floor(Math.random() * symbols.length)];
                    this.color = '{particle_color_js}';
                }}
                update() {{
                    this.x += this.speedX; this.y += this.speedY;
                    if (this.x > canvas.width + 20) this.x = -20;
                    if (this.x < -20) this.x = canvas.width + 20;
                    if (this.y > canvas.height + 20) this.y = -20;
                    if (this.y < -20) this.y = canvas.height + 20;
                }}
                draw() {{
                    ctx.fillStyle = this.color;
                    ctx.font = this.size + 'px Poppins';
                    ctx.fillText(this.symbol, this.x, this.y);
                }}
            }}

            function init() {{
                particles.length = 0;
                for (let i = 0; i < numberOfParticles; i++) {{ particles.push(new Particle()); }}
            }}

            function animate() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                for (let i = 0; i < particles.length; i++) {{ particles[i].update(); particles[i].draw(); }}
                requestAnimationFrame(animate);
            }}

            window.addEventListener('resize', () => {{
                canvas.width = window.innerWidth;
                canvas.height = window.innerHeight;
                init();
            }});
            
            init();
            animate();
        </script>
    </body>
    </html>
    """
    
    # Renderiza o componente HTML. A altura aqui é menos crítica, pois o CSS está controlando o layout.
    st.components.v1.html(html_code, height=900, scrolling=False)


# EXEMPLO - BISSEÇÃO =================================================================================
elif pagina == "ex_bissecao":
    st.subheader("📊 Exemplo: Método da Bisseção")
    st.info("Este vídeo mostra a aplicação gráfica do método da bisseção.")
    st.markdown("### 🎬 Assista ao vídeo:")
    try:
        with open("BissecaoDividido.mp4", "rb") as f:
            video_bytes = f.read()
            st.video(video_bytes)
    except FileNotFoundError:
        st.error("Arquivo de vídeo 'BissecaoDividido.mp4' não encontrado. Coloque o vídeo na mesma pasta do script.")

# EXEMPLO - FALSA POSIÇÃO ============================================================================
elif pagina == "ex_falsaposicao":
    st.subheader("📊 Exemplo: Método da Falsa Posição")
    st.info("Este vídeo mostra a aplicação gráfica do método da falsa posição.")
    st.markdown("### 🎬 Assista ao vídeo:")
    try:
        with open("FalsaPosicaoDividido.mp4", "rb") as f:
            video_bytes = f.read()
            st.video(video_bytes)
    except FileNotFoundError:
        st.error("Arquivo de vídeo 'FalsaPosicaoDividido.mp4' não encontrado. Coloque o vídeo na mesma pasta do script.")

# C1 - DERIVADAS (com configuração global de eixos) ==================================================
elif pagina == "derivadas":
    st.subheader("✏️ Relação Gráfica entre uma Função e sua Derivada")
    
    # Lê o valor do limite do eixo a partir do estado da sessão (definido no popover global)
    limite_eixo = st.session_state.limite_eixo

    # Input da função
    func_str = st.text_input("Digite a função f(x):", "sin(x)")

    try:
        # --- Cálculos com Sympy ---
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        df_expr = sp.diff(f_expr, x)
        df_expr_simplified = sp.simplify(df_expr)

        # Converte as expressões para funções numéricas
        f_numeric = sp.lambdify(x, f_expr, 'numpy')
        df_numeric = sp.lambdify(x, df_expr_simplified, 'numpy')

        # --- Exibição dos Resultados ---
        st.markdown("---")
        st.success(f"A derivada da função $f(x) = {sp.latex(f_expr)}$ é:")
        st.latex(r"f'(x) = " + sp.latex(df_expr_simplified))
        st.markdown("---")

        # --- Seção Interativa para Análise em um Ponto ---
        analisar_ponto = st.toggle("Analisar em um ponto específico?", value=True)
        x0 = None

        if analisar_ponto:
            # O slider do ponto de análise agora respeita o limite do eixo
            valor_default_slider = 1.5 if 1.5 < limite_eixo else float(limite_eixo/2)
            x0 = st.slider("Escolha o ponto de análise $x_0$:", 
                           float(-limite_eixo), 
                           float(limite_eixo), 
                           valor_default_slider, 
                           step=0.1)

        # --- Criação do Gráfico ---
        x_vals = np.linspace(-limite_eixo, limite_eixo, 1000)
        y_vals = np.array([f_numeric(val) if np.isfinite(f_numeric(val)) else np.nan for val in x_vals])
        df_vals = np.array([df_numeric(val) if np.isfinite(df_numeric(val)) else np.nan for val in x_vals])

        fig, ax = plt.subplots(figsize=(8, 8))

        # Plot da função original e da derivada
        ax.plot(x_vals, y_vals, label="$f(x)$ (Função Original)", color='blue', linewidth=2)
        ax.plot(x_vals, df_vals, label="$f'(x)$ (A Derivada)", color='red', linestyle='--', linewidth=2)

        # --- Elementos visuais da análise no ponto ---
        if analisar_ponto and x0 is not None:
            y0 = f_numeric(x0)
            df_at_x0 = df_numeric(x0)
            
            if np.isfinite(y0) and np.isfinite(df_at_x0):
                tangent_line = df_at_x0 * (x_vals - x0) + y0
                ax.plot(x_vals, tangent_line, label=f"Reta Tangente em x={x0:.1f}", color='green', linestyle=':', linewidth=2.5)
                ax.scatter([x0], [y0], color='blue', s=100, zorder=5, edgecolors='black', label=f'Ponto em f(x): ({x0:.1f}, {y0:.2f})')
                ax.scatter([x0], [df_at_x0], color='red', s=100, zorder=5, edgecolors='black', label=f"Valor de f'(x): {df_at_x0:.2f}")
                ax.plot([x0, x0], [y0, df_at_x0], color='black', linestyle='-.', linewidth=1.2)
        
        # Configurações do gráfico
        ax.axhline(0, color='black', linewidth=0.8, linestyle='-')
        ax.axvline(0, color='black', linewidth=0.8, linestyle='-')
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title("Gráfico Comparativo de $f(x)$ e $f'(x)$")
        ax.legend(loc='upper left')
        ax.grid(True, which='both', linestyle=':', linewidth=0.5)
        
        ax.set_xlim(-limite_eixo, limite_eixo)
        ax.set_ylim(-limite_eixo, limite_eixo)
        ax.set_aspect('equal', adjustable='box')

        st.pyplot(fig)

        # --- Exibição dos valores calculados ---
        if analisar_ponto and x0 is not None:
            y0_val = f_numeric(x0)
            df_val = df_numeric(x0)
            if np.isfinite(y0_val) and np.isfinite(df_val):
                st.markdown("### Análise no Ponto $x_0$")
                col1, col2 = st.columns(2)
                col1.metric(label=f"Valor da função, $f({x0:.2f})$", value=f"{y0_val:.4f}")
                col2.metric(label=f"Valor da derivada, $f'({x0:.2f})$", value=f"{df_val:.4f}")
                st.info(f"Observe que a inclinação da reta tangente verde é exatamente o valor da derivada: **{df_val:.4f}**.")
            else:
                st.warning(f"A função ou sua derivada não está definida ou é infinita no ponto $x_0 = {x0:.2f}$.")

        # --- Guia Didático Geral ---
        st.markdown("### Como interpretar o gráfico?")
        st.info("""
        - **Curva Azul ($f(x)$):** Sua função original.
        - **Curva Vermelha ($f'(x)$):** Representa a inclinação da curva azul em cada ponto.
        
        **Relações importantes:**
        1. Onde a **curva azul sobe**, a **vermelha é positiva**.
        2. Onde a **curva azul desce**, a **vermelha é negativa**.
        3. Em um pico ou vale da **curva azul**, a **vermelha cruza o zero**.
        """)

    except Exception as e:
        st.error(f"Houve um erro ao interpretar a sua função. Verifique a sintaxe. (Ex: use 'x**2' para $x^2$). Erro: {str(e)}")


# C1 - INTEGRAIS (VERSÃO REVISADA E CORRIGIDA) =================================================================
elif pagina == "integrais":
    # Importa as classes necessárias para desenhar as formas
    from matplotlib.patches import Rectangle, Polygon

    st.subheader("📐 Visualizando a Integral Definida (Soma de Riemann)")
    
    # Lê o valor do limite do eixo a partir do estado da sessão
    limite_eixo = st.session_state.limite_eixo

    # --- Entradas do Usuário ---
    func_str = st.text_input("Digite a função f(x):", "4 - x**2")
    
    col1, col2 = st.columns(2)
    with col1:
        # Garante que os limites de integração respeitem os limites do gráfico
        a = st.number_input("Limite inferior de integração (a):", 
                              min_value=float(-limite_eixo), 
                              max_value=float(limite_eixo), 
                              value=0.0)
    with col2:
        b = st.number_input("Limite superior de integração (b):", 
                              min_value=float(-limite_eixo), 
                              max_value=float(limite_eixo), 
                              value=2.0)

    method = st.selectbox(
        "Escolha o método de aproximação:",
        ("Ponto Esquerdo", "Ponto Direito", "Ponto Médio", "Trapézio"),
        help="Define como a altura de cada subdivisão é calculada."
    )
    
    n = st.slider("Número de subdivisões (n):", 1, 200, 10, help="Quanto mais subdivisões, mais precisa a aproximação.")

    try:
        # --- Cálculos com Sympy ---
        x = sp.symbols('x')
        func_sympy = sp.sympify(func_str)
        func_numeric = sp.lambdify('x', func_sympy, 'numpy')

        # --- Criação do Gráfico ---
        fig, ax = plt.subplots(figsize=(8, 8))
        
        # Plot da função no intervalo do gráfico global
        x_graph = np.linspace(-limite_eixo, limite_eixo, 1000)
        y_graph = func_numeric(x_graph)
        ax.plot(x_graph, y_graph, label="f(x)", color="blue", linewidth=2)

        # Preenche a área exata sob a curva no intervalo [a, b]
        x_fill = np.linspace(a, b, 200)
        y_fill = func_numeric(x_fill)
        ax.fill_between(x_fill, y_fill, where=(y_fill > 0), color='skyblue', alpha=0.5, label="Área exata (positiva)")
        ax.fill_between(x_fill, y_fill, where=(y_fill < 0), color='salmon', alpha=0.5, label="Área exata (negativa)")

        # --- Lógica de aproximação e plot das formas ---
        area_aproximada = 0
        if n > 0 and b > a:
            dx = (b - a) / n
            for i in range(n):
                x_i = a + i * dx
                x_i_plus_1 = x_i + dx
                
                if method == "Ponto Esquerdo":
                    height = func_numeric(x_i)
                    shape = Rectangle((x_i, 0), dx, height, edgecolor="black", facecolor="orange", alpha=0.7)
                    area_aproximada += height * dx
                elif method == "Ponto Direito":
                    height = func_numeric(x_i_plus_1)
                    shape = Rectangle((x_i, 0), dx, height, edgecolor="black", facecolor="orange", alpha=0.7)
                    area_aproximada += height * dx
                elif method == "Ponto Médio":
                    height = func_numeric(x_i + dx/2)
                    shape = Rectangle((x_i, 0), dx, height, edgecolor="black", facecolor="orange", alpha=0.7)
                    area_aproximada += height * dx
                elif method == "Trapézio":
                    y_i = func_numeric(x_i)
                    y_i_plus_1 = func_numeric(x_i_plus_1)
                    # Agora o Polygon está definido corretamente
                    shape = Polygon([[x_i, 0], [x_i_plus_1, 0], [x_i_plus_1, y_i_plus_1], [x_i, y_i]], edgecolor="black", facecolor="orange", alpha=0.7)
                    area_aproximada += (y_i + y_i_plus_1) / 2 * dx
                
                ax.add_patch(shape)

        # Configurações do gráfico
        ax.axhline(0, color='black', linewidth=0.8)
        ax.axvline(0, color='black', linewidth=0.8)
        ax.set_title(f"Aproximação por '{method}' com n={n}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid(True, which='both', linestyle=':', linewidth=0.5)
        
        # Aplicando configuração global de eixos
        ax.set_xlim(-limite_eixo, limite_eixo)
        ax.set_ylim(-limite_eixo, limite_eixo)
        ax.set_aspect('equal', adjustable='box')
        ax.legend()
        st.pyplot(fig)

        # --- Exibição dos Resultados ---
        st.markdown("### Resultados")
        col_res1, col_res2 = st.columns(2)
        
        col_res1.metric(label=f"Área Aproximada ({method})", value=f"{area_aproximada:.6f}")
        
        try:
            integral_exata = sp.integrate(func_sympy, (x, a, b)).evalf()
            col_res2.metric(label="Área Exata (Integral)", value=f"{integral_exata:.6f}", delta=f"{(area_aproximada - integral_exata):.6f}", delta_color="inverse")
        except Exception:
            col_res2.info("Não foi possível calcular a integral exata.")

        # --- Guia Didático ---
        st.markdown("### Como interpretar o gráfico?")
        st.info("""
        A integral definida de $f(x)$ de $a$ até $b$ representa a **área líquida** sob a curva.

        - **Área Colorida:** O valor exato da integral.
        - **Formas Laranjas:** A aproximação da área usando o método escolhido.
        
        **Observe:**
        1.  Ao **aumentar o número de subdivisões (n)**, a soma das áreas laranjas se aproxima cada vez mais da área colorida.
        2.  Dependendo da função e do método, a aproximação pode ser uma **subestimação** ou uma **superestimação**.
        """)

    except Exception as e:
        st.error(f"Erro ao processar a função: {str(e)}")

# C1 - LIMITES (VERSÃO CORRIGIDA E MAIS INTUITIVA) ===================================================================
elif pagina == "limites":
    import math # Importa a biblioteca de matemática para a comparação de floats

    st.subheader("📏 Visualizando o Conceito de Limite")

    # Lê o valor do limite do eixo a partir do estado da sessão
    limite_eixo_global = st.session_state.limite_eixo

    # --- Entradas do Usuário ---
    func_str = st.text_input("Digite a função f(x):", "sin(x)/x")
    
    try:
        # --- Cálculos com Sympy ---
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        f_numeric = sp.lambdify(x, f_expr, modules=['numpy', 'math'])

        limite_tipo = st.selectbox("Escolha o tipo de limite:", ["Limite em um Ponto", "Limite no Infinito"])

        # --- LÓGICA PARA LIMITE EM UM PONTO ---
        if limite_tipo == "Limite em um Ponto":
            x0 = st.number_input("Ponto de análise (onde x tende):", 
                                   min_value=float(-limite_eixo_global), 
                                   max_value=float(limite_eixo_global), 
                                   value=0.0)
            
            try:
                lim_dir = sp.limit(f_expr, x, x0, dir='+')
                lim_esq = sp.limit(f_expr, x, x0, dir='-')
                limite_val = sp.limit(f_expr, x, x0)
                
                st.markdown("---")
                col1, col2, col3 = st.columns(3)
                col1.latex(fr"\lim_{{x \to {x0}^-}} f(x) = {latex(lim_esq)}")
                col2.latex(fr"\lim_{{x \to {x0}^+}} f(x) = {latex(lim_dir)}")

                # CORREÇÃO: Usar math.isclose para comparar floats de forma segura
                # Isso evita erros de arredondamento
                if lim_dir.is_finite and lim_esq.is_finite and math.isclose(float(lim_dir), float(lim_esq)):
                    col3.latex(fr"\lim_{{x \to {x0}}} f(x) = {latex(limite_val)}")
                else:
                    col3.error(r"\text{Limite não existe ou diverge}")

            except Exception as e:
                st.error(f"Não foi possível calcular o limite: {e}")
                st.stop()
            
            st.markdown("---")
            # O valor inicial do delta foi reduzido para uma visualização mais próxima
            delta = st.slider("Proximidade (δ):", min_value=0.01, max_value=3.0, value=0.5, step=0.01)

            # --- Gráfico ---
            fig, ax = plt.subplots(figsize=(8, 8))
            
            x_graph = np.linspace(-limite_eixo_global, limite_eixo_global, 1000)
            y_graph = np.array([f_numeric(val) for val in x_graph])
            ax.plot(x_graph, y_graph, label="f(x)", color="blue", linewidth=2, zorder=2)

            # --- Elementos Visuais da Aproximação ---
            x_esq_aprox = x0 - delta
            x_dir_aprox = x0 + delta
            y_esq_aprox = f_numeric(x_esq_aprox)
            y_dir_aprox = f_numeric(x_dir_aprox)

            ax.scatter([x_esq_aprox, x_dir_aprox], [y_esq_aprox, y_dir_aprox], color='purple', s=80, zorder=5, label=f'Pontos em x₀ ± δ')
            ax.axvline(x0, color='red', linestyle='--', label=f'Análise em x={x0}')

            if limite_val.is_finite:
                L = float(limite_val)
                ax.axhline(L, color='green', linestyle='--', label=f'Limite L={L:.3f}', zorder=1)
                
                ax.plot([x_esq_aprox, x_esq_aprox], [y_esq_aprox, L], color='orange', linestyle='--', lw=2, label='Distância |f(x) - L|')
                ax.plot([x_dir_aprox, x_dir_aprox], [y_dir_aprox, L], color='orange', linestyle='--', lw=2)

                with np.errstate(invalid='ignore'):
                    if not np.isfinite(f_numeric(x0)):
                        ax.scatter(x0, L, facecolors='none', edgecolors='red', s=150, zorder=7, linewidth=2, label=f'f({x0}) é indefinido')
                    else:
                        ax.scatter(x0, L, color='green', s=100, zorder=6, edgecolors='black')

            # Configurações do gráfico
            ax.axhline(0, color='black', linewidth=0.8)
            ax.grid(True, which='both', linestyle=':', linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Aproximação do Limite de f(x) quando x → {x0}")
            ax.set_xlim(-limite_eixo_global, limite_eixo_global)
            ax.set_ylim(-limite_eixo_global, limite_eixo_global)
            ax.set_aspect('equal', adjustable='box')
            handles, labels = ax.get_legend_handles_labels()
            by_label = dict(zip(labels, handles))
            ax.legend(by_label.values(), by_label.keys(), loc='best')
            st.pyplot(fig)

            st.markdown("### Valores da Aproximação")
            col_aprox1, col_aprox2 = st.columns(2)
            col_aprox1.metric(label=f"Valor à esquerda f({x_esq_aprox:.2f})", value=f"{y_esq_aprox:.4f}")
            col_aprox2.metric(label=f"Valor à direita f({x_dir_aprox:.2f})", value=f"{y_dir_aprox:.4f}")
            
            # Guia didático atualizado
            st.markdown("### Como interpretar o gráfico?")
            st.info("""
            **Objetivo:** Use o slider **Proximidade (δ)** para aproximar os **pontos roxos** da **linha vermelha**.

            - O limite existe se, ao fazer isso, o comprimento das **linhas laranjas** diminuir e tender a zero.
            - As linhas laranjas representam a distância vertical dos pontos de aproximação até o valor do limite (a linha verde).
            """)

        # --- LÓGICA PARA LIMITE NO INFINITO ---
        elif limite_tipo == "Limite no Infinito":
            infinito_tipo = st.selectbox("Escolha o infinito:", ["+∞", "-∞"])
            inf_symbol = oo if infinito_tipo == "+∞" else -oo
            
            try:
                limite_val = limit(f_expr, x, inf_symbol)
                st.markdown(fr"$$ \text{{O limite de }} f(x) \text{{ quando }} x \to {latex(inf_symbol)} \text{{ é: }} {latex(limite_val)} $$")
            except Exception as e:
                st.error(f"Erro ao calcular o limite: {e}")
                st.stop()
            
            x_graph_inf = np.linspace(-500, 500, 2000) 
            y_graph_inf = np.array([f_numeric(val) for val in x_graph_inf])
            
            fig, ax = plt.subplots(figsize=(10,6))
            ax.plot(x_graph_inf, y_graph_inf, label="f(x)", color='blue')

            if limite_val.is_finite:
                L = float(limite_val)
                ax.axhline(y=L, color='green', linestyle='dashed', label=f'Assíntota Horizontal y = {L:.2f}')
                ax.set_ylim(L - limite_eixo_global, L + limite_eixo_global)

            ax.axhline(0, color='black', linewidth=0.8)
            ax.grid(True, which='both', linestyle=':', linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.set_title(f"Comportamento de f(x) quando x → {latex(inf_symbol)}")
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao interpretar a função: {str(e)}")


################################## CALCULO 2 ##############################################################

#C2 - TAYLOR===============================================================================================
elif pagina == "taylor":
    st.subheader("📊 Séries de Taylor")
    st.info("(EM BREVE)")


#C2 - INTEGRAL DUPLA=======================================================================================
elif pagina == "integrais_duplas":
    st.subheader("🔁 Integrais Duplas")
    st.info("(EM BREVE)")


#C2 - EQUAÇÕES DIFERENCIAIS==================================================================================
elif pagina == "equacoes_diferenciais":
    st.subheader("🌀 Equações Diferenciais")
    st.info("(EM BREVE)")



################################## CALCULO NUMÉRICO ########################################################

#C.N - PONTO FIXO============================================================================================

elif pagina == "ponto_fixo":
    import sympy as sp
    st.subheader("⮍ Método do Ponto Fixo")

    casas_decimais = st.slider("Número de casas decimais para exibição", 2, 10, 4)

    func_str = st.text_input("Digite a função f(x):", "x**2 - 3*x + 2")
    x = sp.symbols('x')
    f_expr = sp.sympify(func_str)

    if st.button("🔄 Gerar g(x) automaticamente"):
        g_expr_auto = x - f_expr
        st.session_state.g_expr_sugerido = str(g_expr_auto)

    g_default = st.session_state.get("g_expr_sugerido", "(x**2 + 2)/3")
    g_str = st.text_input("Digite a função g(x) (isole x):", g_default)

    try:
        g_expr = sp.sympify(g_str)
        f = sp.lambdify(x, f_expr, 'numpy')
        g = sp.lambdify(x, g_expr, 'numpy')
        g_prime_expr = sp.diff(g_expr, x)
        g_prime = sp.lambdify(x, g_prime_expr, 'numpy')

        x0 = st.number_input("Valor inicial x₀:", value=1.0)
        a = st.number_input("Intervalo de teste: limite inferior (a):", value=x0 - 1.0)
        b = st.number_input("Intervalo de teste: limite superior (b):", value=x0 + 1.0)
        tolerancia = st.number_input("Tolerância:", value=0.0001, format="%.5f")
        max_iter = st.number_input("Número máximo de iterações:", value=20, step=1)

        verifica_funcional = sp.simplify(g_expr - x + f_expr)
        if verifica_funcional != 0:
            st.warning("⚠️ A função g(x) pode não estar corretamente relacionada com f(x) = 0.")

        x_vals = np.linspace(a, b, 500)
        derivadas = np.abs(g_prime(x_vals))
        max_derivada = np.max(derivadas)
        if max_derivada < 1:
            st.success(f"Convergência provável: Máx |g'(x)| = {max_derivada:.4f} < 1")
        else:
            st.warning(f"⚠️ Convergência não garantida: Máx |g'(x)| = {max_derivada:.4f} ≥ 1")

        if abs(g(x0) - x0) > 0.01:
            st.warning("⚠️ A função g(x) pode não ser adequada: g(x₀) está longe de x₀.")

        if st.button("Executar Método do Ponto Fixo"):
            iteracoes = []
            x_atual = x0

            for i in range(max_iter):
                x_novo = g(x_atual)
                fx_n = f(x_novo)
                erro_rel = abs((x_novo - x_atual) / x_novo) * 100 if i > 0 and x_novo != 0 else None
                iteracoes.append((i, x_atual, x_novo, fx_n, erro_rel))
                if erro_rel is not None and erro_rel < tolerancia:
                    break
                x_atual = x_novo

            st.success(f"Aproximação final: {x_novo:.{casas_decimais}f}")

            st.subheader("Iterações passo a passo")
            for i, x_antigo, x_novo, fx_n, erro_rel in iteracoes:
                col1, col2 = st.columns(2)
                with col1:
                    try:
                        x_vals = np.linspace(x0 - 5, x0 + 5, 400)

                        y_f_vals = []
                        y_g_vals = []
                        for v in x_vals:
                            try:
                                f_val = f(v)
                            except:
                                f_val = np.nan

                            try:
                                try:
                                    with np.errstate(over='ignore', invalid='ignore'):
                                        f_val = f(v)
                                except:
                                    f_val = np.nan

                                try:
                                    with np.errstate(over='ignore', invalid='ignore'):
                                        g_val = g(v)
                                except:
                                    g_val = np.nan

                            except:
                                g_val = np.nan

                            if np.isfinite(f_val):
                                y_f_vals.append(f_val)
                            else:
                                y_f_vals.append(np.nan)

                            if np.isfinite(g_val):
                                y_g_vals.append(g_val)
                            else:
                                y_g_vals.append(np.nan)


                        fig, ax = plt.subplots()
                        ax.plot(x_vals, y_f_vals, label="f(x)", color='green')
                        ax.plot(x_vals, y_g_vals, label="g(x)", color='blue')
                        ax.plot(x_vals, x_vals, '--', color='black', label="y = x")

                        try:
                            y_gxn = g(x_antigo)
                            if np.isfinite(y_gxn):
                                ax.plot([x_antigo, x_antigo], [0, y_gxn], color='red', linestyle='--', label='projeção')
                                ax.scatter([x_antigo], [y_gxn], color='red', zorder=5, label=f"x_{{{i+1}}}")
                        except Exception as e:
                            st.warning(f"Não foi possível plotar g(x_antigo): {e}")

                        ax.axhline(0, color='black', linewidth=0.5)
                        ax.axvline(0, color='black', linewidth=0.5)
                        ax.set_xlim(-10, 10)
                        ax.set_ylim(-10, 10)
                        ax.set_xlabel("x")
                        ax.set_ylabel("y")
                        ax.grid(True)
                        ax.legend()
                        ax.set_title(f"Iteração {i+1}")
                        st.pyplot(fig)

                    except Exception as e:
                        st.error(f"Erro ao construir o gráfico: {e}")

                with col2:
                    st.latex(rf"x_{{{i}}} = {x_antigo:.{casas_decimais}f}")
                    st.latex(rf"g(x_{{{i}}}) = {x_novo:.{casas_decimais}f}")
                    st.latex(rf"f(x_{{{i+1}}}) = {fx_n:.{casas_decimais}f}")
                    if erro_rel is not None:
                        st.latex(
                            rf"\text{{Erro relativo}} = \left| \frac{{x_{{{i+1}}} - x_{{{i}}}}}{{x_{{{i+1}}}}} \right| \times 100 = {erro_rel:.{casas_decimais}f}\%"
                        )
                    else:
                        st.latex("—")

            st.subheader("📊 Tabela de Iterações")
            st.dataframe({
                "Iteração": [i for i, *_ in iteracoes],
                "x_n": [x_n for _, x_n, *_ in iteracoes],
                "g(x_n)": [gx for _, _, gx, *_ in iteracoes],
                "f(x_n)": [fx for *_, fx, _ in iteracoes],
                "Erro Relativo (%)": [
                    f"{erro:.{casas_decimais}f}" if erro is not None else "—"
                    for *_, erro in iteracoes
                ]
            })

    except Exception as e:
        st.error(f"Erro ao interpretar a função: {str(e)}")


#C.N - BISSEÇÃO============================================================================================

elif pagina == "bissecao":
    import imageio.v2 as imageio

    st.subheader("🔍 Bisseção")
    
    casas_decimais = st.slider("Número de casas decimais para exibição", 2, 10, 4)

    def criar_funcao(expr):
        def f(x):
            return eval(expr, {"x": x, "np": np, "sin": np.sin, "cos": np.cos,
                               "tan": np.tan, "exp": np.exp, "log": np.log,
                               "sqrt": np.sqrt, "pi": np.pi, "e": np.e, "__builtins__": {}})
        return f

    def bissecao(f, a, b, tol=1e-6, max_iter=100):
        if f(a) * f(b) >= 0:
            raise ValueError("O intervalo [a, b] não contem uma mudança de sinal (f(a)*f(b) < 0).")
        iteracoes = []
        iter_count = 0
        erro = None
        while (b - a) / 2 > tol and iter_count < max_iter:
            c = (a + b) / 2
            erro = abs(b - a) / 2
            if len(iteracoes) > 0:
                c_anterior = iteracoes[-1][3]  # o último c da lista
                erro_rel = abs((c - c_anterior) / c) * 100 if c != 0 else None
            else:
                erro_rel = None

            iteracoes.append((iter_count, a, b, c, f(a), f(b), f(c), erro, erro_rel))
            if abs(f(c)) < tol:
                break
            if f(c) * f(a) < 0:
                b = c
            else:
                a = c
            iter_count += 1
        return (a + b) / 2, iteracoes

    expr = st.text_input("Digite a função f(x):", value="x**3 - x - 2")

    if expr:
        try:
            func = criar_funcao(expr)

            st.markdown("### Escolha do intervalo [a, b]")
            a = st.number_input("Valor de a:", value=1.0)
            b = st.number_input("Valor de b:", value=2.0)
            tol = st.number_input("Tolerância:", value=1e-6, format="%.10f")
            max_iter = st.number_input("Máximo de iterações:", value=50, step=1)

            if st.button("Executar Método da Bisseção"):
                try:
                    raiz, iteracoes = bissecao(func, a, b, tol, max_iter)
                    st.success(f"Raiz aproximada: {raiz:.10f}")

                    st.markdown("### Iterações passo a passo")
                    for i, (it, a_i, b_i, c_i, fa, fb, fc, erro, erro_rel) in enumerate(iteracoes):
                        col1, col2 = st.columns(2)
                        with col1:
                            fig, ax = plt.subplots()
                            x_vals = np.linspace(-10, 10, 1000)
                            y_vals = [func(x) for x in x_vals]
                            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
                            ax.axhline(0, color='black')
                            ax.axvline(a_i, color='green', linestyle='--', label='a')
                            ax.axvline(b_i, color='red', linestyle='--', label='b')
                            ax.axvline(c_i, color='orange', linestyle='--', label='c')
                            ax.set_xlim(-10, 10)
                            ax.set_ylim(-10, 10)
                            ax.legend()
                            ax.set_title(f"Iteração {i + 1}")
                            ax.grid(True)
                            st.pyplot(fig)
                        with col2:
                            st.latex(rf"a_{{{i+1}}} = {a_i:.6f} \,\quad b_{{{i+1}}} = {b_i:.6f}")
                            st.latex(rf"f(a_{{{i+1}}}) = {fa:.6f} \,\quad f(b_{{{i+1}}}) = {fb:.6f}")
                            st.latex(rf"c_{{{i+1}}} = \frac{{a_{{{i+1}}} + b_{{{i+1}}}}}{{2}} = {c_i:.6f}")
                            st.latex(rf"f(c_{{{i+1}}}) = {fc:.6f}")
                            if erro_rel is not None:
                                st.latex(rf"\text{{Erro relativo}} = \left| \frac{{c_{{{i+1}}} - c_{{{i}}}}}{{c_{{{i+1}}}}} \right| \times 100 = {erro_rel:.{casas_decimais}f}\%")
                            else:
                                st.latex("-----")

                except Exception as e:
                    st.error(f"Erro durante a execução do método: {str(e)}")

                st.subheader("📊 Tabela de Iterações")
                st.dataframe({
                    "Iteração": [it[0] for it in iteracoes],
                    "a": [it[1] for it in iteracoes],
                    "b": [it[2] for it in iteracoes],
                    "c": [it[3] for it in iteracoes],
                    "f(a)": [it[4] for it in iteracoes],
                    "f(b)": [it[5] for it in iteracoes],
                    "f(c)": [it[6] for it in iteracoes],
                    "Erro relativo (%)": [
                            f"{it[8]:.{casas_decimais}f}" if it[8] is not None else "—" for it in iteracoes
                        ]                    
                })


        except Exception as e:
            st.error(f"Erro ao interpretar a função: {str(e)}")


#C.N - FALSA POSIÇÃO==========================================================================================
elif pagina == "falsa_posicao":
    import imageio.v2 as imageio

    st.subheader("🟰 Falsa Posição (Regula Falsi)")

    casas_decimais = st.slider("Número de casas decimais para exibição", 2, 10, 4)

    def criar_funcao(expr):
        def f(x):
            return eval(expr, {"x": x, "np": np, "sin": np.sin, "cos": np.cos,
                               "tan": np.tan, "exp": np.exp, "log": np.log,
                               "sqrt": np.sqrt, "pi": np.pi, "e": np.e, "__builtins__": {}})
        return f

    def falsa_posicao(f, a, b, tol=1e-6, max_iter=100):
        if f(a) * f(b) >= 0:
            raise ValueError("O intervalo [a, b] não contém uma mudança de sinal.")

        iteracoes = []
        c_anterior = None

        for i in range(max_iter):
            fa = f(a)
            fb = f(b)
            c = (a * fb - b * fa) / (fb - fa)
            fc = f(c)

            if c_anterior is None:
                erro_rel = None
            else:
                erro_rel = abs((c - c_anterior) / c) * 100 if c != 0 else None

            iteracoes.append((i, a, b, c, fa, fb, fc, erro_rel))

            if erro_rel is not None and erro_rel < tol:
                break

            if fa * fc < 0:
                b = c
            else:
                a = c

            c_anterior = c

        return c, iteracoes

    expr = st.text_input("Digite a função f(x):", value="x**3 - x - 2")

    if expr:
        try:
            func = criar_funcao(expr)

            st.markdown("### Escolha do intervalo [a, b] e parâmetros")
            a = st.number_input("Valor de a:", value=1.0)
            b = st.number_input("Valor de b:", value=2.0)
            tol = st.number_input("Tolerância:", value=1e-6, format="%.10f")
            max_iter = st.number_input("Máximo de iterações:", value=50, step=1)

            x_vals = np.linspace(-10, 10, 1000)
            y_vals = [func(x) for x in x_vals]

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
            ax.axhline(0, color='black', linewidth=1)
            ax.axvline(0, color='black', linewidth=1)
            ax.axvline(a, color='green', linestyle='--', label=f'a = {a}')
            ax.axvline(b, color='red', linestyle='--', label=f'b = {b}')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.set_title("Gráfico de f(x) e intervalo inicial")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            if st.button("Executar Método da Falsa Posição"):
                try:
                    raiz, iteracoes = falsa_posicao(func, a, b, tol, max_iter)
                    st.success(f"Raiz aproximada: {raiz:.10f}")

                    st.markdown("### Iterações passo a passo")
                    for i, a_i, b_i, c_i, fa, fb, fc, erro_rel in iteracoes:
                        col1, col2 = st.columns(2)
                        with col1:
                            fig, ax = plt.subplots()
                            x_vals = np.linspace(-10, 10, 1000)
                            y_vals = [func(x) for x in x_vals]
                            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
                            ax.axhline(0, color='black')
                            ax.axvline(a_i, color='green', linestyle='--', label='a')
                            ax.axvline(b_i, color='red', linestyle='--', label='b')
                            ax.axvline(c_i, color='orange', linestyle='--', label='c')
                            ax.plot([a_i, b_i], [fa, fb], 'r--', label='secante')
                            ax.set_xlim(-10, 10)
                            ax.set_ylim(-10, 10)
                            ax.set_title(f"Iteração {i+1}")
                            ax.grid(True)
                            ax.legend()
                            st.pyplot(fig)
                        with col2:
                            st.latex(rf"a_{{{i+1}}} = {a_i:.6f} \,\quad b_{{{i+1}}} = {b_i:.6f}")
                            st.latex(rf"f(a_{{{i+1}}}) = {fa:.6f} \,\quad f(b_{{{i+1}}}) = {fb:.6f}")
                            st.latex(rf"c_{{{i+1}}} = \frac{{a f(b) - b f(a)}}{{f(b) - f(a)}} = {c_i:.6f}")
                            st.latex(rf"f(c_{{{i+1}}}) = {fc:.6f}")
                            if erro_rel is not None:
                                st.latex(rf"\text{{Erro relativo}} = \left| \frac{{c_{{{i+1}}} - c_{{{i}}}}}{{c_{{{i+1}}}}} \right| \times 100 = {erro_rel:.{casas_decimais}f}\%")
                            else:
                                st.latex("-----")

                    st.subheader("📊 Tabela de Iterações")
                    st.dataframe({
                        "Iteração": [i[0] for i in iteracoes],
                        "a": [i[1] for i in iteracoes],
                        "b": [i[2] for i in iteracoes],
                        "c": [i[3] for i in iteracoes],
                        "f(a)": [i[4] for i in iteracoes],
                        "f(b)": [i[5] for i in iteracoes],
                        "f(c)": [i[6] for i in iteracoes],
                        "Erro relativo (%)": [
                            f"{i[7]:.{casas_decimais}f}" if i[7] is not None else "—" for i in iteracoes
                        ]
                    })

                except Exception as e:
                    st.error(f"Erro durante a execução do método: {str(e)}")

        except Exception as e:
            st.error(f"Erro ao interpretar a função: {str(e)}")




#C.N - MÉTODO GRAFICO=========================================================================================
elif pagina == "metodo_grafico":
    st.subheader("📉 Método Gráfico")

    func_str = st.text_input("Digite a função f(x):", value="x**2 - 4")

    try:
        x = sp.symbols('x')
        func_expr = sp.sympify(func_str)
        func = sp.lambdify(x, func_expr, 'numpy')

        st.markdown("### Intervalo de destaque (opcional)")
        a = st.number_input("x mínimo do intervalo destacado:", value=-1.0)
        b = st.number_input("x máximo do intervalo destacado:", value=2.0)

        x_vals = np.linspace(-10, 10, 1000)
        y_vals = func(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f'f(x) = {func_str}', color='blue')
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.axvline(a, color='green', linestyle='--', label='x mínimo (a)')
        ax.axvline(b, color='red', linestyle='--', label='x máximo (b)')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)

        st.markdown("### 🎯 Adivinhe uma raiz da função!")
        palpite = st.number_input("Qual o valor de x que você acha ser uma raiz da função?", value=0.0)

        y_palpite = func(palpite)
        st.write(f"Em x = {palpite}, f(x) = {y_palpite:.4f}")

        if abs(y_palpite) < 0.01:
            st.success("🎉 Parabéns! Seu palpite está muito próximo de uma raiz.")
        else:
            st.warning("🤔 Ainda não é uma raiz exata. Continue tentando!")

        st.markdown("### 🔎 Zoom na região do seu chute")
        x_zoom = np.linspace(palpite - 1, palpite + 1, 500)
        y_zoom = func(x_zoom)
        fig_zoom, ax_zoom = plt.subplots()
        ax_zoom.plot(x_zoom, y_zoom, label='Função real', color='blue')
        ax_zoom.axhline(0, color='black', linewidth=0.5)
        ax_zoom.axvline(palpite, color='orange', linestyle='--', label='Seu chute')
        ax_zoom.set_title(f'Zoom em x = {palpite}')
        ax_zoom.legend()
        ax_zoom.grid(True)
        st.pyplot(fig_zoom)

    except Exception as e:
        st.error(f"Erro ao processar a função: {str(e)}")


#C.N - MÉTODO SECANTE=========================================================================================
elif pagina == "secante":
    import sympy as sp
    import io
    import imageio.v2 as imageio

    st.subheader("⚙️ Método da Secante")

    casas_decimais = st.slider("Número de casas decimais para exibição", 2, 10, 4)

    func_str = st.text_input("Digite a função f(x):", "x**3 - x - 2")

    try:
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x, f_expr, 'numpy')

        x0 = st.number_input("Digite o valor inicial x₀:", value=1.0)
        x1 = st.number_input("Digite o segundo valor inicial x₁:", value=2.0)
        tolerancia = st.number_input("Tolerância:", value=0.0001, format="%.5f")
        max_iter = st.number_input("Número máximo de iterações:", value=20, step=1)

        if st.button("Executar Método da Secante"):
            iteracoes = []
            imagens = []

            for i in range(max_iter):
                f_x0 = f(x0)
                f_x1 = f(x1)

                if f_x1 - f_x0 == 0:
                    st.error(f"Divisão por zero na iteração {i}. Interrompendo.")
                    break

                x2 = x1 - f_x1 * (x1 - x0) / (f_x1 - f_x0)
                erro_rel = abs((x2 - x1) / x2) * 100 if i > 0 and x2 != 0 else None

                iteracoes.append((i, x0, x1, x2, f_x0, f_x1, erro_rel))

                if erro_rel is not None and erro_rel < tolerancia:
                    break

                x0, x1 = x1, x2

            st.success(f"Aproximação final da raiz: {x2:.{casas_decimais}f}")
            st.subheader("Iterações passo a passo")

            for i, x0_i, x1_i, x2_i, fx0, fx1, erro_rel in iteracoes:
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    x_vals = np.linspace(-10, 10, 400)
                    y_vals = [f(val) for val in x_vals]
                    ax.plot(x_vals, y_vals, label="f(x)", color='blue')
                    ax.axhline(0, color='black', linewidth=0.5)
                    ax.axvline(0, color='black', linewidth=0.5)
                    ax.plot([x0_i, x1_i], [fx0, fx1], 'r--', label='Reta Secante')
                    ax.plot(x2_i, 0, 'ro', label=f"x_{i+2}")
                    ax.set_xlim(-10, 10)
                    ax.set_ylim(-10, 10)
                    ax.grid(True)
                    ax.legend()
                    ax.set_title(f"Iteração {i + 1}")
                    st.pyplot(fig)

                with col2:
                    st.latex(rf"x_{{{i}}} = {x0_i:.{casas_decimais}f}, \quad x_{{{i+1}}} = {x1_i:.{casas_decimais}f}")
                    st.latex(rf"f(x_{{{i}}}) = {fx0:.{casas_decimais}f}, \quad f(x_{{{i+1}}}) = {fx1:.{casas_decimais}f}")
                    st.latex(rf"x_{{{i+2}}} = x_{{{i+1}}} - \frac{{f(x_{{{i+1}}})(x_{{{i+1}}} - x_{{{i}}})}}{{f(x_{{{i+1}}}) - f(x_{{{i}}})}} = {x2_i:.{casas_decimais}f}")
                    if erro_rel is not None:
                        st.latex(
                            rf"\text{{Erro relativo}} = \left| \frac{{x_{{{i+2}}} - x_{{{i+1}}}}}{{x_{{{i+2}}}}} \right| \times 100 = {erro_rel:.{casas_decimais}f}\%"
                        )
                    else:
                        st.latex("—")

                # salvar imagem para gif
                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                imagens.append(imageio.imread(buf))
                plt.close(fig)

            if imagens:
                st.subheader("Animação do processo:")
                gif_path = "/tmp/secante_iteracoes.gif"
                imageio.mimsave(gif_path, imagens, fps=1)
                with open(gif_path, "rb") as f:
                    gif_bytes = f.read()
                st.image(gif_bytes)

            # TABELA DE ITERAÇÕES
            st.subheader("📊 Tabela de Iterações")
            st.dataframe({
                "Iteração": [i for i, *_ in iteracoes],
                "x_n-1": [x0_i for _, x0_i, *_ in iteracoes],
                "x_n": [x1_i for _, _, x1_i, *_ in iteracoes],
                "x_n+1": [x2_i for _, _, _, x2_i, *_ in iteracoes],
                "f(x_n-1)": [fx0 for _, _, _, _, fx0, *_ in iteracoes],
                "f(x_n)": [fx1 for _, _, _, _, _, fx1, *_ in iteracoes],
                "Erro Relativo (%)": [
                    f"{erro:.{casas_decimais}f}" if erro is not None else "—"
                    for *_, erro in iteracoes
                ]
            })

    except Exception as e:
        st.error(f"Erro ao processar a função: {str(e)}")


#C.N - MÉTODO NEWTON==========================================================================================
elif pagina == "newton":
    import io
    import imageio.v2 as imageio
    from sympy import symbols, diff, lambdify, sympify

    st.subheader("⚙️ Método de Newton - Visualização Iterativa")

    casas_decimais = st.slider("Número de casas decimais para exibição", 2, 10, 4)

    funcao = st.text_input("Digite a função f(x):", value="x**2 - 2")

    if funcao:
        x = symbols('x')
        f_expr = sympify(funcao)
        f_prime_expr = diff(f_expr, x)

        f = lambdify(x, f_expr, 'numpy')
        f_prime = lambdify(x, f_prime_expr, 'numpy')

        x_vals = np.linspace(-10, 10, 400)
        try:
            y_vals = f(x_vals)
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label=f'f(x) = {funcao}')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_title('Gráfico da Função')
            ax.legend()
            st.pyplot(fig)
        except:
            st.error("Erro ao tentar avaliar a função. Verifique a sintaxe.")
            st.stop()

        x0 = st.number_input("Digite o valor inicial x₀:", value=1.0)
        tolerancia = st.number_input("Digite a tolerância:", value=0.0001, format="%.5f")
        max_iter = st.number_input("Número máximo de iterações:", value=10, step=1)

        if st.button("Executar Método de Newton"):
            iteracoes = []
            x_atual = x0

            for i in range(max_iter):
                f_x = f(x_atual)
                f_deriv = f_prime(x_atual)

                if f_deriv == 0:
                    st.error(f"Derivada nula em x = {x_atual}. Método interrompido.")
                    break

                x_novo = x_atual - f_x / f_deriv
                erro_rel = abs((x_novo - x_atual) / x_novo) * 100 if i > 0 and x_novo != 0 else None

                iteracoes.append({
                    'i': i,
                    'x_n': x_atual,
                    'f(x_n)': f_x,
                    "f'(x_n)": f_deriv,
                    'x_{n+1}': x_novo,
                    'erro_rel': erro_rel
                })

                if erro_rel is not None and erro_rel < tolerancia:
                    break

                x_atual = x_novo

            st.subheader("Iterações passo a passo")
            imagens = []

            for it in iteracoes:
                i = it['i']
                x_n = it['x_n']
                fx = it['f(x_n)']
                dfx = it["f'(x_n)"]
                x_n1 = it['x_{n+1}']
                erro = it['erro_rel']
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    ax.plot(x_vals, f(x_vals), label='f(x)', color='blue')
                    tangente = lambda x_val: dfx * (x_val - x_n) + fx
                    ax.plot(x_vals, tangente(x_vals), 'g--', label='Tangente')
                    ax.plot(x_n, fx, 'ro', label=f'x{i+1}')
                    ax.plot(x_n1, 0, 'bo', label=f'x{i+2}')
                    ax.plot([x_n1, x_n1], [0, f(x_n1)], 'k--', linewidth=1)
                    ax.axhline(0, color='black', linewidth=0.5)
                    ax.axvline(0, color='black', linewidth=0.5)
                    ax.set_xlim(-10, 10)
                    ax.set_ylim(-10, 10)
                    ax.set_title(f"Iteração {i + 1}")
                    ax.legend()
                    ax.grid(True)
                    st.pyplot(fig)

                with col2:
                    st.latex(rf"x_{{{i}}} = {x_n:.{casas_decimais}f}")
                    st.latex(rf"f(x_{{{i}}}) = {fx:.{casas_decimais}f}")
                    st.latex(rf"f'(x_{{{i}}}) = {dfx:.{casas_decimais}f}")
                    st.latex(rf"x_{{{i+1}}} = x_{{{i}}} - \frac{{f(x_{{{i}}})}}{{f'(x_{{{i}}})}} = {x_n1:.{casas_decimais}f}")
                    if erro is not None:
                        st.latex(
                            rf"\text{{Erro relativo}} = \left| \frac{{x_{{{i+1}}} - x_{{{i}}}}}{{x_{{{i+1}}}}} \right| \times 100 = {erro:.{casas_decimais}f}\%"
                        )
                    else:
                        st.latex("—")

                buf = io.BytesIO()
                fig.savefig(buf, format='png')
                buf.seek(0)
                imagens.append(imageio.imread(buf))
                plt.close(fig)

            if imagens:
                st.subheader("Animação do processo:")
                gif_path = "/tmp/newton_iteracoes.gif"
                imageio.mimsave(gif_path, imagens, fps=1)
                with open(gif_path, "rb") as f:
                    gif_bytes = f.read()
                st.image(gif_bytes)

            st.subheader("📊 Tabela de Iterações")
            st.dataframe({
                "Iteração": [it['i'] for it in iteracoes],
                "x_n": [it['x_n'] for it in iteracoes],
                "f(x_n)": [it['f(x_n)'] for it in iteracoes],
                "f'(x_n)": [it["f'(x_n)"] for it in iteracoes],
                "x_{n+1}": [it['x_{n+1}'] for it in iteracoes],
                "Erro Relativo (%)": [
                    f"{it['erro_rel']:.{casas_decimais}f}" if it['erro_rel'] is not None else "—"
                    for it in iteracoes
                ]
            })


#C.N - MÉTODO JACOBI==========================================================================================
elif pagina == "jacobi":
    st.subheader("🧶 Método de Jacobi-Richardson")
    st.markdown("""
        <style>
        div[data-testid="stTextInput"] {
            width: 50px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stTextInput"] input {
            width: 100% !important;
            text-align: center;
            font-size: 14px;
            padding: 2px 4px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("Escolha o tamanho do sistema e preencha os coeficientes da matriz A e do vetor b:")
    n = st.number_input("Tamanho do sistema (n x n):", min_value=2, max_value=10, value=3)

    st.markdown("### Sistema linear (matriz A | vetor b):")
    A = np.zeros((n, n))
    b = np.zeros(n)

    with st.container():
        col_central = st.columns([0.25, 0.5, 0.25])[1]
        with col_central:
            for i in range(n):
                linha = st.columns(n + 2, gap="small") 
                for j in range(n):
                    with linha[j]:
                        val = st.text_input(f"A{i}{j}", value="0", key=f"A_{i}_{j}", label_visibility="collapsed")
                        try:
                            A[i][j] = float(val.replace(",", "."))
                        except:
                            A[i][j] = 0.0
                with linha[n]:
                    st.markdown("**|**", unsafe_allow_html=True)
                with linha[n + 1]:
                    val_b = st.text_input(f"b{i}", value="0", key=f"b_{i}", label_visibility="collapsed")
                    try:
                        b[i] = float(val_b.replace(",", "."))
                    except:
                        b[i] = 0.0

    tol = st.number_input("Tolerância:", value=0.0000001, format="%.12f")
    max_iter = st.number_input("Número máximo de iterações:", value=100, step=1)
    casas = st.slider("Casas decimais:", 2, 10, 4)

    if st.button("Executar Método de Jacobi"):
        try:
            dominante = True
            for i in range(n):
                diag = abs(A[i][i])
                soma_outros = np.sum(np.abs(A[i])) - diag
                if diag <= soma_outros:
                    dominante = False
                    break

            if dominante:
                st.success("✅ A matriz A é diagonal dominante. O método deve convergir.")
            else:
                st.warning("⚠️ A matriz A NÃO é diagonal dominante. O método pode não convergir.")

            D = np.diag(A)
            R = A - np.diagflat(D)
            x = np.zeros_like(b)
            iteracoes = []

            st.subheader("🔍 Passo a passo das iterações")
            for k in range(1, max_iter + 1):
                x_novo = (b - np.dot(R, x)) / D
                erro_iter = np.linalg.norm(x_novo - x, ord=np.inf)
                erro_relativo = erro_iter / (np.linalg.norm(x_novo, ord=np.inf) + 1e-12)

                iteracoes.append({
                    "Iteracao": k,
                    "x": x_novo.copy(),
                    "Erro It": erro_iter,
                    "Relativo": erro_relativo
                })

                with st.expander(f"🔹 Iteração {k}"):
                    for i in range(n):
                        soma = " + ".join([f"{A[i][j]:.2f} ⋅ {x[j]:.{casas}f}" for j in range(n) if j != i])
                        st.latex(
                            rf"x_{{{i+1}}}^{{({k})}} = \frac{{1}}{{{A[i][i]:.2f}}} ( {b[i]:.2f} - ( {soma} ) ) = {x_novo[i]:.{casas}f}"
                        )
                    st.latex(rf"\|x^{{({k})}} - x^{{({k-1})}}\|_\infty = {erro_iter:.{casas}f}")
                    st.latex(rf"\text{{Erro relativo}} = \frac{{\|x^{{({k})}} - x^{{({k-1})}}\|_\infty}}{{\|x^{{({k})}}\|_\infty}} = {erro_relativo:.{casas}f}")

                if erro_relativo < tol:
                    break
                x = x_novo

            st.success(f"Solução aproximada após {len(iteracoes)} iterações:")
            for i, val in enumerate(x_novo):
                st.latex(f"x_{{{i+1}}} = {val:.{casas}f}")

            st.subheader("📊 Tabela de Iterações")
            tabela = {
                "Iteração": [it["Iteracao"] for it in iteracoes],
                **{f"x{i+1}": [round(it["x"][i], casas) for it in iteracoes] for i in range(n)},
                "Erro It": [round(it["Erro It"], casas) for it in iteracoes],
                "Relativo": [round(it["Relativo"], casas) for it in iteracoes]
            }
            st.dataframe(tabela)

            st.subheader("🧪 Verificação da Solução")
            b_calc = np.dot(A, x_novo)
            for i in range(n):
                st.latex(
                    f"Ax_{{{i+1}}} = {b_calc[i]:.{casas}f} \\Rightarrow\\ b_{{{i+1}}} = {b[i]:.{casas}f} \\Rightarrow\\ |erro| = {abs(b[i] - b_calc[i]):.{casas}f}"
                )

        except Exception as e:
            st.error(f"Erro: {str(e)}")

        try:
            x_exata = np.linalg.solve(A, b)
            st.subheader("🌟 Comparação com solução exata (np.linalg.solve):")
            for i in range(n):
                erro_abs = abs(x_exata[i] - x_novo[i])
                st.latex(
                    rf"x_{{{i+1}}} \approx {x_novo[i]:.{casas}f} \;\; \text{{vs}} \;\; x_{{{i+1}}}^* = {x_exata[i]:.{casas}f} \Rightarrow \left| \text{{erro}} \right| = {erro_abs:.{casas}f}"
                )
        except:
            st.info("Não foi possível calcular a solução exata com numpy (sistema talvez mal definido).")
