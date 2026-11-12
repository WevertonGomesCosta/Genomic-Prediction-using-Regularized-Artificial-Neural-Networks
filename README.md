# Genomic Prediction using Regularized Artificial Neural Networks

[English](#english) | [Português](#português)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
![R](https://img.shields.io/badge/Made%20with-R-blue.svg)
[![Website](https://img.shields.io/badge/Project%20Site-online-brightgreen)](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/)

**Project website:** <https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/>

---

## English

### Purpose

This repository contains a reproducible `workflowr` project for genomic prediction using regularized artificial neural networks and a GBLUP-ADE genomic mixed-model benchmark.

The study combines controlled simulated genomic data with real longitudinal *Coffea arabica* data. The central objective is to evaluate whether L1 and L2 weight regularization improves predictive performance and generalization relative to an unregularized neural network and GBLUP-ADE under matched validation designs.

Five genomic-prediction configurations are evaluated:

- **GBLUP-ADE** — additive, dominance, and epistatic genomic effects;
- **ANN-0** — artificial neural network without L1/L2 weight penalties;
- **ANN-L1** — ANN with L1 weight regularization;
- **ANN-L2** — ANN with L2 weight regularization;
- **ANN-L1+L2** — ANN with simultaneous L1 and L2 weight regularization.

### Analytical workflow

The project contains two complementary analysis branches.

#### Simulated data

```text
simulated_data_audit.Rmd
        |
        v
simulated_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
simulated_data_gblup.Rmd   simulated_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
      simulated_data_comparison.Rmd
```

The simulated branch prepares the source data, defines a common validation design, fits GBLUP-ADE and ANN models independently, and performs terminal model comparison. Known true genetic values provide an independent evaluation target and are not used for model fitting or selection.

#### Real data

```text
real_data_phenotype.Rmd
        |
        v
real_data_audit.Rmd
        |
        v
real_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
real_data_gblup.Rmd       real_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
        real_data_comparison.Rmd
```

The real-data branch begins with the complete longitudinal field dataset. The phenotypic module fits the defined longitudinal mixed model by REML and obtains individual BLUPs. The data-preparation module then integrates those BLUPs with the canonical `geno_real.rds` genotype object, aligns individuals, performs marker quality control, and creates the common object used by validation and genomic prediction.

Phenotypic analysis, genotype integration, validation design, model fitting, and terminal comparison are kept in separate modules.

### Validation scope

All competing genomic-prediction methods use matched outer-assessment partitions within each analysis branch.

Outer-assessment responses are excluded from model fitting and model selection. ANN hyperparameter and epoch selection are restricted to the corresponding outer-analysis sample, and competing methods are evaluated on the same held-out individuals.

For simulated data, true genetic values are used only as an independent assessment target. For real data, the response for genomic prediction consists of individual BLUPs estimated from the longitudinal phenotypic mixed model.

Held-out genomic predictions are predictive quantities generated under the documented validation design and should not be interpreted as final breeding values from a model refitted with all available responses.

### Repository structure

- `analysis/`: `workflowr` source pages defining the analytical modules;
- `data/`: canonical source data and data contracts;
- `code/`: reusable analytical functions and utilities shared across modules;
- `output/`: derived analytical objects, fitted-model outputs, summaries, tables, and figures;
- `docs/`: rendered `workflowr` website tracked by Git;
- `renv.lock` and `renv/`: metadata for the reproducible R environment.

Additional directory contracts are documented in [`data/README.md`](data/README.md), [`code/README.md`](code/README.md), and [`output/README.md`](output/README.md).

### Reproducibility

The repository supports two complementary reproducibility tasks.

#### Inspect the analytical workflow

The rendered website under `docs/` provides the versioned public record of the analytical pages, code, diagnostics, and reported results committed to the repository.

#### Reconstruct the analyses

Full computational reconstruction requires the canonical source data and deliberate execution of the documented analysis modules. Computationally intensive model-fitting steps may read or write persisted analytical objects under `output/` rather than being rerun automatically during routine website rendering.

R package dependencies are recorded with `renv`, while `workflowr` records the relationship between source analyses and rendered pages.

### Citation and license

Project citation metadata are provided in [`CITATION.cff`](CITATION.cff).

Except where otherwise indicated, original materials created for this repository are distributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license. See [`LICENSE.md`](LICENSE.md) and the project [License](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/license.html) page.

---

## Português

### Objetivo

Este repositório contém um projeto reprodutível em `workflowr` para predição genômica utilizando redes neurais artificiais regularizadas e um modelo misto genômico GBLUP-ADE como referência de comparação.

O estudo combina dados genômicos simulados controlados com dados longitudinais reais de *Coffea arabica*. O objetivo central é avaliar se a regularização L1 e L2 dos pesos melhora o desempenho preditivo e a generalização em relação a uma rede neural não regularizada e ao GBLUP-ADE sob desenhos de validação equivalentes.

Cinco configurações de predição genômica são avaliadas:

- **GBLUP-ADE** — efeitos genômicos aditivos, de dominância e epistáticos;
- **ANN-0** — rede neural artificial sem penalização L1/L2;
- **ANN-L1** — ANN com regularização L1;
- **ANN-L2** — ANN com regularização L2;
- **ANN-L1+L2** — ANN com regularização simultânea L1 e L2.

### Fluxo analítico

O projeto contém dois ramos complementares de análise.

#### Dados simulados

```text
simulated_data_audit.Rmd
        |
        v
simulated_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
simulated_data_gblup.Rmd   simulated_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
      simulated_data_comparison.Rmd
```

O ramo simulado prepara os dados-fonte, define um desenho comum de validação, ajusta GBLUP-ADE e ANN de forma independente e realiza a comparação terminal dos modelos. Os valores genéticos verdadeiros conhecidos fornecem um alvo independente de avaliação e não são usados no ajuste ou na seleção dos modelos.

#### Dados reais

```text
real_data_phenotype.Rmd
        |
        v
real_data_audit.Rmd
        |
        v
real_data_validation.Rmd
        |
        +-------------------+
        |                   |
        v                   v
real_data_gblup.Rmd       real_data_ann.Rmd
        |                   |
        +---------+---------+
                  |
                  v
        real_data_comparison.Rmd
```

O ramo de dados reais começa com o conjunto longitudinal completo de observações de campo. O módulo fenotípico ajusta o modelo misto longitudinal definido por REML e obtém BLUPs individuais. Em seguida, o módulo de preparação dos dados integra esses BLUPs ao objeto genotípico canônico `geno_real.rds`, alinha os indivíduos, aplica o controle de qualidade dos marcadores e cria o objeto comum utilizado pela validação e pela predição genômica.

A análise fenotípica, a integração genótipo-fenótipo, o desenho de validação, os ajustes dos modelos e a comparação terminal permanecem em módulos separados.

### Escopo da validação

Todos os métodos concorrentes de predição genômica utilizam partições externas de avaliação correspondentes dentro de cada ramo analítico.

As respostas dos indivíduos de avaliação externa são excluídas do ajuste e da seleção dos modelos. A seleção de hiperparâmetros e de épocas das ANN é restrita à respectiva amostra de análise externa, e os métodos concorrentes são avaliados sobre os mesmos indivíduos mantidos fora do ajuste.

Nos dados simulados, os valores genéticos verdadeiros são utilizados somente como alvo independente de avaliação. Nos dados reais, a resposta da predição genômica consiste nos BLUPs individuais estimados a partir do modelo misto fenotípico longitudinal.

As predições genômicas obtidas fora da amostra são quantidades preditivas geradas sob o desenho de validação documentado e não devem ser interpretadas como valores genéticos finais provenientes de um modelo reajustado com todas as respostas disponíveis.

### Estrutura do repositório

- `analysis/`: páginas-fonte do `workflowr` que definem os módulos analíticos;
- `data/`: dados-fonte canônicos e contratos de dados;
- `code/`: funções analíticas e utilitários reutilizáveis entre módulos;
- `output/`: objetos analíticos derivados, saídas de modelos ajustados, resumos, tabelas e figuras;
- `docs/`: site `workflowr` renderizado e versionado no Git;
- `renv.lock` e `renv/`: metadados do ambiente R reprodutível.

Contratos adicionais dos diretórios estão documentados em [`data/README.md`](data/README.md), [`code/README.md`](code/README.md) e [`output/README.md`](output/README.md).

### Reprodutibilidade

O repositório contempla duas tarefas complementares de reprodutibilidade.

#### Inspecionar o fluxo analítico

O site renderizado em `docs/` fornece o registro público versionado das páginas analíticas, códigos, diagnósticos e resultados reportados que foram commitados no repositório.

#### Reconstruir as análises

A reconstrução computacional completa exige os dados-fonte canônicos e a execução deliberada dos módulos analíticos documentados. Etapas computacionalmente intensivas de ajuste podem ler ou gravar objetos analíticos persistidos em `output/`, em vez de serem repetidas automaticamente durante a renderização rotineira do site.

As dependências dos pacotes R são registradas com `renv`, enquanto o `workflowr` registra a relação entre as análises-fonte e as páginas renderizadas.

### Citação e licença

Os metadados para citação do projeto estão em [`CITATION.cff`](CITATION.cff).

Salvo indicação diferente, os materiais originais produzidos para este repositório são distribuídos sob a licença Creative Commons Atribuição-NãoComercial-CompartilhaIgual 4.0 Internacional. Consulte [`LICENSE.md`](LICENSE.md) e a página [Licença](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/license.html) do projeto.

---

## Contact / Contato

**Weverton Gomes da Costa**<br>
Postdoctoral Researcher / Pesquisador Pós-Doutoral<br>
Department of Statistics / Departamento de Estatística<br>
Federal University of Viçosa / Universidade Federal de Viçosa<br>
[weverton.costa@ufv.br](mailto:weverton.costa@ufv.br)
