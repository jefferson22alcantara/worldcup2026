import random
import streamlit as st
from copa_data import GRUPOS, BRACKET_R32, BRACKET_R16, BRACKET_QF, BRACKET_SF
from db import salvar_participante, salvar_palpites, salvar_terceiros, salvar_fases, email_ja_cadastrado

st.set_page_config(
    page_title="World Cup 2026 Betting Pool",
    page_icon="⚽",
    layout="wide",
)

st.markdown("""
<style>
    .titulo { font-size: 2.2rem; font-weight: 700; color: #1a1a2e; }
    .grupo-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem 1rem 0.2rem 1rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #009c3b;
    }
    .grupo-titulo { font-weight: 700; font-size: 1rem; color: #009c3b; margin-bottom: 0.2rem; }
    .fase-titulo  { font-weight: 700; font-size: 1.1rem; color: #003580; margin-bottom: 0.4rem; }
    .stButton > button { background-color: #009c3b; color: white; border-radius: 8px; }
    .stButton > button:hover { background-color: #007a2f; }
</style>
""", unsafe_allow_html=True)

FASES_LABELS = {
    1: "Registration",
    2: "Group Stage",
    3: "Round of 32",
    4: "Round of 16",
    5: "Quarterfinals",
    6: "Semifinals",
    7: "Final",
}


# ---------------------------------------------------------------------------
# Bracket helpers
# ---------------------------------------------------------------------------

def sortear_terceiros(palpites: dict) -> list[str]:
    pool = []
    for grupo, times in GRUPOS.items():
        escolhidos = {palpites[grupo]["primeiro"], palpites[grupo]["segundo"]}
        pool.extend(t for t in times if t not in escolhidos)
    return random.sample(pool, 8)


def gerar_r32(palpites: dict, terceiros: list[str]) -> list[dict]:
    mapa = {}
    for grupo, p in palpites.items():
        mapa[("1", grupo)] = p["primeiro"]
        mapa[("2", grupo)] = p["segundo"]

    terceiros_pool = list(terceiros)
    random.shuffle(terceiros_pool)
    t_iter = iter(terceiros_pool)

    jogos = []
    for jogo_num, pos1, pos2 in BRACKET_R32:
        time1 = next(t_iter) if pos1[0] == "3" else mapa[pos1]
        time2 = next(t_iter) if pos2[0] == "3" else mapa[pos2]
        jogos.append({"jogo": jogo_num, "time1": time1, "time2": time2})
    return jogos


def gerar_fase(bracket: list[tuple], picks: dict) -> list[dict]:
    return [
        {"jogo": jnum, "time1": picks[p1], "time2": picks[p2]}
        for jnum, p1, p2 in bracket
    ]


def get_loser(jogo: dict, picks: dict) -> str:
    winner = picks[jogo["jogo"]]
    return jogo["time2"] if winner == jogo["time1"] else jogo["time1"]


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

def init_state():
    defaults = {
        "step": 1,
        "participante": {},
        "palpites": {},
        "terceiros": [],
        "r32_jogos": [],  "r32_picks": {},
        "r16_jogos": [],  "r16_picks": {},
        "qf_jogos": [],   "qf_picks": {},
        "sf_jogos": [],   "sf_picks": {},
        "terceiro_jogo": {}, "terceiro_pick": "",
        "final_jogo": {},    "final_pick": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------------------------------------------------------------------------
# UI helpers
# ---------------------------------------------------------------------------

def header():
    st.markdown('<p class="titulo">⚽ World Cup 2026 Betting Pool</p>', unsafe_allow_html=True)
    step = st.session_state.step
    if step <= 7:
        label = FASES_LABELS.get(step, "")
        st.progress((step - 1) / 6, text=f"Stage {step} of 7 - {label}")
    st.divider()


# ---------------------------------------------------------------------------
# Telas
# ---------------------------------------------------------------------------

def tela_cadastro():
    header()
    st.subheader("Your Information")

    with st.form("cadastro"):
        nome = st.text_input("Full Name")
        telefone = st.text_input("Phone (with area code)")
        email = st.text_input("Email Address")
        submitted = st.form_submit_button("Continue →", type="primary")

    if submitted:
        if not (nome.strip() and telefone.strip() and email.strip()):
            st.error("Please fill in all fields.")
            return
        if "@" not in email:
            st.error("Invalid email address.")
            return
        try:
            if email_ja_cadastrado(email.strip()):
                st.error("This email is already registered.")
                return
        except Exception:
            st.error("Error connecting to the database. Please check the environment variables.")
            return

        st.session_state.participante = {
            "nome": nome.strip(),
            "telefone": telefone.strip(),
            "email": email.strip(),
        }
        st.session_state.step = 2
        st.rerun()


def tela_grupos():
    header()
    st.subheader("Choose the 1st and 2nd place teams from each group")
    st.caption("The 8 best 3rd place teams will be drawn automatically.")
    st.write("")

    palpites_temp: dict = {}
    grupos_incompletos: list[str] = []

    cols = st.columns(2, gap="large")
    for i, (grupo, times) in enumerate(GRUPOS.items()):
        with cols[i % 2]:
            st.markdown(
                f'<div class="grupo-card"><p class="grupo-titulo">GROUP {grupo}</p></div>',
                unsafe_allow_html=True,
            )
            primeiro = st.selectbox(
                "🥇 1st place", times,
                key=f"g1_{grupo}", index=None, placeholder="Select...",
            )
            segundo_options = [t for t in times if t != primeiro]
            segundo = st.selectbox(
                "🥈 2nd place", segundo_options,
                key=f"g2_{grupo}", index=None, placeholder="Select...",
                disabled=primeiro is None,
            )

            if primeiro is None or segundo is None:
                grupos_incompletos.append(grupo)
            else:
                palpites_temp[grupo] = {"primeiro": primeiro, "segundo": segundo}

    st.write("")
    if st.button("Confirm groups and continue →", type="primary", use_container_width=True):
        if grupos_incompletos:
            st.error(f"Complete the following groups: {', '.join(grupos_incompletos)}")
            return

        terceiros = sortear_terceiros(palpites_temp)
        r32_jogos = gerar_r32(palpites_temp, terceiros)

        st.session_state.palpites = palpites_temp
        st.session_state.terceiros = terceiros
        st.session_state.r32_jogos = r32_jogos
        st.session_state.step = 3
        st.rerun()


def _tela_fase_generica(titulo: str, subtitulo: str, jogos_key: str,
                         radio_prefix: str, next_step: int, on_confirm):
    header()
    st.subheader(titulo)
    st.caption(subtitulo)
    st.write("")

    jogos = st.session_state[jogos_key]
    cols = st.columns(2, gap="large")

    for i, jogo in enumerate(jogos):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(
                    f'<p class="fase-titulo">Match {jogo["jogo"]}</p>',
                    unsafe_allow_html=True,
                )
                st.radio(
                    label="v",
                    options=[jogo["time1"], jogo["time2"]],
                    key=f"{radio_prefix}_{jogo['jogo']}",
                    index=None,
                    label_visibility="collapsed",
                )

    st.write("")
    if st.button("Continue →", type="primary", use_container_width=True):
        picks = {}
        for jogo in jogos:
            val = st.session_state.get(f"{radio_prefix}_{jogo['jogo']}")
            if val is None:
                st.error("Choose the winner of every match before continuing.")
                return
            picks[jogo["jogo"]] = val

        on_confirm(picks)
        st.session_state.step = next_step
        st.rerun()


def tela_r32():
    def on_confirm(picks):
        st.session_state.r32_picks = picks
        st.session_state.r16_jogos = gerar_fase(BRACKET_R16, picks)

    _tela_fase_generica(
        "Round of 32",
        "Choose the winner of each matchup (32 qualified teams)",
        "r32_jogos", "r32", 4, on_confirm,
    )


def tela_r16():
    def on_confirm(picks):
        st.session_state.r16_picks = picks
        st.session_state.qf_jogos = gerar_fase(BRACKET_QF, picks)

    _tela_fase_generica(
        "Round of 16",
        "Choose the winner of each matchup",
        "r16_jogos", "r16", 5, on_confirm,
    )


def tela_qf():
    def on_confirm(picks):
        st.session_state.qf_picks = picks
        st.session_state.sf_jogos = gerar_fase(BRACKET_SF, picks)

    _tela_fase_generica(
        "Quarterfinals",
        "Choose the winner of each matchup",
        "qf_jogos", "qf", 6, on_confirm,
    )


def tela_sf():
    def on_confirm(picks):
        st.session_state.sf_picks = picks
        sf = st.session_state.sf_jogos

        w1 = picks[sf[0]["jogo"]]
        w2 = picks[sf[1]["jogo"]]
        l1 = get_loser(sf[0], picks)
        l2 = get_loser(sf[1], picks)

        st.session_state.final_jogo    = {"jogo": 104, "time1": w1, "time2": w2}
        st.session_state.terceiro_jogo = {"jogo": 103, "time1": l1, "time2": l2}

    _tela_fase_generica(
        "Semifinals",
        "Choose the winner of each semifinal",
        "sf_jogos", "sf", 7, on_confirm,
    )


def tela_final():
    header()
    st.subheader("Final Stage")
    st.write("")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("**🥉 Third-place Playoff - Match 103**")
        tj = st.session_state.terceiro_jogo
        with st.container(border=True):
            st.radio(
                label="v",
                options=[tj["time1"], tj["time2"]],
                key="pick_3lugar",
                index=None,
                label_visibility="collapsed",
            )

    with col2:
        st.markdown("**🏆 Grand Final - Match 104**")
        fj = st.session_state.final_jogo
        with st.container(border=True):
            st.radio(
                label="v",
                options=[fj["time1"], fj["time2"]],
                key="pick_final",
                index=None,
                label_visibility="collapsed",
            )

    st.write("")
    if st.button("Save all predictions ✅", type="primary", use_container_width=True):
        t3_pick    = st.session_state.get("pick_3lugar")
        final_pick = st.session_state.get("pick_final")

        if not t3_pick or not final_pick:
            st.error("Select the winner of the third-place playoff and the final.")
            return

        st.session_state.terceiro_pick = t3_pick
        st.session_state.final_pick    = final_pick

        with st.spinner("Saving your predictions..."):
            try:
                pid = salvar_participante(st.session_state.participante)
                salvar_palpites(pid, st.session_state.palpites)
                salvar_terceiros(pid, st.session_state.terceiros)

                fases_rows = []
                for fase_nome, jogos, picks in [
                    ("r32", st.session_state.r32_jogos, st.session_state.r32_picks),
                    ("r16", st.session_state.r16_jogos, st.session_state.r16_picks),
                    ("qf",  st.session_state.qf_jogos,  st.session_state.qf_picks),
                    ("sf",  st.session_state.sf_jogos,  st.session_state.sf_picks),
                ]:
                    for j in jogos:
                        fases_rows.append({
                            "participante_id": pid,
                            "fase": fase_nome,
                            "jogo": j["jogo"],
                            "time1": j["time1"],
                            "time2": j["time2"],
                            "vencedor": picks[j["jogo"]],
                        })

                for fase_nome, jogo_dict, vencedor in [
                    ("3lugar", st.session_state.terceiro_jogo, t3_pick),
                    ("final",  st.session_state.final_jogo,    final_pick),
                ]:
                    fases_rows.append({
                        "participante_id": pid,
                        "fase": fase_nome,
                        "jogo": jogo_dict["jogo"],
                        "time1": jogo_dict["time1"],
                        "time2": jogo_dict["time2"],
                        "vencedor": vencedor,
                    })

                salvar_fases(fases_rows)

            except Exception as e:
                st.error(f"Error saving data: {e}")
                return

        st.session_state.step = 8
        st.rerun()


def tela_confirmacao():
    st.balloons()
    nome       = st.session_state.participante["nome"]
    campeo     = st.session_state.final_pick
    terceiro   = st.session_state.terceiro_pick

    st.markdown('<p class="titulo">✅ Prediction saved!</p>', unsafe_allow_html=True)
    st.success(f"Thanks, **{nome}**! Your full prediction was saved successfully.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏆 Champion", campeo)
    with col2:
        st.metric("🥉 Third Place", terceiro)

    st.divider()

    with st.expander("📋 Group Stage", expanded=False):
        cols = st.columns(3)
        for i, (grupo, p) in enumerate(st.session_state.palpites.items()):
            with cols[i % 3]:
                st.markdown(f"**Group {grupo}**  \n🥇 {p['primeiro']}  \n🥈 {p['segundo']}")

    with st.expander("🎲 8 Best Third-Place Teams (drawn)", expanded=False):
        cols = st.columns(4)
        for i, t in enumerate(st.session_state.terceiros):
            with cols[i % 4]:
                st.markdown(f"**{i+1}.** {t}")

    fases_resumo = [
        ("Round of 32",     st.session_state.r32_jogos, st.session_state.r32_picks),
        ("Round of 16",     st.session_state.r16_jogos, st.session_state.r16_picks),
        ("Quarterfinals",   st.session_state.qf_jogos,  st.session_state.qf_picks),
        ("Semifinals",      st.session_state.sf_jogos,  st.session_state.sf_picks),
    ]
    for titulo, jogos, picks in fases_resumo:
        with st.expander(f"🏟️ {titulo}", expanded=False):
            cols = st.columns(2)
            for i, j in enumerate(jogos):
                with cols[i % 2]:
                    st.markdown(
                        f"**Match {j['jogo']}:** {j['time1']} × {j['time2']}  \n"
                        f"✅ {picks[j['jogo']]}"
                    )

    st.divider()
    if st.button("Make a new prediction", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ---------------------------------------------------------------------------
# Roteador principal
# ---------------------------------------------------------------------------

init_state()

TELAS = {
    1: tela_cadastro,
    2: tela_grupos,
    3: tela_r32,
    4: tela_r16,
    5: tela_qf,
    6: tela_sf,
    7: tela_final,
    8: tela_confirmacao,
}

TELAS.get(st.session_state.step, tela_cadastro)()
