# Relatório

Relatório final para o laboratório de caracterização da atividade de code review no GitHub

## Introdução

A prática de code review tornou-se uma constante nos processos de desenvolvimento agéis. Em linhas gerais, ela consiste na interação entre desenvolvedores e revisores visando inspecionar o código produzido antes de integrá-lo à base principal. Assim, garante-se a qualidade do código integrado, evitando-se também a inclusão de defeitos. No contexto de sistemas open source, mais especificamente dos desenvolvidos através do GitHub, as atividades de code review acontecem a partir da avaliação de contribuições submetidas por meio de Pull Requests (PR). Ou seja, para que se integre um código na branch principal, é necessário que seja realizada uma solicitação de pull, que será avaliada e discutida por um colaborador do projeto. Ao final, a solicitação de merge pode ser aprovada ou rejeitada pelo revisor. Em muitos casos, ferramentas de verificação estática realizam uma primeira análise, avaliando requisitos de estilo de programação ou padrões definidos pela organização.

Neste contexto, o objetivo deste laboratório é analisar a atividade de code review desenvolvida em repositórios populares do GitHub, identificando variáveis que influenciam no merge de um PR, sob a perspectiva de desenvolvedores que submetem código aos repositórios selecionados. 

## Questões de Pesquisa e Hipóteses Informais

Com base no dataset coletado, responderemos às seguintes questões de pesquisa, definidos de acordo com duas dimensões:

**A. Feedback Final das Revisões (Status do PR):**

- **RQ 01.** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

Hipótese: PRs com um tamanho menor podem ter uma maior probabilidade de serem aprovados, pois podem ser mais fáceis de revisar e menos propensos a conter problemas ocultos. Por outro lado, PRs muito grandes podem demandar uma análise mais detalhada devido à sua complexidade e extensão, o que pode resultar em uma menor probabilidade de serem aprovados.

- **RQ 02.** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

Hipótese: PRs que requerem um tempo mais longo para análise podem indicar problemas mais complexos ou extensos, levando a um feedback mais detalhado e possivelmente a uma menor taxa de merge.

- **RQ 03.** Qual a relação entre a descrição dos PRs e o feedback final das revisões?

Hipótese: PRs com descrições mais extensas podem facilitar a compreensão do código proposto, reduzindo a necessidade de feedback adicional e aumentando a probabilidade de merge.

- **RQ 04.** Qual a relação entre as interações nos PRs e o feedback final das revisões?

Hipótese: Maior interação nos PRs, incluindo discussões construtivas e respostas rápidas a comentários, pode indicar uma colaboração eficaz entre desenvolvedores e revisores, levando a um feedback mais completo e a uma maior probabilidade de merge.

---

**B. Número de Revisões:**

- **RQ 05.** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

Hipótese: PRs com um tamanho maior podem requerer mais revisões devido à complexidade e extensão do código alterado.

- **RQ 06.** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

Hipótese: Pode-se esperar que PRs que levam mais tempo para serem analisados tenham um número maior de revisões, pois podem indicar uma complexidade que exige uma análise mais detalhada e, portanto, mais iterações de revisão.

- **RQ 07.** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

Hipótese: Descrições mais detalhadas e informativas nos PRs podem reduzir a necessidade de revisões adicionais, pois ajudam os revisores a entender melhor o propósito e a implementação das alterações.

- **RQ 08.** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

Hipótese: Uma maior interação nos PRs, com discussões ativas e resolução rápida de problemas levantados, pode levar a um número menor de revisões, indicando uma comunicação eficaz entre os colaboradores.

## Resultados

- **RQ 01.** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Tamanho_Feedback_Arquivos](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/aa43470a-84b2-459c-9877-137f7c6cacb6) | ![Media_Tamanho_Feedback_Arquivos](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/9e6089d6-69d6-49c0-a05a-f9f56c806d09) | ![Mediana_Tamanho_Feedback_Arquivos](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/c55270b1-4110-4f4f-9614-51e4271d181e) |

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Tamanho_Feedback_LinhasAdicioandas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/077619cd-95ba-4ce4-a3e1-7822a9d18043) | ![Media_Tamanho_Feedback_LinhasAdicioandas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/12c65aef-0d1b-44f1-92be-b13502b35b00) | ![Mediana_Tamanho_Feedback_LinhasAdicioandas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/b6dee58f-fb92-4d14-8b57-d13f9980f9f9) |

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Tamanho_Feedback_LinhasExcluidas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/8da82b19-db42-4186-8e35-a978e2a00475) | ![Media_Tamanho_Feedback_LinhasExcluidas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a2a586cb-9d0a-430c-a393-51d1a13dabed) | ![Mediana_Tamanho_Feedback_LinhasExcluidas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/2106d1fa-6a25-4d22-9558-db601a37b779) |

- **RQ 02.** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Tempo_Analise_X_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/843617d8-3b4e-4154-bb03-e0d159be1fd6) | ![Media_Tempo_Analise_X_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/fa625779-3802-43e7-aa5e-5a53beffa096) | ![Mediana_Tempo_Analise_X_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/00ea44c3-b655-41c1-adb9-46fa5fa87c90) |

- **RQ 03.** Qual a relação entre a descrição dos PRs e o feedback final das revisões?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Descricao_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/645b0386-ef6d-4265-8af6-7cad74d91811) | ![Media_Descricao_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a08ae430-3dda-4e29-9643-b36e946d59c4) | ![Mediana_Descricao_Feedback](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/75241304-bf9f-4dcb-b108-0527fcddc704) |

- **RQ 04.** Qual a relação entre as interações nos PRs e o feedback final das revisões?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Interacoes_Feedback_Participantes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/7ad3c173-4933-4991-ba85-554736959c50) | ![Media_Interacoes_Feedback_Participantes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/4262846a-a770-458c-98a1-a8e657110434) | ![Mediana_Interacoes_Feedback_Participantes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/3495ab96-9fb2-49c5-8ea7-3b8090e2918c) |

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Interacoes_Feedback_Comentarios](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/6c4bfd9b-cc95-4756-b7e8-43d259d3e25e) | ![Media_Interacoes_Feedback_Comentarios](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/581e8584-bee6-4cee-8781-3c5ba9dfefb6) | ![Mediana_Interacoes_Feedback_Comentarios](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/9225ba62-b08b-412a-a2e8-68fc46d703a7) |

- **RQ 05.** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

| | | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Correlacao_Tamanho_TotalRevisoes_ArquivosAlterados](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/8217a471-2f31-40a5-a8ea-8d286c3a04e0) | ![Correlacao_Tamanho_TotalRevisoes_LinhasAdicionadas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/5dcfaf4e-b550-45a5-a841-7171efcf918b) | ![Correlacao_Tamanho_TotalRevisoes_LinhasExcluidas](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/ca7ac606-3ecf-444e-8d22-5011d106ebb7) |

- **RQ 06.** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

![Correlacao_CriacaoUltimaAtividade_TotalRevisoes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/afae629d-6619-42f3-803a-a8e06a47b232)

- **RQ 07.** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

![Correlacao_Descricao_Caracteres_TotalRevisoes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a9950234-918c-468a-b4e7-2be4961e84c5)

- **RQ 08.** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

| | |
| -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| ![Correlacao_Interacoes_TotalRevisoes_Participantes](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/7eb356d7-862e-488d-8a8c-ca3fc2e4c2e1) | ![Correlacao_Interacoes_TotalRevisoes_Comentarios](https://github.com/Frederico-dos-Santos/template-lab-experimentacao3/assets/90854484/a4db9493-604a-4d45-a013-4a61e15683a7) |


