# Relatório

Relatório final para o laboratório de caracterização da atividade de code review no GitHub

## Introdução

A prática de code review tornou-se uma constante nos processos de desenvolvimento agéis. Em linhas gerais, ela consiste na interação entre desenvolvedores e revisores visando inspecionar o código produzido antes de integrá-lo à base principal. Assim, garante-se a qualidade do código integrado, evitando-se também a inclusão de defeitos. No contexto de sistemas open source, mais especificamente dos desenvolvidos através do GitHub, as atividades de code review acontecem a partir da avaliação de contribuições submetidas por meio de Pull Requests (PR). Ou seja, para que se integre um código na branch principal, é necessário que seja realizada uma solicitação de pull, que será avaliada e discutida por um colaborador do projeto. Ao final, a solicitação de merge pode ser aprovada ou rejeitada pelo revisor. Em muitos casos, ferramentas de verificação estática realizam uma primeira análise, avaliando requisitos de estilo de programação ou padrões definidos pela organização.

Neste contexto, o objetivo deste laboratório é analisar a atividade de code review desenvolvida em repositórios populares do GitHub, identificando variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados.

Para alcançar este objetivo, foram levantadas oito Questões de Pesquisa que relacionam duas dimenções: as métricas de Tamanho, Tempo e Análise de cada PR, a Descrição e as Iterações, e o feedback final das revisões e a quantidade delas.

##### A. Feedback Final das Revisões (Status do PR):

* RQ 01. Qual a relação entre o **tamanho** dos PRs e o feedback final das revisões?
* RQ 02. Qual a relação entre o **tempo de análise** dos PRs e o feedback final das revisões?
* RQ 03. Qual a relação entre a **descrição** dos PRs e o feedback final das revisões?
* RQ 04. Qual a relação entre as **interações** nos PRs e o feedback final das revisões?

##### B. Número de Revisões:

* RQ 05. Qual a relação entre o **tamanho** dos PRs e o número de revisões realizadas?
* RQ 06. Qual a relação entre o **tempo de análise** dos PRs e o número de revisões realizadas?
* RQ 07. Qual a relação entre a **descrição** dos PRs e o número de revisões realizadas?
* RQ 08. Qual a relação entre as **interações** nos PRs e o número de revisões realizadas?
 
#### 3. Definição de Métricas
As métricas utilizadas nas questões de pesquisa estão definidas a seguir:

* **Tamanho**: número de arquivos; total de linhas adicionadas e removidas.
* **Tempo de Análise**: intervalo entre a criação do PR e a última atividade (fechamento ou merge).
* **Descrição**: número de caracteres do corpo de descrição do PR (na versão markdown).
* **Interações**: número de participantes; número de comentários.
* **Feedback Final das Revisões**: a decisão da revisão.

## Hipóteses Informais

Nesta seção, serão levantadas as hipóteses informais relacionadas às Questões de Pesquisa:

#### **A. Feedback Final das Revisões (Status do PR):**

- **RQ 01.** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

Hipótese: PRs com um tamanho menor podem ter uma maior probabilidade de serem aprovados, pois podem ser mais fáceis de revisar e menos propensos a conter problemas ocultos. Por outro lado, PRs muito grandes podem demandar uma análise mais detalhada devido à sua complexidade e extensão, o que pode resultar em uma menor probabilidade de serem aprovados.

- **RQ 02.** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

Hipótese: PRs que requerem um tempo mais longo para análise podem indicar problemas mais complexos ou extensos, levando a um feedback mais detalhado e possivelmente a uma menor taxa de merge.

- **RQ 03.** Qual a relação entre a descrição dos PRs e o feedback final das revisões?

Hipótese: PRs com descrições mais extensas podem facilitar a compreensão do código proposto, reduzindo a necessidade de feedback adicional e aumentando a probabilidade de merge.

- **RQ 04.** Qual a relação entre as interações nos PRs e o feedback final das revisões?

Hipótese: Maior interação nos PRs, incluindo discussões construtivas e respostas rápidas a comentários, pode indicar uma colaboração eficaz entre desenvolvedores e revisores, levando a um feedback mais completo e a uma maior probabilidade de merge.

---

#### **B. Número de Revisões:**

- **RQ 05.** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

Hipótese: PRs com um tamanho maior podem requerer mais revisões devido à complexidade e extensão do código alterado.

- **RQ 06.** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

Hipótese: Pode-se esperar que PRs que levam mais tempo para serem analisados tenham um número maior de revisões, pois podem indicar uma complexidade que exige uma análise mais detalhada e, portanto, mais iterações de revisão.

- **RQ 07.** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

Hipótese: Descrições mais detalhadas e informativas nos PRs podem reduzir a necessidade de revisões adicionais, pois ajudam os revisores a entender melhor o propósito e a implementação das alterações.

- **RQ 08.** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

Hipótese: Uma maior interação nos PRs, com discussões ativas e resolução rápida de problemas levantados, pode levar a um número menor de revisões, indicando uma comunicação eficaz entre os colaboradores.

## Metodologia

#### 1. Criação do Dataset
O dataset utilizado será composto por PRs submetidos a repositórios:

* populares (ou seja, avaliaremos PRs submetidos aos 200 repositórios mais populares do GitHub);
* que possuam pelos menos 100 PRs (MERGED + CLOSED).

Além disso, a fim de analisar PRs que tenham passado pelo processo de code review, selecionaremos apenas aqueles:

* com status MERGED ou CLOSED;
* que possuam pelo menos uma revisão (total count do campo review).

#### 2. Coleta dos dados
Para criar o dataset, será desenvolvido um código em Python que fará a extração dos dados necessários usando a API do GitHub através do GraphQL. Esse código será projetado para coletar informações como tamanho dos PRs, tempo de análise, descrições, interações nos PRs e status do merge, garantindo assim a obtenção de dados completos e relevantes para a análise.

#### 3. Processamento dos Dados
Nesta etapa, ocorrerá a Limpeza e Tratamento dos dados coletados. Isso incluirá a remoção de informações inconsistentes ou irrelevantes para a análise, como PRs que foram revisados automaticamente por bots ou ferramentas de CI/CD. Será feita uma seleção específica de PRs, considerando apenas aqueles cuja revisão demandou pelo menos uma hora, identificada pela diferença entre a data de criação e a data de merge (ou close) superior a uma hora. Além disso, os dados brutos serão transformados e organizados em formato CSV para facilitar a manipulação e a permanência das informações.

#### 4. Análise dos Dados
Na  Análise, serão utilizados gráficos como bar charts e scatter plots, gerados a partir do código em Python, para uma visualização mais clara dos dados. Esses gráficos ajudarão a identificar padrões, tendências e relações entre as variáveis estudadas.

#### 5. Discussão das Hipóteses
Com base nas análises realizadas, será feita a Discussão das Hipóteses levantadas inicialmente. Essa discussão visa validar ou refutar as suposições da pesquisa, comparando os Resultados Obtidos com as Hipóteses formuladas, a fim de avaliar se os dados suportam as hipóteses propostas ou se há necessidade de revisão. 

## Resultados Obtidos

A seção de Resultados Obtidos do presente trabalho apresenta uma análise das relações entre métricas de qualidade de código (CBO, DIT, LCOM) e a popularidade, maturidade, atividade e tamanho dos repositórios Java, medido pelo número de estrelas, ano de criação do repositório, número de releases lançadas e o número de linhas de código (LOC), respectivamente.

Para a análise do coeficiente de correlação, será considerados estes valores:

<div align="center" style="display:flex;">

| Intervalo de _p-value_ | Classificação        |
| :--------------------- | :------------------- |
| _p-value_ < 0,001      | Existe correlação    |
| _p-value_ >= 0,001     | Não existe correlação |

</div>
 
<div align="center" style="display:flex;">

| Intervalo de ρ  | Classificação  |
| :-------------- | :------------- |
| 0,0 <= ρ < 0,1  | Sem correlação |
| 0,1 <= ρ < 0,3  | Insignificante |
| 0,3 <= ρ < 0,5  | Baixo          |
| 0,5 <= ρ < 0,7  | Moderado       |
| 0,7 <= ρ < 0,9  | Alto           |
| 0,9 <= ρ < 1,00 | Muito alto     |

</div>

- **RQ 01.** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

| | | | 
| --- | --- | --- |
| ![Correlação entre Arquivos Alterados e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/8b9f3265-18ad-4911-a072-b9d28003e85e) | ![Correlação entre Linhas Adicionadas e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/af601c41-dc2b-411b-a8b3-d638221ac3dc) | ![Correlação entre Linhas Excluídas e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/6b5633b9-861f-4dfd-8267-e97f8892a850) |

| | | | 
| --- | --- | --- |
| ![Correlação entre Arquivos Alterados e Revisões com Mudanças Requisitadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/ec1b3da2-ce6a-44e6-b6d2-84e4f721d2f3)  | ![Correlação entre Linhas Adicionadas e Revisões com Mudanças Requisitadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/4af75ae0-9235-4152-a821-4fb601f3e9ce)  | ![Correlação entre Linhas Excluídas e Revisões com Mudanças Requisitadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/724b074e-8e4e-4603-9cc1-ebb457243ad7) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
 
   |         | APPROVED               | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :--------------------- | :---------------- | :-------------- |
   | ρ       | 0.33                   | 0.12              | 0.23            |
   | p-value | 1.61 × 10<sup>-6</sup> | 0.08              | 0.0012          |
 
   |         | APPROVED | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :------- | :---------------- | :-------------- |
   | ρ       | 0.20     | 0.13              | 0.18            |
   | p-value | 0.0039   | 0.077             | 0.012           |

   |         | APPROVED | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :------- | :---------------- | :-------------- |
   | ρ       | 0.19     | 0.09              | 0.09            |
   | p-value | 0.006    | 0.185             | 0.186           |
</div>

A análise da relação entre o tamanho dos Pull Requests (PRs) e o feedback final das revisões revela uma tendência interessante: PRs menores têm maior probabilidade de aprovação ou necessidade de revisão. Isso se evidencia pela mediana menor e pelos quartis nos gráficos de Linhas Excluídas e Arquivos Alterados nos boxplots dos PRs aprovados. Além disso, a correlação positiva fraca entre o tamanho do PR e os diferentes tipos de feedback sugere que PRs maiores enfrentam revisões mais exigentes, sendo notável uma maior chance de aprovação para pull requests de refatoração que reduzem o número de linhas. A influência do tamanho do PR no resultado das revisões é clara, especialmente nos PRs aprovados, demonstrada pelos valores significativos de p-value na análise de Spearman. Entretanto, é crucial ressaltar que outros fatores também têm impacto, o que ressalta a complexidade do processo de revisão de código.

Além disso, em relação às linhas adicionadas, percebe-se uma tendência maior de requerer revisões para aprovação. Isso reafirma a maior exigência de verificação de novas funcionalidades no sistema.

- **RQ 02.** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

| | |
| --- | --- |
| ![Correlação entre Intervalo Criação e Última Atividade e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/b417be2b-c079-48da-b197-29c7a85c7b34) | ![Correlação entre Intervalo Criação e Última Atividade e Revisões Aprovadas e com Mudanças Requisitadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/efd06def-fd77-488a-93db-e98579ae8146) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
   |         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :---- | :--------------------- | :---- |
   | ρ | -0.49  | -0.08  | -0.24  |
   | p-value | 2.074 × 10<sup>-13</sup> | 0.28 | 0.0007 |

</div>

Os gráficos revelam que PRs que recebem solicitações de alterações (CHANGES_REQUESTED) geralmente demandam mais tempo em comparação com PRs aprovados ou aqueles que requerem revisão (REVIEW_REQUIRED). Isso pode estar relacionado ao processo de revisão, especialmente para PRs com um grande número de linhas adicionadas. Eles passam por múltiplos estágios, como revisão inicial (REVIEW_REQUESTED) e, caso haja inconsistências ou erros, são solicitadas alterações (CHANGES_REQUESTED), seguidas por uma nova revisão e assim por diante, conforme visto no gráfico de "Correlação entre Linhas Adicionadas e Feedback final das Revisões". Esse ciclo de revisões múltiplas pode consumir mais tempo devido à necessidade de envolvimento de várias partes no processo de revisão.

- **RQ 03.** Qual a relação entre a descrição dos PRs e o feedback final das revisões?

| | |
| --- | --- |
| ![Correlação entre Caracteres Corpo PR e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/26224048-e079-4b95-936b-f458e076b894) | ![Correlação entre Caracteres Corpo PR e Revisões com Mudanças Requisitadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/46c892f1-0103-4858-9ac1-275f45a1a34e) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
|         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
| :------ | :---- | :--------------------- | :---- |
| ρ | 0.36  | 0.15  | 0.2  |
| p-value | 1.55 × 10<sup>-7</sup> | 0.033 | 0.004 |

</div>

A análise revela que PRs com descrições mais extensas têm uma ligeira vantagem na probabilidade de aprovação e podem reduzir a necessidade de revisões adicionais. Isso é apoiado pela mediana e quartis superiores dos PRs aprovados em comparação com os PRs que requerem mudanças ou revisões adicionais. A correlação de Spearman confirma essa tendência, mostrando uma correlação positiva fraca entre o tamanho da descrição e o feedback final das revisões para todos os tipos de PRs.

- **RQ 04.** Qual a relação entre as interações nos PRs e o feedback final das revisões?

| | |
| --- | --- |
| ![Correlação entre Participantes do PR e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/6251c32c-768b-43fa-9ff6-1d9804a213bb) | ![Correlação entre Comentários do PR e Feedback final das Revisões](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/77488551/9102dfff-05c4-4f80-a161-fd4d32f37f47) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
     
   |         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :---- | :--------------------- | :---- |
   | ρ | 0.25  | 0.17  | 0.024  |
   | p-value | 0.0003 | 0.013 | 0.729 |
    
   |         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
   | :------ | :---- | :--------------------- | :---- |
   | ρ | 0.25  | 0.14  | 0.04  |
   | p-value | 0.0003 | 0.042 | 0.526 |
        
</div>


Os resultados dos gráficos e das correlações de Spearman sugerem que os PRs que requerem mudanças (CHANGES_REQUESTED) apresentam, em média, mais interações entre os participantes e, consequentemente, mais comentários para criar a comunicação entre esses envolvidos.

- **RQ 05.** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Correlacao_Tamanho_TotalRevisoes_ArquivosAlterados](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/8217a471-2f31-40a5-a8ea-8d286c3a04e0) | ![Correlacao_Tamanho_TotalRevisoes_LinhasAdicionadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/5dcfaf4e-b550-45a5-a841-7171efcf918b) | ![Correlacao_Tamanho_TotalRevisoes_LinhasExcluidas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/ca7ac606-3ecf-444e-8d22-5011d106ebb7) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
|         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
| :------ | :---- | :--------------------- | :---- |
| ρ | 0.05  | 0.14  | 0.07  |
| p-value | 0.102 | 1.66 × 10<sup>-5</sup> | 0.037 |

</div>

- **RQ 06.** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

![Correlacao_CriacaoUltimaAtividade_TotalRevisoes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/afae629d-6619-42f3-803a-a8e06a47b232)

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
|         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
| :------ | :---- | :--------------------- | :---- |
| ρ | 0.05  | 0.14  | 0.07  |
| p-value | 0.102 | 1.66 × 10<sup>-5</sup> | 0.037 |

</div>

- **RQ 07.** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

![Correlacao_Descricao_Caracteres_TotalRevisoes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a9950234-918c-468a-b4e7-2be4961e84c5)

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
|         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
| :------ | :---- | :--------------------- | :---- |
| ρ | 0.05  | 0.14  | 0.07  |
| p-value | 0.102 | 1.66 × 10<sup>-5</sup> | 0.037 |

</div>

- **RQ 08.** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

| | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Correlacao_Interacoes_TotalRevisoes_Participantes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/7eb356d7-862e-488d-8a8c-ca3fc2e4c2e1) | ![Correlacao_Interacoes_TotalRevisoes_Comentarios](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a4db9493-604a-4d45-a013-4a61e15683a7) |

**<h4 align="center">Coeficiente de Spearman</h4>**

<div align="center" style="display:flex;">
    
|         | APPROVED   | CHANGES_REQUESTED | REVIEW_REQUIRED |
| :------ | :---- | :--------------------- | :---- |
| ρ | 0.05  | 0.14  | 0.07  |
| p-value | 0.102 | 1.66 × 10<sup>-5</sup> | 0.037 |

</div>


