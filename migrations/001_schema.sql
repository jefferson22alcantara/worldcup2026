-- Tabela de participantes do bolão
CREATE TABLE IF NOT EXISTS participantes (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    nome        TEXT        NOT NULL,
    telefone    TEXT        NOT NULL,
    email       TEXT        NOT NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- Tabela de palpites (1 linha por participante por grupo)
CREATE TABLE IF NOT EXISTS palpites (
    id               UUID   DEFAULT gen_random_uuid() PRIMARY KEY,
    participante_id  UUID   NOT NULL REFERENCES participantes(id) ON DELETE CASCADE,
    grupo            CHAR(1) NOT NULL CHECK (grupo IN ('A','B','C','D','E','F','G','H','I','J','K','L')),
    primeiro         TEXT   NOT NULL,
    segundo          TEXT   NOT NULL,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (participante_id, grupo)
);

-- RLS: permitir inserção anônima (sem autenticação)
ALTER TABLE participantes ENABLE ROW LEVEL SECURITY;
ALTER TABLE palpites      ENABLE ROW LEVEL SECURITY;

CREATE POLICY "insert_participantes" ON participantes FOR INSERT WITH CHECK (true);
CREATE POLICY "insert_palpites"      ON palpites      FOR INSERT WITH CHECK (true);
