# calculadora_streamlit.py

#bibliotecas-----------------------------------------------------------------------------------------
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
from sympy import symbols

#titulo da pagina------------------------------------------------------------------------------------
st.set_page_config(layout="wide")
st.markdown("""
    <h1 style='text-align: center;'>🧠 Cálculo (Dora)</h1>
    <hr style='border: 1px solid #ccc;' />
""", unsafe_allow_html=True)

#Menu lateral----------------------------------------------------------------------------------------
if 'pagina_atual' not in st.session_state:
    st.session_state.pagina_atual = 'home'

with st.sidebar:
    st.markdown("### 🧭 Navegação")
    if st.button("🏠 Início"):
        st.session_state.pagina_atual = "home"
    with st.expander("EXEMPLOS"):
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

        
# Conteúdo principal == métodos =========================================================================

pagina = st.session_state.pagina_atual

#HOME=====================================================================================================

if pagina == "home":
    st.subheader("🏠 Bem-vindo ao Cálculo (Dora)!")
    st.markdown("---")

    st.info("""
    Este site foi desenvolvido para ser um **ambiente completo de apoio** no estudo de:
    """)

    st.success("""
    📘 **Cálculo 1**:
    - Derivadas
    - Integrais
    - Limites
    """)

    st.success("""
    📙 **Cálculo 2**:
    - Séries de Taylor
    - Integrais Duplas
    - Equações Diferenciais
    """)

    st.success("""
    📗 **Cálculo Numérico**:
    - Método Gráfico
    - Método da Bisseção
    - Método da Falsa Posição
    - Método do Ponto Fixo
    - Método de Newton
    - Método da Secante
    """)

    st.markdown("---")
    st.caption("🚀 Projeto desenvolvido por **Lucas Matias**.")

################################## EXEMPLOS ###############################################################

#EX - BISSEÇÃO==============================================================================================

elif pagina == "ex_bissecao":
    st.subheader("📊 Exemplo: Método da Bisseção")
    st.info("Este vídeo mostra a aplicação gráfica do método da bisseção.")

    st.markdown("### 🎬 Assista ao vídeo:")
    with open("BissecaoDividido.mp4", "rb") as f:
        video_bytes = f.read()
        st.video(video_bytes)


#EX -FALSA POSIÇÃO=========================================================================================

elif pagina == "ex_falsaposicao":
    st.subheader("📊 Exemplo: Método da Falsa Posição")
    st.info("Este vídeo mostra a aplicação gráfica do método da falsa posição.")

    st.markdown("### 🎬 Assista ao vídeo:")
    with open("FalsaPosicaoDividido.mp4", "rb") as f:
        video_bytes = f.read()
        st.video(video_bytes)


################################## CALCULO 1 ##############################################################

#C1 - DERIVADA==============================================================================================

elif pagina == "derivadas":
    import sympy as sp

    st.subheader("✏️ Calculadora de Derivadas")

    func_str = st.text_input("Digite a função f(x):", "x**2")

    try:
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        f = sp.lambdify(x, f_expr, 'numpy')
        df_expr = sp.diff(f_expr, x)
        df_expr_simplified = sp.simplify(df_expr)
        df = sp.lambdify(x, df_expr, 'numpy')

        st.success(f"A derivada da função $f(x) = {func_str}$ é:")
        st.latex(r"f'(x) = " + sp.latex(df_expr_simplified))

        x0 = st.slider("Escolha o ponto x₀:", -5.0, 5.0, 0.0, step=0.1)

        f_x0 = f(x0)
        df_x0 = df(x0)

        x_vals = np.linspace(-5, 5, 400)
        y_vals = f(x_vals)
        df_vals = df(x_vals)

        tangent_line = df_x0 * (x_vals - x0) + f_x0

        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
            ax.plot(x_vals, df_vals, label="f'(x)", color='green', linestyle='dashed')
            ax.plot(x_vals, tangent_line, label="Reta Tangente", color='red', linestyle='dotted')
            ax.scatter([x0], [f_x0], color='black', zorder=3, label="Ponto de Tangência")
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)
            ax.set_xlabel("x")
            ax.set_ylabel("y")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        with col2:
            st.markdown("### 📄 Valores no ponto escolhido")
            st.latex(r"f(x_0) = " + f"{f_x0:.4f}")
            st.latex(r"f'(x_0) = " + f"{df_x0:.4f}")

    except Exception as e:
        st.error(f"Erro ao interpretar a função: {str(e)}")


#C1 - INTEGRAL==============================================================================================

elif pagina == "integrais":
    import sympy as sp
    from sympy import sympify, lambdify, integrate, Rational
    from matplotlib.patches import Rectangle

    st.subheader("📐 Aproximação de Integrais com Retângulos")

    user_input = st.text_input("Digite a função f(x):", "x^2")

    try:
        x = sp.symbols('x')
        func_sympy = sympify(user_input)
        func = lambdify('x', func_sympy, 'numpy')

        a = st.number_input("Limite inferior (a):", value=0)
        b = st.number_input("Limite superior (b):", value=5)

        if 'show_integral_graph' not in st.session_state:
            st.session_state.show_integral_graph = False
        if 'n_rects' not in st.session_state:
            st.session_state.n_rects = 10

        if st.button("Calcular Integral"):
            st.session_state.show_integral_graph = True

        if st.session_state.show_integral_graph:
            n = st.slider("Número de retângulos:", 1, 100, st.session_state.n_rects)
            st.session_state.n_rects = n

            def plot_function_and_rectangles(func, a, b, n):
                x_vals = np.linspace(a, b, 500)
                y_vals = func(x_vals)

                fig, ax = plt.subplots(1, 2, figsize=(14, 6))

                # Função original
                ax[0].plot(x_vals, y_vals, label="f(x)", color="blue")
                ax[0].fill_between(x_vals, y_vals, color='skyblue', alpha=0.5)
                ax[0].set_title("Função e área sob a curva")
                ax[0].set_xlabel("x")
                ax[0].set_ylabel("f(x)")
                ax[0].grid(True)
                ax[0].legend()

                # Aproximação com retângulos
                if n > 0:
                    dx = (b - a) / n
                    for i in range(n):
                        x0 = a + i * dx
                        x_mid = x0 + dx/2
                        y0 = func(x_mid)
                        ax[1].add_patch(Rectangle((x0, 0), dx, y0, edgecolor="black", facecolor="orange", alpha=0.6))

                ax[1].plot(x_vals, y_vals, label="f(x)", color="blue")
                ax[1].set_xlim(a, b)
                ax[1].set_ylim(0, np.max(y_vals) + 1)
                ax[1].set_title(f"Aproximação com {n} retângulos")
                ax[1].set_xlabel("x")
                ax[1].set_ylabel("f(x)")
                ax[1].grid(True)
                ax[1].legend()

                plt.tight_layout()
                return fig

            def approximate_integral(func, a, b, n):
                if n == 0:
                    return 0
                dx = (b - a) / n
                x_mids = np.linspace(a + dx/2, b - dx/2, n)
                y_mids = func(x_mids)
                return np.sum(y_mids * dx)

            fig = plot_function_and_rectangles(func, a, b, n)
            st.pyplot(fig)

            area_aproximada = approximate_integral(func, a, b, n)
            st.success(f"A área aproximada sob a curva é: {area_aproximada:.4f}")

            integral_exata = integrate(func_sympy, (x, a, b))
            st.info(f"O valor exato da integral é: {integral_exata.evalf()}")

            if isinstance(integral_exata, Rational):
                st.info(f"Forma fracionária da integral: {integral_exata}")

        if st.button("Mostrar Solução Teórica"):
            st.subheader("📄 Explicação Passo a Passo")
            st.write("**Passo 1: Definição da Integral**")
            st.latex(r"\int_a^b f(x) \, dx")

            st.write("**Passo 2: Integral Indefinida**")
            integral_indef = integrate(func_sympy, x)
            st.latex(r"\int f(x) \, dx = " + str(integral_indef))

            st.write("**Passo 3: Aplicação dos Limites**")
            F_b = integral_indef.subs(x, b)
            F_a = integral_indef.subs(x, a)
            st.latex(r"F(b) = " + str(F_b))
            st.latex(r"F(a) = " + str(F_a))

            st.write("**Passo 4: Cálculo da Área**")
            area_exata = F_b - F_a
            st.latex(r"\text{Área} = F(b) - F(a) = " + str(area_exata))

    except Exception as e:
        st.error(f"Erro ao processar a função: {str(e)}")


#C1 - LIMITES================================================================================================

elif pagina == "limites":
    import sympy as sp

    st.subheader("📏 Cálculo de Limites")

    func_str = st.text_input("Digite a função f(x):", "(1 - cos(x))/(2*sin(x)**2)")

    try:
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)

        limite_tipo = st.selectbox("Escolha o tipo de limite:", ["Limite Finito", "Limite no Infinito"])

        if limite_tipo == "Limite Finito":
            x0 = st.slider("Escolha o ponto x₀:", -5.0, 5.0, 0.0, step=0.1)

            try:
                limite = sp.limit(f_expr, x, x0)
                st.success(f"O limite de $f(x)$ quando $x \\to {x0}$ é:")
                st.latex(f"\\lim_{{x \\to {x0}}} f(x) = {limite}")
            except Exception as e:
                st.error(f"Erro ao calcular o limite: {e}")
                st.stop()

            # Gráfico
            x_vals = np.linspace(-5, 5, 400)
            y_vals = []

            for val in x_vals:
                try:
                    y = f_expr.subs(x, val)
                    if y == sp.oo or y == -sp.oo or np.isnan(float(y)):
                        y_vals.append(np.nan)
                    else:
                        y_vals.append(float(y))
                except:
                    y_vals.append(np.nan)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            # Destacar o ponto de limite
            try:
                limite_y = float(f_expr.subs(x, x0))
                ax.scatter([x0], [limite_y], color='red', zorder=5, label=f'Limite em x = {x0}')
                ax.plot([x0, x0], [0, limite_y], color='red', linestyle='--')
                ax.plot([0, x0], [limite_y, limite_y], color='green', linestyle='--')
            except:
                pass

            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        elif limite_tipo == "Limite no Infinito":
            infinito_tipo = st.selectbox("Escolha o infinito:", ["+∞", "-∞"])

            try:
                if infinito_tipo == "+∞":
                    limite = sp.limit(f_expr, x, sp.oo)
                else:
                    limite = sp.limit(f_expr, x, -sp.oo)

                st.success(f"O limite de $f(x)$ quando $x \\to {infinito_tipo}$ é:")
                st.latex(f"\\lim_{{x \\to {infinito_tipo}}} f(x) = {limite}")
            except Exception as e:
                st.error(f"Erro ao calcular o limite: {e}")
                st.stop()

            # Gráfico
            x_vals = np.linspace(-5, 5, 400)
            y_vals = []

            for val in x_vals:
                try:
                    y = f_expr.subs(x, val)
                    if y == sp.oo or y == -sp.oo or np.isnan(float(y)):
                        y_vals.append(np.nan)
                    else:
                        y_vals.append(float(y))
                except:
                    y_vals.append(np.nan)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            # Linha horizontal para o limite
            if limite != sp.oo and limite != -sp.oo:
                ax.axhline(y=float(limite), color='green', linestyle='dashed', label=f'Limite: {limite}')

            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao interpretar a função: {str(e)}")



################################## CALCULO 2 ##############################################################

#C2 - TAYLOR===============================================================================================
elif pagina == "taylor":
    st.subheader("📊 Séries de Taylor")
    st.info("(O conteúdo da ferramenta será carregado aqui)")


#C2 - INTEGRAL DUPLA=======================================================================================
elif pagina == "integrais_duplas":
    st.subheader("🔁 Integrais Duplas")
    st.info("(O conteúdo da ferramenta será carregado aqui)")


#C2 - EQUAÇÕES DIFERENCIAIS==================================================================================
elif pagina == "equacoes_diferenciais":
    st.subheader("🌀 Equações Diferenciais")
    st.info("(O conteúdo da ferramenta será carregado aqui)")



################################## CALCULO NUMÉRICO ########################################################

#C.N - PONTO FIXO============================================================================================

elif pagina == "ponto_fixo":
    import sympy as sp
    st.subheader("🔁 Método do Ponto Fixo")

    func_str = st.text_input("Digite a função f(x):", "x**2 - 3*x + 2")
    g_str = st.text_input("Digite a função g(x) (rearranjada):", "(x**2 + 2)/3")

    try:
        x = sp.symbols('x')
        f_expr = sp.sympify(func_str)
        g_expr = sp.sympify(g_str)
        g = sp.lambdify(x, g_expr, 'numpy')

        # Derivada de g(x)
        g_prime_expr = sp.diff(g_expr, x)
        g_prime = sp.lambdify(x, g_prime_expr, 'numpy')

        x0 = st.number_input("Valor inicial x₀:", value=1.0)
        tolerancia = st.number_input("Tolerância:", value=0.0001, format="%.5f")
        max_iter = st.number_input("Número máximo de iterações:", value=20, step=1)

        # Avaliar |g'(x₀)|
        try:
            derivada_inicial = abs(g_prime(x0))
            if derivada_inicial < 1:
                st.success(f"Condição de convergência favorável: |g'(x₀)| = {derivada_inicial:.4f} < 1")
            else:
                st.warning(f"⚠️ Atenção: |g'(x₀)| = {derivada_inicial:.4f} ≥ 1, pode não convergir!")
        except:
            st.warning("⚠️ Não foi possível calcular g'(x₀).")

        if st.button("Executar Método do Ponto Fixo"):
            iteracoes = []
            x_atual = x0

            for i in range(max_iter):
                x_novo = g(x_atual)
                erro = abs(x_novo - x_atual)
                iteracoes.append((i, x_atual, x_novo, erro))
                if erro < tolerancia:
                    break
                x_atual = x_novo

            st.success(f"Aproximação final: {x_novo:.6f}")

            st.subheader("Iterações passo a passo")
            for i, x_antigo, x_novo, erro in iteracoes:
                col1, col2 = st.columns(2)
                with col1:
                    fig, ax = plt.subplots()
                    x_vals = np.linspace(-10, 10, 400)
                    y_vals = [g(v) for v in x_vals]
                    ax.plot(x_vals, y_vals, label="g(x)", color='blue')
                    ax.plot(x_vals, x_vals, '--', color='black', label="y = x")
                    ax.scatter([x_antigo], [g(x_antigo)], color='red', zorder=5, label=f"x_{i}")
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

                with col2:
                    st.latex(rf"x_{{{i}}} = {x_antigo:.6f}")
                    st.latex(rf"x_{{{i+1}}} = g(x_{{{i}}}) = {x_novo:.6f}")
                    st.latex(rf"\text{{Erro}} = |x_{{{i+1}}} - x_{{{i}}}| = {erro:.6f}")

    except Exception as e:
        st.error(f"Erro ao interpretar a função: {str(e)}")


#C.N - BISSEÇÃO============================================================================================

elif pagina == "bissecao":
    import imageio.v2 as imageio

    st.subheader("🔍 Bisseção")

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
            iteracoes.append((iter_count, a, b, c, f(a), f(b), f(c), erro))
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
                    for i, (it, a_i, b_i, c_i, fa, fb, fc, erro) in enumerate(iteracoes):
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
                            st.latex(rf"\text{{Erro}} = \frac{{b - a}}{{2}} = {erro:.6f}")

                except Exception as e:
                    st.error(f"Erro durante a execução do método: {str(e)}")

        except Exception as e:
            st.error(f"Erro ao interpretar a função: {str(e)}")


#C.N - FALSA POSIÇÃO==========================================================================================
elif pagina == "falsa_posicao":
    import imageio.v2 as imageio

    st.subheader("🔍 Falsa Posição (Regula Falsi)")

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
        iter_count = 0
        c = a
        while abs(f(c)) > tol and iter_count < max_iter:
            c = (a * f(b) - b * f(a)) / (f(b) - f(a))
            erro = abs(f(c))
            iteracoes.append((iter_count, a, b, c, f(a), f(b), f(c), erro))
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
            iter_count += 1
        return c, iteracoes

    def estimar_iteracoes_necessarias(a, b, tol):
        return int(np.ceil(np.log2((b - a) / tol)))

    expr = st.text_input("Digite a função f(x):", value="x**3 - x - 2")

    if expr:
        try:
            func = criar_funcao(expr)

            st.markdown("### Visualização da função")
            x_vals = np.linspace(-10, 10, 1000)
            y_vals = [func(x) for x in x_vals]

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, label="f(x)", color='blue')
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')
            ax.set_xlim(-10, 10)
            ax.set_ylim(-10, 10)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True)
            ax.legend()
            st.pyplot(fig)

            st.markdown("### Escolha do intervalo [a, b] e parâmetros")
            a = st.number_input("Valor de a:", value=1.0)
            b = st.number_input("Valor de b:", value=2.0)
            tol = st.number_input("Tolerância:", value=1e-6, format="%.10f")

            if b <= a:
                st.warning("Certifique-se de que b > a.")
            else:
                est = estimar_iteracoes_necessarias(a, b, tol)
                st.write(f"Estimativa mínima de iterações: **{est}**")
                max_iter = st.number_input("Máximo de iterações:", value=est, step=1)

                if st.button("Executar Método da Falsa Posição"):
                    try:
                        raiz, iteracoes = falsa_posicao(func, a, b, tol, max_iter)
                        st.success(f"Raiz aproximada: {raiz:.10f}")

                        st.markdown("### Iterações passo a passo")
                        for i, (it, a_i, b_i, c_i, fa, fb, fc, erro) in enumerate(iteracoes):
                            col1, col2 = st.columns(2)
                            with col1:
                                fig_it, ax_it = plt.subplots()
                                ax_it.plot(x_vals, y_vals, label="f(x)", color='blue')
                                ax_it.axhline(0, color='black')
                                ax_it.axvline(a_i, color='green', linestyle='--', label=f'a (it. {i})')
                                ax_it.axvline(b_i, color='red', linestyle='--', label=f'b (it. {i})')
                                ax_it.plot([a_i, b_i], [fa, fb], 'r--', label='reta secante')
                                ax_it.axvline(c_i, color='orange', linestyle='-.', label=f'c (it. {i})')
                                ax_it.set_xlim(min(a_i, b_i) - 1, max(a_i, b_i) + 1)
                                ax_it.set_ylim(min(fa, fb, fc) - 1, max(fa, fb, fc) + 1)
                                ax_it.set_xlabel("x")
                                ax_it.set_ylabel("f(x)")
                                ax_it.grid(True)
                                ax_it.legend()
                                ax_it.set_title(f"Iteração {i + 1}")
                                st.pyplot(fig_it)

                            with col2:
                                st.latex(rf"a_{{{i+1}}} = {a_i:.6f} \quad b_{{{i+1}}} = {b_i:.6f}")
                                st.latex(rf"f(a_{{{i+1}}}) = {fa:.6f} \quad f(b_{{{i+1}}}) = {fb:.6f}")
                                st.latex(rf"c_{{{i+1}}} = \frac{{a_{{{i+1}}}f(b_{{{i+1}}}) - b_{{{i+1}}}f(a_{{{i+1}}})}}{{f(b_{{{i+1}}}) - f(a_{{{i+1}}})}} = {c_i:.6f}")
                                st.latex(rf"f(c_{{{i+1}}}) = {fc:.6f}")
                                st.latex(rf"\text{{Erro}} = |f(c_{{{i+1}}})| = {erro:.6f}")

                    except Exception as e:
                        st.error(f"Erro durante o cálculo: {str(e)}")

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
                erro = abs(x2 - x1)
                iteracoes.append((i, x0, x1, x2, f_x0, f_x1, erro))

                if erro < tolerancia:
                    break

                x0, x1 = x1, x2

            st.success(f"Aproximação final da raiz: {x2:.6f}")
            st.subheader("Iterações passo a passo")

            for i, x0_i, x1_i, x2_i, fx0, fx1, erro in iteracoes:
                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    x_vals = np.linspace(-10, 10, 400)
                    y_vals = [f(val) for val in x_vals]
                    ax.plot(x_vals, y_vals, label="f(x)", color='blue')
                    ax.axhline(0, color='black', linewidth=0.5)
                    ax.axvline(0, color='black', linewidth=0.5)

                    # Reta secante
                    ax.plot([x0_i, x1_i], [fx0, fx1], 'r--', label='Reta Secante')
                    ax.plot(x2_i, 0, 'ro', label=f"x_{i+2}")

                    ax.set_xlim(-10, 10)
                    ax.set_ylim(-10, 10)
                    ax.grid(True)
                    ax.legend()
                    ax.set_title(f"Iteração {i + 1}")
                    st.pyplot(fig)

                with col2:
                    st.latex(rf"x_{{{i}}} = {x0_i:.6f}, \quad x_{{{i+1}}} = {x1_i:.6f}")
                    st.latex(rf"f(x_{{{i}}}) = {fx0:.6f}, \quad f(x_{{{i+1}}}) = {fx1:.6f}")
                    st.latex(rf"x_{{{i+2}}} = x_{{{i+1}}} - \frac{{f(x_{{{i+1}}})(x_{{{i+1}}} - x_{{{i}}})}}{{f(x_{{{i+1}}}) - f(x_{{{i}}})}} = {x2_i:.6f}")
                    st.latex(rf"\text{{Erro}} = |x_{{{i+2}}} - x_{{{i+1}}}| = {erro:.6f}")

                # salvar imagem para GIF
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

    except Exception as e:
        st.error(f"Erro ao processar a função: {str(e)}")



#C.N - MÉTODO NEWTON==========================================================================================
elif pagina == "newton":
    import io
    import imageio.v2 as imageio
    from sympy import symbols, diff, lambdify, sympify

    st.subheader("⚙️ Método de Newton - Visualização Iterativa")

    funcao = st.text_input("Digite a função f(x):", value="x**2 - 2")

    if funcao:
        x = symbols('x')
        f = sympify(funcao)
        f_prime = diff(f, x)
        funcao_lambda = lambdify(x, f, 'numpy')
        derivada_lambda = lambdify(x, f_prime, 'numpy')

        x_vals = np.linspace(-10, 10, 400)
        try:
            y_vals = funcao_lambda(x_vals)
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
                f_x = funcao_lambda(x_atual)
                f_deriv = derivada_lambda(x_atual)
                if f_deriv == 0:
                    st.error(f"Derivada nula em x = {x_atual}. Método interrompido.")
                    break
                x_novo = x_atual - f_x / f_deriv
                iteracoes.append({
                    'x_n': x_atual,
                    'f(x_n)': f_x,
                    "f'(x_n)": f_deriv,
                    'x_{n+1}': x_novo
                })
                if abs(f_x) < tolerancia:
                    break
                x_atual = x_novo

            st.subheader("Iterações passo a passo")
            imagens = []

            for i, it in enumerate(iteracoes):
                x_n = it['x_n']
                y_n = it['f(x_n)']
                x_n1 = it['x_{n+1}']
                y_n1 = funcao_lambda(x_n1)
                derivada = it["f'(x_n)"]
                erro = abs(x_n1 - x_n)

                col1, col2 = st.columns(2)

                with col1:
                    fig, ax = plt.subplots()
                    ax.plot(x_vals, funcao_lambda(x_vals), label='f(x)', color='blue')
                    reta_tangente = lambda x_val: derivada * (x_val - x_n) + y_n
                    ax.plot(x_vals, reta_tangente(x_vals), 'g--', label='Tangente')
                    ax.plot(x_n, y_n, 'ro', label=f'x{i+1} = {x_n:.4f}')
                    ax.plot(x_n1, 0, 'bo', label=f'x{i+2} = {x_n1:.4f}')
                    ax.plot([x_n1, x_n1], [0, y_n1], 'k--', linewidth=1)
                    ax.axhline(0, color='black', linewidth=0.5)
                    ax.axvline(0, color='black', linewidth=0.5)
                    ax.set_xlim(-10, 10)
                    ax.set_ylim(-10, 10)
                    ax.set_title(f"Iteração {i + 1}")
                    ax.legend()
                    st.pyplot(fig)

                with col2:
                    st.latex(rf"f(x_{{{i+1}}}) = {y_n:.6f}")
                    st.latex(rf"f'(x_{{{i+1}}}) = {derivada:.6f}")
                    st.latex(rf"x_{{{i+2}}} = x_{{{i+1}}} - \frac{{f(x_{{{i+1}}})}}{{f'(x_{{{i+1}}})}} = {x_n:.6f} - \frac{{{y_n:.6f}}}{{{derivada:.6f}}} = {x_n1:.6f}")
                    st.latex(rf"|x_{{{i+2}}} - x_{{{i+1}}}| = {erro:.6f}")

                if abs(y_n1) < tolerancia:
                    st.success(f"Convergência alcançada! f(x) ≈ 0 em x = {x_n1:.6f}")
                else:
                    st.warning(f"Ainda não convergiu: f(x) = {y_n1:.6f}")

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
                st.image(gif_bytes, format="gif")

################################## EXEMPLOS ##############################################################
