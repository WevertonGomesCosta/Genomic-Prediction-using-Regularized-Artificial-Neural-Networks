# Genomic Prediction using Regularized Artificial Neural Networks

[English](#english) | [Português](#português)

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
![R](https://img.shields.io/badge/Made%20with-R-blue.svg)
[![Website](https://img.shields.io/badge/Project%20Site-online-brightgreen)](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/)

**Project website:** <https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/>

---

## English

### Purpose

This repository contains a reproducible `workflowr` project for genomic prediction comparing three GBLUP genomic mixed models with four artificial neural-network (ANN) configurations: one reference without explicit L1/L2 weight penalties and three variants with L1 and/or L2 weight penalties.

The study combines controlled simulated genomic data with real phenotypic and genomic *Coffea arabica* data. The central objective is to compare GBLUP-A, GBLUP-AD, GBLUP-ADE, and four ANN configurations under matched validation designs, while evaluating whether L1 and L2 weight regularization improves predictive performance and generalization relative to ANN-0, the reference without explicit L1/L2 penalties.

Seven genomic-prediction configurations are evaluated:

- **GBLUP-A** — additive genomic effects;
- **GBLUP-AD** — additive and dominance genomic effects;
- **GBLUP-ADE** — additive, dominance, and additive-by-additive epistatic genomic effects;
- **ANN-0** — artificial neural network without L1/L2 weight penalties;
- **ANN-L1** — ANN with L1 weight regularization;
- **ANN-L2** — ANN with L2 weight regularization;
- **ANN-L1+L2** — ANN with simultaneous L1 and L2 weight regularization.

All four ANN configurations use early stopping to select training duration, which can provide implicit regularization.

### Datasets

| Feature | Simulated data | Real data |
|:--|:--|:--|
| Individuals | 1,000 | 195 |
| Markers used | 4,010 | 20,887 retained SNPs |
| Population | F2 | 13 coffee progenies |
| Scenarios or traits | Six genetic scenarios (C1–C6) | Cer, BM and LP |
| Response for fitting | Simulated phenotype | Individual phenotypic BLUP |
| Primary assessment target | Known true genetic value | Individual phenotypic BLUP |
| Complementary target | Simulated phenotype | — |

### Model selection and evaluation metrics

ANN hyperparameters are selected by mean RMSE across inner assessment folds, with mean Pearson correlation used to resolve performance ties.

Predictive performance is evaluated using Pearson and Spearman correlations, RMSE, and MAE. Prediction bias and calibration slope are complementary measures. The real-data comparison also evaluates matched ANN–GBLUP contrasts, global Spearman correlation and absolute rank errors after averaging repeated out-of-fold (OOF) predictions, recovery of the highest 20% of BLUPs, exact agreement and mean absolute difference between predicted quintiles, and linearly weighted Cohen's kappa between models.

### Analytical sequence

Analyses are conducted using simulated genomic data and real phenotypic and genomic data from *Coffea arabica*.

#### Simulated data

1. [M01 — Data preprocessing](analysis/simulated_data_audit.Rmd): preparation of phenotypes, genotypes, genetic maps, QTL information, and simulation scenarios.
2. [M02 — Pre-validation](analysis/simulated_data_validation.Rmd): repeated outer cross-validation and inner partitions for ANN hyperparameter selection.
3. [M03 — GBLUP](analysis/simulated_data_gblup.Rmd): additive, dominance and additive-by-additive epistatic models.
4. [M04 — Regularized ANN](analysis/simulated_data_ann.Rmd): network tuning, training duration and held-out prediction.
5. [M05 — Model comparison](analysis/simulated_data_comparison.Rmd): scenario-specific performance against true genetic values and simulated phenotypes.

Known true genetic values provide an independent target for predictive assessment and are not used for model fitting or selection.

#### Real data

1. [R01 — Phenotypes](analysis/real_data_phenotype.Rmd): phenotypic characterization, phenotypic mixed-model analysis by REML, variance components, and individual BLUPs.
2. [R02 — Data preprocessing](analysis/real_data_audit.Rmd): integration of BLUPs with the `geno_real.rds` genotype data, correspondence among individuals, and marker quality control.
3. [R03 — Pre-validation](analysis/real_data_validation.Rmd): shared outer and inner cross-validation partitions.
4. [R04A — GBLUP](analysis/real_data_gblup.Rmd): three genomic covariance structures and held-out prediction.
5. [R04B — Regularized ANN](analysis/real_data_ann.Rmd): nested tuning, training duration and held-out prediction.
6. [R05 — Model comparison](analysis/real_data_comparison.Rmd): predictive performance, matched contrasts, individual rankings and model agreement.

All genomic prediction models are evaluated using the same validation partitions within each dataset.

### Validation scope

All competing genomic-prediction methods use matched outer-assessment partitions within each dataset: five repetitions of five outer folds, with four inner folds per outer-analysis set for ANN hyperparameter selection. The outer analysis and assessment sizes are 800 and 200 in the simulations, and 156 and 39 in the real data.

Outer-assessment responses are excluded from model fitting and model selection. ANN hyperparameter and epoch selection are restricted to the corresponding outer-analysis sample, and competing methods are evaluated on the same held-out individuals.

For simulated data, true genetic values are used only as an independent assessment target. For real data, the response for genomic prediction consists of individual BLUPs estimated from the phenotypic mixed model.

Genomic predictions are obtained out of fold for each assessment individual, using models fitted without that individual's response. The GBLUP relationship matrices use the complete available genotyped panel. The real-data BLUPs are estimated from field observations before the genomic partitions are defined; the separation of training and assessment responses therefore applies to genomic fitting, not to upstream BLUP estimation. The design evaluates prediction within the represented populations.

The [About](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/about.html) page explains the scientific scope, model definitions and limits of interpretation. The [simulated](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/simulated_data_comparison.html) and [real-data](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/real_data_comparison.html) comparison pages present the scenario-specific and trait-specific findings. Repeated splits are dependent, and neither descriptive contrasts nor high agreement between models establish statistical significance or predictive superiority.

### Repository structure

- `analysis/`: `workflowr` source pages defining the analytical modules;
- `data/`: source data and associated documentation;
- `output/`: derived analytical objects, fitted-model outputs, summaries, tables, and figures;
- `docs/`: rendered `workflowr` website tracked by Git;
- `renv.lock` and `renv/`: metadata for the reproducible R environment.

Additional information on source data and analytical results is available in [`data/README.md`](data/README.md) and [`output/README.md`](output/README.md).

### Software and reproducibility

The analyses use R and R Markdown. The scientific website is produced with `workflowr`, and R package versions are specified with `renv`.

#### Inspect the published analysis

The rendered website tracked in `docs/` provides access to the tutorial, methodological code, tables and rendered figures without requiring a new model fit. The comparison modules use previously computed predictions and results; machine-readable summaries are documented in [output/README.md](output/README.md). High-resolution TIFF exports are kept locally rather than versioned.

#### Reconstruct the analytical workflow

Full reconstruction requires access to the canonical inputs documented in [data/README.md](data/README.md), the R environment recorded in `renv.lock`, and the deliberate execution of the analytical stages listed above. Restore the recorded R dependencies with `renv::restore()` and inspect the environment with `renv::status()`. The computationally intensive model-fitting and ANN tuning blocks are not run automatically by routine website rendering. Reading the published website and reconstructing the analyses are distinct tasks.

The real-data workflow reads the canonical genotype input from `data/dados_reais/geno_real.rds` and integrates it with phenotypic BLUPs. The processed object `output/real/audit/preprocessed_real_common.rds` contains the marker panel and aligned prediction targets used by the downstream models.

### Citation and license

Project citation metadata are provided in [`CITATION.cff`](CITATION.cff).

Except where otherwise indicated, original materials created for this repository are distributed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license. See [`LICENSE.md`](LICENSE.md) and the project [License](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/license.html) page.

---

## Português

### Objetivo

Este repositório contém um projeto reprodutível em `workflowr` para predição genômica comparando três modelos mistos genômicos GBLUP com quatro configurações de redes neurais artificiais (ANN): uma de referência sem penalizações explícitas L1/L2 dos pesos e três com penalizações L1 e/ou L2 dos pesos.

O estudo combina dados genômicos simulados controlados com dados fenotípicos e genômicos reais de *Coffea arabica*. O objetivo central é comparar GBLUP-A, GBLUP-AD, GBLUP-ADE e quatro configurações de ANN sob procedimentos equivalentes de validação cruzada, avaliando também se a regularização L1 e L2 dos pesos melhora o desempenho preditivo e a generalização em relação à ANN-0, referência sem penalizações explícitas L1/L2.

Sete configurações de predição genômica são avaliadas:

- **GBLUP-A** — efeitos genômicos aditivos;
- **GBLUP-AD** — efeitos genômicos aditivos e de dominância;
- **GBLUP-ADE** — efeitos genômicos aditivos, de dominância e epistáticos aditivo por aditivo;
- **ANN-0** — rede neural artificial sem penalização L1/L2;
- **ANN-L1** — ANN com regularização L1;
- **ANN-L2** — ANN com regularização L2;
- **ANN-L1+L2** — ANN com regularização simultânea L1 e L2.

As quatro configurações ANN utilizam early stopping para selecionar a duração do treinamento, o que pode proporcionar regularização implícita.

### Conjuntos de dados

| Característica | Dados simulados | Dados reais |
|:--|:--|:--|
| Indivíduos | 1.000 | 195 |
| Marcadores utilizados | 4.010 | 20.887 SNPs mantidos |
| População | F2 | 13 progênies de cafeeiro |
| Cenários ou características | Seis cenários genéticos (C1–C6) | Cer, BM e LP |
| Resposta para ajuste | Fenótipo simulado | BLUP fenotípico individual |
| Alvo principal de avaliação | Valor genético verdadeiro conhecido | BLUP fenotípico individual |
| Alvo complementar | Fenótipo simulado | — |

### Seleção dos modelos e métricas de avaliação

A seleção dos hiperparâmetros das ANN utiliza o RMSE médio nas partições internas de avaliação como critério principal e a correlação média de Pearson para desempate.

O desempenho preditivo é avaliado pelas correlações de Pearson e Spearman, RMSE e MAE. O viés das predições e a inclinação de calibração complementam essas medidas. A comparação dos dados reais também avalia contrastes pareados ANN–GBLUP, correlação global de Spearman e erros absolutos de classificação após a média das predições repetidas fora do fold (OOF), recuperação dos 20% maiores BLUPs, concordância exata e diferença absoluta média entre quintis preditos e kappa de Cohen com ponderação linear entre modelos.

### Sequência analítica

As análises utilizam dados genômicos simulados e dados fenotípicos e genômicos reais de *Coffea arabica*.

#### Dados simulados

1. [M01 — Pré-processamento dos dados](analysis/simulated_data_audit.Rmd): preparação dos fenótipos, genótipos, mapas genéticos, informações de QTL e cenários de simulação.
2. [M02 — Pré-validação](analysis/simulated_data_validation.Rmd): validação cruzada externa repetida e partições internas para seleção dos hiperparâmetros das ANN.
3. [M03 — GBLUP](analysis/simulated_data_gblup.Rmd): modelos aditivo, de dominância e epistático aditivo por aditivo.
4. [M04 — ANN regularizadas](analysis/simulated_data_ann.Rmd): seleção de hiperparâmetros, duração do treinamento e predição fora da amostra.
5. [M05 — Comparação dos modelos](analysis/simulated_data_comparison.Rmd): desempenho por cenário em relação aos valores genéticos verdadeiros e fenótipos simulados.

Os valores genéticos verdadeiros são utilizados como referência independente na avaliação preditiva, sem participação no ajuste ou na seleção dos modelos.

#### Dados reais

1. [R01 — Fenótipos](analysis/real_data_phenotype.Rmd): caracterização fenotípica, análise fenotípica por modelos mistos e REML, componentes de variância e BLUPs individuais.
2. [R02 — Pré-processamento dos dados](analysis/real_data_audit.Rmd): integração dos BLUPs ao conjunto genotípico `geno_real.rds`, correspondência entre indivíduos e controle de qualidade dos marcadores.
3. [R03 — Pré-validação](analysis/real_data_validation.Rmd): partições externas e internas compartilhadas de validação cruzada.
4. [R04A — GBLUP](analysis/real_data_gblup.Rmd): três estruturas de covariância genômica e predição fora da amostra.
5. [R04B — ANN regularizadas](analysis/real_data_ann.Rmd): seleção aninhada de hiperparâmetros, duração do treinamento e predição fora da amostra.
6. [R05 — Comparação dos modelos](analysis/real_data_comparison.Rmd): desempenho preditivo, contrastes pareados, classificações individuais e concordância entre modelos.

Todos os métodos são avaliados nas mesmas partições de validação dentro de cada conjunto de dados.

### Escopo da validação

Todos os métodos concorrentes de predição genômica utilizam as mesmas partições externas de avaliação dentro de cada conjunto de dados: cinco repetições de cinco folds externos, com quatro folds internos por amostra de análise externa para seleção dos hiperparâmetros das ANN. As amostras de análise e avaliação externa contêm 800 e 200 indivíduos nas simulações, e 156 e 39 nos dados reais.

As respostas dos indivíduos de avaliação externa são excluídas do ajuste e da seleção dos modelos. A seleção de hiperparâmetros e de épocas das ANN é restrita à respectiva amostra de análise externa, e os métodos concorrentes são avaliados sobre os mesmos indivíduos mantidos fora do ajuste.

Nos dados simulados, os valores genéticos verdadeiros são utilizados somente como alvo independente de avaliação. Nos dados reais, a resposta da predição genômica consiste nos BLUPs individuais estimados a partir do modelo misto fenotípico.

As predições genômicas são obtidas fora do fold para cada indivíduo de avaliação, utilizando modelos ajustados sem sua resposta. As matrizes de parentesco dos GBLUP utilizam o painel genotípico completo disponível. Os BLUPs dos dados reais são estimados a partir das observações de campo antes da definição das partições genômicas; portanto, a separação das respostas de treinamento e avaliação aplica-se ao ajuste genômico, e não à estimação prévia dos BLUPs. O desenho avalia a predição dentro das populações representadas.

A página [Sobre](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/about.html) explica o escopo científico, as definições dos modelos e os limites de interpretação. As páginas de comparação dos [dados simulados](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/simulated_data_comparison.html) e [dados reais](https://wevertongomescosta.github.io/Genomic-Prediction-using-Regularized-Artificial-Neural-Networks/real_data_comparison.html) apresentam os resultados específicos por cenário e característica. As partições repetidas são dependentes, e contrastes descritivos ou alta concordância entre modelos não estabelecem significância estatística ou superioridade preditiva.

### Estrutura do repositório

- `analysis/`: páginas-fonte do `workflowr` que definem os módulos analíticos;
- `data/`: dados-fonte e documentação associada;
- `output/`: objetos analíticos derivados, saídas de modelos ajustados, resumos, tabelas e figuras;
- `docs/`: site `workflowr` renderizado e versionado no Git;
- `renv.lock` e `renv/`: metadados do ambiente R reprodutível.

Informações adicionais sobre dados-fonte e resultados analíticos estão disponíveis em [`data/README.md`](data/README.md) e [`output/README.md`](output/README.md).

### Recursos computacionais e reprodutibilidade

As análises utilizam R e R Markdown. O site científico é produzido com `workflowr`, e as versões dos pacotes R são especificadas com `renv`.

#### Inspecionar a análise publicada

O website renderizado e versionado em `docs/` permite consultar o tutorial, o código metodológico, as tabelas e as figuras renderizadas sem exigir novo ajuste de modelos. Os módulos de comparação utilizam predições e resultados previamente calculados; os resumos legíveis por máquina estão documentados em [output/README.md](output/README.md). As exportações TIFF de alta resolução são mantidas localmente, sem versionamento.

#### Reconstruir o fluxo analítico

A reconstrução completa exige acesso aos dados canônicos documentados em [data/README.md](data/README.md), ao ambiente R registrado em `renv.lock` e a execução deliberada das etapas analíticas listadas acima. Restaure as dependências R registradas com `renv::restore()` e inspecione o ambiente com `renv::status()`. Os blocos computacionalmente intensivos de ajuste dos modelos e seleção de hiperparâmetros das ANN não são executados automaticamente durante a renderização rotineira do site. Consultar o website publicado e reconstruir as análises são tarefas distintas.

O fluxo de dados reais lê o arquivo genotípico canônico `data/dados_reais/geno_real.rds` e o integra aos BLUPs fenotípicos. O objeto processado `output/real/audit/preprocessed_real_common.rds` contém o painel de marcadores e os alvos preditivos alinhados utilizados pelos modelos seguintes.

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
