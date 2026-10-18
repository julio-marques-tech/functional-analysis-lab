-- Apaga todas as tabelas do schema atual (LAB). Útil para recomeçar o lab do zero.
-- Executar com Alt+X no DBeaver (Execute script).
BEGIN
    FOR t IN (SELECT table_name FROM user_tables) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE "' || t.table_name || '" CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/
