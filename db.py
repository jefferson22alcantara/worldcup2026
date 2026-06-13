import streamlit as st
from supabase import create_client, Client

_client: Client | None = None


def get_client() -> Client:
    global _client
    if _client is None:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_ANON_KEY"]
        _client = create_client(url, key)
    return _client


def salvar_participante(dados: dict) -> str:
    result = get_client().table("participantes").insert({
        "nome": dados["nome"],
        "telefone": dados["telefone"],
        "email": dados["email"],
    }).execute()
    return result.data[0]["id"]


def salvar_palpites(participante_id: str, palpites: dict) -> None:
    rows = [
        {
            "participante_id": participante_id,
            "grupo": grupo,
            "primeiro": p["primeiro"],
            "segundo": p["segundo"],
        }
        for grupo, p in palpites.items()
    ]
    get_client().table("palpites").insert(rows).execute()


def salvar_terceiros(participante_id: str, terceiros: list[str]) -> None:
    rows = [{"participante_id": participante_id, "time": t} for t in terceiros]
    get_client().table("terceiros").insert(rows).execute()


def salvar_fases(fases_data: list[dict]) -> None:
    get_client().table("fases_palpites").insert(fases_data).execute()


def email_ja_cadastrado(email: str) -> bool:
    result = get_client().table("participantes").select("id").eq("email", email).execute()
    return len(result.data) > 0
