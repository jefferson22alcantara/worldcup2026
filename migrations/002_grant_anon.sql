-- Concede permissão de INSERT ao role anon (usado pela anon key do Supabase)
GRANT USAGE ON SCHEMA public TO anon;
GRANT INSERT ON participantes TO anon;
GRANT INSERT ON palpites TO anon;

-- Recria as policies explicitando o role anon
DROP POLICY IF EXISTS "insert_participantes" ON participantes;
DROP POLICY IF EXISTS "insert_palpites"      ON palpites;

CREATE POLICY "insert_participantes" ON participantes
  FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "insert_palpites" ON palpites
  FOR INSERT TO anon WITH CHECK (true);
