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



