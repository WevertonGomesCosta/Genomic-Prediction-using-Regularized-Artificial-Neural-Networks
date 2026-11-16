# Genomic Prediction using Regularized Artificial Neural Networks

[English](#english) | [Português](#português)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
![R](https://img.shields.io/badge/Made%20with-R-blue.svg)
[![Website](https://img.shields.io/badge/Project%20Site-online-brightgreen)](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/)

**Project website:** <https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/>

---

## English

### Purpose

This repository contains a reproducible `workflowr` project for genomic prediction comparing three GBLUP genomic mixed models with four artificial neural-network (ANN) configurations: one unregularized baseline and three variants with L1 and/or L2 weight penalties.

The study combines controlled simulated genomic data with real phenotypic and genomic *Coffea arabica* data. The central objective is to compare GBLUP-A, GBLUP-AD, GBLUP-ADE, and four ANN configurations under matched validation designs, while evaluating whether L1 and L2 weight regularization improves predictive performance and generalization relative to the unregularized ANN.

Seven genomic-prediction configurations are evaluated:

- **GBLUP-A** — additive genomic effects;
- **GBLUP-AD** — additive and dominance genomic effects;
- **GBLUP-ADE** — additive, dominance, and additive-by-additive epistatic genomic effects;
- **ANN-0** — artificial neural network without L1/L2 weight penalties;
- **ANN-L1** — ANN with L1 weight regularization;
- **ANN-L2** — ANN with L2 weight regularization;
- **ANN-L1+L2** — ANN with simultaneous L1 and L2 weight regularization.

### Model selection and evaluation metrics

ANN hyperparameters are selected by mean RMSE across inner assessment folds, with mean Pearson correlation used to resolve performance ties.

Predictive performance is evaluated using Pearson and Spearman correlations, RMSE, and MAE. Prediction bias and calibration slope are complementary measures.

### Analytical sequence

Analyses are conducted using simulated genomic data and real phenotypic and genomic data from *Coffea arabica*.

#### Simulated data

1. [Data preprocessing](analysis/simulated_data_audit.Rmd): preparation of phenotypes, genotypes, genetic maps, QTL information, and simulation scenarios.
2. [Pre-validation](analysis/simulated_data_validation.Rmd): repeated outer cross-validation and inner partitions for ANN hyperparameter selection.
3. Genomic prediction models: [GBLUP-A, GBLUP-AD, and GBLUP-ADE](analysis/simulated_data_gblup.Rmd) and [ANN configurations](analysis/simulated_data_ann.Rmd).
4. [Model comparison](analysis/simulated_data_comparison.Rmd): comparison of predictions and performance in matched validation partitions.

Known true genetic values provide an independent target for predictive assessment and are not used for model fitting or selection.

#### Real data

1. [Phenotypes](analysis/real_data_phenotype.Rmd): phenotypic characterization, phenotypic mixed-model analysis by REML, variance components, and individual BLUPs.
2. [Data preprocessing](analysis/real_data_audit.Rmd): integration of BLUPs with the `geno_real.rds` genotype data, correspondence among individuals, and marker quality control.
3. [Pre-validation](analysis/real_data_validation.Rmd): shared outer and inner cross-validation partitions.
4. Genomic prediction models: [GBLUP-A, GBLUP-AD, and GBLUP-ADE](analysis/real_data_gblup.Rmd) and [ANN configurations](analysis/real_data_ann.Rmd).
5. [Model comparison](analysis/real_data_comparison.Rmd): comparison of genomic predictions and rankings under matched validation partitions.

All genomic prediction models are evaluated using the same validation partitions within each dataset.

### Validation scope

All competing genomic-prediction methods use matched outer-assessment partitions within each dataset.

Outer-assessment responses are excluded from model fitting and model selection. ANN hyperparameter and epoch selection are restricted to the corresponding outer-analysis sample, and competing methods are evaluated on the same held-out individuals.

For simulated data, true genetic values are used only as an independent assessment target. For real data, the response for genomic prediction consists of individual BLUPs estimated from the phenotypic mixed model.

Held-out genomic predictions are predictive quantities generated under the specified validation procedure and should not be interpreted as final breeding values from a model refitted with all available responses.

### Repository structure

- `analysis/`: `workflowr` source pages defining the analytical modules;
- `data/`: source data and associated documentation;
- `output/`: derived analytical objects, fitted-model outputs, summaries, tables, and figures;
- `docs/`: rendered `workflowr` website tracked by Git;
- `renv.lock` and `renv/`: metadata for the reproducible R environment.

Additional information on source data and analytical results is available in [`data/README.md`](data/README.md) and [`output/README.md`](output/README.md).

### Software and reproducibility

The analyses use R and R Markdown. The scientific website is produced with `workflowr`, and R package versions are specified with `renv`.

The genotype matrix `data/dados_reais/geno_real.rds` is not included in the version-controlled repository. Full reproduction of the real-data genomic analyses requires obtaining this file separately, subject to its applicable access and use conditions.

### Citation and license

Project citation metadata are provided in [`CITATION.cff`](CITATION.cff).

Except where otherwise indicated, original materials created for this repository are distributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license. See [`LICENSE.md`](LICENSE.md) and the project [License](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/license.html) page.

---

## Português

### Objetivo

Este repositório contém um projeto reprodutível em `workflowr` para predição genômica comparando três modelos mistos genômicos GBLUP com quatro configurações de redes neurais artificiais (ANN): uma sem regularização e três com penalizações L1 e/ou L2 dos pesos.

O estudo combina dados genômicos simulados controlados com dados fenotípicos e genômicos reais de *Coffea arabica*. O objetivo central é comparar GBLUP-A, GBLUP-AD, GBLUP-ADE e quatro configurações de ANN sob procedimentos equivalentes de validação cruzada, avaliando também se a regularização L1 e L2 dos pesos melhora o desempenho preditivo e a generalização em relação à ANN não regularizada.

Sete configurações de predição genômica são avaliadas:

- **GBLUP-A** — efeitos genômicos aditivos;
- **GBLUP-AD** — efeitos genômicos aditivos e de dominância;
- **GBLUP-ADE** — efeitos genômicos aditivos, de dominância e epistáticos aditivo por aditivo;
- **ANN-0** — rede neural artificial sem penalização L1/L2;
- **ANN-L1** — ANN com regularização L1;
- **ANN-L2** — ANN com regularização L2;
- **ANN-L1+L2** — ANN com regularização simultânea L1 e L2.

### Seleção dos modelos e métricas de avaliação

A seleção dos hiperparâmetros das ANN utiliza o RMSE médio nas partições internas de avaliação como critério principal e a correlação média de Pearson para desempate.

O desempenho preditivo é avaliado pelas correlações de Pearson e Spearman, RMSE e MAE. O viés das predições e a inclinação de calibração complementam essas medidas.

### Sequência analítica

As análises utilizam dados genômicos simulados e dados fenotípicos e genômicos reais de *Coffea arabica*.

#### Dados simulados

1. [Pré-processamento dos dados](analysis/simulated_data_audit.Rmd): preparação dos fenótipos, genótipos, mapas genéticos, informações de QTL e cenários de simulação.
2. [Pré-validação](analysis/simulated_data_validation.Rmd): validação cruzada externa repetida e partições internas para seleção dos hiperparâmetros das ANN.
3. Modelos de predição genômica: [GBLUP-A, GBLUP-AD e GBLUP-ADE](analysis/simulated_data_gblup.Rmd) e [configurações de ANN](analysis/simulated_data_ann.Rmd).
4. [Comparação dos modelos](analysis/simulated_data_comparison.Rmd): comparação das predições e do desempenho nas mesmas partições de validação.

Os valores genéticos verdadeiros são utilizados como referência independente na avaliação preditiva, sem participação no ajuste ou na seleção dos modelos.

#### Dados reais

1. [Fenótipos](analysis/real_data_phenotype.Rmd): caracterização fenotípica, análise fenotípica por modelos mistos e REML, componentes de variância e BLUPs individuais.
2. [Pré-processamento dos dados](analysis/real_data_audit.Rmd): integração dos BLUPs ao conjunto genotípico `geno_real.rds`, correspondência entre indivíduos e controle de qualidade dos marcadores.
3. [Pré-validação](analysis/real_data_validation.Rmd): partições externas e internas compartilhadas de validação cruzada.
4. Modelos de predição genômica: [GBLUP-A, GBLUP-AD e GBLUP-ADE](analysis/real_data_gblup.Rmd) e [configurações de ANN](analysis/real_data_ann.Rmd).
5. [Comparação dos modelos](analysis/real_data_comparison.Rmd): comparação das predições genômicas e das classificações nas mesmas partições de validação.

Todos os métodos são avaliados nas mesmas partições de validação dentro de cada conjunto de dados.

### Escopo da validação

Todos os métodos concorrentes de predição genômica utilizam partições externas de avaliação equivalentes dentro de cada conjunto de dados.

As respostas dos indivíduos de avaliação externa são excluídas do ajuste e da seleção dos modelos. A seleção de hiperparâmetros e de épocas das ANN é restrita à respectiva amostra de análise externa, e os métodos concorrentes são avaliados sobre os mesmos indivíduos mantidos fora do ajuste.

Nos dados simulados, os valores genéticos verdadeiros são utilizados somente como alvo independente de avaliação. Nos dados reais, a resposta da predição genômica consiste nos BLUPs individuais estimados a partir do modelo misto fenotípico.

As predições genômicas obtidas fora da amostra são quantidades preditivas geradas sob o procedimento de validação especificado e não devem ser interpretadas como valores genéticos finais provenientes de um modelo reajustado com todas as respostas disponíveis.

### Estrutura do repositório

- `analysis/`: páginas-fonte do `workflowr` que definem os módulos analíticos;
- `data/`: dados-fonte e documentação associada;
- `output/`: objetos analíticos derivados, saídas de modelos ajustados, resumos, tabelas e figuras;
- `docs/`: site `workflowr` renderizado e versionado no Git;
- `renv.lock` e `renv/`: metadados do ambiente R reprodutível.

Informações adicionais sobre dados-fonte e resultados analíticos estão disponíveis em [`data/README.md`](data/README.md) e [`output/README.md`](output/README.md).

### Recursos computacionais

As análises utilizam R e R Markdown. O site científico é produzido com `workflowr`, e as versões dos pacotes R são especificadas com `renv`.

A matriz genotípica `data/dados_reais/geno_real.rds` não está incluída no repositório versionado. A reprodução integral das análises genômicas com dados reais requer a obtenção desse arquivo separadamente, respeitando as condições aplicáveis de acesso e utilização.

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
