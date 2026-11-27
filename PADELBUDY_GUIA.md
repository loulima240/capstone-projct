# PadelBudy — guia de implementação e acesso às plataformas

Atualizado em 15/11/2026. Documento de trabalho baseado na proposta, nas guidelines, nos notebooks locais e na documentação oficial indicada no fim. Distingue requisitos confirmados de recomendações e questões por validar.

## 1. Objetivo e decisões confirmadas

O PadelBudy agrega e compara opções de padel entre Playtomic, TiePlayer/TieSports e outros fornecedores ou sites de clubes. O utilizador descreve localização, data, intervalo horário, duração, orçamento e tipo de campo; recebe opções ordenadas e links reais para concluir a reserva no fornecedor.

- Não substituir as plataformas existentes.
- Não processar pagamentos na nossa aplicação.
- A proposta já prevê redirecionamento para concluir a reserva; criar reservas por API não é necessário para esse fluxo.
- Ler confirmação de reserva em fotografia/PDF, extrair informação e repartir o custo pelos jogadores é uma funcionalidade prevista na proposta.
- O envio de emails com a repartição também está proposto; implementar apenas com destinatários verificados e confirmação explícita de envio.
- Raquetes, acompanhamento de resultados e expansão a ténis são ideias opcionais, sem prioridade sobre o núcleo.
- Papéis iniciais na proposta: Afonso no backend e Lourenço no frontend; ambos têm de compreender todo o projeto e colaborar nas várias partes.
- A alegação da proposta de que páginas públicas permitem consultar todos os horários sem login é uma hipótese por validar, clube a clube. Não é evidência de acesso autorizado ou estável.

## 2. Estado observado no código

| Ficheiro | Estado observado | Implicação |
|---|---|---|
| app.py | Interface Streamlit, formulário com filtros, seleção de campo e chat Anthropic | Existe protótipo de interface; o chat ainda não chama as funções de pesquisa |
| courts.py | Três opções estáticas identificadas como Demo data, com datas fixas | Não há consulta de disponibilidade real; manter o aviso de demonstração |
| players.py | Vazio | Encontrar jogadores ainda não está implementado |
| README.md | Texto do template, com referências a Gemini | Atualizar para refletir o código Anthropic e as instruções reais |
| pyproject.toml | Python >=3.12, Streamlit, Anthropic e google-genai | Rever dependências usadas e fixar versões conforme as guidelines; existe uv.lock |

Não assumir que selecionar um campo equivale a reservá-lo. Não apresentar preços, jogadores ou horários inventados como resultados reais. A chave do LLM e as credenciais dos fornecedores são acessos diferentes.

## 3. Requisitos da cadeira

Fonte: Project_Guidelines (1).pdf, páginas numeradas 2–6.

1. Backend Python e utilização real de um LLM. Quando o código age sobre a resposta, usar output estruturado com schema.
2. Agente conversacional multi-turn que escolhe tools, encadeia chamadas e usa o contexto. Um formulário com filtros e um chat separado não satisfaz, por si só, este requisito.
3. Tools próprias para ler e alterar dados da aplicação, documentadas em docs/TOOLS.md. Podem alterar dados internos, como pesquisas guardadas e repartições: não precisam de escrever nas plataformas de reservas.
4. Falhas devolvidas como resultados compreensíveis para o agente. Retry apenas para falhas transitórias de operações seguras de repetir. Pedir confirmação antes de eliminar/sobrescrever, salvo quando existe undo.
5. Leitura de documentos com utilidade concreta. A confirmação de reserva é uma boa aplicação para este projeto.
6. Arquitetura em camadas: interface, lógica, acesso ao AI e tools separados; configuração, prompts e schemas em módulos próprios.
7. Uma trace por pedido, com spans para cada chamada ao modelo e cada tool, incluindo no deployment. Registar modelo, tempos, tokens, erros, falhas tratadas, outcome e conversa. Definir conteúdo registado e retenção.
8. Dependências fixadas a versões exatas, deployment público e documentação reproduzível.
9. Informar os utilizadores da interação com AI, respeitar dados pessoais e os termos dos serviços usados. Isto é um requisito do enunciado, não uma análise jurídica deste documento.

Recomendado: conjunto de 10–20 casos com resultados esperados e script de avaliação. Não acrescentar técnicas apenas para preencher requisitos.

### Entregas

- Proposta técnica: 06/12/2026, 23:59; as duas propostas valem 15%.
- Entrega final: 03/01/2027, 23:59; entrega e defesa valem 75%; quizzes completam 10%.
- Confirmar no Moodle eventuais alterações de calendário.
- GitHub com mb-cardoso como colaborador; código na default branch; README com URL pública e setup; docs/ARCHITECTURE.md; docs/TOOLS.md; .env.example sem segredos.
- Moodle: mesmo código num TeamName_FinalProject.zip.
- Cada membro pode ser questionado sobre qualquer parte do código.

## 4. Onde nos basearmos nas weeks

Todos os caminhos seguintes são relativos à pasta projetocurso. Os números são secções dos notebooks, não slides inventados.

| Necessidade | Material exato | Secções a consultar | Aplicação ao PadelBudy |
|---|---|---|---|
| Ambiente e primeira chamada | aulas/template-20260918/Week_1_Session_2_Environment_Setup.ipynb | Steps 2–5 | uv, variáveis de ambiente, diagnóstico e teste simples |
| API do LLM e falhas | aulas/template-20260918/Week_2_Session_1_LLM_Fundamentals_UNSOLVED.ipynb | 2, 4 e 5 | Instruções, conversa e tratamento de chamadas falhadas |
| Memória | aulas/template-20260918/Week_2_Session_2_Conversation_Memory_UNSOLVED.ipynb | 3–6 | Manter critérios quando o utilizador diz “e mais tarde?” ou “até 40 euros” |
| Pedido em critérios estruturados | aulas/template-20260918/Week_3_Session_1_Prompts_and_Structured_Output.ipynb | 2–6, sobretudo 5 e 6 | Schema de pesquisa; separar instruções e dados do utilizador |
| Validação e avaliação | aulas/template-20260918/Week_3_Session_2_From_Output_to_Application_UNSOLVED.ipynb | 1–3 | Um JSON válido não prova que um horário existe; validar no código |
| Ler confirmação PDF/imagem | aulas/template-20260918/Week_4_Session_1_Documents_and_Images.ipynb | 1–4 | Extrair clube, data, hora, moeda e total; tratar documentos como dados |
| Medir extração | aulas/template-20260918/Week_4_Session_2_Measure_then_Build.ipynb | 1 e 3 | Comparar campos extraídos com confirmações anotadas |
| Declarar tools e executar o loop | aulas/template-20260918/Week_05/Week_5_Session_1_Tools_and_the_Loop.ipynb | 1–4 | Pesquisa real como função; schema, loop e falhas devolvidas ao agente |
| Regras impostas pelo código | aulas/template-20260918/Week_05/Week_5_Session_2_What_Code_Must_Decide.ipynb | 1–5 | Injection, confirmação, retry seguro, factos vindos das tools, docs/TOOLS.md |
| Agente integrado | aulas/template-20260918/Week_6_Session_1_The_Agent_Step_by_Step.ipynb | 2, Steps 1–10; 3 e 4 | Integrar contexto, validação, execução, resultados e estado |
| Tracing | aulas/template-20260918/Week_7_Session_1_Recording_What_Happened.ipynb | 1–5 | Uma trace por pedido, spans, falhas tratadas e privacidade |

Os exemplos de aula usam sobretudo Gemini; o código atual usa Anthropic. Adaptar os conceitos e os schemas ao SDK escolhido; não misturar objetos ou formatos dos dois SDKs. Claude está previsto nas guidelines.

## 5. Arquitetura recomendada

Estrutura proposta, ainda não implementada:

- app.py: widgets e apresentação.
- src/padelbuddy/config.py: configuração e leitura de variáveis.
- src/padelbuddy/prompts.py: instruções do agente.
- src/padelbuddy/schemas.py: critérios, opções e resultados das tools.
- src/padelbuddy/ai.py: chamadas ao SDK Anthropic atual do projeto.
- src/padelbuddy/agent.py: ciclo do agente e gestão da conversa.
- src/padelbuddy/tools.py: funções expostas ao agente.
- src/padelbuddy/providers/: adaptadores por fornecedor, isolando autenticação e formatos.
- src/padelbuddy/storage.py: dados internos; SQLite é uma opção simples a avaliar.
- docs/TOOLS.md e docs/ARCHITECTURE.md: contratos e decisões.

Começar com um fornecedor e um clube. Acrescentar o segundo depois de uma pesquisa funcionar de ponta a ponta.

### Dados e regras

Pesquisa: local, data, hora inicial/final, duração, orçamento total em EUR, indoor/outdoor e número de jogadores. Interpretar datas relativas com Europe/Lisbon e pedir informação em falta que altere a pesquisa.

Opção: provider, club_id, court_id, início/fim com timezone, duração, tipo de campo, preço total, moeda, booking_url, fetched_at e origem live/demo. Se um dado não existe, mantê-lo desconhecido; não inventá-lo.

- Comparar a mesma duração e distinguir preço total de preço por pessoa.
- Não deduzir disponibilidade só por ausência de reservas: faltam horários, bloqueios, regras, antecedência e preços.
- Links vêm do diretório validado ou do fornecedor; o LLM não os inventa.
- Timeout ou acesso negado não significa “sem campos disponíveis”. Mostrar falha parcial por fornecedor.
- Guardar apenas os dados pessoais necessários; omitir segredos e dados de jogadores das traces por defeito.

## 6. Primeiro passo — obter acesso real

Pesquisa verificada em 15/11/2026. O objetivo prioritário é consultar horários livres e preços, não criar reservas.

| Plataforma | Evidência pública | Caminho prático | Por confirmar |
|---|---|---|---|
| Playtomic | API de clubes read-only; planos Champion/Master; credenciais no Manager; programa Connect | Pedir acesso académico via Connect e/ou colaborar com um clube elegível | Endpoint autorizado de disponibilidade e preços, cobertura e permissão para comparação |
| TiePlayer / TieSports | TieManager anuncia API e webhooks | Contactar equipa pela página oficial e propor piloto com um clube | Docs, autenticação, leitura de slots/preços, escrita, custos e sandbox |
| AirCourts | Centro de ajuda e páginas de clubes; há clubes migrados para Playtomic | Verificar primeiro os clubes-alvo e o fornecedor atual | API de terceiros autorizada e condições de integração; não foi encontrada documentação pública suficiente |

### Playtomic: o que a API confirmada faz

A documentação do Manager confirma leitura e ausência de criação/edição/eliminação. Não é uma API geral aberta a qualquer conta de jogador. A documentação técnica descreve GET /api/v1/bookings para reservas existentes, com tenant_id e intervalo UTC. A lista de endpoints consultada inclui autenticação, bookings, players e payments; não confirma um endpoint de horários livres/preços para agregadores.

O programa Playtomic Connect permite candidaturas a integrações. Não há garantia de aceitação académica nem de permissões de escrita: perguntar explicitamente. A Playtomic também anuncia restrições a integrações não autorizadas; evitar construir o núcleo em endpoints privados descobertos por engenharia inversa.

### Sequência de ação

1. Escolher um clube piloto e registar fornecedor atual, contacto institucional e URL oficial de reservas.
2. Pedir à plataforma acesso académico/de demonstração para disponibilidade e preços desse clube. Em paralelo, perguntar ao clube se aceita participar e qual a via de integração suportada.
3. Playtomic: usar https://playtomic.com/connect. Se o clube tiver acesso elegível, o gestor consulta Settings > Developer tools; não pedir a password pessoal do gestor.
4. TieSports: usar https://www.tiesports.com/contact e pedir documentação da API/webhooks anunciada no TieManager. Esta é uma via promissora para investigar, não uma integração já garantida.
5. Perguntar: clubes/campos, slots, duração, preços/moeda, timezone, autenticação, scopes, limites, sandbox, custos, cache, autorização para mostrar/comparar dados e links oficiais.
6. Separar três capacidades na resposta: ler reservas existentes; consultar disponibilidade/preços; criar/cancelar reservas. Não aceitar “temos API” como resposta suficiente.
7. Depois das credenciais e autorização, testar uma chamada mínima fora do LLM, normalizar o resultado e compará-lo manualmente com a página do clube.
8. Só depois transformar a consulta numa tool, seguindo Week 5; integrar o agente pela Week 6 e tracing pela Week 7.

### Texto pronto a adaptar para formulário ou email (não enviado)

Assunto: Pedido de acesso académico à API — PadelBudy / NOVA IMS

Olá,

Somos estudantes da NOVA IMS e estamos a desenvolver o PadelBudy no âmbito do Capstone Project. A aplicação interpreta pedidos em linguagem natural, compara opções de campos de padel e encaminha o utilizador para concluir a reserva na plataforma original. Não processamos pagamentos.

Gostaríamos de testar uma integração autorizada, inicialmente com um clube piloto e um volume reduzido de pedidos. Precisamos de consultar campos, horários disponíveis, duração, preços e links oficiais de reserva.

Podem confirmar se disponibilizam estes dados através de API ou programa de parceiros, se existe acesso académico/sandbox e quais são a documentação, autenticação, limites e condições de utilização? Se o acesso disponível apenas lista reservas existentes, existe uma via específica para consultar disponibilidade e preços?

Não precisamos de dados pessoais dos jogadores para a pesquisa. Podemos adaptar o piloto ao âmbito e às condições que autorizarem.

Obrigado,
Equipa PadelBudy — NOVA IMS

### Exemplo técnico de primeiro teste Playtomic

Apenas depois de obter credenciais autorizadas. O pedido de autenticação é POST https://thirdparty.playtomic.io/api/v1/oauth/token com JSON contendo client_id e secret; o campo de resposta documentado é token, não access_token. Usar Authorization: Bearer nas chamadas seguintes. Um POST de autenticação não concede escrita em reservas.

A consulta GET https://thirdparty.playtomic.io/api/v1/bookings exige tenant_id e, sem booking_id, start_booking_date/end_booking_date em UTC. Pedir uma janela pequena, tratar paginação e limites atuais. Não guardar nem imprimir o JSON bruto com dados de jogadores. Este teste prova acesso a reservas existentes, não prova acesso a slots livres.

Critério de conclusão do primeiro passo: autorização registada + documentação + credenciais ou mecanismo suportado + consulta real de disponibilidade/preços validada. Neste momento: pesquisa documental concluída; acesso e teste autenticado pendentes.

### Se não houver API de disponibilidade

- Consultar se existe widget/feed/parceria oficial de disponibilidade com autorização de reutilização.
- Páginas públicas só como fonte após confirmar termos/permissão e viabilidade técnica. Estar acessível sem login não garante autorização para automatizar/republicar.
- Para desenvolver enquanto aguardamos resposta, usar dados mock explicitamente identificados; não os apresentar como solução do acesso real.
- Se só conseguirmos diretório + links, reduzir o compromisso da proposta técnica com o professor: não prometer comparação live que ainda não existe.

## 7. Ordem de implementação recomendada

1. Resolver fonte de disponibilidade com um clube e um fornecedor.
2. Criar contrato de pesquisa e resultado normalizado; validar preços, duração e timezone.
3. Implementar consulta determinística e uma pesquisa end-to-end com dados reais.
4. Expor search_availability como tool e ligar o chat às funções, com critérios estruturados e clarificações.
5. Acrescentar tools de dados internos, por exemplo guardar/listar pesquisas e criar uma repartição de despesas. Documentar parâmetros, retornos, falhas, efeitos e confirmação.
6. Ligar tracing desde a primeira interação funcional; fazer deployment cedo.
7. Integrar segundo fornecedor e ordenar por regras explícitas. Explicar o ranking sem inventar atributos.
8. Ler confirmação PDF/imagem; validar total/moeda e repartir em cêntimos, garantindo que a soma bate certo. Só marcar como reserva confirmada com evidência apropriada.
9. Implementar envio de resumo por email após confirmar destinatários e ação, se houver tempo e acesso ao serviço.
10. Avaliar, documentar e testar setup a partir de clone limpo.

Casos essenciais: pedido incompleto; data relativa; restrição impossível; nenhum resultado; fornecedor indisponível; resultado parcial; preço desconhecido; confirmação ilegível; erro transitório; tentativa de instruções maliciosas num documento. Comparar factos devolvidos com a fonte e confirmar que uma falha nunca vira disponibilidade inventada.

## 8. Fontes

### Locais, efetivamente consultadas

- capstone-projct/PadelBudy_Proposal (1).pdf — problema, agregação, redirecionamento, documentos, divisão de despesas e ideias opcionais.
- capstone-projct/Project_Guidelines (1).pdf — requisitos, avaliação e entregas.
- capstone-projct/app.py, courts.py, players.py, README.md e pyproject.toml — estado do protótipo.
- Notebooks identificados na tabela das weeks — secções verificadas no conteúdo Markdown.

### Oficiais, consultadas em 15/11/2026

- Playtomic, guia de acesso: https://helpmanager.playtomic.com/hc/en-gb/articles/38836515997073-Playtomic-API-Complete-Guide
- Documentação técnica: https://third-party.playtomic.io/
- Autenticação: https://third-party.playtomic.io/endpoints/auth/
- Reservas: https://third-party.playtomic.io/endpoints/bookings/
- Playtomic Connect: https://playtomic.com/connect
- Integrações autorizadas: https://helpmanager.playtomic.com/hc/en-gb/articles/47390286355089-Third-party-integrations-and-Playtomic-Connect
- TieSports funcionalidades API/webhooks: https://www.tiesports.com/tiemanager/all-features
- TieSports contacto: https://www.tiesports.com/contact
- AirCourts ajuda: https://intercom.help/aircourts/pt/
- Exemplo de clube migrado, que não prova migração de todos: https://www.aircourts.com/index.php/site/view_club/alley-courts

As páginas TieSports apareceram na pesquisa oficial mas devolveram 403 na abertura direta. Não foi possível inspecionar documentação técnica ou confirmar os métodos da API. Rever as capacidades antes de implementar.
