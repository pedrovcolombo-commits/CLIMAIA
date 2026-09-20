# CLIMAIA

<div align="center">

### 🌩️ Climate AI Analysis

**Sistema de Inteligência Artificial para Previsão e Validação de Eventos Climáticos Extremos**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2+-1e293b?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-3.0+-150458?style=flat-square&logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Status-Produção-10b981?style=flat-square)

</div>

---

## 🌍 Visão Geral

**CLIMAIA** é um software desktop premium desenvolvido para prever, identificar e validar eventos climáticos extremos com base na análise comparativa de dados meteorológicos brutos e pré-processados (tratados).

O projeto combina **Deep Learning** (Redes Neurais Recorrentes LSTM), **Machine Learning** (XGBoost Ensemble) e **Modelos Estatísticos Clássicos** (EVT, Gumbel, Z-Score) para avaliar séries temporais climáticas e detectar anomalias no tratamento de dados.

## 🎯 Principais Objetivos

1. **Previsão de Eventos Extremos:** Modelos preditivos já pré-treinados para antecipar ocorrências climáticas críticas (Temperatura, Radiação, Umidade e Velocidade do Vento).
2. **Avaliação da Integridade dos Dados:** Validação do impacto de tratamentos de dados (interpolação/limpeza) comparando eventos extremos entre série bruta e tratada.
   - Os eventos são criados artificialmente pela interpolação?
   - Os eventos extremos reais são suprimidos durante o tratamento?
3. **Software Desktop Premium:** Aplicação com interface moderna, dark mode, e suporte nativo para tabelas `.xlsx` e `.csv` (padrão brasileiro).

---

## 🚀 Como Executar e Testar

O projeto foi inteiramente desenhado para oferecer uma experiência "Zero Config" para o usuário final no sistema Windows.

### 🪟 Windows (Método Recomendado)

Se você baixou este código no Windows, você pode rodar o sistema nativamente usando os scripts automatizados fornecidos. Não é necessário mexer no terminal.

1. Baixe e instale o **Python** (certifique-se de marcar a opção "Add Python to PATH" durante a instalação).
2. Para **Apenas Testar/Rodar** a interface:
   - Dê um duplo clique no arquivo **`run_windows.bat`**. 
   - Ele criará o ambiente virtual isolado, instalará as dependências (`requirements.txt`) e abrirá a interface na tela.
3. Para **Gerar o Executável (.exe)** final:
   - Dê um duplo clique no arquivo **`build_windows.bat`**.
   - O processo irá empacotar todos os scripts, dependências e **os modelos de Inteligência Artificial pré-treinados** em um único executável portátil.
   - O seu aplicativo final estará dentro da pasta `dist/` com o nome `CLIMAIA.exe`.

### 🐧 Linux / Mac (Terminal)

Para rodar nativamente em ambientes Linux ou macOS:

```bash
# 1. Clone o repositório e acesse a pasta
git clone https://github.com/VituColombo0/CLIMAIA.git
cd CLIMAIA

# 2. (Apenas Ubuntu/Debian) Instale o pacote tkinter do sistema
sudo apt install python3-tk

# 3. Crie e ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Execute o software
python main.py
```

---

## 🧠 Modelos de Inteligência Artificial Inclusos

O sistema já é distribuído com **16 modelos e artefatos pré-treinados** integrados na pasta `data/models_trained/`. Estes modelos foram treinados sobre 4 anos de dados meteorológicos para 4 variáveis distintas:
- **Temperatura (°C)**
- **Velocidade do Vento (m/s)**
- **Umidade Relativa (%)**
- **Radiação Solar (W/m²)**

Para retreinar os modelos com dados atualizados no futuro, cientistas de dados podem utilizar o script offline de pipeline `train_model.py`.

---

## 🔬 Como Funciona

1. **Ingestão de Dados:** Carregue os dados brutos e tratados na aba "Dados". O sistema aceita `.xlsx` nativamente e auto-detecta `.csv` com separadores em ponto-e-vírgula.
2. **Detecção Estatística:** Configure o método (EVT, Gumbel, Z-Score, Percentil, IQR) na aba "Análise" para identificar eventos extremos.
3. **Comparação Analítica:** A aba "Comparação" audita as diferenças entre as detecções nos dados brutos vs tratados gerando um laudo de impacto da interpolação.
4. **Previsão com IA:** Na aba "Previsão", selecione "Carregar Modelo Treinado" para executar inferências instantâneas usando a IA empacotada sem travar o processamento da interface.

---

## 🕹️ Guia de Uso Detalhado da Interface

O CLIMAIA foi projetado para ter um fluxo de trabalho progressivo. Navegue pelas abas do menu lateral esquerdo de cima para baixo para realizar a sua análise completa.

### 1. 📂 Aba: Dados (Data Ingestion)
Esta é a porta de entrada do software. Aqui você alimenta o motor do sistema com as bases de dados que deseja avaliar.
- **Botão "Selecionar Arquivo" (Dados Brutos)**: Clique aqui para abrir a janela de seleção e escolher a sua planilha original (`.csv`, `.xlsx`). Esta planilha deve conter os dados extraídos diretamente dos sensores meteorológicos, possivelmente contendo ruídos, lacunas (dados faltantes) e anomalias.
- **Botão "Selecionar Arquivo" (Dados Tratados)**: Clique aqui para selecionar a planilha correspondente que já passou por algum processo de limpeza ou interpolação por parte da sua equipe de cientistas de dados.
- **Comportamento Automático**: Assim que um arquivo é selecionado, o CLIMAIA faz a leitura em background. Se a leitura for bem-sucedida, um badge verde com "CARREGADO" aparecerá. O painel inferior também exibirá automaticamente as 5 primeiras linhas da sua planilha para você conferir se as colunas e as datas foram lidas perfeitamente.
- **Botões "Limpar" (Ícone de Lixeira)**: Caso tenha carregado o arquivo errado, clique aqui para deletar o *dataframe* apenas deste painel específico da memória RAM, permitindo carregar um novo arquivo.

### 2. 🧮 Aba: Análise (Statistical Engine)
Nesta tela reside o núcleo matemático do CLIMAIA. Ela é responsável por caçar valores que saiam do padrão normal (eventos extremos) nas planilhas carregadas.
- **Caixas de Seleção "Aplicar Em"**: Você pode marcar se deseja procurar por extremos apenas nos "Dados Brutos", apenas nos "Dados Tratados", ou em ambos simultaneamente.
- **Opções de Variáveis (Checkboxes)**: Marque explicitamente quais variáveis meteorológicas você quer auditar (ex: *Velocidade do Vento*, *Temperatura*, *Radiação Solar*). O sistema só irá processar as opções marcadas, poupando processamento.
- **Menu "Método Estatístico"**: Um menu suspenso onde você escolhe o algoritmo matemático que definirá o que é um "extremo":
  - *Z-Score*: Mede o afastamento em relação à média (ideal para anomalias gerais).
  - *Gumbel / EVT*: Focado exclusivamente em picos máximos raros, usando a Teoria de Valores Extremos.
  - *IQR (Interquartil)*: Identifica limites com base em percentis (ótimo para dados com muita variação irregular).
- **Controle Deslizante (Threshold)**: Permite aumentar ou diminuir a rigidez da matemática (ex: multiplicar o Z-score por 2x, 3x, etc). Quanto maior o valor, mais difícil será um evento ser classificado como "extremo".
- **Botão "Executar Análise"**: Inicia o processamento pesado. O progresso aparecerá na tela e o **Log de Análise** (console preto na parte inferior) narrará linha a linha quantos extremos foram encontrados.
- **Botão "Limpar Console"**: Apaga todo o texto do console de log inferior para facilitar a leitura de novas execuções.

### 3. ⚖️ Aba: Comparação (Audit & Validation)
Aqui o CLIMAIA funciona como um auditor. Ele cruza os resultados da Aba 2 para descobrir se a sua equipe prejudicou os dados ao tentar "tratá-los".
- **Painel de Requisitos (Checklist)**: Mostra três selos (Bruto, Tratado, Análise). Se algum deles estiver vermelho (❌), significa que você esqueceu de carregar os dados ou esqueceu de rodar a análise na aba anterior. O botão de comparação ficará bloqueado até que tudo esteja verde (✅).
- **Botão "Executar Comparação"**: Ao clicar, o sistema desenha gráficos interativos. Ele sobrepõe a linha de tempo dos dados brutos contra os dados tratados. Pontos de divergência extrema serão evidenciados.
- **Tabela de Laudo (Bottom Panel)**: Exibe uma métrica fundamental dividida por variável:
  - *Coincidentes*: Eventos extremos que existem em ambos os arquivos (O tratamento manteve a realidade).
  - *Criados*: O tratamento matemático acidentalmente INVENTOU picos anormais onde não existiam.
  - *Suprimidos*: O tratamento APAGOU ou suavizou eventos reais que constavam no arquivo bruto.
- **Botão "Exportar Relatório"**: Salva essas métricas exatas e os painéis numéricos em uma nova tabela CSV no seu computador para prestação de contas.

### 4. 🔮 Aba: Previsão (Machine Learning & AI)
Módulo preditivo e de regressão para tentar descobrir o futuro climático com base no histórico que foi fornecido.
- **Menu "Variável Alvo"**: Define o que a Inteligência Artificial vai tentar adivinhar (ex: prever a Radiação Solar de amanhã).
- **Botão "Carregar Modelo Treinado"**: O CLIMAIA já possui 16 cérebros de IA (XGBoost e LSTM) pré-treinados empacotados dentro do arquivo `.exe` e do código fonte. Ao clicar aqui, você ativa essa inteligência instantaneamente sem precisar gastar energia e tempo treinando o seu computador.
- **Botões de Histórico e Épocas**: Controles deslizantes que dizem para a IA o quanto ela deve olhar para o passado (Histórico de Dias) para tentar adivinhar o futuro.
- **Botão "Treinar Novo Modelo"**: Utilize este botão **somente** se você tiver inserido planilhas com dados de regiões completamente novas que a IA original desconhece. Ele irá rodar algoritmos de *gradient boosting* no background. O console inferior mostrará o andamento do treinamento (RMSE, MAE e Loss).
- **Botão "Salvar Modelo"**: Grava os novos cérebros recém-treinados em disco (formato `.json` para árvores, `.h5` para redes neurais).
- **Botão "Executar Previsão"**: É a ação final. Ele lê os dados mais recentes que você carregou, processa na IA e plota na tela a curva prevista para os próximos dias (conforme escolhido no menu *Horizonte de Previsão*), além de pintar em vermelho se a previsão tocar na faixa que a Aba de Análise classificou como perigo/extremo.

### 5. ⚙️ Aba: Configurações (Preferences & Maintenance)
Central de controle visual e manutenção de memória do software.
- **Menus "Aparência" e "Escala"**: Altere instantaneamente o software do modo *Escuro* (Dark) para *Claro* (Light) e use o multiplicador de *Escala* (ex: 120%) se estiver utilizando o aplicativo em uma televisão ou monitor de alta resolução para deixar as letras maiores.
- **Painel de "Importação de CSV"**: Em 90% das vezes o sistema auto-detecta formatos (vírgulas vs ponto-e-vírgula). Se por acaso o seu CSV for carregado na "Aba Dados" como uma única coluna bagunçada, venha aqui e force o **Separador** para `,` ou `;`, defina o **Encoding** (UTF-8 ou ISO-8859-1) e digite o nome exato da **Coluna de Datas**.
- **Botões "Exportar Ambos / Exportar Tratado"**: Uma funcionalidade extremamente útil. Baixe o *dataframe* finalizado da memória para o seu HD convertendo-o para formatos mais leves e rápidos, como o **Parquet**, ou padronize-os rapidamente para o Excel (`.xlsx`).
- **Botões "Limpar Dados" e "Resetar Tudo"**: Ações de perigo. Clicar nestes ícones vermelhos funciona como se você tivesse fechado e aberto o programa novamente. Ele limpa todas as variáveis e pesos de IA do Python (`app_state`), poupando sua memória RAM e deixando o CLIMAIA zerado para você analisar o histórico climático de uma cidade nova.

---

## 📅 Linha do Tempo do Projeto (Cronograma)

```text
                    CLIMAIA — Roadmap de Desenvolvimento
═══════════════════════════════════════════════════════════════════
```

### 📌 05/05/2026 a 08/05/2026 — Planejamento e Estruturação
- Definição da arquitetura e escopo do projeto.
- Análise de viabilidade matemática dos modelos (EVT vs Gumbel).
- Estudo e abstração dos algoritmos iniciais de Machine Learning e previsão em base histórica.

### 🎨 10/05/2026 a 12/05/2026 — Arquitetura de Interface (Fase 1A)
- Pesquisa de referências visuais e implementação do **Design System** (`theme.py`).
- Criação das 6 abas principais do sistema integradas a um menu lateral CustomTkinter.

### 🧠 14/05/2026 a 16/05/2026 — Lógica de Estado e Matemática
- Desenvolvimento do **Estado Centralizado** para sincronizar dados entre as telas.
- Implementação dos algoritmos estatísticos puros (`extreme_detection.py`), validando a sensibilidade do Z-Score e do IQR.

### ⚙️ 19/05/2026 a 21/05/2026 — Motores de Comparação e IA Preditiva
- Criação do "Motor Analítico" para gerar o laudo de discrepância (Bruto vs Tratado).
- Modelagem preditiva com Redes Neurais (**LSTM**) e **XGBoost** (`forecaster.py`).
- Implementação de sub-processos (threading) para manter a fluidez da GUI.

### 📊 23/05/2026 a 25/05/2026 — Visualização e Testes de UX
- Integração do Matplotlib no framework gráfico para plotagem interativa.
- Cálculos de limite de confiança e renderização visual das bandas de incerteza da previsão.

### 🚀 26/05/2026 — Empacotamento Inicial Windows
- Criação dos scripts automatizados (`run_windows.bat`, `build_windows.bat`) para uso facilitado.

### 🛡️ Junho/2026 — Auditoria Final, Otimização e Limpeza
- Treinamento final dos modelos LSTM e XGBoost com os anos 2022 a 2025 (`train_model.py`).
- Inclusão nativa de suporte a planilhas `.xlsx` e parsing de datas em formato Brasileiro.
- Refatoração do PyInstaller (`_MEIPASS`) para empacotar os 16 modelos pré-treinados dentro do executável (`.exe`) permitindo a entrega em produção.
- Limpeza rigorosa de protótipos de backend e otimização das dependências (`requirements.txt`) garantindo um empacotamento Windows leve e livre de quebras de interface.

---

## 💡 Status Final

```text
Fase 1 (Interface e UX Design):        ██████████████████████████████ 100% ✅
Fase 2 (Motor Estatístico de Eventos): ██████████████████████████████ 100% ✅
Fase 3 (Modelagem LSTM/XGBoost):       ██████████████████████████████ 100% ✅
Fase 4 (Comparador Bruto vs Tratado):  ██████████████████████████████ 100% ✅
Fase 5 (Gráficos e Laudos):            ██████████████████████████████ 100% ✅
Fase 6 (Suporte XLSX e Arquivos Brutos)██████████████████████████████ 100% ✅
Fase 7 (Empacotamento IA p/ Windows):  ██████████████████████████████ 100% ✅
```

---

## 👤 Autor

**Pedro Vieira Colombo**  
Licença: Público
