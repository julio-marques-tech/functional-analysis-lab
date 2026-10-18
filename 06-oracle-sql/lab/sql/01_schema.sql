-- Modelo físico (Oracle) do Sistema de Gestão de Prestações Sociais.
-- Origem: 01-data-modeling/modelo-logico.md. Caso de estudo fictício.
-- Executar com Alt+X no DBeaver (Execute script), ligado ao schema LAB.
-- Nota: as FKs não têm índices de propósito; na fase de planos de execução
-- vamos ver o efeito de os acrescentar.

-- ---------------------------------------------------------------- catálogos
CREATE TABLE distrito (
    id_distrito  NUMBER(10)    CONSTRAINT pk_distrito PRIMARY KEY,
    nome         VARCHAR2(100) NOT NULL
);

CREATE TABLE tipo_prestacao (
    id_tipo_prestacao NUMBER(10)    CONSTRAINT pk_tipo_prestacao PRIMARY KEY,
    codigo            VARCHAR2(20)  NOT NULL CONSTRAINT uk_tipo_prestacao_codigo UNIQUE,
    nome              VARCHAR2(100) NOT NULL
);

CREATE TABLE escalao (
    id_escalao      NUMBER(10)    CONSTRAINT pk_escalao PRIMARY KEY,
    nome            VARCHAR2(50)  NOT NULL,
    rendimento_min  NUMBER(12,2)  NOT NULL,
    rendimento_max  NUMBER(12,2)
);

CREATE TABLE estado (
    id_estado  NUMBER(10)   CONSTRAINT pk_estado PRIMARY KEY,
    nome       VARCHAR2(50) NOT NULL
);

CREATE TABLE motivo_indeferimento (
    id_motivo  NUMBER(10)    CONSTRAINT pk_motivo_indeferimento PRIMARY KEY,
    descricao  VARCHAR2(200) NOT NULL
);

CREATE TABLE tipo_documento (
    id_tipo_documento  NUMBER(10)    CONSTRAINT pk_tipo_documento PRIMARY KEY,
    nome               VARCHAR2(100) NOT NULL
);

-- ------------------------------------------------------------- organização
CREATE TABLE servico_local (
    id_servico_local  NUMBER(10)    CONSTRAINT pk_servico_local PRIMARY KEY,
    codigo            VARCHAR2(20)  NOT NULL CONSTRAINT uk_servico_local_codigo UNIQUE,
    nome              VARCHAR2(100) NOT NULL,
    id_distrito       NUMBER(10)    NOT NULL
        CONSTRAINT fk_servico_local_distrito REFERENCES distrito (id_distrito)
);

CREATE TABLE tecnico (
    id_tecnico        NUMBER(10)    CONSTRAINT pk_tecnico PRIMARY KEY,
    nome              VARCHAR2(100) NOT NULL,
    id_servico_local  NUMBER(10)    NOT NULL
        CONSTRAINT fk_tecnico_servico_local REFERENCES servico_local (id_servico_local)
);

-- ---------------------------------------------------------------- cidadãos
CREATE TABLE cidadao (
    id_cidadao       NUMBER(10)    CONSTRAINT pk_cidadao PRIMARY KEY,
    niss             VARCHAR2(11)  NOT NULL CONSTRAINT uk_cidadao_niss UNIQUE,
    nome             VARCHAR2(100) NOT NULL,
    data_nascimento  DATE          NOT NULL,
    nif              VARCHAR2(9),
    email            VARCHAR2(100),
    telemovel        VARCHAR2(20)
);

CREATE TABLE morada (
    id_morada              NUMBER(10)    CONSTRAINT pk_morada PRIMARY KEY,
    id_cidadao             NUMBER(10)    NOT NULL
        CONSTRAINT fk_morada_cidadao REFERENCES cidadao (id_cidadao),
    id_servico_local       NUMBER(10)    NOT NULL
        CONSTRAINT fk_morada_servico_local REFERENCES servico_local (id_servico_local),
    rua                    VARCHAR2(200),
    codigo_postal          VARCHAR2(10),
    localidade             VARCHAR2(100),
    data_inicio_vigencia   DATE          NOT NULL,
    data_fim_vigencia      DATE,
    CONSTRAINT ck_morada_vigencia
        CHECK (data_fim_vigencia IS NULL OR data_fim_vigencia >= data_inicio_vigencia)
);

CREATE TABLE rel_dependente (
    id_cidadao_responsavel  NUMBER(10)   NOT NULL
        CONSTRAINT fk_rel_dep_responsavel REFERENCES cidadao (id_cidadao),
    id_cidadao_dependente   NUMBER(10)   NOT NULL
        CONSTRAINT fk_rel_dep_dependente REFERENCES cidadao (id_cidadao),
    tipo_relacao            VARCHAR2(50) NOT NULL,
    CONSTRAINT pk_rel_dependente PRIMARY KEY (id_cidadao_responsavel, id_cidadao_dependente)
);

-- -------------------------------------------------------- valores e regras
CREATE TABLE valor_escalao (
    id_tipo_prestacao  NUMBER(10)   NOT NULL
        CONSTRAINT fk_valor_esc_prestacao REFERENCES tipo_prestacao (id_tipo_prestacao),
    id_escalao         NUMBER(10)   NOT NULL
        CONSTRAINT fk_valor_esc_escalao REFERENCES escalao (id_escalao),
    ano                NUMBER(4)    NOT NULL,
    valor              NUMBER(12,2) NOT NULL,
    CONSTRAINT pk_valor_escalao PRIMARY KEY (id_tipo_prestacao, id_escalao, ano)
);

CREATE TABLE documento_obrigatorio (
    id_tipo_prestacao  NUMBER(10) NOT NULL
        CONSTRAINT fk_doc_obrig_prestacao REFERENCES tipo_prestacao (id_tipo_prestacao),
    id_tipo_documento  NUMBER(10) NOT NULL
        CONSTRAINT fk_doc_obrig_tipo_doc REFERENCES tipo_documento (id_tipo_documento),
    CONSTRAINT pk_documento_obrigatorio PRIMARY KEY (id_tipo_prestacao, id_tipo_documento)
);

-- ------------------------------------------------------------------ pedidos
CREATE TABLE pedido (
    id_pedido          NUMBER(10) CONSTRAINT pk_pedido PRIMARY KEY,
    id_cidadao         NUMBER(10) NOT NULL
        CONSTRAINT fk_pedido_cidadao REFERENCES cidadao (id_cidadao),
    id_tipo_prestacao  NUMBER(10) NOT NULL
        CONSTRAINT fk_pedido_prestacao REFERENCES tipo_prestacao (id_tipo_prestacao),
    id_escalao         NUMBER(10)
        CONSTRAINT fk_pedido_escalao REFERENCES escalao (id_escalao),
    data_submissao     DATE       NOT NULL
);

CREATE TABLE pedido_dependente (
    id_pedido              NUMBER(10) NOT NULL
        CONSTRAINT fk_ped_dep_pedido REFERENCES pedido (id_pedido),
    id_cidadao_dependente  NUMBER(10) NOT NULL
        CONSTRAINT fk_ped_dep_cidadao REFERENCES cidadao (id_cidadao),
    CONSTRAINT pk_pedido_dependente PRIMARY KEY (id_pedido, id_cidadao_dependente)
);

CREATE TABLE atribuicao (
    id_atribuicao  NUMBER(10) CONSTRAINT pk_atribuicao PRIMARY KEY,
    id_pedido      NUMBER(10) NOT NULL
        CONSTRAINT fk_atribuicao_pedido REFERENCES pedido (id_pedido),
    id_tecnico     NUMBER(10) NOT NULL
        CONSTRAINT fk_atribuicao_tecnico REFERENCES tecnico (id_tecnico),
    data_inicio    DATE       NOT NULL,
    data_fim       DATE,
    CONSTRAINT ck_atribuicao_datas CHECK (data_fim IS NULL OR data_fim >= data_inicio)
);

CREATE TABLE historico_estado (
    id_historico_estado  NUMBER(10)    CONSTRAINT pk_historico_estado PRIMARY KEY,
    id_pedido            NUMBER(10)    NOT NULL
        CONSTRAINT fk_hist_estado_pedido REFERENCES pedido (id_pedido),
    id_estado            NUMBER(10)    NOT NULL
        CONSTRAINT fk_hist_estado_estado REFERENCES estado (id_estado),
    id_motivo            NUMBER(10)
        CONSTRAINT fk_hist_estado_motivo REFERENCES motivo_indeferimento (id_motivo),
    observacao           VARCHAR2(500),
    data_mudanca         DATE          NOT NULL
);

CREATE TABLE documento (
    id_documento       NUMBER(10)    CONSTRAINT pk_documento PRIMARY KEY,
    id_pedido          NUMBER(10)    NOT NULL
        CONSTRAINT fk_documento_pedido REFERENCES pedido (id_pedido),
    id_tipo_documento  NUMBER(10)    NOT NULL
        CONSTRAINT fk_documento_tipo REFERENCES tipo_documento (id_tipo_documento),
    data_entrega       DATE          NOT NULL,
    ficheiro           VARCHAR2(300)
);

-- --------------------------------------------------------------- pagamentos
CREATE TABLE conta_bancaria (
    id_conta              NUMBER(10)   CONSTRAINT pk_conta_bancaria PRIMARY KEY,
    id_pedido             NUMBER(10)   NOT NULL
        CONSTRAINT fk_conta_pedido REFERENCES pedido (id_pedido),
    iban                  VARCHAR2(34) NOT NULL,
    data_inicio_vigencia  DATE         NOT NULL,
    data_fim_vigencia     DATE,
    CONSTRAINT ck_conta_vigencia
        CHECK (data_fim_vigencia IS NULL OR data_fim_vigencia >= data_inicio_vigencia)
);

CREATE TABLE pagamento (
    id_pagamento    NUMBER(10)   CONSTRAINT pk_pagamento PRIMARY KEY,
    id_pedido       NUMBER(10)   NOT NULL
        CONSTRAINT fk_pagamento_pedido REFERENCES pedido (id_pedido),
    id_conta        NUMBER(10)   NOT NULL
        CONSTRAINT fk_pagamento_conta REFERENCES conta_bancaria (id_conta),
    mes_referencia  DATE         NOT NULL,
    valor           NUMBER(12,2) NOT NULL,
    data_pagamento  DATE         NOT NULL
);
