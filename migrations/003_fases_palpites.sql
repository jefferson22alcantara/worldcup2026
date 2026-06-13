-- Tabela para palpites das fases eliminatórias
CREATE TABLE IF NOT EXISTS fases_palpites (
    id               UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    participante_id  UUID NOT NULL REFERENCES participantes(id) ON DELETE CASCADE,
    fase             TEXT NOT NULL,   -- r32, r16, qf, sf, 3lugar, final
    jogo             INT  NOT NULL,
    time1            TEXT NOT NULL,
    time2            TEXT NOT NULL,
    vencedor         TEXT NOT NULL,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (participante_id, fase, jogo)
);
